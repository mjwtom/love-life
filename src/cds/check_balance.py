#!/usr/bin/env python

import sys
import pprint

disk_types = ('ssd', 'sata', 'premium_ssd')


def get_rack(ip):
    parts = ip.split('.')
    return '.'.join(parts[:-1])


def get_value(line):
    parts = line.split(' ')
    return parts[-1].strip()


def get_nodes(node_file):
    with open(node_file, 'r') as f:
        lines = f.readlines()
    nodes = dict()
    node = dict()
    current_disk_type = 'no'
    for line in lines:
        if 'node: ' in line:
            node = dict()
            ip = get_value(line)
            nodes[ip] = node
            node['ip'] = ip
            node['name'] = ip
        elif 'region: ' in line:
            node['region'] = get_value(line)
        elif 'zone: ' in line:
            node['zone'] = get_value(line)
        elif 'disk_type: ' in line:
            current_disk_type = get_value(line)
        elif 'quota_gb: ' in line:
            node[current_disk_type] = int(get_value(line))
    return nodes


def update_pick_info(nodes):
    regions = dict()
    for ip, node in nodes.items():
        region_name = node['region']
        region = regions.get(region_name)
        if not region:
            region = dict()
            regions[region_name] = region
            # region['name'] = region_name
        zone_name = node['zone']
        zone = region.get(zone_name)
        if not zone:
            zone = dict()
            region[zone_name] = zone
            zone['name'] = zone_name
        node_dict = zone.get('nodes')
        if not node_dict:
            node_dict = dict()
            zone['nodes'] = node_dict
        node_dict[ip] = node
        for disk_type in disk_types:
            quota = node.get(disk_type)
            if not quota:
                continue
            if zone.get(disk_type):
                zone[disk_type] += quota
            else:
                zone[disk_type] = quota
    return regions


def nature_region(nodes):
    region = dict()
    for ip, node in nodes.items():
        zone_name = get_rack(node['ip'])
        zone = region.get(zone_name)
        if not zone:
            zone = dict()
            region[zone_name] = zone
            zone['name'] = zone_name
        node_dict = zone.get('nodes')
        if not node_dict:
            node_dict = dict()
            zone['nodes'] = node_dict
        node_dict[ip] = node
        for disk_type in disk_types:
            quota = node.get(disk_type)
            if not quota:
                continue
            if zone.get(disk_type):
                zone[disk_type] += quota
            else:
                zone[disk_type] = quota
    return region


def able_balance(region, goal):
    disk_zones = dict()
    for disk_type in disk_types:
        zones = [zone for zone in region.values() if zone.get(disk_type)]
        zones = sorted(zones, lambda x, y: cmp(x[disk_type], y[disk_type]), reverse = True)
        disk_zones[disk_type] = zones
    for disk_type, zones in disk_zones.items():
        continue
        print('disk type %s has zones:' % disk_type)
        print(zones)
    for disk_type, zones in disk_zones.items():
        if len(zones) < goal + 1:
            print('%s unable to rebalance since there are %d zones' % (disk_type, len(zones)))
            for zone in zones:
                print('name: %s, size: %d, node size: %d' %
                      (zone['name'], zone[disk_type], len(zone['nodes'])))
            continue
        big_head = zones[:goal-1]
        rest = zones[goal-1 :]
        sum_head = 0
        sum_rest = 0
        for zone in big_head:
            sum_head += zone[disk_type]
        for zone in rest:
            sum_rest += zone[disk_type]
        if sum_head > sum_rest:
            print('%s unable to rebalance since there are large zones' % disk_type)
            for zone in zones:
                print('name: %s, size: %d, node size: %d' %
                      (zone['name'], zone[disk_type], len(zone['nodes'])))


def analyze(node_file):
    nodes = get_nodes(node_file)
    regions = update_pick_info(nodes)
    pprint.pprint('current status')
    for name, region in regions.items():
        pprint.pprint(name)
        able_balance(region, 3)

    pprint.pprint('if we can safe')
    region = nature_region(nodes)
    able_balance(region, 3)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('need nodes file')
        exit(-1)
    analyze(sys.argv[1])