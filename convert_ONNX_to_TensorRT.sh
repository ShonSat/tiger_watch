#!/bin/bash
set -euo  # exit if CMD fails with non-zero

onnx2engine() {
  local ONNX_name="$1"
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


LOG_DIR="./logs"
if [ -f "$1" ]; then
  LOG_FILE="$LOG_DIR/$(basename "$0")_$(basename "$1").log"
else [ -d "$1" ];
  LOG_FILE="$LOG_DIR/$(basename "$0")_ONNX_batch_directory_$((10000 + RANDOM % 90000)).log"
fi

if [ ! -d "$LOG_DIR" ]; then
	mkdir -p "$LOG_DIR"
fi
exec > >(tee -a "$LOG_FILE") 2>&1
echo "Saving execution for $0 in $LOG_FILE"

# Check if the onnx argument is missing
if [ -z "$1" ]; then
    echo "Error: No ONNX models provided."
    echo "Usage: $0 <path_to_onnx_file_or_directory>"
    exit 1
fi

user_arg="$1"
# single onnx file
if [ -f "$user_arg" ]; then
    echo "Target file: $user_arg"
    onnx2engine "$user_arg"
# directory
elif [ -d "$user_arg" ]; then
    echo "Target directory: $user_arg."
    echo "Scanning for .onnx files"
    ls -lah "$user_arg"/*.onnx
    for file in "$user_arg"*.onnx; do
        onnx2engine "$file"   # process *.onnx files in a loop
    done
else
    echo "Error: $user_arg is not a valid file or directory." >&2 # redirect stdout to stderr
    exit 1
fi



