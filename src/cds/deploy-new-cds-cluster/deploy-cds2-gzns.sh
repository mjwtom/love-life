#!/usr/bin/env bash

#before run the script, please change the configuration

# some configurations

: '
cds2 nodes on gzns
gzns-cds-ssd060.gzns
gzns-cds-ssd066.gzns
gzns-cds-ssd044.gzns
gzns-cds-ssd061.gzns
gzns-cds-ssd033.gzns
gzns-cds-ssd092.gzns
gzns-cds-ssd072.gzns
gzns-cds-ssd080.gzns
gzns-cds-ssd039.gzns
gzns-cds-ssd079.gzns
'

# small cluster for test
# masters
MASTERS="gzns-cds-ssd060.gzns
gzns-cds-master-gzns-01.gzns
gzns-cds-master-gzns-02.gzns"
# we have to start a master as the leader first (bootstrap)
LEADER_MASTER=`echo ${MASTERS} | awk '{print $1}'`
FOLLOWER_MASTERS=`echo ${MASTERS} | sed -r 's/^[^ ]* *//g'`
# blockservers
BLOCKSERVERS="gzns-cds-ssd066.gzns
gzns-cds-ssd044.gzns
gzns-cds-ssd061.gzns
gzns-cds-ssd033.gzns
gzns-cds-ssd092.gzns
gzns-cds-ssd072.gzns
gzns-cds-ssd080.gzns
gzns-cds-ssd039.gzns
gzns-cds-ssd079.gzns"
#heavyworks
HEAVYWORKERS="gzns-cds-ssd066.gzns
gzns-cds-ssd044.gzns
gzns-cds-ssd061.gzns
gzns-cds-ssd033.gzns
gzns-cds-ssd092.gzns
gzns-cds-ssd072.gzns
gzns-cds-ssd080.gzns
gzns-cds-ssd039.gzns
gzns-cds-ssd079.gzns"
#cds_tool, do not have to be a remote server
CDS_TOOL_SERVER="gzns-cds-ssd060.gzns"
DISKS="/home/ssd1
/home/ssd2
/home/ssd3
/home/ssd4
/home/ssd5
"
###### end the configuration ######

# after binding dns use the bound dns, but now, we have to use this one
# TODO: change it to DNS
#MASTER_DNS=${LEADER_MASTER}
MASTER_DNS="cluster.cds.gzns.bce-internal.baidu.com"
MASTER_PORT=8987
BLOCKSERVER_PORT=8977
HEAVYWORKER_PORT=8990
CDS_TOOL_PORT=8988

LOCAL_HOME=`pwd`
LOCAL_BIN_DIR=${LOCAL_HOME}/output/bin
LOCAL_CONF_DIR=${LOCAL_HOME}/output/conf
SCRIPT_DIR=${LOCAL_HOME}/scripts

REMOTE_HOME=/home/cds

REMOTE_MASTER_DIR=${REMOTE_HOME}/master
REMOTE_MASTER_BIN_DIR=${REMOTE_MASTER_DIR}/bin
REMOTE_MASTER_CONF_DIR=${REMOTE_MASTER_DIR}/conf

REMOTE_BLOCKSERVER_DIR=${REMOTE_HOME}/blockserver
REMOTE_BLOCKSERVER_BIN_DIR=${REMOTE_BLOCKSERVER_DIR}/bin
REMOTE_BLOCKSERVER_CONF_DIR=${REMOTE_BLOCKSERVER_DIR}/conf

REMOTE_HEAVYWORKER_DIR=${REMOTE_HOME}/heavyworker
REMOTE_HEAVYWORKER_BIN_DIR=${REMOTE_HEAVYWORKER_DIR}/bin
REMOTE_HEAVYWORKER_CONF_DIR=${REMOTE_HEAVYWORKER_DIR}/conf

REMOTE_CDS_TOOL_DIR=${REMOTE_HOME}/tool
REMOTE_CDS_TOOL_BIN_DIR=${REMOTE_CDS_TOOL_DIR}/bin
REMOTE_CDS_TOOL_CONF_DIR=${REMOTE_CDS_TOOL_DIR}/conf


BLOCKSERVER_ZONE_INPUT_FILE="blockservers.txt"
BLOCKSERVER_ZONE_OUTPUT_FILE="blockserver2zone.txt"
ZONE_GENERETER="zone.py"


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

