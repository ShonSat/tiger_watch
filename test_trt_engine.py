import tensorrt as trt
import pycuda.driver as cuda
import pycuda.autoinit
from charset_normalizer import detect
from ultralytics import YOLO
import sys

# Script takes 1 parameter: full path to TRT model
model_engine = sys.argv[1]
#################### TensorRT: engine inspection #########################


# Load the TensorRT engine
logger = trt.Logger(trt.Logger.INFO)
#with open("best.engine", "rb") as f:
with open(model_engine, "rb") as f:
    engine_data = f.read()

runtime = trt.Runtime(logger)
engine = runtime.deserialize_cuda_engine(engine_data)
print("TensorRT engine loaded successfully!")
print(f"  - Number of bindings: {engine.num_bindings}")
for i in range(engine.num_bindings):
    name = engine.get_binding_name(i)
    shape = engine.get_binding_shape(i)
    dtype = engine.get_binding_dtype(i)
    print(f"  - Binding {i}: {name} shape={shape} dtype={dtype}")


########################### Ultralytics: engine inspection ###############################
# Load the exported TensorRT model
#model = YOLO("runs/train/tiger_watch_yolo/weights/best_dynamicOff_end2endOff_opset_9.engine")
model = YOLO(model_engine)
# Run inference
results = model("/home/shon/Sandbox/datasets/YOLO_wildlife/images/val/493977943d101f25.jpg")
# Validate accuracy on the COCO8 dataset
# metrics = model.val(data="coco8.yaml")
metrics =  model.val('/home/shon/Sandbox/datasets/YOLO_wildlife/dataset.yaml')

