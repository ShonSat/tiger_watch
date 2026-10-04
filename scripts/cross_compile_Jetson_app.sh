#!/bin/bash
#
export PROJECT_ROOT="$HOME/Sandbox/3D_cpp/tiger_watch"
export BOOTLIN_TOOLCHAIN_ROOT="/opt/bootlin/aarch64--glibc--stable-final"
export PATH="$BOOTLIN_TOOLCHAIN_ROOT/bin:$PATH"
export CC="$BOOTLIN_TOOLCHAIN_ROOT/bin/aarch64-buildroot-linux-gnu-gcc"
export CXX="$BOOTLIN_TOOLCHAIN_ROOT/bin/aarch64-buildroot-linux-gnu-g++"
export JETSON_SYSROOT="$HOME/Sandbox/Linux_for_Tegra/rootfs"
export PKG_CONFIG_SYSROOT_DIR="$JETSON_SYSROOT"
export PKG_CONFIG_LIBDIR="$JETSON_SYSROOT/usr/lib/aarch64-linux-gnu/pkgconfig:$JETSON_SYSROOT/usr/local/lib/pkgconfig:$JETSON_SYSROOT/usr/share/pkgconfig:$JETSON_SYSROOT/usr/lib/pkgconfig"
unset PKG_CONFIG_PATH


#Configure a fresh build directory and compile the default AArch64 targets:

cmake -S "$PROJECT_ROOT" -B "$PROJECT_ROOT/build-jetson-r35.6.5" \
  -DCMAKE_TOOLCHAIN_FILE="$PROJECT_ROOT/cmake/toolchains/jetson-r35.6.5-aarch64.cmake" \
  -DJETSON_SYSROOT="$JETSON_SYSROOT" \
  -DBOOTLIN_TOOLCHAIN_ROOT="$BOOTLIN_TOOLCHAIN_ROOT"

cmake --build "$PROJECT_ROOT/build-jetson-r35.6.5" \
  --target rs_pointcloud rs_object_detection --parallel "$(nproc)"

file "$PROJECT_ROOT/build-jetson-r35.6.5/rs_pointcloud" \
  "$PROJECT_ROOT/build-jetson-r35.6.5/rs_object_detection"

