#!/usr/bin/env bash

WORK=/home/work/
MJW=majingwei
BIN_DIR=/home/work/normal/cds_system/master/bin/
KSK=/home/work/kongshuaikang/cds_system_test/cds2/auto-deploy-cds/
CDS_SYS=/home/work/normal/cds_system

cd ${KSK}/shell
sh stop_cluster.sh
sh clear_cluster.sh

cd ${KSK}/bin

sh install.sh

for node in cp01-sys-rpm-rdqa238.cp01.baidu.com cp01-sys-rpm-rdqa237.cp01.baidu.com
do
    ssh root@${node} "rm -rf /${WORK}/${MJW}"
    cd ${WORK}
    echo `pwd`
    echo "scp -r ${MJW} root@{node}:${WORK}"
    scp -r ${MJW} root@${node}:${WORK}
    ssh root@${node} "sh /${WORK}/${MJW}/scripts/replace.sh"
    ssh root@${node} "sh /${WORK}/${MJW}/scripts/restart_master.sh"
done

sh /${WORK}/${MJW}/scripts/replace.sh
sh /${WORK}/${MJW}/scripts/restart_master.sh
sleep 5
sh /${WORK}/${MJW}/scripts/add_masters.sh

sleep 30

for node in cp01-sys-rpm-rdqa238.cp01.baidu.com cp01-sys-rpm-rdqa237.cp01.baidu.com
do
    ssh root@${node} "cd ${CDS_SYS} && sh cds_control/stop_blockserver.sh"
done

cd ${CDS_SYS}/tools
./bin/cds_tool --op=list_master_node
./bin/cds_tool --op=list_region

sleep 130

cd ${CDS_SYS}/tools
./bin/cds_tool --op=list_master_node
./bin/cds_tool --op=list_region

