#/usr/bin/env python
from hashlib import md5
import sys

block_size = 64 * 1024 * 1024


def compare_data(ldata, rdata, break_on_diff=True):
    lmd5 = md5(ldata).hexdigest()
    rmd5 = md5(rdata).hexdigest()
    if lmd5 == rmd5:
        return True
    else:
        data_len = len(ldata)
        if data_len > len(rdata):
            data_len = len(rdata)
        for j in range(data_len):
            if ldata[j] != rdata[j]:
                info = 'data offset %d not equal, left:%s, right:%s' \
                    % (j, ldata[j], rdata[j])
                print(info)
                if break_on_diff:
                    return False
        return False


def compare(lfile, rfile):
    with open(lfile, 'r') as lf, open(rfile, 'r') as rf:
        ldata = lf.read(block_size)
        rdata = rf.read(block_size)
        if not compare_data(ldata, rdata):
            parts = lfile.split('/')
            with open('data_' + '_'.join(parts) + '_0', 'w') as ff:
                ff.write(ldata)
            parts = rfile.split('/')
            with open('data_' + '_'.join(parts) + '_0', 'w') as ff:
                ff.write(ldata)
            return


if __name__ == '__main__':
    if len(sys.argv) < 3:
        exit(-1)
    compare(sys.argv[1], sys.argv[2])