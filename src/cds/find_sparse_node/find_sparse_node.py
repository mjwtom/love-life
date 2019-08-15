#!/usr/bin/env python
import subprocess
import json
import time
import sys
import socket
import struct
import ctypes


def int2ip(net_int):
    ip_int = ctypes.c_uint(net_int)
    host_int = socket.ntohl(ip_int.value)
    return socket.inet_ntoa(struct.pack("!I", host_int))


def cds_tool_cmd(master, cmd):
    run_cmd = './bin/cds_tool --master=%s --print_cinder_msg --op=%s' % (master, cmd)
    p = subprocess.Popen(run_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if err:
        print(err)
    parts = out.split('[CINDER_TEXT]')
    json_msg = parts[1]
    return json.loads(json_msg)


def list_node(master):
    sparse_ssd_nodes = []
    cmd = 'list_node'
    nodesout = cds_tool_cmd(master, cmd)
    if nodesout.get('status').get('errcode') != 0:
        print('error with list code')
        print(nodesout.get('status').get('errrmsg'))
        return
    nodes = nodesout.get('nodes')
    for node in nodes:
        # print('analyze node% d' % node.get('node').get('ip'))
        region = node.get('region')
        if 'sparse' not in region:
            # print('no sparse, region: %s' % region)
            continue
        aggregated_disks = node.get('aggregated_disks')
        found = False
        for disk in aggregated_disks:
            disk_type = disk.get('disk_type')
            if disk_type == 1:
                found = True
        if not found:
            continue
        # print(node)
        ip = node.get('node').get('ip')
        print(int2ip(ip))
        # sparse_ssd_nodes.append(node)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('give master address')
        exit(1)
    list_node(sys.argv[1])
