 
# load best custom-trained weights from the run directory
model = YOLO("runs/train/tiger_watch_yolo/weights/best.pt")

#Export to ONNX format
# dynamic=False is critical because TensorRT likes fixed image shapes for optimization
model.export(format='onnx', imgsz=640, dynamic=False)
 

execution:
```
**/home/shon/PycharmProjects/tiger_watch/.venv/bin/python /home/shon/PycharmProjects/tiger_watch/export_YOLO_to_ONNX.py 
Ultralytics 8.4.82 🚀 Python-3.12.3 torch-2.12.1+cu130 CPU (AMD Ryzen 7 8700F 8-Core Processor)
YOLO26n summary (fused): 122 layers, 2,376,006 parameters, 0 gradients, 5.2 GFLOPs

PyTorch: starting from 'runs/train/tiger_watch_yolo/weights/best.pt' with input shape (1, 3, 640, 640) BCHW and output shape(s) (1, 300, 6) (5.1 MB)
...

ONNX: starting export with onnx 1.22.0 opset 20...
/home/shon/PycharmProjects/tiger_watch/.venv/lib/python3.12/site-packages/torch/onnx/_internal/torchscript_exporter/symbolic_opset11.py:954: UserWarning: Exporting aten::index operator of advanced indexing in opset 20 is achieved by combination of multiple ONNX operators, including Reshape, Transpose, Concat, and Gather. If indices include negative values, the exported graph will produce incorrect results.
  return opset9.index(g, self, index)
ONNX: slimming with onnxslim 0.1.94...
ONNX: export success ✅ 4.5s, saved as 'runs/train/tiger_watch_yolo/weights/best.onnx' (9.4 MB)

Export complete (4.7s)
Results saved to /home/shon/PycharmProjects/tiger_watch/runs/train/tiger_watch_yolo/weights/best.onnx
Predict:         yolo predict task=detect model=runs/train/tiger_watch_yolo/weights/best.onnx imgsz=640 
Validate:        yolo val task=detect model=runs/train/tiger_watch_yolo/weights/best.onnx imgsz=640 data=/home/shon/Sandbox/datasets/YOLO_wildlife/dataset.yaml  
Visualize:       https://netron.app
``` 
