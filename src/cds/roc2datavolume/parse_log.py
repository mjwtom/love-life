import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import json
from matplotlib.backends.backend_pdf import PdfPages
import sys


def get_info(line, key):
    parts = line.split(key + ': ')
    parts = parts[1].split(' ')
    value = parts[0]
    return value


def get_time(line):
    parts = line.split('NOTICE')
    parts = parts[1].strip().split(' ')
    time = ' '.join(parts[:2])
    return time


def get_clone_info(line):
    info = dict(
        volume_uuid = get_info(line, 'volume'),
        snapshot_uuid = get_info(line, 'snapshot'),
        bootable = get_info(line, 'bootable'),
        time_str = get_time(line)
    )
    return info


def parse(path):
    clone_jobs = []
    with open(path) as f:
        for line in f:
            if not 'recv clone_volume' in line:
                continue
            try:
                clone_info = get_clone_info(line)
                clone_jobs.append(clone_info)
            except Exception as e:
                print('invalid line: %s' % line)
                print(e)
                continue
    with open('jobs.json', 'w') as f:
        json.dump(clone_jobs, f)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        exit(1)
    parse(sys.argv[1])