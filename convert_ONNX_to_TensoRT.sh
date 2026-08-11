#!/bin/bash

/usr/src/tensorrt/bin/trtexec --onnx=best.onnx --saveEngine=best_model.engine --fp16
