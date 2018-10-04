#!/usr/bin/env python

import json
import os
import threading
import time
import random
import ConfigParser


def id_generator(size=1024):
    return open("/dev/urandom", "rb").read(size)


class IOStat(object):
    def __init__(self):
        self.total_io = 0
        self.lock = threading.Lock()

    def add_one(self):
        with self.lock:
            self.total_io += 1

    def get_ticks(self):
        with self.lock:
            return self.total_io


def rg_file_write(fd, io_size, file_size, run_time, stat):
    data = id_generator(io_size)
    off_end = file_size - io_size
    start = time.time()
    cur = start
    while cur - start < run_time:
        offset = random.randint(0,  off_end)
        # os.pwrite(fd, data, offset)
        fd.seek(offset)
        fd.write(data)
        stat.add_one()
        # print('write one')
        cur = time.time()
    print('write ends')


def load_conf(conf_file=None):
    if not conf_file:
        conf_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test.conf')
    if not os.path.exists(conf_file):
        return None
    conf = ConfigParser.ConfigParser()
    conf.read(conf_file)
    return conf


def run_test():
    stat = IOStat()
    conf = load_conf()
    io_size = int(conf.get('disk', 'io_size'))
    run_time = int(conf.get('disk', 'run_time'))
    file_size_gb = conf.get('disk', 'file_size_gb')
    file_size = int(file_size_gb) * 1024 * 1024 * 1024
    rg_num = int(conf.get('disk', 'rg_num'))
    threads = []
    f = open('test.data', 'w')
    args = (f, io_size, file_size, run_time, stat)
    for _ in range(int(rg_num)):
        t = threading.Thread(target=rg_file_write, args=args)
        t.start()
        threads.append(t)
    start = time.time()
    last_time = start
    cur = start
    last_ticks = 0
    static_serial = []
    while cur - start < run_time:
        cur = time.time()
        total_ticks = stat.get_ticks()
        increased_ticks = total_ticks - last_ticks
        time_used = cur - last_time
        throughput = increased_ticks * io_size / 1024.0 / 1024 / time_used
        iops = increased_ticks / time_used
        statics = dict (
            time_stamp=cur - start,
            throughput=throughput,
            iops=iops
        )
        static_serial.append(statics)
        print(statics)
        time.sleep(1)
        last_ticks = total_ticks
        last_time = cur
    for t in threads:
        t.join()
    print('wait ends')
    f.close()
    os.remove('test.data')
    with open('result.json', 'w') as f:
        json.dump(static_serial, f)


if __name__ == '__main__':
    run_test()