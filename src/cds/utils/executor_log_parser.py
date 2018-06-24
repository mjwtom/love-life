import sys
from datetime import datetime
import json


slice_size = 1024 * 1024
block_size = 4096


def get_value(kv):
    parts = kv.split(':')
    return parts[-1].strip()


def get_date(line):
    parts = line.split('cds-agent')
    parts = parts[0].split(':')
    time_str = ':'.join(parts[1: -1]).strip()
    return time_str
    # return datetime.strptime(time_str, "%m-%d %H:%M:%S:%f")


def parse_io(line):
    io = dict()
    io['date'] = get_date(line)
    parts = line.split(',')
    for part in parts:
        if 'type' in part:
            io['type'] = get_value(part)
        elif 'volume_offset' in part:
            io['offset'] = get_value(part)
            io['slice_index'] = int(io['offset']) / slice_size
        elif 'length' in part:
            io['length'] = get_value(part)
    return io


def get_ios(file_path, volume_uuid):
    ios = []
    with open(file_path, 'r') as f:
        for line in f.readlines():
            if 'request' not in line:
                continue
            if volume_uuid not in line:
                continue
            if 'io_type' not in line:
                continue
            ios.append(parse_io(line))
    return ios


def save_ios_to_file(log_file, io_file):
    parts = log_file.split('.')
    volume_uuid = parts[-1]
    ios = get_ios(log_file, volume_uuid)
    with open(io_file, 'w') as f:
        json.dump(ios, f)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('give log_file and io_file')
        exit(-1)
    save_ios_to_file(sys.argv[1], sys.argv[2])