Jetson AGX Xavier + JetPack 5.1.6 | [https://developer.nvidia.com/embedded/jetpack-sdk-516] | 
| only available for host Ubuntu version 20.04 or less

Realsense SDK setup ref:  https://github.com/realsenseai/librealsense/blob/master/doc/installation_jetson.md
Note: at least 2.5GB of free space needed.

1. Register the server's public key: [https://github.com/realsenseai/librealsense/blob/master/doc/distribution_linux.md#installing-the-packages] 

2. install SDK:
- A)  pre-compiled SDK
```
sudo mkdir -p /etc/apt/keyrings

curl -sSf https://librealsense.realsenseai.com/Debian/librealsenseai.asc | \
gpg --dearmor | sudo tee /etc/apt/keyrings/librealsenseai.gpg > /dev/null

sudo apt-get install apt-transport-https

echo "deb [signed-by=/etc/apt/keyrings/librealsenseai.gpg] https://librealsense.realsenseai.com/Debian/apt-repo $(lsb_release -cs) main" | \
sudo tee /etc/apt/sources.list.d/librealsense.list

sudo apt update

sudo apt-get install librealsense2-dkms
sudo apt-get install librealsense2-utils
sudo apt-get install librealsense2-dev 
sudo apt-get install librealsense2-dbg

pkg-config --modversion realsense2
rs-enumerate-devices
```

  - B) for multi-camera feed: use the V4L Native Backend by applying the kernel patching.
        - Fetch the kernel source trees required to build the kernel and its modules (at least 4GB space needed)
        - Apply librealsense-specific kernel patches and build the modified kernel modules.
         This modifies the Linux native kernel drivers (Video4Linux / V4L2) directly.
        
        
``` 
git clone https://github.com/realsenseai/librealsense.git
cd librealsense/

./scripts/patch-realsense-ubuntu-L4T.sh    # let it run 30min
```

Build librealsense2 SDK.
CUDA compilation Flags: -DBUILD_WITH_CUDA=true in the cmake block. 
Omitting this causes the depth alignment layer calculations to fall back to the CPU, severely throttling your frame rate.

```sudo apt-get update
sudo apt-get install -y libssl-dev libusb-1.0-0-dev pkg-config libgtk-3-dev libglfw3-dev libglu1-mesa-dev libudev-dev
export PATH=/usr/local/cuda/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
 
./scripts/setup_udev_rules.sh

mkdir build && cd build  
cmake .. -DBUILD_EXAMPLES=true -DCMAKE_BUILD_TYPE=release -DFORCE_RSUSB_BACKEND=false -DBUILD_WITH_CUDA=true && make -j$(($(nproc)-1)) && sudo make install
```


 - C) for single-camera feed: use RSUSB backend.
        - Bypasses the kernel entirely and handles UVC data protocols in user-space using libusb
```
sudo apt-get update && sudo apt-get install -y \
    libssl-dev \
    libusb-1.0-0-dev \
    pkg-config \
    libgtk-3-dev \
    libglfw3-dev \
    libglu1-mesa-dev \
    freeglut3-dev \
    libudev-dev

export PATH=/usr/local/cuda-11.4/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda-11.4/lib64:$LD_LIBRARY_PATH

git clone https://github.com/realsenseai/librealsense.git
cd librealsense/
mkdir build && cd build

cmake .. -DFORCE_RSUSB_BACKEND=ON \
         -DBUILD_WITH_CUDA=ON \
         -DBUILD_EXAMPLES=ON \
         -DCMAKE_BUILD_TYPE=Release

 
make -j$(nproc)


sudo make install 
sudo ldconfig
```
At the end of source compilation and tools rebuild, we set them up system-wide (sudo make install && sudo ldconfig), so realsense apps can be called from any directory.
 
- D) Rebuild source for single-camera feed and realsense2 python wrapper.
```
sudo apt-get install -y python3-dev python3-pip python3-setuptools
sudo apt-get update && sudo apt-get install -y \
    libssl-dev \
    libusb-1.0-0-dev \
    pkg-config \
    libgtk-3-dev \
    libglfw3-dev \
    libglu1-mesa-dev \
    freeglut3-dev \
    libudev-dev

nvcc --version
ls /usr/local/cuda*

export PATH=/usr/local/cuda-11.4/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda-11.4/lib64:$LD_LIBRARY_PATH

git clone https://github.com/realsenseai/librealsense.git
cd ~/librealsense
rm -rf build && mkdir build && cd build

cmake .. -DFORCE_RSUSB_BACKEND=ON \
         -DBUILD_WITH_CUDA=ON \
         -DBUILD_EXAMPLES=ON \
         -DBUILD_OPENCV_EXAMPLES=ON \
         -DBUILD_PYTHON_BINDINGS:bool=ON \
         -DPYTHON_EXECUTABLE=/usr/bin/python3 \
         -DCMAKE_BUILD_TYPE=Release

make -j$(nproc)
sudo make install
sudo ldconfig
```
# 
3. Sanity check SDK with sample realsense app
```
cd examples/  
g++ -std=c++17 filename.cpp -lrealsense2
./a.out
```
4. Connect Intel RealSense Deapth camera (D435) to USB-C port on Jetson and check usb devices:
```
nvidia@ubuntu:~/librealsense/tools$ lsusb
Bus 002 Device 002: ID 8086:0b07 Intel Corp. Intel(R) RealSense(TM) Depth Camera 435   
Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
Bus 001 Device 004: ID 0461:4e66 Primax Electronics, Ltd USB 2.0 Hub
Bus 001 Device 003: ID 258a:0001  
Bus 001 Device 002: ID 1a40:0101 Terminus Technology Inc. Hub
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
```

5. Start realsense-viewer app from any directory:
```
realsense-viewer
```
https://github.com/ShonSat/tiger_watch/issues/1#issue-4864595931  

