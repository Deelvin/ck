#!/bin/bash

sudo apt update && sudo apt install mercurial -y

mbed --version > tmp-ver.out

# mbed config -G ARM_PATH ${CM_GCC_ARM_BIN_PATH}
