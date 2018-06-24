import socket
import struct
import json


def int2ip(net_int):
    host_int = socket.ntohl(net_int)
    return socket.inet_ntoa(struct.pack("!I", host_int))


def get_nodes(nodes, capacaty):
    return nodes


def get_disk_nodes(list_output, type):
    nodes = list_output.get('nodes')
    node_disk = dict()
    for node in nodes:
        disks = node.get('aggregated_disks')
        key = int2ip(node.get('node').get('ip')) + ':'\
              + str(node.get('node').get('port'))
        quota = 0
        for disk in disks:
            if disk.get('disk_type') == type:
                quota = disk.get('quota_gb')
        if quota != 0:
            node_disk[key] = quota
    return node_disk


def load(file_path):
    with open(file_path, 'r') as f:
        data = f.read()
        parts = data.split('[CINDER_TEXT]')
        data = json.loads(parts[1])
        return data


def pick():
    nodes = load('/Users/baidu/Downloads/yz01.txt')
    node_disk = get_disk_nodes(nodes, 1) # 1 means ssd
    nodes = get_nodes(node_disk, 100000)
    keys  = sorted(nodes.keys())
    for key in keys:
        quota = nodes.get(key)
        info  = 'node: %s, quota: %d' % (key, quota)
        print(info)


if __name__ == '__main__':
    pick()