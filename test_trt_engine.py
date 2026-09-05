import tensorrt as trt
import pycuda.driver as cuda
import pycuda.autoinit

# Load the TensorRT engine
logger = trt.Logger(trt.Logger.INFO)
with open("best.engine", "rb") as f:
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