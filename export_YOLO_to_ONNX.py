from ultralytics import YOLO

# load best custom-trained weights from the run directory
model = YOLO("runs/train/tiger_watch_yolo/weights/best.pt")
#model = YOLO("runs/detect/train/tiger_watch_yolo_v9s/weights/best.pt")

# Set the model to end-to-end mode BEFORE exporting
model.model.end2end = True

# Export to ONNX format
# docs.ultralytics.com/integrations/tensorrt
# https://docs:ultralytics.com/modes/export
# dynamic=False is critical because TensorRT likes fixed image shapes for optimization

# bug https://github.com/ShonSat/tiger_watch/issues/3
# Ultralytics uses a graph simplifier (onnxslim or onnx-simplifier) by default to merge layers.
# Sometimes this process collapses explicit axis mappings into negative values.

# TensorRT 8.5.2 on Jetson supports onnx opset 17 or less.
# NMS wraps TopK in a TensorRT-compatible plugin and model runs on GPU.
model.export(format='onnx',
             imgsz=640,
             dynamic=False,
             simplify=True,
             verbose=True,
             opset=12,
            # data='/home/shon/Sandbox/datasets/YOLO_wildlife/',
            # Add NMS operation to the graph.
             nms=True,
             max_det=100,   #topk: max number of detections
             conf=0.25,     # confidence for NMS
             iou=0.45,      # IOU threshold for NMS
)



