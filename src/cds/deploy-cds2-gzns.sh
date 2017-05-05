#!/usr/bin/env bash

#before run the script, please change the configuration

# some configurations

# masters
MASTERS="gzns-cds-ssd060.gzns
gzns-cds-ssd066.gzns
gzns-cds-ssd044.gzns"
# we have to start a master as the leader first (bootstrap)
LEADER_MASTER=`echo ${MASTERS} | awk '{print $1}'`
FOLLOWER_MASTERS=`echo ${MASTERS} | sed -r 's/^[^ ]* *//g'`
# blockservers
BLOCKSERVERS="gzns-cds-ssd060.gzns
gzns-cds-ssd066.gzns
gzns-cds-ssd044.gzns
gzns-cds-ssd061.gzns
gzns-cds-ssd033.gzns
gzns-cds-ssd092.gzns
gzns-cds-ssd072.gzns
gzns-cds-ssd080.gzns
gzns-cds-ssd039.gzns
gzns-cds-ssd079.gzns"
#heavyworks
HEAVYWORKERS="gzns-cds-ssd072.gzns
gzns-cds-ssd080.gzns
gzns-cds-ssd039.gzns
gzns-cds-ssd079.gzns"
#cds_tool, do not have to be a remote server
CDS_TOOL_SERVER=gzns-cds-ssd060.gzns
###### end the configuration ######

# after binding dns use the bound dns, but now, we have to use this one
# TODO: change it to DNS
MASTER_DNS=${LEADER_MASTER}
#MASTER_DNS="cluster.cds.gzns.bce-internal.baidu.com"
MASTER_PORT=8987
BLOCKSERVER_PORT=8977
HEAVYWORKER_PORT=8990
CDS_TOOL_PORT=8988

LOCAL_HOME=`pwd`
LOCAL_BIN_DIR=${LOCAL_HOME}/output/bin
LOCAL_CONF_DIR=${LOCAL_HOME}/output/conf

REMOTE_HOME=/home/cds

REMOTE_MASTER_DIR=${REMOTE_HOME}/master
REMOTE_MASTER_BIN_DIR=${REMOTE_MASTER_DIR}/bin
REMOTE_MASTER_CONF_DIR=${REMOTE_MASTER_DIR}/conf

REMOTE_BLOCKSERVER_DIR=${REMOTE_HOME}/blockserver
REMOTE_BLOCKSERVER_BIN_DIR=${REMOTE_BLOCKSERVER_DIR}/bin
REMOTE_BLOCKSERVER_CONF_DIR=${REMOTE_BLOCKSERVER_DIR}/conf

REMOTE_HEAVYWORKWE_DIR=${REMOTE_HOME}/heavyworker
REMOTE_HEAVYWORKWE_BIN_DIR=${REMOTE_HEAVYWORKWE_DIR}/bin
REMOTE_HEAVYWORKER_CONF_DIR=${REMOTE_HEAVYWORKWE_DIR}/conf

REMOTE_CDS_TOOL_DIR=${REMOTE_HOME}/cds_tool
REMOTE_CDS_TOOL_BIN_DIR=${REMOTE_CDS_TOOL_DIR}/bin
REMOTE_CDS_TOOL_CONF_DIR=${REMOTE_CDS_TOOL_DIR}/conf



# get the bin files
function get_production() {
    echo "get the production..."
    wget -r -nH --level=0 --cut-dirs=7 getprod@product.scm.baidu.com:/data/prod-64/baidu/bce/cds/cds_1-0-0-14_PD_BL/  --user getprod --password getprod --preserve-permissions
}


# change the configurations
function configure_file() {
    # master
    conf=${LOCAL_CONF_DIR}/master.conf
    sed -i "1s/8987/${MASTER_PORT}/g" ${conf}

    # blockserver
    conf=${LOCAL_CONF_DIR}/blockserver.conf
    sed -i "1s/1987/${BLOCKSERVER_PORT}/g" ${conf}
    sed -i "2s/cds_test.baidu.com:8987/${MASTER_DNS}:${MASTER_PORT}/g" ${conf}

    # heavyworker
    conf=${LOCAL_CONF_DIR}/heavyworker.conf
    sed -i "1s/8990/${HEAVYWORKER_PORT}/g" ${conf}
    sed -i "2s/cds_test.baidu.com:8987/${MASTER_DNS}:${MASTER_PORT}/g" ${conf}

    # cds_tool
    conf=${LOCAL_CONF_DIR}/tool.conf
    sed -i "1s/8988/${CDS_TOOL_PORT}/g" ${conf}
    sed -i "2s/cds_test.baidu.com:8987/${MASTER_DNS}:${MASTER_PORT}/g" ${conf}
}

