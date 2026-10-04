## ONNX to TensorRT Engine on Jetson

Export the model with a fixed 640x640 input shape (`dynamic=False`) as described in [Export_YOLO_to_ONNX.md](Export_YOLO_to_ONNX.md). Copy the ONNX file to the Jetson; build the TensorRT engine on the target device so it matches the Jetson GPU and installed TensorRT version.

From the host, set the Jetson SSH destination and copy the exported model:
```bash
export JETSON_TARGET='<jetson-user>@<jetson-host>'
ONNX_MODEL='runs/train/tiger_watch_yolo/weights/best.onnx'
scp "$ONNX_MODEL" "$JETSON_TARGET:~/tiger_watch/models/"
```

On the Jetson, convert the ONNX file to an FP16 engine with the repository script, then ask TensorRT to load and execute the serialized engine:
```bash
cd ~/tiger_watch
ONNX_MODEL='models/best.onnx'
ONNX_MODEL_DIR='models/'
bash scripts/convert_ONNX_to_TensorRT.sh "$ONNX_MODEL"   
bash scripts/convert_ONNX_to_TensorRT.sh "$ONNX_MODEL_DIR"   


ENGINE_MODEL="${ONNX_MODEL%.*}.engine"
/usr/src/tensorrt/bin/trtexec --loadEngine="$ENGINE_MODEL" --verbose
```

The conversion script saves the `.engine` beside its input ONNX file and writes conversion output under `logs/`. Successful `trtexec` execution confirms that TensorRT can deserialize and run the engine; it does not replace checking detection accuracy with representative images or camera input.

### Inspect an engine with the Python test script

The repository currently provides `scripts/test_trt_engine.py` (not `test_trt_engine.sh`). It loads the serialized engine with the Jetson's TensorRT Python bindings and prints its binding count, tensor names, shapes, data types, and input/output modes. Run it on the Jetson with the engine path as its only argument:
```bash
cd ~/tiger_watch
ENGINE_MODEL='models/best.engine'
python3 scripts/test_trt_engine.py "$ENGINE_MODEL"
```

The Python environment must be able to import TensorRT and PyCUDA. A successful run prints `TensorRT engine loaded successfully!` followed by the engine's binding details. This checks that the engine can be deserialized and inspected; use the `trtexec --loadEngine` command above to also execute it with TensorRT-generated input data.

TensorRT engine plans are hardware- and software-stack-specific. Keep the ONNX model as the portable source artifact and regenerate the engine on the target Jetson when changing the GPU, TensorRT/CUDA version, precision, or build options. Do not assume an engine produced on an x86 host or a different Jetson is compatible. See bugs: https://github.com/ShonSat/tiger_watch/issues/3  and  https://github.com/ShonSat/tiger_watch/issues/6 



