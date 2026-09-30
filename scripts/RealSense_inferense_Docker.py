import time
import cv2
import numpy as np
import pyrealsense2 as rs
from ultralytics import YOLO


def main():
    # 1. Initialize the YOLO model using the TensorRT engine format
    # Inside Docker, point this to your mounted volume path
    model_path = "/workspace/tiger_watch/runs/train/tiger_watch_yolo/weights/best.engine"
    print(f"[INFO] Loading TensorRT Engine: {model_path}...")
    model = YOLO(model_path, task="detect")

    # 2. Configure the RealSense Pipeline
    pipeline = rs.pipeline()
    config = rs.config()

    # Configure streams (D435 optimal resolution/FPS for edge inference)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

    # Start streaming
    print("[INFO] Starting Intel RealSense D435 pipeline...")
    pipeline.start(config)

    try:
        print("[INFO] Pipeline active. Press 'q' in the display window to exit.")
        while True:
            start_time = time.time()

            # Wait for a coherent pair of frames (depth and color)
            frames = pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()

            if not color_frame:
                continue

            # Convert RealSense frame to a standard NumPy array for OpenCV/YOLO
            frame = np.asanyarray(color_frame.get_data())

            # 3. Run Inference via TensorRT
            # verbose=False keeps the terminal clean for accurate benchmarking
            results = model(frame, verbose=False, device=0)

            # 4. Calculate FPS & Profile Performance
            fps = 1.0 / (time.time() - start_time)

            # 5. Draw bounding boxes and FPS overlay using Ultralytics plotting tool
            annotated_frame = results[0].plot()
            cv2.putText(
                annotated_frame, f"Edge FPS: {fps:.2f}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2
            )

            # 6. Display the stream
            cv2.imshow("Tiger Watch - Jetson AGX Xavier Inference", annotated_frame)

            # Break loop on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception as e:
        print(f"[ERROR] An error occurred during runtime: {e}")

    finally:
        # Stop streaming and close windows safely
        print("[INFO] Closing camera pipeline and destroying windows.")
        pipeline.stop()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
