#!/bin/bash
set -e  # exit if CMD fails

# Check if the onnx argument is missing
if [ -z "$1" ]; then
    echo "Error: No ONNX model provided."
    echo "Usage: $0 <path_to_model.onnx>"
    exit 1
fi

ONNX_name="$1"
LOG_DIR="./logs"
LOG_FILE="$LOG_DIR/jetson_trtexec_onnx2engine.log"
if [ ! -d "$LOG_DIR" ]; then
	mkdir -p "$LOG_DIR"
fi
exec > >(tee -a "$LOG_FILE") 2>&1
echo "Saving log for "$0" execution in $LOG_FILE"

echo "Saving log for $0 execution in $LOG_FILE"
echo "trtexec now will convert ONNX model: $ONNX_name to .engine format."

# Extract the base name to dynamically name the output engine
ENGINE_name="${ONNX_name%.*}.engine"   # swap out the last extension after .

# Execute trtexec
/usr/src/tensorrt/bin/trtexec \
    --onnx="$ONNX_name" \
    --saveEngine="$ENGINE_name" \
    --fp16 \
    --verbose

