#!/usr/bin/env python

import json
import sys
import gzip
from datetime import datetime


def get_date(line):
    parts = line.split('utils.h')
    parts = parts[0].split(' ')
    time_str = ' '.join(parts[1:3])
    return datetime.strptime(time_str, "%m%d %H:%M:%S.%f"), time_str


def rg_id2str(rg_id):
    return rg_id.get('pool') + '_' + str(rg_id.get('id'))


def parse_out(file_name):
    timestamp = datetime.strptime('0628 12:00:00.0000', "%m%d %H:%M:%S.%f")
    block_map = dict()
    with gzip.GzipFile(file_name, 'r') as f:
        for line in f:
            try:
                d_time, t_str = get_date(line)
                if d_time > timestamp:
                    continue
                parts = line.split('[CDS_METRIC]')
                json_part = parts[1]
                data = json.loads(json_part)
                key = rg_id2str(data.get('rg_id'))
                block_num_time = block_map.get(key)
                if block_num_time:
                    current_date_time = block_num_time.get('datetime')
                    if d_time > current_date_time:
                        block_num_time['datetime'] = d_time
                        block_num_time['datetime_str'] = t_str
                        for k in data.keys():
                            block_num_time[k] = data.get(k)
                else:
                    block_num_time = dict()
                    block_num_time['datetime'] = d_time
                    block_num_time['datetime_str'] = t_str
                    for k in data.keys():
                        block_num_time[k] = data.get(k)
                    block_map[key] = block_num_time
            except Exception as e:
                pass
    new_map = dict()
    for k, v in block_map.items():
        block_num_time = dict()
        block_num_time['datetime_str'] = v.get('datetime_str')
        for key in v.keys():
            if key == 'datetime':
                continue
            block_num_time[key] = v.get(key)
        new_map[k] = block_num_time
    with open(file_name+'.time_distributed.json', 'w') as f:
        json.dump(new_map, f)


if __name__ == '__main__':
    parse_out(sys.argv[1])