# copy the
function copy_files() {
    for server in ${MASTERS}; do
        echo "copy master bin and configuration to ${server}..."
        ssh cds@${server} "mkdir -p ${REMOTE_MASTER_BIN_DIR} && mkdir -p ${REMOTE_MASTER_CONF_DIR}"
        scp ${LOCAL_BIN_DIR}/master cds@${server}:${REMOTE_MASTER_BIN_DIR}
        scp ${LOCAL_CONF_DIR}/master.conf cds@${server}:${REMOTE_MASTER_CONF_DIR}
    done

    for server in ${BLOCKSERVERS}; do
        echo "copy blockserver bin and configuration to ${server}..."
        ssh cds@${server} "mkdir -p ${REMOTE_BLOCKSERVER_BIN_DIR} && mkdir -p ${REMOTE_BLOCKSERVER_CONF_DIR}"
        scp ${LOCAL_BIN_DIR}/blockserver cds@${server}:${REMOTE_BLOCKSERVER_BIN_DIR}
        scp ${LOCAL_CONF_DIR}/blockserver.conf cds@${server}:${REMOTE_BLOCKSERVER_CONF_DIR}
    done

    for server in ${HEAVYWORKERS}; do
        echo "copy heavyworker bin and configuration to ${server}..."
        ssh cds@${server} "mkdir -p ${REMOTE_HEAVYWORKWE_BIN_DIR} && mkdir -p ${REMOTE_HEAVYWORKER_CONF_DIR}"
        scp ${LOCAL_BIN_DIR}/heavyworker cds@${server}:${REMOTE_HEAVYWORKWE_BIN_DIR}
        scp ${LOCAL_CONF_DIR}/heavyworker.conf cds@${server}:${REMOTE_HEAVYWORKER_CONF_DIR}
    done

    echo "copy cds_tool bin and configuration to ${server}..."
    ssh cds@${server} "mkdir -p ${REMOTE_CDS_TOOL_BIN_DIR} && mkdir -p ${REMOTE_CDS_TOOL_CONF_DIR}"
    scp ${LOCAL_BIN_DIR}/cds_tool cds@${server}:${REMOTE_CDS_TOOL_BIN_DIR}
    scp ${LOCAL_CONF_DIR}/tool.conf cds@${server}:${REMOTE_CDS_TOOL_CONF_DIR}
}

# start up
function start_servers() {
    echo "start master: ${LEADER_MASTER} as the first master with --bootstrap"
    ssh cds@${LEADER_MASTER} "cd ${REMOTE_MASTER_DIR} && ./bin/master --bootstrap > 1.log 2>&1"

    for server in ${FOLLOWER_MASTERS}; do
        echo "start master: ${server}..."
        ssh cds@${server} "cd ${REMOTE_MASTER_DIR} && ./bin/master > 1.log 2>&1"
    done

    for server in ${BLOCKSERVERS}; do
        echo "start blockserver ${server}..."
        ssh cds@${server} "cd ${REMOTE_BLOCKSERVER_DIR} && ./bin/blockserver > 1.log 2>&1"
    done

    for server in ${HEAVYWORKERS}; do
        echo "start heavyworker ${server}..."
        ssh cds@${server} "cd ${REMOTE_BLOCKSERVER_DIR} && ./bin/blockserver > 1.log 2>&1"
    done
}

function cds_tool_run() {
    echo "run the command 'cds_tool --op=${1}'"
    ssh cds@${CDS_TOOL_SERVER} "cd ${REMOTE_CDS_TOOL_DIR} && ./bin/cds_tool --op=${1}"
}

function get_ip() {
    if [ $# -lt 1 ]; then
        echo $0 need a parameter
        exit 0
    fi
    addr=$1
    str=`ping ${addr} packetsize 1 | grep ${addr} | head -n 1`
    return echo ${str} | cut -d'(' -f 2 | cut -d')' -f1
}

# add resource
function add_resources() {
    echo "add resource..."
    echo "add masters.."
    nodes=get_ip ${LEADER_MASTER}
    nodes=${nodes}:${MASTER_PORT}
    for server in ${FOLLOWER_MASTERS}; do
        echo "add master: ${server}..."
        ip=get__ip ${server}
        cmd="add_master_node --node=${ip}:${MASTER_PORT} --cur_nodes=${nodes}"
        nodes=${nodes},${ip}:${MASTER_PORT}
        cds_tool_run ${cmd}
    done

    echo "add blockservers..."
    for server in ${BLOCKSERVERS}; do
        ip=get_ip ${server}
        cmd="add_node --node=${ip}:${BLOCKSERVER_PORT}"
    done
}

function print_cluster_configuration() {
    echo "###### the configuration of the cluster ######"
    echo "###### masters ######"
    echo ${MASTERS}
    echo "###### leader master ######"
    echo ${LEADER_MASTER}
    echo "###### follower masters ######"
    echo ${FOLLOWER_MASTERS}
    echo "###### blockservers ######"
    echo ${BLOCKSERVERS}
    echo "###### heavyworkers ######"
    echo ${HEAVYWORKERS}
}

# copy master files to masters
function deploy() {
    print_cluster_configuration
    #get_production
    #configure_file
    #copy_files
    #start_servers
}

# caution: this will destroy the cluster, be careful to use it
function destroy() {
 echo "destroy...."
}

echo "pray for that we make it..."
deploy
echo "I guess we have done..."
