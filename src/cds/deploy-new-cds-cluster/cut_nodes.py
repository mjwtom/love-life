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
        host = host.strip()
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

    a = []
    b = []
    switch = 0
    for zone, hosts in table.items():
        l = len(hosts)
        if l % 2 == 0:
            half = l / 2
        else:
            half = l / 2 + switch
            if switch == 0:
                switch = 1
            elif switch == 1:
                switch = 0
        part1 = hosts[:half]
        part2 = hosts[half:]

        a.extend(part1)
        b.extend(part2)

    info = "a len: %d, nodes:" % len(a)
    print(info)
    for node in a:
        print(node)

    info = "b len: %d, nodes:" % len(b)
    print(info)
    for node in b:
        print(node)


if __name__ == '__main__':
    # path = '/home/majingwei/servers/bjyz_sata_140.list'
    # path = '/home/majingwei/servers/cq02_sata_140.list'
    path = '/home/majingwei/servers/cq02_ssd_40_host_host.list'
    print_zones(path)
