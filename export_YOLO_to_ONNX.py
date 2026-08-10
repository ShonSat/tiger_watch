from ultralytics import YOLO

# load best custom-trained weights from the run directory
model = YOLO("runs/train/tiger_watch_yolo/weights/best.pt")

# Export to ONNX format
# https://docs.ultralytics.com/integrations/tensorrt
# https://docs.ultralytics.com/modes/export
# dynamic=False is critical because TensorRT likes fixed image shapes for optimization

# Fix for bug https://github.com/ShonSat/tiger_watch/issues/3
# Ultralytics uses a graph simplifier (onnxslim or onnx-simplifier) by default to merge layers.
# Sometimes this process collapses explicit axis mappings into negative values.
# simplify=False
model.export(format='onnx', imgsz=640, dynamic=False, simplify=False, verbose=True, opset=17)




