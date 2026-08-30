# Install onnx-simplifier
# pip install onnx-simplifier

# Simplify your ONNX model
import onnx
from onnxsim import simplify

# Load the model
model_path='/home/shon/PycharmProjects/tiger_watch/runs/train/tiger_watch_yolo/weights/'
model_name='best_end2endOn_simplifyTrue_nmsOn_max_det100.onnx'
model = onnx.load( model_path + model_name)

# Simplify
model_simp, check = simplify(model)
assert check, 'Simplification failed'

# Save the fixed model
onnx.save(model_simp, model_path + 'simplified_' + model_name)
print('✅ ONNX model simplified successfully!')

