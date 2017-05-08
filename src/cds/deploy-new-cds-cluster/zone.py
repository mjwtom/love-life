#!/usr/bin/env python
import sys
import os


def generate_zone(src_file, dst_file):
    zone_node_number = dict()
    zone_prefix_index = dict()
    node_num_per_zone = 2
    if not os.path.exists(src_file):
        print('please give the right source file')
        return -1
    with open(src_file, 'r') as src, open(dst_file, 'w') as dst:
        for line in src:
            zone = 'error_zone_name'
            ip = line.strip()
            segments = ip.split('.')
            zone_prefix = '.'.join(segments[:-1])
            candidate_index = zone_prefix_index.get(zone_prefix)
            if candidate_index is None:
                zone = zone_prefix+'.0'
                zone_prefix_index[zone_prefix] = 0
                zone_node_number[zone] = 1
            else:
                candidate_zone = zone_prefix+'.'+str(candidate_index)
                node_num = zone_node_number.get(candidate_zone)
                if not node_num:
                    print('something error happened')
                    return -1
                if node_num < node_num_per_zone:
                    zone_node_number[candidate_zone] += 1
                    zone = candidate_zone
                else:
                    candidate_index += 1
                    zone_prefix_index[zone_prefix] += candidate_index
                    zone = zone_prefix +'.'+str(candidate_index)
                    zone_node_number[zone] = 1
            line = ip + ' ' + zone +'\n'
            dst.write(line)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('please give the source file and dst file')
        exit(-1)
    exit(generate_zone(sys.argv[1], sys.argv[2]))
