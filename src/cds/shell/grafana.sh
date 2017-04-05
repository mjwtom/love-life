#!/usr/bin/env bash


BCE=${HOME}/coding/baidu/bce
BAIDU_GRAFANA=${BCE}/grafana
GRAFANA_TAR_GZ=${BCE}/grafana.tar.gz

if [ -e "${GRAFANA_TAR_GZ}" ]; then
    echo "removing grafana.tar.gz"
    rm ${GRAFANA_TAR_GZ}
fi

cd ${BCE}
rz
echo "extract grafana"
rm -rf grafana
tar -zxvf grafana.tar.gz

cd ${BAIDU_GRAFANA}
python deploy.py


