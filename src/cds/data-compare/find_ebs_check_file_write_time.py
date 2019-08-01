#/usr/bin/env python
from hashlib import md5
import sys


def get_off_and_len(line):
    parts = line.split('offset:')
    parts = parts[-1].split(',')
    offset = int(parts[0])
    parts = line.split('size:')
    parts = parts[-1].split(',')
    length = int(parts[0])
    return offset, length


def find_write_time(log_path):
    with open(log_path, 'r') as f:
        lines = f.readlines()
    assert_line = lines[-2]
    target_off, target_len = get_off_and_len(assert_line)
    for line in lines:
        if 'write offset' not in line:
            continue
        offset, length = get_off_and_len(line)
        if target_off < (offset + length) and offset < (target_off + target_len):
            print(line)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        exit(-1)
    find_write_time(sys.argv[1])