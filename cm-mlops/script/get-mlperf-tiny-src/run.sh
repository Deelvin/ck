#!/bin/bash

CUR_DIR=$PWD
SCRIPT_DIR=${CM_TMP_CURRENT_SCRIPT_PATH}

echo "******************************************************"
echo "Cloning MLCommons from ${CM_GIT_URL} with branch ${CM_GIT_CHECKOUT} ${CM_GIT_DEPTH} ${CM_GIT_RECURSE_SUBMODULES} ..."

if [ ! -d "tiny" ]; then
    if [ -z ${CM_GIT_SHA} ]; then
        git clone ${CM_GIT_RECURSE_SUBMODULES} -b "${CM_GIT_CHECKOUT}" ${CM_GIT_URL} ${CM_GIT_DEPTH} tiny
        cd tiny
    else
        git clone ${CM_GIT_RECURSE_SUBMODULES} ${CM_GIT_URL} ${CM_GIT_DEPTH} tiny
        cd tiny
        git checkout -b "${CM_GIT_CHECKOUT}"
    fi
    if [ "${?}" != "0" ]; then 
        exit 1 
    fi

cd "$CUR_DIR"