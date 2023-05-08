#!/bin/bash

if [[ ${CM_MLPERF_TINY_RTOS_NAME} == "mbed" ]]; then
    cd ${CM_MLPERF_TINY_REFERENCE_SUBMISSION}/${CM_MLPERF_TINY_USE_CASE}
    ./setup_example.sh
fi