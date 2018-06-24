#!/usr/bin/env python

import sys
import random
import string
import json


def id_generator(size=1024):
    return open("/dev/urandom", "rb").read(size)


def replay(device, io_file):
    with open(io_file, 'r') as f:
        ios = json.load(f)
    with open(device, 'r+') as f:
        for io in ios:
            f.seek(int(io.get('offset')))
            if io.get('type') == 'read':
                f.read(int(io.get('length')))
            else:
                data = id_generator(int(io.get('length')))
                f.write(data)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('give device and executor log')
        exit(-1)
    replay(sys.argv[1], sys.argv[2])