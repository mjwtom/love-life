#!/usr/bin/env python

import sys
import os


def filter(in_file, offset, length, out_file):
    with open(in_file, 'r') as f:
        f.seek(int(offset), os.SEEK_SET)
        data = f.read(int(length))

    with open(out_file, 'w') as f:
        f.write(data)


if __name__ == '__main__':
    if len(sys.argv) < 5:
        print('rang_filter log_file offset length')
        exit(-1)
    filter(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])