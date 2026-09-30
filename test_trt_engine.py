import tensorrt as trt
import pycuda.driver as cuda
import pycuda.autoinit
from charset_normalizer import detect
#from ultralytics import YOLO
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
    
    #read engine binary data stream into engine_data object
    with open(engine_path, "rb") as f:
        engine_data = f.read()

    '''
    create empty trt.Runtime object that has: 
        - a pointer to trt.Logger
        - inits default memory allocator to comm to CUDA driver to claim and release VRAM blocks on jetson;
        - GPU context init by pyCuda: it IDs Compute Capability to handle to .engine file
        - Deserialization engine blueprint: core internal logic and C++ backend functions to read and decode heavily optimized TenorRT structural format. 
    '''
    runtime = trt.Runtime(logger)


    '''
    Deserialize .engine byte stream into ICudaEngine object:
        - Parse bytestream and decodes structural map of the network architecture.
        - Load weights into VRAM: allocates memory blocks and populates with model weights and biases.
        - Recontructs CUDA kernels: prepares CUDA kernels preselected during compilation, so they are armed and ready to execute.
        - Returns ICudaEngine Engine object that holds engines structural metadata (tensor names, shapes, dtypes) and a template for execution context for running inference. Note: ICudaEngine can not run data by itself (it's stateless) to perform inference. It needs IExecutionContext object as active workspace. 
    '''
    engine = runtime.deserialize_cuda_engine(engine_data)

    
    print("TensorRT engine loaded successfully!")
    print(f"Number of bindings: {engine.num_bindings}")

    for i in range(engine.num_bindings):
        name = engine.get_tensor_name(i)
        shape = engine.get_tensor_shape(name)
        dtype = engine.get_tensor_dtype(name)
        mode = engine.get_tensor_mode(name)
        
        print(f"Tensor {i} ({mode}): Name='{name}' shape={shape} dtype={dtype}")
    
    # delete TRT objects tp free GPU before function exit.
    del engine
    del runtime

if __name__ == "__main__":
    inspect_engine(my_engine)
    print("Ciao!!!")


'''
########################### Ultralytics: engine inspection ###############################
# Load the exported TensorRT model
model = YOLO("runs/train/tiger_watch_yolo/weights/best_dynamicOff_end2endOff_opset_9.engine")

model = YOLO(model_engine)
# Run inference
results = model("/home/shon/Sandbox/datasets/YOLO_wildlife/images/val/493977943d101f25.jpg")
# Validate accuracy on the COCO8 dataset
metrics = model.val(data="coco8.yaml")
metrics =  model.val('/home/shon/Sandbox/datasets/YOLO_wildlife/dataset.yaml')
'''