# copy the data to the corresponding nodes
function copy_files() {
    for server in ${MASTERS};
    do
        echo "copy master bin and configuration to ${server}..."
        ssh cds@${server} "mkdir -p ${REMOTE_MASTER_BIN_DIR} && mkdir -p ${REMOTE_MASTER_CONF_DIR}"
        scp ${LOCAL_BIN_DIR}/master cds@${server}:${REMOTE_MASTER_BIN_DIR}
        scp ${LOCAL_CONF_DIR}/master.conf cds@${server}:${REMOTE_MASTER_CONF_DIR}
        scp ${SCRIPT_DIR}/master/bin/control.inc cds@${server}:${REMOTE_MASTER_BIN_DIR}
        scp ${SCRIPT_DIR}/master/bin/control.func cds@${server}:${REMOTE_MASTER_BIN_DIR}
        scp ${SCRIPT_DIR}/master/bin/master_control cds@${server}:${REMOTE_MASTER_BIN_DIR}
        scp ${SCRIPT_DIR}/master/conf/control.conf cds@${server}:${REMOTE_MASTER_CONF_DIR}
    done

    for server in ${BLOCKSERVERS};
    do
        echo "copy blockserver bin and configuration to ${server}..."
        ssh cds@${server} "mkdir -p ${REMOTE_BLOCKSERVER_BIN_DIR} && mkdir -p ${REMOTE_BLOCKSERVER_CONF_DIR}"
        scp ${LOCAL_BIN_DIR}/blockserver cds@${server}:${REMOTE_BLOCKSERVER_BIN_DIR}
        scp ${LOCAL_CONF_DIR}/blockserver.conf cds@${server}:${REMOTE_BLOCKSERVER_CONF_DIR}
        scp ${SCRIPT_DIR}/blockserver/bin/control.inc cds@${server}:${REMOTE_BLOCKSERVER_BIN_DIR}
        scp ${SCRIPT_DIR}/blockserver/bin/control.func cds@${server}:${REMOTE_BLOCKSERVER_BIN_DIR}
        scp ${SCRIPT_DIR}/blockserver/bin/blockserver_control cds@${server}:${REMOTE_BLOCKSERVER_BIN_DIR}
        scp ${SCRIPT_DIR}/blockserver/conf/control.conf cds@${server}:${REMOTE_BLOCKSERVER_CONF_DIR}
    done

    for server in ${HEAVYWORKERS};
    do
        echo "copy heavyworker bin and configuration to ${server}..."
        ssh cds@${server} "mkdir -p ${REMOTE_HEAVYWORKER_BIN_DIR} && mkdir -p ${REMOTE_HEAVYWORKER_CONF_DIR}"
        scp ${LOCAL_BIN_DIR}/heavyworker cds@${server}:${REMOTE_HEAVYWORKER_BIN_DIR}
        scp ${LOCAL_CONF_DIR}/heavyworker.conf cds@${server}:${REMOTE_HEAVYWORKER_CONF_DIR}
        scp ${SCRIPT_DIR}/heavyworker/bin/control.inc cds@${server}:${REMOTE_HEAVYWORKER_BIN_DIR}
        scp ${SCRIPT_DIR}/heavyworker/bin/control.func cds@${server}:${REMOTE_HEAVYWORKER_BIN_DIR}
        scp ${SCRIPT_DIR}/heavyworker/bin/heavyworker_control cds@${server}:${REMOTE_HEAVYWORKER_BIN_DIR}
        scp ${SCRIPT_DIR}/heavyworker/conf/control.conf cds@${server}:${REMOTE_HEAVYWORKER_CONF_DIR}
    done

    echo "copy cds_tool bin and configuration to ${server}..."
    ssh cds@${CDS_TOOL_SERVER} "mkdir -p ${REMOTE_CDS_TOOL_BIN_DIR} && mkdir -p ${REMOTE_CDS_TOOL_CONF_DIR}"
    scp ${LOCAL_BIN_DIR}/cds_tool cds@${CDS_TOOL_SERVER}:${REMOTE_CDS_TOOL_BIN_DIR}
    scp ${LOCAL_CONF_DIR}/tool.conf cds@${CDS_TOOL_SERVER}:${REMOTE_CDS_TOOL_CONF_DIR}
}

