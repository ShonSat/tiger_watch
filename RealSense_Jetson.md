Jetson AGX Xavier + JetPack 5.1.6 | [https://developer.nvidia.com/embedded/jetpack-sdk-516] | 
| only available for host Ubuntu version 20.04 or less

Realsense SDK setup ref:  https://github.com/realsenseai/librealsense/blob/master/doc/installation_jetson.md
Note: at least 2.5GB of free space needed.

1. Register the server's public key: [https://github.com/realsenseai/librealsense/blob/master/doc/distribution_linux.md#installing-the-packages] 

2. install SDK:
    - A)  pre-compiled SDK
```
sudo apt-get install librealsense2-utils
sudo apt-get install librealsense2-dev
```
    - B)  compile SDK from source using Native Backend with GPU enabled
     
    Use the V4L Native backend by applying the kernel patching.
        - Fetch the kernel source trees required to build the kernel and its modules.
        - Apply Librealsense-specific kernel patches and build the modified kernel modules.
        - Try to insert the modules into the kernel.
```
git clone https://github.com/IntelRealSense/librealsense.git
cd librealsense/
./scripts/patch-realsense-ubuntu-L4T.sh    # let it run 30min
```

    Build librealsense2 SDK.
    The CMAKE -DBUILD_WITH_CUDA=true flag assumes CUDA modules are installed. 
```
sudo apt-get install libglfw3-dev libgl1-mesa-dev libglu1-mesa-dev
sudo apt-get install git libssl-dev libusb-1.0-0-dev libudev-dev pkg-config libgtk-3-dev -y
./scripts/setup_udev_rules.sh  
mkdir build && cd build  
cmake .. -DBUILD_EXAMPLES=true -DCMAKE_BUILD_TYPE=release -DFORCE_RSUSB_BACKEND=false -DBUILD_WITH_CUDA=true && make -j$(($(nproc)-1)) && sudo make install
```
CUDA Compilation Flags: -DBUILD_WITH_CUDA=true in the cmake block. 
Omitting this causes the depth alignment layer calculations to fall back to the CPU, severely throttling your frame rate.

3. Sanity check SDK with sample realsense app
```
# git clone https://github.com/IntelRealSense/librealsense.git
cd librealsense/example/sample
g++ -std=c++11 filename.cpp -lrealsense2
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

5. Start realsense-viewer app:
```
cd ~/librealsense/tools
realsense-viewer
```
https://github.com/ShonCamarlinghi/tiger_watch/issues/1#issue-4864595931  

