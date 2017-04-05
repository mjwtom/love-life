#!/usr/bin/env bash


EVM_TAR=evm.tar.xz
EVM=evm
BCE=${HOME}/coding/baidu/bce
BAIDU_EVM=${BCE}/${EVM}
EVM_TAR_PATH=${BCE}/${EVM_TAR}

if [ -e "${EVM_TAR_PATH}" ]; then
    echo "removing ${EVM_TAR}"
    rm ${EVM_TAR_PATH}
fi

cd ${BCE}
rz
echo "extract evm"
rm -rf evm
tar -Jxvf ${EVM_TAR}

cd ${BAIDU_EVM}
bcloud build


