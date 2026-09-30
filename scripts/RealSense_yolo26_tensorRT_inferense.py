import pyrealsense2 as rs
import numpy as np
import cv2
import tensorrt as trt
import pycuda.driver as cuda
import pycuda.autoinit  # Automatically manages the CUDA context


TRT_LOGGER = trt.Logger(trt.Logger.WARNING)
# Define your custom dataset label names here
#CLASS_NAMES = ["class_0", "class_1", "class_2"]  # Update with your custom classes
CLASS_NAMES = ["Dog", "Cat", "Tiger", "Bird", "Snake", "Bear"]
CONF_THRESHOLD = 0.25  # Confidence cutoff filter  , for step 3.  Initialize TensorRT assets

# 1. Setup TensorRT logger and execution runtime
def load_engine(engine_path):
    """Loads a serialized TensorRT engine file."""
    with open(engine_path, "rb") as f, trt.Runtime(TRT_LOGGER) as runtime:
        return runtime.deserialize_cuda_engine(f.read())


def allocate_buffers(engine):
    """Allocates host and device buffers needed for inference."""
    inputs = []
    outputs = []
    bindings = []
    stream = cuda.Stream()

    for binding in engine:
        size = trt.volume(engine.get_binding_shape(binding)) * engine.max_batch_size
        dtype = trt.nptype(engine.get_binding_dtype(binding))
        # Allocate host (CPU) and device (GPU) memory buffers
        host_mem = cuda.pagelocked_empty(size, dtype)
        device_mem = cuda.mem_alloc(host_mem.nbytes)

        bindings.append(int(device_mem))
        if engine.binding_is_input(binding):
            inputs.append({'host': host_mem, 'device': device_mem})
        else:
            outputs.append({'host': host_mem, 'device': device_mem})
    return inputs, outputs, bindings, stream


# 2. Configure and start the Intel RealSense Pipeline
pipeline = rs.pipeline()
config = rs.config()
# Standard streaming profile matching the model's preferred aspect scale
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
pipeline.start(config)

# 3. Initialize TensorRT assets
# Precondition:  Convert your ONNX file to engine via: /usr/src/tensorrt/bin/trtexec --onnx=model.onnx --saveEngine=model.engine --fp16
engine = load_engine("best_model.engine")
inputs, outputs, bindings, stream = allocate_buffers(engine)
context = engine.create_execution_context()



try:
    while True:
        # Wait for aligned coherent frame sets
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue

        # Convert RealSense frame data to standard OpenCV BGR image
        frame_raw = np.asanyarray(color_frame.get_data())
        h_orig, w_orig, _ = frame_raw.shape

        # --- PREPROCESSING ---
        # 1. Letterbox/Resize to 640x640 (Strict size required by your export constraints)
        input_w, input_h = 640, 640
        img_resized = cv2.resize(frame_raw, (input_w, input_h))

        # 2. Format adjustment: BGR to RGB
        img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)

        # 3. Normalize pixels (0.0 to 1.0) and transpose to Channel-First format (C, H, W)
        img_normalized = img_rgb.astype(np.float32) / 255.0
        img_chw = np.transpose(img_normalized, (2, 0, 1))

        # Flatten the input array data into our pinned TensorRT Host Memory allocation
        inputs[0]['host'][:] = img_chw.ravel()

        # --- TENSORRT INFERENCE ---
        # Asynchronously copy memory from CPU host to GPU device
        cuda.memcpy_htod_async(inputs[0]['device'], inputs[0]['host'], stream)
        # Execute the model mapping
        context.execute_async_v2(bindings=bindings, stream_handle=stream.handle)
        # Asynchronously copy back predictions from GPU device to CPU host
        cuda.memcpy_dtoh_async(outputs[0]['host'], outputs[0]['device'], stream)
        # Wait for all streams to finish execution steps
        stream.synchronize()

        # --- POST-PROCESSING ---
        # YOLO26 End-to-End shape maps to exactly (1, 300, 6)
        # 6 elements contain: [x1, y1, x2, y2, confidence_score, class_id]
        predictions = outputs[0]['host'].reshape(1, 300, 6)[0]

        for pred in predictions:
            x1, y1, x2, y2, score, class_id = pred

            if score < CONF_THRESHOLD:
                continue  # Skip predictions below target threshold

            # Map the coordinates back to the source RealSense frame size (640x480)
            x1_scaled = int(x1 * (w_orig / input_w))
            y1_scaled = int(y1 * (h_orig / input_h))
            x2_scaled = int(x2 * (w_orig / input_w))
            y2_scaled = int(y2 * (h_orig / input_h))

            class_id = int(class_id)
            label = f"{CLASS_NAMES[class_id] if class_id < len(CLASS_NAMES) else class_id}: {score:.2f}"

            # Draw the bounding box and class text overlay onto screen output
            cv2.rectangle(frame_raw, (x1_scaled, y1_scaled), (x2_scaled, y2_scaled), (0, 255, 0), 2)
            cv2.putText(frame_raw, label, (x1_scaled, max(y1_scaled - 10, 15)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Render output stream tracking frame
        cv2.imshow('Jetson AGX Xavier - RealSense YOLO26 Inference', frame_raw)

        # Press 'ESC' key to end application processing loops safely
        if cv2.waitKey(1) == 27:
            break
finally:
    pipeline.stop()
    cv2.destroyAllWindows()
