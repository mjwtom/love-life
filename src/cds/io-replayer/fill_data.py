#!/usr/bin/env python

import sys
import os
from repay import id_generator

BLOCK_SIZE_BYTES = 512 # usually?  always?  *shrug*

DATA_BLOCK_SIZE = 16 * 1024 * 1024


def get_disk_size(blockdev):
    blocks = int(open('/sys/block/{blockdev}/size'.format(**locals())).read())
    return blocks * BLOCK_SIZE_BYTES


def fill_random_data(dev):
    size = get_disk_size(dev)
    info = 'volume size in %d GB' % (size / 1024 / 1024 /1024)
    print(info)
    num = size / DATA_BLOCK_SIZE
    path = os.path.join('/dev', dev)
    if not os.path.exists(path):
        print('device not exist')
        return
    with open(path, 'r+') as f:
        for i in range(num):
            data = id_generator(DATA_BLOCK_SIZE)
            info = 'roud %d left %d' % (i, num -i)
            print(info)
            f.write(data)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('give device and executor log')
        exit(-1)
    fill_random_data(sys.argv[1])