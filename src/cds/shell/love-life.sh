#!/usr/bin/env bash


LL_TAR_GZ=${HOME}/love-life.tar.gz

if [ -e "${LL_TAR_GZ}" ]; then
    echo "removing love-life.tar.gz"
    rm ${LL_TAR_GZ}
fi

cd ${HOME}
rz
tar -zxvf love-life.tar.gz


