#!/usr/bin/env bash

SERVERS="gzns-cds-ssd060.gzns
gzns-cds-ssd066.gzns
gzns-cds-ssd044.gzns
gzns-cds-ssd061.gzns
gzns-cds-ssd033.gzns
gzns-cds-ssd092.gzns
gzns-cds-ssd072.gzns
gzns-cds-ssd080.gzns
gzns-cds-ssd039.gzns
gzns-cds-ssd079.gzns"

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

function get_zone_from_ip() {
    ip=${1}
    zone="`echo "$ip" | rev | cut -d. -f2- | rev`."
    echo ${zone}
}

for server in ${SERVERS};
do
   ip="$(get_ip ${server})"
   zone="$(get_zone ${ip})"
   echo "${ip}-->${zone}"
done
