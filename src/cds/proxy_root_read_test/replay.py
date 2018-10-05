#!/usr/bin/env python

import sys
import random
import string
import json
import os
import mmap
from datetime import datetime


replay_time_length_s = 100
buf_size = 100*1024*1024

with open("/dev/urandom", "rb") as f:
    buf = f.read(buf_size)


def id_generator(size=1024):
    return buf[:size]


def replay(device, io_file, time_length_s=replay_time_length_s):
    with open(io_file, 'r') as f:
        ios = json.load(f)
    f = os.open(device, os.O_DIRECT | os.O_RDWR)
    read_count = 0
    write_count = 0
    start_date = datetime.strptime(ios[0]['date'], "%m-%d %H:%M:%S:%f")
    for io in ios:
        cur_date = datetime.strptime(io['date'], "%m-%d %H:%M:%S:%f")
        delta_date = cur_date - start_date
        info = 'total seconds %f ' % delta_date.total_seconds()
        print(info)
        if delta_date.total_seconds() > time_length_s:
            break
        length = int(io.get('length'))
        offset = int(io.get('offset'))
        os.lseek(f, offset, os.SEEK_SET)
        if io.get('type') == 'read':
            mm = mmap.mmap(f, int((length + 4096) / 4096) * 4096,
                offset=int(offset/4096) * 4096, access=mmap.ACCESS_READ)
            mm.read(int((length + 4096) / 4096) * 4096)
            mm.close()
            info = 'read offset: %d, length: %d' % (offset, length)
            print(info)
            read_count += 1
        else:
            m = mmap.mmap(-1, length)
            data = id_generator(length)
            m.write(data)
            os.write(f, m)
            info = 'write offset: %d, length: %d' % (offset, length)
            print(info)
            write_count += 1
    os.close(f)
    info = 'read count: %d, write count: %d' % (read_count, write_count)
    print(info)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('give device and executor log')
        exit(-1)
    replay(sys.argv[1], sys.argv[2])