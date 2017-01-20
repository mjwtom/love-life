#!/usr/bin/env bash

WORK=/home/work/
MJW=majingwei
BIN_DIR=/home/work/normal/cds_system/master/bin/

rm ${BIN_DIR}/master
rm ${BIN_DIR}/master_debug

cp ${WORK}/${MJW}/baidu/bce/cds/output/bin/master_debug ${BIN_DIR}/master

