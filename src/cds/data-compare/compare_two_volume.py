#!/usr/bin/env python

import subprocess
import os
import sys
from hashlib import md5


pwd = '/home/majingwei/tools'
os.chdir(pwd)
block_size = 64 * 1024 * 1024


def pull_data(volume, offset, length, out_file):
    cmd = './bin/cds_check_tool -l %d' \
          ' -f %s --volume_uuid=%s --io_op=read --io_offset=%d' \
          ' --io_size=%d --clean_exist_file=true --monitor_interval_s=1' \
         % (length, out_file, volume, offset, length)
    print(cmd)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if err:
        return None
    parts = out.split()
    ip = parts[-1]
    return ip


def get_volume_size(volume):
    cmd = './bin/cds_tool --op=stat_volume --volume_uuid=%s' % volume
    print(cmd)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if err:
        return None
    print(out)
    lines = out.split('\n')
    for line in lines:
        if 'volume_size:' in line:
            parts = line.split(':')
            return int(parts[-1].strip())
    return 0


def compare(volume1, volume2):
    compare_size  = get_volume_size(volume1)
    size = get_volume_size(volume2)
    if compare_size > size:
        compare_size = size
    count = compare_size / block_size
    for i in range(count):
        offset = i * block_size
        file1 = '%s_%d_%d' % (volume1, offset, block_size)
        pull_data(volume1, offset, block_size, file1)
        file2 = '%s_%d_%d' % (volume2, offset, block_size)
        pull_data(volume2, offset, block_size, file2)
        with open(file1, 'r') as f1, open(file2, 'r') as f2:
            data1 = f1.read()
            data2 = f2.read()
            md5_1 = md5(data1).hexdigest()
            md5_2 = md5(data2).hexdigest()
            if md5_1 == md5_2:
                info = 'volume offset %d length %d equals, %s:%s %s:%s' \
                       % (offset, block_size, volume1, md5_1, volume2, md5_2)
                print(info)
                os.remove(file1)
                os.remove(file2)
            else:
                info = 'volume offset %d length %d not equal, %s:%s, %s:%s' \
                       % (offset, block_size, volume1, md5_1, volume2, md5_2)
                print(info)
                for i in range(block_size):
                    if data1[i] != data2[i]:
                        offset += i
                        info = 'volume offset %d not equal, %s:%s, %s:%s' \
                        % (offset, volume1, data1[i], volume2, data2[i])
                        print(info)
                        return


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('give two volumes')
        exit(-1)
    compare(sys.argv[1], sys.argv[2])
