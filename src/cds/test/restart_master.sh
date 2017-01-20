#!/usr/bin/env bash

CDS_DIR=/home/work/normal/cds_system/

cd ${CDS_DIR}
sh cds_control/stop_master.sh
sleep 5
sh cds_control/start_master.sh


