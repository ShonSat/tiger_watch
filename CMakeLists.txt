cmake_minimum_required(VERSION 3.16)
project(tiger_watch LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Project-wide include paths.
include_directories(${CMAKE_SOURCE_DIR}/include)
include_directories(${CMAKE_SOURCE_DIR}/include/tiger_watch)
include_directories(${CMAKE_SOURCE_DIR}/include/librealsense2)
include_directories(${CMAKE_SOURCE_DIR}/include/librealsense2-gl)
include_directories(${CMAKE_SOURCE_DIR}/third-party)

# RealSense SDK
if (NOT TARGET realsense2::realsense2)
    find_package(realsense2 CONFIG QUIET)
endif()

if (NOT TARGET realsense2::realsense2)
    find_package(PkgConfig REQUIRED)
    pkg_check_modules(REALSENSE2 REQUIRED IMPORTED_TARGET realsense2)
    add_library(realsense2::realsense2 INTERFACE IMPORTED GLOBAL)
    target_link_libraries(realsense2::realsense2 INTERFACE PkgConfig::REALSENSE2)
endif()

# OpenGL + GLFW + GLU needed by the pointcloud examples.
find_package(OpenGL REQUIRED)
find_library(GLU_LIBRARY NAMES GLU REQUIRED)
find_package(glfw3 REQUIRED)

# TensorRT + OpenCV + CUDA are optional for the GPU inference app.
find_package(OpenCV REQUIRED)
find_package(CUDAToolkit QUIET)

# Prefer the system TensorRT install, but allow downstream configs to provide it.
if (NOT TENSORRT_LIBRARY)
    find_library(TENSORRT_LIBRARY NAMES nvinfer libnvinfer)
endif()
if (NOT TENSORRT_PLUGIN_LIBRARY)
    find_library(TENSORRT_PLUGIN_LIBRARY NAMES nvinfer_plugin libnvinfer_plugin)
endif()
if (NOT TENSORRT_INCLUDE_DIR)
    find_path(TENSORRT_INCLUDE_DIR NvInfer.h PATH_SUFFIXES include)
endif()

function(add_realsense_example target source_file)
    add_executable(${target} ${source_file})

    target_include_directories(${target}
        PRIVATE
            ${CMAKE_SOURCE_DIR}/include
            ${CMAKE_SOURCE_DIR}/include/tiger_watch
            ${CMAKE_SOURCE_DIR}/include/librealsense2
            ${CMAKE_SOURCE_DIR}/include/librealsense2-gl
            ${CMAKE_SOURCE_DIR}/third-party
    )

    target_link_libraries(${target}
        PRIVATE
            realsense2::realsense2
            OpenGL::GL
            ${GLU_LIBRARY}
            glfw
    )
endfunction()

# Built-in RealSense samples
add_realsense_example(rs_pointcloud src/rs-pointcloud.cpp)
add_realsense_example(rs_object_detection src/rs-object-detection.cpp)

if(CUDAToolkit_FOUND AND TENSORRT_LIBRARY AND TENSORRT_INCLUDE_DIR)
    add_executable(tiger_watch_trt_object_detection src/trt_object_detection.cpp)

    target_include_directories(tiger_watch_trt_object_detection
        PRIVATE
            ${CMAKE_SOURCE_DIR}/include
            ${CMAKE_SOURCE_DIR}/include/tiger_watch
            ${CMAKE_SOURCE_DIR}/include/librealsense2
            ${CMAKE_SOURCE_DIR}/include/librealsense2-gl
            ${TENSORRT_INCLUDE_DIR}
            ${OpenCV_INCLUDE_DIRS}
    )

    target_link_libraries(tiger_watch_trt_object_detection
        PRIVATE
            realsense2::realsense2
            ${OpenCV_LIBS}
            CUDA::cudart
            ${TENSORRT_LIBRARY}
            ${TENSORRT_PLUGIN_LIBRARY}
    )
endif()

