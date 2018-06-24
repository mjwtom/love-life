#!/usr/bin/env python
import subprocess
import json
import socket
import struct
import ctypes


def int2ip(net_int):
    ip_int = ctypes.c_uint(net_int)
    host_int = socket.ntohl(ip_int.value)
    return socket.inet_ntoa(struct.pack("!I", host_int))


def run_cmd(cmd):
    shell_cmd = './bin/cds_tool --op=%s --print_cinder_msg' % cmd
    p = subprocess.Popen(shell_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, _ = p.communicate()
    parts = out.split('[CINDER_TEXT]')
    response = json.loads(parts[1])
    return response


def get_normal_replicas(rg_id):
    normal_replicas_addr = []
    cmd = 'stat_rg --rg=%s' % rg_id
    response = run_cmd(cmd)
    replicas = response.get('replicas')
    for replica in replicas:
        if replica.get('replica_state') != 3:
            continue
        int_ip = replica.get('node').get('ip')
        ip = int2ip(int_ip)
        addr_string = '%s:%d' % (ip, replica.get('node').get('port'))
        normal_replicas_addr.append(addr_string)
    return normal_replicas_addr


def get_replicas(state):
    str_replicas = []
    cmd = 'list_unnormal_rg'
    response = run_cmd(cmd)
    replicas = response.get(state)
    for replica in replicas:
        str_replica = '%s_%d' % (replica.get('pool'), replica.get('id'))
        str_replicas.append(str_replica)
    return str_replicas


def set_state_peer(state):
    rgs = get_replicas(state)
    for rg in rgs:
        normal_replicas = get_normal_replicas(rg)
        print('# set peer for %s' % rg)
        cmd = './bin/cds_tool --op=set_peer --force_set_peer --rg=%s --peers=' % rg
        for r in normal_replicas:
            cmd += (r + ',')
        cmd = cmd.strip(',')
        print(cmd)


if __name__ == '__main__':
    set_state_peer('lack_replica_rgs')
