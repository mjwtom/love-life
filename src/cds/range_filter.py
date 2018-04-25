#!/usr/bin/env python

import sys


def get_offset_length(line):
    parts = line.split('offset:')
    parts = parts[-1].split(',')
    offset = int(parts[0].strip())
    parts = line.split('size:')
    parts = parts[-1].split(',')
    length = int(parts[0].strip())
    return offset, length


def filter(log_file, range_offset, range_length):
    with open(log_file, 'r') as f:
        lines = f.readlines()

    range_start = int(range_offset)
    range_end = int(range_offset) + int(range_length)
    for line in lines:
        if 'file' in line:
            continue
        offset, length = get_offset_length(line)
        end = offset + length
        if offset < range_end and end > range_start:
            print(line)


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('rang_filter log_file offset length')
        exit(-1)
    filter(sys.argv[1], sys.argv[2], sys.argv[3])