# start up
function start_servers() {
    echo "start master: ${LEADER_MASTER} as the first master with --bootstrap"
    ssh -f cds@${LEADER_MASTER} "sh -c 'cd ${REMOTE_MASTER_DIR} && ./bin/master_control start'"

    for server in ${FOLLOWER_MASTERS};
    do
        echo "start master: ${server}..."
        ssh -f cds@${server} "sh -c 'cd ${REMOTE_MASTER_DIR} && ./bin/master_control start'"
    done

    for server in ${BLOCKSERVERS};
    do
        echo "start blockserver ${server}..."
        ssh -f cds@${server} "sh -c 'cd ${REMOTE_BLOCKSERVER_DIR} && ./bin/blockserver_control start'"
    done

    for server in ${HEAVYWORKERS};
    do
        echo "start heavyworker ${server}..."
        ssh -f cds@${server} "sh -c 'cd ${REMOTE_HEAVYWORKER_DIR} && ./bin/heavyworker_control start'"
    done
}

function cds_tool_run() {
    echo "run the command 'cds_tool --op=${*}'"
    #ssh cds@${CDS_TOOL_SERVER} "sh -c 'cd ${REMOTE_CDS_TOOL_DIR} && ./bin/cds_tool --op=${*}'"
    cd ./output
    ./bin/cds_tool --op=${*}
    cd -
}

