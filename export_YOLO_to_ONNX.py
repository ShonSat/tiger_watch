from ultralytics import YOLO

# load best custom-trained weights from the run directory
model = YOLO("runs/train/tiger_watch_yolo/weights/best.pt")

# Export to ONNX format
# dynamic=False is critical because TensorRT likes fixed image shapes for optimization
model.export(format='onnx', imgsz=640, dynamic=False)

