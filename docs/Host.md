#### Host system SW Environment setup for model training
OS: Ubuntu 24.04 

venv setup in terminal
```bash
python -m venv .venv
source .venv/bin/activate            # Linux
python --version                     # confirm 3.9+  
```

```bash
pip install -r requirements.txt
```
Besides other packages needed for the project, requirement.txt contains ultralytics.   
"pip install ultralytics" gets you the following:
- ultralytics python package (up to version 12 currently supported)
- Yolo command-line tool
- a pinned PyTorch matching your platform

To access environment with ultralytics and torch:
```bash
source .venv/bin/activate
```
Run yolo check
```bash
cd ~/tiger_watch
yolo check
```
Output:
```  
(.venv) (base) shon@s2:~/PycharmProjects/tiger_watch$ yolo check
Ultralytics 8.4.82 🚀 Python-3.12.3 torch-2.12.1+cu130 CUDA:0 (NVIDIA GeForce RTX 4060 Ti, 7806MiB)
Setup: complete ✅ (16 CPUs, 31.0 GB RAM, 292.6/914.8 GB disk)

OS                     Linux-6.17.0-29-generic-x86_64-with-glibc2.39
Environment            Linux
Python                 3.12.3
Install                git
Path                   /home/shon/PycharmProjects/tiger_watch/.venv/lib/python3.12/site-packages/ultralytics
RAM                    30.99 GB
Disk                   292.6/914.8 GB
CPU                    AMD Ryzen 7 8700F 8-Core Processor
CPU count              16
GPU                    NVIDIA GeForce RTX 4060 Ti, 7806MiB
GPU count              1
CUDA                   13.0
numpy                  ✅ 2.5.0>=1.23.0
matplotlib             ✅ 3.11.0>=3.3.0
opencv-python          ✅ 4.13.0.92>=4.6.0
pillow                 ✅ 12.2.0>=7.1.2
pyyaml                 ✅ 6.0.3>=5.3.1
requests               ✅ 2.34.2>=2.23.0
torch                  ✅ 2.12.1>=1.8.0
torch                  ✅ 2.12.1!=2.4.0,>=1.8.0; sys_platform == "win32"
torchvision            ✅ 0.27.1>=0.9.0
psutil                 ✅ 7.2.2>=5.8.0
polars                 ✅ 1.42.0>=0.20.0
nvidia-ml-py           ✅ 13.610.43>=12.0.0
ultralytics-thop       ✅ 2.0.20>=2.0.18
(.venv) (base) shon@s2:~/PycharmProjects/tiger_watch$ 
```
Inference sanity check
```bash
yolo predict model=yolo26n.pt source='https://ultralytics.com/images/bus.jpg'
```
Fixed ONNX Shapes: YOLO export command must run with dynamic=False. TensorRT optimization engines on the Jetson platform rely heavily on rigid, static tensor memory allocations for peak execution throughput.


#### Host system SW Environment setup for Jetson app development 
https://developer.nvidia.com/embedded/jetson-linux-r3564
https://docs.nvidia.com/jetson/archives/r35.6.4/DeveloperGuide/AT/JetsonLinuxToolchain.html 

If your dev host Ubuntu version non 20.04, you need to run docker instance with 20.04 and pull nvidia jetson 5.1.6 rootfs and dev environment to match target system, (jetson agx xavier, ubuntu 20.04, cuda11.4, TensoRt8.5.2, etc.), cross-compile tools for ARM aarch64 target (aarch64-linux-gnu-g++), etc.


On host system, download the Jetson Linux R35.6.4 Driver Package (BSP) from NVIDIA, then extract it under ~/Sandbox. That should create ~/Sandbox/Linux_for_Tegra with contents such as tools/samplefs
Download the matching R35.6.4 Sample Root Filesystem and extract it into Linux_for_Tegra/rootfs, then follow NVIDIA’s rootfs instructions to apply the BSP binaries.
Binaries saved here: 
tiger_watch/msc/Jetson_Linux_R35.6.4_aarch64.tbz2
tiger_watch/msc/Tegra_Linux_Sample-Root-Filesystem_R35.6.4_aarch64.tbz2
```
cd ~/Sandbox
sudo tar -xpf Jetson_Linux_R35.6.4_aarch64.tbz2 
sudo tar -xpf Tegra_Linux_Sample-Root-Filesystem_R35.6.4_aarch64.tbz2 \
  -C Jetson_Linux_R35.6.4_aarch64/Linux_for_Tegra/rootfs

ls Jetson_Linux_R35.6.4_aarch64/Linux_for_Tegra/tools/samplefs/nv_build_samplefs.sh



```
 Afterward, Docker’s existing mount, -v "$HOME/Sandbox/Linux_for_Tegra:/l4t", will expose those files under /l4t.
-v "$HOME/Sandbox/Jetson_Linux_R35.6.4_aarch64/Linux_for_Tegra:/l4t"


Install docker, qemu-user-static and qemu-aarch64 
```
sudo apt update && sudo apt install -y docker.io
docker --version

sudo apt update
sudo apt install -y qemu-user-static binfmt-support
sudo update-binfmts --enable qemu-aarch64
cat /proc/sys/fs/binfmt_misc/qemu-aarch64
```

Run ubuntu 20.04 docker container 
inside docker container, mount $HOME/Sandbox/Linux_for_Tegra to /l4t docker directory. 
```
sudo docker run --privileged -it --rm \
  -v "$HOME/Sandbox/Jetson_Linux_R35.6.4_aarch64/Linux_for_Tegra:/l4t" \
  ubuntu:20.04

apt-get update
apt-get install -y qemu-user-static wget sudo
cd /l4t/tools/samplefs
sudo ./nv_build_samplefs.sh --abi aarch64 --distro ubuntu --flavor basic --version focal

cd /l4t
./apply_binaries.sh
```
Note: qemu-user-static lets your x86 host execute ARM64 Linux programs through QEMU’s user-mode emulation. NVIDIA’s rootfs script may need to run ARM64 commands while preparing the Xavier’s ARM64 filesystem, and QEMU enables that.

It does not emulate the full Jetson or its GPU. It won’t run CUDA/TensorRT GPU inference or reproduce Xavier performance.




