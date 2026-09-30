#!/bin/bash

##### NOTE for script run #######
# Add below line to visudo for jetson username
# nvidia ALL=(ALL:ALL) NOPASSWD:ALL

set -euo pipefail # Guard forces execution to halt immediately if any single underlying dependency install or compilation flag fails
LOG_DIR="./logs"
LOG_FILE="./logs/jetson_yolo_setup.log"
if [ ! -d "$LOG_DIR" ]; then
	mkdir -p "$LOG_DIR"
fi
exec > >(tee -a "$LOG_FILE") 2>&1
echo "Saving installation log for "$0" script in /logs/jetson_yolo_setup.log"


############ Maximize Hardware Power Performance  ####################

# 1. Unlock the maximum performance power profile (MAXN Mode)
sudo nvpmodel -m 0

# 2. Force the CPU and GPU clocks to their absolute maximum frequencies
sudo jetson_clocks

# 3. Verify the changes applied successfully
sudo nvpmodel -q

###########  Python Virtual Environment ################################

# 1. Install the virtualenv tool
sudo apt-get install -y python3-venv

# 2. Create a virtual environment named 'edge_env' in your home folder
python3 -m venv ~/edge_env

# 3. Activate the environment
source ~/edge_env/bin/activate


############ Install Ultralytics on the edge ##########################

# 1. Ensure your pip tool is fully updated
pip install --upgrade pip

# 2. Install the core ultralytics package 
# Note: This will pull basic CPU-bound PyTorch automatically. 
# TensorRT bypassing means we do not need the heavy NVIDIA PyTorch wheel just for trtexec benchmarking.
pip install ultralytics[export]

#The above ultralytics installation will install Torch and Torchvision. However, these two packages installed via pip are not compatible with the Jetson platform, which is based on ARM64 architecture. Therefore, we need to manually install a pre-built PyTorch pip wheel and compile or install Torchvision from source.

#####  Uninstall currently installed PyTorch and Torchvision

pip uninstall torch torchvision

########### Install PyTorch and Torchvision for Jetson
## compatability matrix: https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform-release-notes/pytorch-jetson-rel.html#pytorch-jetson-rel

pip install https://github.com/ultralytics/assets/releases/download/v0.0.0/torch-2.1.0a0+41361538.nv23.06-cp38-cp38-linux_aarch64.whl

pip install https://github.com/ultralytics/assets/releases/download/v0.0.0/torchvision-0.16.2+c6f3977-cp38-cp38-linux_aarch64.whl


########### Install onnxruntime-gpu ##########################33

wget https://nvidia.box.com/shared/static/zostg6agm00fb6t5uisw51qi6kpcuwzd.whl -O onnxruntime_gpu-1.17.0-cp38-cp38-linux_aarch64.whl

pip install onnxruntime_gpu-1.17.0-cp38-cp38-linux_aarch64.whl

# onnxruntime-gpu will automatically revert back the NumPy version to latest. 
# So we need to reinstall NumPy to 1.23.5 to fix an issue by executing:

pip install numpy==1.23.5


```
test
```

