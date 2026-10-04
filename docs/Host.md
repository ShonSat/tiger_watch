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
https://developer.nvidia.com/embedded/jetson-linux-r3565
https://docs.nvidia.com/jetson/archives/r35.6.5/DeveloperGuide/AT/JetsonLinuxToolchain.html 
https://catalog.ngc.nvidia.com/orgs/nvidia/-/containers/l4t-base/-

If your dev host Ubuntu version non 20.04, you need to run docker instance with 20.04 and pull the NVIDIA Jetson 5.1.7 rootfs and dev environment to match the target system (Jetson AGX Xavier, Ubuntu 20.04, CUDA 11.4, TensorRT 8.5.2, etc.), along with the ARM aarch64 cross-compile tools.

On the host system, download the Jetson Linux R35.6.5 Driver Package (BSP) from NVIDIA, then extract it under ~/Sandbox. That creates ~/Sandbox/Linux_for_Tegra with contents such as tools/samplefs.
Download the matching R35.6.5 Sample Root Filesystem and extract it into ~/Sandbox/Linux_for_Tegra/rootfs, then follow NVIDIA’s rootfs instructions to apply the BSP binaries.
Binaries saved here:
tiger_watch/msc/Jetson_Linux_R35.6.5_aarch64.tbz2
tiger_watch/msc/Tegra_Linux_Sample-Root-Filesystem_R35.6.5_aarch64.tbz2
```
cd ~/Sandbox
sudo tar -xpf Jetson_Linux_R35.6.5_aarch64.tbz2
sudo tar -xpf Tegra_Linux_Sample-Root-Filesystem_R35.6.5_aarch64.tbz2 \
  -C ~/Sandbox/Linux_for_Tegra/rootfs

ls ~/Sandbox/Linux_for_Tegra/tools/samplefs/nv_build_samplefs.sh

```

