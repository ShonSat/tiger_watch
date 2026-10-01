import tensorrt as trt
import pycuda.driver as cuda
import pycuda.autoinit
from charset_normalizer import detect
import sys

# Script takes 1 parameter: full path to TRT model
if len(sys.argv) < 2:
    print("Error: missing model path argument")
    sys.exit()
my_engine = sys.argv[1]
#################### TensorRT: engine inspection #########################


# Load the TensorRT engine
def inspect_engine(engine_path):
    logger = trt.Logger(trt.Logger.INFO)
    
    #with open("best.engine", "rb") as f:
    with open(engine_path, "rb") as f:
        engine_data = f.read()

    runtime = trt.Runtime(logger)
    engine = runtime.deserialize_cuda_engine(engine_data)



    print("TensorRT engine loaded successfully!")
    print(f"Number of bindings: {engine.num_bindings}")

    for i in range(engine.num_bindings):
        name = engine.get_tensor_name(i)
        shape = engine.get_tensor_shape(name)
        dtype = engine.get_tensor_dtype(name)
        mode = engine.get_tensor_mode(name)
        
        print(f"Tensor {i} ({mode}): Name='{name}' shape={shape} dtype={dtype}")
    




    # delete TRT objects to free GPU before function exit.
    del context
    del engine
    del runtime

if __name__ == "__main__":
    inspect_engine(my_engine)
    print("Ciao Cacao!")
