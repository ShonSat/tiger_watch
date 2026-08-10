# Issue:
# Ref: https://forums.developer.nvidia.com/t/onnx-model-to-trt-conversion-error/126744/6

import sys
import onnx
#filename = yourONNXmodel
filename = "runs/train/tiger_watch_yolo/weights/best_negative_axis.onnx"
model = onnx.load(filename)
onnx.checker.check_model(model)
