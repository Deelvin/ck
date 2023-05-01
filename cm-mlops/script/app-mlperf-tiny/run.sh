#!/bin/bash

cd ${CM_MLPERF_TINY_REFERENCE_SUBMISSION}/${CM_MLPERF_TINY_USE_CASE}/setup_example.sh

mbed compile -m ${CM_MLPERF_TINY_BOARD_TARGET} -t GCC_ARM
