#!/usr/bin/env python

import subprocess
import os
import sys
from hashlib import md5
import json
import threading
from compare_data import compare_data

block_size = 64 * 1024 * 1024


def run_cds_cmd(cmd):
    run_cmd = './bin/cds_tool --op=%s --print_cinder_msg' % cmd
    print(run_cmd)
    p = subprocess.Popen(run_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    print(out)
    parts = out.split('[CINDER_TEXT]')
    return json.loads(parts[1])


def pull_data(volume, offset, length, out_file):
    cmd = './bin/cds_check_tool -l %d' \
          ' -f %s --volume_uuid=%s --io_op=read --io_offset=%d' \
          ' --io_size=%d --clean_exist_file=true --monitor_interval_s=1' \
         % (length, out_file, volume, offset, length)
    print(cmd)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    print(err)
    print(out)


def get_volume_size(volume):
    cmd = 'stat_volume --volume_uuid=%s' % volume
    r = run_cds_cmd(cmd)
    return r.get('volume_info').get('volume_size')


def compare_block(lvolume, rvolume, block_index, block_size):
    offset = block_index * block_size
    lfile = '%s_%d_%d' % (lvolume, offset, block_size)
    pull_data(lvolume, offset, block_size, lfile)
    rfile = '%s_%d_%d' % (rvolume, offset, block_size)
    pull_data(rvolume, offset, block_size, rfile)
    with open(lfile, 'r') as lf, open(rfile, 'r') as rf:
        ldata = lf.read()
        rdata = rf.read()
        if not compare_data(ldata, rdata):
            return False
    return True


def compare(lvolume, rvolume):
    l_size = get_volume_size(lvolume)
    r_size = get_volume_size(rvolume)
    compare_len = l_size
    if l_size > r_size:
        compare_len = r_size
    count = compare_len / block_size
    threads = []
    for i in range(count):
        args = (lvolume, rvolume, i, block_size)
        t = threading.Thread(target=compare_block, args=args)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('give two volumes')
        exit(-1)
    compare(sys.argv[1], sys.argv[2])
