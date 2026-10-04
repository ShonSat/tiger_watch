set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR aarch64)

get_filename_component(TIGER_WATCH_ROOT "${CMAKE_CURRENT_LIST_DIR}/../.." ABSOLUTE)
set(BOOTLIN_TOOLCHAIN_ROOT "${TIGER_WATCH_ROOT}/.toolchains/bootlin" CACHE PATH
	"Extracted NVIDIA Bootlin aarch64 toolchain")
set(BOOTLIN_TOOLCHAIN_BIN "${BOOTLIN_TOOLCHAIN_ROOT}/bin" CACHE PATH
	"Directory containing the Bootlin cross-compiler executables")
set(JETSON_SYSROOT "$ENV{HOME}/Sandbox/Linux_for_Tegra/rootfs" CACHE PATH
	"Jetson R35.6.5 BSP target root filesystem")

set(glfw3_DIR "${JETSON_SYSROOT}/usr/lib/aarch64-linux-gnu/cmake/glfw3" CACHE PATH
	"GLFW3 CMake package directory in the Jetson sysroot")
set(OpenCV_DIR "${JETSON_SYSROOT}/usr/lib/aarch64-linux-gnu/cmake/opencv4" CACHE PATH
	"OpenCV CMake package directory in the Jetson sysroot")
set(OPENGL_opengl_LIBRARY "${JETSON_SYSROOT}/usr/lib/aarch64-linux-gnu/libOpenGL.so" CACHE FILEPATH
	"OpenGL library in the Jetson sysroot")
set(OPENGL_glx_LIBRARY "${JETSON_SYSROOT}/usr/lib/aarch64-linux-gnu/libGLX.so" CACHE FILEPATH
	"GLX library in the Jetson sysroot")
set(GLU_LIBRARY "${JETSON_SYSROOT}/usr/lib/aarch64-linux-gnu/libGLU.so" CACHE FILEPATH
	"GLU library in the Jetson sysroot")

set(CMAKE_SYSROOT "${JETSON_SYSROOT}")

set(ENV{PKG_CONFIG_SYSROOT_DIR} "${JETSON_SYSROOT}")
set(ENV{PKG_CONFIG_LIBDIR}
	"${JETSON_SYSROOT}/usr/lib/aarch64-linux-gnu/pkgconfig:${JETSON_SYSROOT}/usr/local/lib/pkgconfig:${JETSON_SYSROOT}/usr/share/pkgconfig:${JETSON_SYSROOT}/usr/lib/pkgconfig")
set(ENV{PKG_CONFIG_PATH} "")

set(JETSON_MULTIARCH_INCLUDE_DIR "${JETSON_SYSROOT}/usr/include/aarch64-linux-gnu")
set(JETSON_MULTIARCH_LIBRARY_DIR "${JETSON_SYSROOT}/usr/lib/aarch64-linux-gnu")
set(CMAKE_C_FLAGS_INIT
	"-isystem ${JETSON_MULTIARCH_INCLUDE_DIR} -B${JETSON_MULTIARCH_LIBRARY_DIR}/")
set(CMAKE_CXX_FLAGS_INIT
	"-isystem ${JETSON_MULTIARCH_INCLUDE_DIR} -B${JETSON_MULTIARCH_LIBRARY_DIR}/")
set(CMAKE_EXE_LINKER_FLAGS_INIT
	"-L${JETSON_MULTIARCH_LIBRARY_DIR} -Wl,-rpath-link,${JETSON_MULTIARCH_LIBRARY_DIR}")

find_program(BOOTLIN_C_COMPILER
	NAMES aarch64-buildroot-linux-gnu-gcc
	PATHS "${BOOTLIN_TOOLCHAIN_BIN}"
	NO_DEFAULT_PATH)
find_program(BOOTLIN_CXX_COMPILER
	NAMES aarch64-buildroot-linux-gnu-g++
	PATHS "${BOOTLIN_TOOLCHAIN_BIN}"
	NO_DEFAULT_PATH)

if(NOT BOOTLIN_C_COMPILER OR NOT BOOTLIN_CXX_COMPILER)
	message(FATAL_ERROR
		"Bootlin GCC 9.3 not found under '${BOOTLIN_TOOLCHAIN_BIN}'. "
		"Set BOOTLIN_TOOLCHAIN_BIN to the directory containing the aarch64 compiler executables.")
endif()

set(CMAKE_C_COMPILER "${BOOTLIN_C_COMPILER}")
set(CMAKE_CXX_COMPILER "${BOOTLIN_CXX_COMPILER}")
set(CMAKE_ASM_COMPILER "${BOOTLIN_C_COMPILER}")

# Ensure CMake searches the target sysroot rather than the host system.
set(CMAKE_FIND_ROOT_PATH "${JETSON_SYSROOT}")
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY)

# Keep the target ABI consistent with Jetson Linux 35.6.5.
set(CMAKE_CROSSCOMPILING_EMULATOR "")

# enable strong security defaults for the target environment.
set(CMAKE_TRY_COMPILE_TARGET_TYPE STATIC_LIBRARY)
