from ultralytics import YOLO

'''
Export to ONNX format
docs.ultralytics.com/integrations/tensorrt
https://docs:ultralytics.com/modes/export

I'm tweaking parameters for export to ONNX format to address https://github.com/ShonSat/tiger_watch/issues/6
simplify=False  # Ultralytics uses a graph simplifier (onnxslim or onnx-simplifier) by default to merge layers.
                  Sometimes this process collapses explicit axis mappings into negative values.
dynamic=False  # is critical to set dynamic=False, because TensorRT likes fixed image shapes for optimization
opset=12       # TensorRT 8.5.2 on Jetson supports onnx opset 17 or less.
quantize=8     # quantization step requires path to the training dataset yaml
data='/home/shon/Sandbox/datasets/YOLO_wildlife/',  # needed for quantization
nms=True       # NMS wraps TopK in a TensorRT-compatible plugin and model runs on GPU.
max_det=100,   #topk: max number of detections, to reduce complexity
conf=0.25,     # confidence for NMS
iou=0.45,      # IOU threshold for NMS

'''

# load best custom-trained weights from the run directory
model = YOLO("runs/train/tiger_watch_yolo/weights/best.pt")
# model = YOLO("runs/detect/train/tiger_watch_yolo_v9s/weights/best.pt")

# Set the model to end-to-end mode BEFORE exporting
model.model.end2end = True

# Export to ONNX
model.export(format='onnx',
             imgsz=640,
             dynamic=False,
             simplify=False,
             verbose=True,
             opset=12,
             nms=True,      # Add NMS operation with its arguments to the graph.
             max_det=100,   # topk: max number of detections
             conf=0.25,     # confidence for NMS
             iou=0.45,      # IOU threshold for NMS
)



