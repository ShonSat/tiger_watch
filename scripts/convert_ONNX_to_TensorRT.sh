#!/bin/bash
set -euo pipefail

onnx2engine() {
  local ONNX_name="$1"
  echo "========================================================================"
  echo ""
  echo "Now processing: $(basename "$1")"
  # Extract the base name to dynamically name the output engine
  ENGINE_name="${ONNX_name%.*}.engine"   # swap out the last extension after .

  # Execute trtexec
  /usr/src/tensorrt/bin/trtexec \
          --onnx="$ONNX_name" \
          --saveEngine="$ENGINE_name" \
          --fp16 \
          --verbose

  echo "Saved file: $ENGINE_name"
}


if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <path_to_onnx_file_or_directory>"
    exit 1
fi

user_arg="$1"
if [ ! -f "$user_arg" ] && [ ! -d "$user_arg" ]; then
    echo "Error: $user_arg is not a valid file or directory." >&2
    exit 1
fi

LOG_DIR="./logs"
if [ -f "$user_arg" ]; then
  LOG_FILE="$LOG_DIR/$(basename "$0")_$(basename "$user_arg").log"
elif [ -d "$user_arg" ]; then
  LOG_FILE="$LOG_DIR/$(basename "$0")_ONNX_batch_directory_$((10000 + RANDOM % 90000)).log"
fi

if [ ! -d "$LOG_DIR" ]; then
	mkdir -p "$LOG_DIR"
fi
exec > >(tee -a "$LOG_FILE") 2>&1
echo "Saving execution for $0 in $LOG_FILE"

# single onnx file
if [ -f "$user_arg" ]; then
    echo "Target file: $user_arg"
    onnx2engine "$user_arg"
# directory
elif [ -d "$user_arg" ]; then
    echo "Target directory: $user_arg."
    echo "Scanning for .onnx files"
    ls -lah "$user_arg"/*.onnx
    for file in "$user_arg"/*.onnx; do
        onnx2engine "$file"   # process *.onnx files in a loop
    done
else
    echo "Error: $user_arg is not a valid file or directory." >&2 # redirect stdout to stderr
    exit 1
fi