Download the Bootlin GCC 9.3 binary toolchain from [NVIDIA's Bootlin toolchain page](https://developer.nvidia.com/embedded/jetson-linux/bootlin-toolchain-gcc-93). The page downloads the `aarch64--glibc--stable-final.tar.gz` archive. The separate Bootlin toolchain sources archive is not needed to cross-compile applications.

Extract the downloaded archive into the project-local toolchain directory:
```bash
cd ~/Sandbox/3D_cpp/tiger_watch
mkdir -p .toolchains/bootlin
tar -xzf ~/Downloads/aarch64--glibc--stable-final.tar.gz \
  -C .toolchains/bootlin

find "$PWD/.toolchains/bootlin" -type f \
  \( -name '*gcc' -o -name '*g++' \) -print
```
The binaries should be `aarch64-buildroot-linux-gnu-gcc` and `aarch64-buildroot-linux-gnu-g++` under `.toolchains/bootlin/bin`. Keep the extracted toolchain out of version control. The Bootlin compiler provides the host-side cross-compiler; the target sysroot must separately provide ARM64 headers and libraries.

Afterward, Docker’s existing mount, -v "$HOME/Sandbox/Linux_for_Tegra:/l4t", will expose those files under /l4t.
-v "$HOME/Sandbox/Linux_for_Tegra:/l4t"


Install docker, qemu-user-static and qemu-aarch64 
```
sudo apt update && sudo apt install -y docker.io
docker --version

sudo apt update
sudo apt install -y qemu-user-static binfmt-support
sudo update-binfmts --enable qemu-aarch64
cat /proc/sys/fs/binfmt_misc/qemu-aarch64
```

Run ubuntu 20.04 docker container.
Inside the container, mount $HOME/Sandbox/Linux_for_Tegra to the /l4t Docker directory.
```
docker run -it --rm --privileged \
  -v "$HOME/Sandbox/Linux_for_Tegra:/l4t" \
  -w /l4t \
  ubuntu:20.04 /bin/bash
 

apt-get update
apt-get install -y qemu-user-static wget sudo
cd /l4t/tools/samplefs
sudo ./nv_build_samplefs.sh --abi aarch64 --distro ubuntu --flavor basic --version focal

cd /l4t
./apply_binaries.sh
```

Note: qemu-user-static lets your x86 host execute ARM64 Linux programs through QEMU’s user-mode emulation. NVIDIA’s rootfs script may need to run ARM64 commands while preparing the Xavier’s ARM64 filesystem, and QEMU enables that.


Note:
./nv_build_samplefs.sh ran in Docker should create the rootfs and packages under /l4t/rootfs/ and /l4t/tools/samplefs/, which you can verify on the host root where the Docker /l4t mount is stored:
```
shon@s2:~/Sandbox/Linux_for_Tegra$ ls tools/samplefs/
nv_build_samplefs.sh
nvubuntu-focal-aarch64-samplefs
nvubuntu-focal-basic-aarch64-packages
nvubuntu-focal-desktop-aarch64-packages
nvubuntu-focal-minimal-aarch64-packages
nvubuntu_samplefs.sh
sample_fs.tbz2
shon@s2:~/Sandbox/Linux_for_Tegra$ ls rootfs/
bin   dev  home  media  opt   README.txt  run   snap  sys  usr
boot  etc  lib   mnt    proc  root        sbin  srv   tmp  var
```

It does not emulate the full Jetson or its GPU. It won’t run CUDA/TensorRT GPU inference or reproduce Xavier performance.

#### Cross-compiling AArch64 C++ on the host

The Jetson rootfs is the target sysroot. Build the default RealSense examples against target ARM64 libraries; do not let `pkg-config` resolve the host's x86 libraries. The required default dependencies are RealSense 2, OpenGL/GLX, GLU, GLFW, and OpenCV. The TensorRT inference target is optional and needs a separate, matching CUDA/TensorRT cross-link setup.

On the Jetson, install the development packages listed in [Jetson.md](Jetson.md), build/install librealsense as described in [RealSense_Jetson.md](RealSense_Jetson.md), and verify the ARM64 library locations before syncing. The following command copies only the relevant headers, CMake/pkg-config metadata, and libraries while preserving symlinks. Set the two connection variables to your own SSH alias or host details; do not put passwords or private keys in the command.

```bash
export JETSON_USER='<jetson-user>'
export JETSON_HOST='<jetson-host-or-dns-name>'
export JETSON_TARGET="${JETSON_USER}@${JETSON_HOST}"
export JETSON_SYSROOT="$HOME/Sandbox/Linux_for_Tegra/rootfs"

ssh "$JETSON_TARGET" '
  cd / && {
    printf "%s\n" \
      usr/include/GL \
      usr/include/KHR \
      usr/include/GLFW \
      usr/include/opencv4 \
      usr/lib/aarch64-linux-gnu/cmake/glfw3 \
      usr/lib/aarch64-linux-gnu/cmake/opencv4 \
      usr/lib/aarch64-linux-gnu/pkgconfig/glu.pc \
      usr/lib/aarch64-linux-gnu/pkgconfig/glfw3.pc \
      usr/lib/aarch64-linux-gnu/pkgconfig/opencv4.pc \
      usr/share/opencv4 \
      usr/local/include/librealsense2 \
      usr/local/lib/pkgconfig/realsense2.pc
    find usr/lib/aarch64-linux-gnu -maxdepth 1 \
      \( -type f -o -type l \) \
      \( -name "libGL.so*" -o -name "libGLX.so*" -o -name "libOpenGL.so*" \
         -o -name "libGLU.so*" -o -name "libGLU.a" -o -name "libglfw.so*" \
         -o -name "libopencv*.so*" \) -print
    find usr/local/lib -maxdepth 1 \
      \( -type f -o -type l \) \
      \( -name "librealsense2.so*" -o -name "librealsense2-gl.so*" \) -print
  } | tar -C / -cf - -T -
' | sudo tar -C "$JETSON_SYSROOT" -xpf -
```

The current Jetson librealsense pkg-config file uses an x86-style library directory. Correct the copy in the host sysroot only; do not change the Jetson's installed file:
```bash
sudo sed -i -E \
  's#^libdir[[:space:]]*=.*#libdir=${exec_prefix}/lib#' \
  "$JETSON_SYSROOT/usr/local/lib/pkgconfig/realsense2.pc"
```

Set the host build environment. The toolchain file also sets the target pkg-config paths and the Ubuntu ARM64 multiarch include/linker paths when CMake loads it.
```bash
export PROJECT_ROOT="$HOME/Sandbox/3D_cpp/tiger_watch"
export BOOTLIN_TOOLCHAIN_ROOT="$PROJECT_ROOT/.toolchains/bootlin"
export PATH="$BOOTLIN_TOOLCHAIN_ROOT/bin:$PATH"
export CC="$BOOTLIN_TOOLCHAIN_ROOT/bin/aarch64-buildroot-linux-gnu-gcc"
export CXX="$BOOTLIN_TOOLCHAIN_ROOT/bin/aarch64-buildroot-linux-gnu-g++"
export JETSON_SYSROOT="$HOME/Sandbox/Linux_for_Tegra/rootfs"
export PKG_CONFIG_SYSROOT_DIR="$JETSON_SYSROOT"
export PKG_CONFIG_LIBDIR="$JETSON_SYSROOT/usr/lib/aarch64-linux-gnu/pkgconfig:$JETSON_SYSROOT/usr/local/lib/pkgconfig:$JETSON_SYSROOT/usr/share/pkgconfig:$JETSON_SYSROOT/usr/lib/pkgconfig"
unset PKG_CONFIG_PATH
```

Configure a fresh build directory and compile the default AArch64 targets:
```bash
cmake -S "$PROJECT_ROOT" -B "$PROJECT_ROOT/build-jetson-r35.6.5" \
  -DCMAKE_TOOLCHAIN_FILE="$PROJECT_ROOT/cmake/toolchains/jetson-r35.6.5-aarch64.cmake" \
  -DJETSON_SYSROOT="$JETSON_SYSROOT" \
  -DBOOTLIN_TOOLCHAIN_ROOT="$BOOTLIN_TOOLCHAIN_ROOT"

cmake --build "$PROJECT_ROOT/build-jetson-r35.6.5" \
  --target rs_pointcloud rs_object_detection --parallel "$(nproc)"

file "$PROJECT_ROOT/build-jetson-r35.6.5/rs_pointcloud" \
  "$PROJECT_ROOT/build-jetson-r35.6.5/rs_object_detection"
```
The final `file` output should identify both binaries as ARM aarch64. These binaries must run on the Jetson, not on the x86 host. `tiger_watch_trt_object_detection` is conditional in `CMakeLists.txt`; do not rely on the host CUDA installation to satisfy the Jetson CUDA/TensorRT dependencies.