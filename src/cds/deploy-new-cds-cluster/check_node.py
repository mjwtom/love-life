#!/usr/bin/env python

import subprocess
import socket


def host2ip(host):
    cmd = 'host %s' % host
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if err:
        return None
    parts = out.split()
    ip = parts[-1]
    return ip


def gather_ip(hosts):
    table = dict()
    for host in hosts:
        if len(host.strip()) == 0:
            continue
        ip = host2ip(host)
        parts = ip.split('.')
        zone = '.'.join(parts[:-1])
        if table.get(zone):
            table[zone].append(host)
        else:
            table[zone] = [host]
    return table


def print_zones(path):
    with open(path, 'r') as f:
        lines = f.readlines()

    table = gather_ip(lines)

    for zone, hosts in table.items():
        info = '%s: %d' % (zone, len(hosts))
        print(info)

if __name__ == '__main__':
    #path = '/home/majingwei/servers/bjyz_sata_100.list'
    path = '/home/majingwei/servers/cq02_sata_100.list'
    print_zones(path)