function get_ip() {
    if [ $# -lt 1 ];
    then
        echo $0 need a parameter
        exit 0
    fi
    addr=${1}
    ip=`getent hosts ${addr} | awk '{ print $1 }'`
    echo ${ip}
}

disk_id=0
# add resource
function add_resources() {
    echo "add resource..."
    echo "add masters.."
    nodes="$(get_ip ${LEADER_MASTER})"
    nodes="${nodes}:${MASTER_PORT}"
    for server in ${FOLLOWER_MASTERS};
    do
        echo "add master: ${server}..."
        ip="$(get_ip ${server})"
        cmd="add_master_node --node=${ip}:${MASTER_PORT} --cur_nodes=${nodes}"
        nodes="${nodes},${ip}:${MASTER_PORT}"
        cds_tool_run ${cmd}
	sleep 1
    done

    echo "add blockservers..."
    echo "using python to generate zone..."
    if [ -f "${BLOCKSERVER_ZONE_INPUT_FILE}" ];
    then
        rm ${BLOCKSERVER_ZONE_INPUT_FILE}
    fi

    touch ${BLOCKSERVER_ZONE_INPUT_FILE}

    for server in ${BLOCKSERVERS};
    do
        ip="$(get_ip ${server})"
        echo "${ip}" >> ${BLOCKSERVER_ZONE_INPUT_FILE}
    done

    python ${ZONE_GENERETER} ${BLOCKSERVER_ZONE_INPUT_FILE} ${BLOCKSERVER_ZONE_OUTPUT_FILE}

    while read -r line
    do
        echo "line: ${line}"
        ip=`echo ${line} | cut -d ' ' -f 1`
        zone=`echo ${line} | cut -d ' ' -f 2`
        echo "add node: ${ip} to zone: ${zone}"
        cmd="add_node --node=${ip}:${BLOCKSERVER_PORT} --region=r1 --zone=${zone} --force=true"
        cds_tool_run ${cmd}
	sleep 1
    done < "${BLOCKSERVER_ZONE_OUTPUT_FILE}"


    for server in ${BLOCKSERVERS};
    do
        for disk in ${DISKS};
        do
            ip="$(get_ip ${server})"
            disk_uuid="$(echo ${disk_id})"
            cmd="add_disk --node=${ip}:${BLOCKSERVER_PORT} --disk_id=${disk_uuid} --disk_type=premium_ssd --disk_path=${disk}"
            cds_tool_run ${cmd}
            let disk_id+=1;
	    sleep 1
        done
    done

    echo "create pool: ssd_pool"
    cmd="add_pool --pool=premium_ssd_pool --disk_type=premium_ssd --rg_num=10000 --rg_goal=3 --regions=r1"
    cds_tool_run ${cmd}
    sleep 1
    
    echo "alter bos key"
    cmd="alter_bos_key --access_key=9ed6365bb45e42d892a43fe10ea39808 --access_secret=61273988685d48c6bcb8b1ebbf1ebbcd"
    cds_tool_run ${cmd}
    sleep 1
    cmd="show_bos_key"
    cds_tool_run ${cmd}
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

function kill_master() {
    ssh cds@${1} "cd ${REMOTE_MASTER_DIR} && killall ./bin/master"
}

function kill_blockserver() {
    ssh cds@${1} "cd ${REMOTE_BLOCKSERVER_DIR} && killall ./bin/blockserver"
}

function kill_heavyworker() {
    ssh cds@${1} "cd ${REMOTE_HEAVYWORKER_DIR} && killall ./bin/heavyworker"
}

function kill_cds_on_node() {
    echo "do not kill node in batch, it is an online system"
    return
    for server in ${HEAVYWORKERS};
    do
        echo "kill heavyworker ${server}..."
        kill_heavyworker ${server}
        kill_blockserver ${server}
        kill_master ${server}
    done

    for server in ${BLOCKSERVERS};
    do
        echo "kill blockserver ${server}..."
        kill_heavyworker ${server}
        kill_blockserver ${server}
        kill_master ${server}
    done

    for server in ${MASTERS};
    do
        echo "kill master: ${server}..."
        kill_heavyworker ${server}
        kill_blockserver ${server}
        kill_master ${server}
    done
}

function destroy_data() {
    echo "do not use destroy, it is an online system"
    return
    for server in ${HEAVYWORKERS};
    do
        echo "remove data on ${server}..."
        ssh cds@${server} "rm -rf ${REMOTE_CDS_TOOL_DIR}"
        ssh cds@${server} "rm -rf ${REMOTE_HEAVYWORKER_DIR}"
        ssh cds@${server} "rm -rf ${REMOTE_BLOCKSERVER_DIR}"
        ssh cds@${server} "rm -rf ${REMOTE_MASTER_DIR}"
    done

    for server in ${BLOCKSERVERS};
    do
        echo "remove data on ${server}..."
        ssh cds@${server} "rm -rf ${REMOTE_CDS_TOOL_DIR}"
        ssh cds@${server} "rm -rf ${REMOTE_HEAVYWORKER_DIR}"
        ssh cds@${server} "rm -rf ${REMOTE_BLOCKSERVER_DIR}"
        ssh cds@${server} "rm -rf ${REMOTE_MASTER_DIR}"
	for disk in ${DISKS};
	do
		echo "remove replicas on disk ${disk}"
        	ssh cds@${server} "rm -rf ${disk}/*"
	done
    done

    for server in ${MASTERS};
    do
        echo "remove data on ${server}..."
        ssh cds@${server} "rm -rf ${REMOTE_CDS_TOOL_DIR}"
        ssh cds@${server} "rm -rf ${REMOTE_HEAVYWORKER_DIR}"
        ssh cds@${server} "rm -rf ${REMOTE_BLOCKSERVER_DIR}"
        ssh cds@${server} "rm -rf ${REMOTE_MASTER_DIR}"
    done
}

function copy_tool() {
    for server in ${BLOCKSERVERS};
    do
    echo "copy cds_tool bin and configuration to ${server}..."
     ssh cds@${server} "mkdir -p ${REMOTE_CDS_TOOL_BIN_DIR} && mkdir -p ${REMOTE_CDS_TOOL_CONF_DIR}"
     scp ${LOCAL_BIN_DIR}/cds_tool cds@${server}:${REMOTE_CDS_TOOL_BIN_DIR}
     scp ${LOCAL_CONF_DIR}/tool.conf cds@${server}:${REMOTE_CDS_TOOL_CONF_DIR}
    done
    for server in ${MASTERS};
    do
    echo "copy cds_tool bin and configuration to ${server}..."
     ssh cds@${server} "mkdir -p ${REMOTE_CDS_TOOL_BIN_DIR} && mkdir -p ${REMOTE_CDS_TOOL_CONF_DIR}"
     scp ${LOCAL_BIN_DIR}/cds_tool cds@${server}:${REMOTE_CDS_TOOL_BIN_DIR}
     scp ${LOCAL_CONF_DIR}/tool.conf cds@${server}:${REMOTE_CDS_TOOL_CONF_DIR}
    done
}


# copy master files to masters
function deploy() {
    print_cluster_configuration
    kill_cds_on_node
    destroy_data
    get_production
    configure_file
    copy_files
    start_servers
    add_resources
	copy_tool
}

echo "pray for that we make it..."
deploy
echo "I guess we have done..."
