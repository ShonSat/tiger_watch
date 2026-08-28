from ultralytics import YOLO

# load best custom-trained weights from the run directory
#model = YOLO("runs/train/tiger_watch_yolo/weights/best.pt")
model = YOLO("runs/detect/train/tiger_watch_yolo_v9s/weights/best.pt")

# Export to ONNX format
# docs.ultralytics.com/integrations/tensorrt
# https://docs:ultralytics.com/modes/export
# dynamic=False is critical because TensorRT likes fixed image shapes for optimization

# bug https://github.com/ShonSat/tiger_watch/issues/3
# Ultralytics uses a graph simplifier (onnxslim or onnx-simplifier) by default to merge layers.
# Sometimes this process collapses explicit axis mappings into negative values.
# simplify=False
# TensorRT 8.5.2 on Jetson supports onnx opset 17 or less: opset=17
model.export(format='onnx', imgsz=640, dynamic=False, simplify=True, nms=True, verbose=True, opset=12, data='/home/shon/Sandbox/datasets/YOLO_wildlife/')


