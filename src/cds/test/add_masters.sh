#!/usr/bin/env bash

BIN_DIR=/home/work/normal/cds_system/tools/

cd ${BIN_DIR}

./bin/cds_tool --op=list_master_node
sleep 3
./bin/cds_tool --op=add_master_node --node=10.99.121.31:8050 --cur_nodes=10.99.121.12:8050
sleep 3
./bin/cds_tool --op=list_master_node
sleep 3
./bin/cds_tool --op=add_master_node --node=10.99.121.13:8050 --cur_nodes=10.99.121.12:8050,10.99.121.31:8050
sleep 3
./bin/cds_tool --op=list_master_node

