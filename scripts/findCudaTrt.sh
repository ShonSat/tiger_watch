#!/bin/bash
#
printf '%s\n' 'CUDA header:'; find /usr/local/cuda/include -name cuda_runtime_api.h -print; printf '%s\n' 'TensorRT header candidates:'; find /usr /opt -name NvInfer.h -print 2>/dev/null | head -20; printf '%s\n' 'TensorRT libraries:'; ldconfig -p | grep -E 'libnvinfer|libnvonnxparser' || true


find /usr/local/cuda /usr/local/cuda-13 /usr/local/cuda-13.2 -name cuda_runtime_api.h -print 2>/dev/null; find /usr/local -iname '*tensorrt*' -o -name NvInfer.h 2>/dev/null | head -40; dpkg -l | grep -Ei 'tensorrt|nvinfer|cuda-toolkit' || true


grep -E 'CUDAToolkit|TENSORRT|OpenCV' ../build/CMakeCache.txt | head -50




