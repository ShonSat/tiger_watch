# Install onnx-simplifier
# pip install onnx-simplifier

# Simplify your ONNX model
import onnx
from onnxsim import simplify

# Load the model
model_path='/home/shon/PycharmProjects/tiger_watch/runs/detect/train/tiger_watch_yolo_v9s/weights/'
model = onnx.load( model_path + 'best.onnx')

# Simplify
model_simp, check = simplify(model)
assert check, 'Simplification failed'

# Save the fixed model
onnx.save(model_simp, model_path + 'best_simplified_yolo_v9s.onnx')
print('✅ ONNX model simplified successfully!')

