#!/usr/bin/env python

import subprocess
import socket


def ip2host(ip):
    cmd = 'host %s' % ip
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if err:
        return None
    parts = out.split()
    host = parts[-1].strip().strip('.')
    return host


def print_zones(ip_path, host_path):
    with open(ip_path, 'r') as f:
        lines = f.readlines()
    hosts = []
    for line in lines:
        host = ip2host(line)
        hosts.append(host)
    with open(host_path, 'w') as f:
        for host in hosts:
            f.write(host+'\n')


if __name__ == '__main__':
    # path = '/home/majingwei/servers/bjyz_sata_140.list'
    # path = '/home/majingwei/servers/cq02_sata_140.list'
    ip_path = '/home/majingwei/servers/cq02_ssd_40_host.list'
    host_path = '/home/majingwei/servers/cq02_ssd_40_host_host.list'
    print_zones(ip_path, host_path)
