#!/usr/bin/env bash


CDS_TAR=cds.tar.xz
BCE=${HOME}/coding/baidu/bce
BAIDU_CDS=${BCE}/cds
CDS_TAR_PATH=${BCE}/${CDS_TAR}

if [ -e "${CDS_TAR_PATH}" ]; then
    echo "removing ${CDS_TAR}"
    rm ${CDS_TAR_PATH}
fi

cd ${BCE}
rz
echo "extract cds"
rm -rf cds
tar -Jxvf ${CDS_TAR}

cd ${BAIDU_CDS}
bcloud build


