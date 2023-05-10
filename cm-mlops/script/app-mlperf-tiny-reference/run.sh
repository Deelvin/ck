#!/bin/bash

if [[ ${CM_MLPERF_TINY_RTOS_NAME} == "mbed" ]]; then
    echo "cd $CM_MLPERF_TINY_REFERENCE_SUBMISSION/$CM_MLPERF_TINY_USE_CASE"
    cd ${CM_MLPERF_TINY_REFERENCE_SUBMISSION}/${CM_MLPERF_TINY_USE_CASE}

    TF_VERSION=v2.3.1
    TF_MAKE_TAGS="cmsis-nn"
    TFMICRO_DIR=tensorflow

    if [ ! -f "$TFMICRO_DIR" ]; then
        wget https://github.com/tensorflow/tensorflow/archive/$TF_VERSION.zip
        unzip -o $TF_VERSION.zip
        pushd tensorflow-*	# we can't use TF_VERSION here, as github seems not to be consistent with naming (v2.3.1 vs 2.3.1) 
        make -f tensorflow/lite/micro/tools/make/Makefile TAGS=$TF_MAKE_TAGS third_party_downloads
        make -f tensorflow/lite/micro/tools/make/Makefile TAGS=$TF_MAKE_TAGS generate_hello_world_mbed_project -j18
        mv -n tensorflow/lite/micro/tools/make/gen/*/prj/hello_world/mbed/* ../
        popd
        rm -rf tensorflow-*
        rm -rf tensorflow/lite/micro/examples/hello_world
    fi
    python3 -m pip install markupsafe==2.0.1 --force
    mbed config root .
    mbed deploy
    cd ./mbed-os
    python3 -m pip install -r requirements.txt
    cd ..

    cp ../../api/internally* api/
    cp ../../main.cpp .
    cp -r ../../util .

    mbed compile -m ${CM_MLPERF_TINY_BOARD} -t GCC_ARM --verbose
    cp BUILD/${CM_MLPERF_TINY_BOARD}/GCC_ARM/${CM_MLPERF_TINY_USE_CASE}.bin /dev/${CM_MLPERF_TINY_PORT}
fi