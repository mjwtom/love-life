#!/usr/bin/env python

import os
import sys
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import math

slice_size = 1024 * 1024
block_size = 4096
log_dir = '/home/majingwei/download/root_read/'
time_limit_s = 2500
extent_width = 60

shapes = ['o', 'v', '^', '<', '>',
          '1', '2', '3', '4', '8',
          's', 'p', '.', ',',
          '*', 'h', 'H', '+', 'x',
          'D', 'd', '|']
shape_index = 0
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
color_index = 0
fig_row = 2
patterns = ['read_throughput', 'write_throughput', 'read_iops', 'write_iops']
cdf_patterns = ['read_mb', 'write_mb', 'read_io', 'write_io']
types = ['logical', 'physical']
fig_size_inches = [18.5, 10.5]


def get_style():
    global shape_index
    global color_index
    style = shapes[shape_index] + colors[color_index] + '-'
    shape_index = (shape_index+1) % len(shapes)
    color_index = (color_index+1) % len(colors)
    return style


def reset_style():
    global shape_index
    global color_index


def get_date(line):
    parts = line.split(' ')
    time_str = parts[1] + ' ' + parts[2].strip()
    return datetime.strptime(time_str, "%m%d %H:%M:%S.%f")


def get_start_time(file_path):
    with open(file_path, 'r') as f:
        for line in f:
            if 'stastistic of' in line:
                return get_date(line)


def get_read_throughput(line):
    parts = line.split('read_throughput')
    parts = parts[1].split('(MB/s):')
    parts = parts[1].split(' ')
    throughput = float(parts[1])
    info = 'read throuhgput: %f' % throughput
    print(info)
    return throughput


def get_write_throughput(line):
    parts = line.split('write_throughput')
    parts = parts[1].split('(MB/s):')
    parts = parts[1].split(' ')
    throughput = float(parts[1])
    info = 'write throuhgput: %f' % throughput
    print(info)
    return throughput


def get_read_iops(line):
    parts = line.split('read_req')
    parts = parts[1].split('(IOPS):')
    parts = parts[1].split(' ')
    iops = float(parts[1])
    info = 'read iops: %f' % iops
    print(info)
    return iops


def get_write_iops(line):
    parts = line.split('write_req')
    parts = parts[1].split('(IOPS):')
    parts = parts[1].split(' ')
    iops = float(parts[1])
    info = 'write iops: %f' % iops
    print(info)
    return iops


def parse_throughput(line):
    io = dict()
    io['date'] = get_date(line)
    if 'logical' in line:
        io['type'] = 'logical'
    elif 'phyiscial' in line:
        io['type'] = 'physical'
    io['read_throughput'] = get_read_throughput(line)
    io['write_throughput'] = get_write_throughput(line)
    io['read_iops'] = get_read_iops(line)
    io['write_iops'] = get_write_iops(line)
    return io


def add_relative_time(attach_date, ios):
    out_ios = []
    for io in ios:
        delta = io['date'] - attach_date
        io['time_s'] = delta.total_seconds()
        if io['time_s'] <= time_limit_s:
            out_ios.append(io)
    return out_ios


def get_throughput(file_path):
    ios = []
    with open(file_path, 'r') as f:
        for line in f:
            if 'stastistic of' not in line:
                continue
            print(line)
            ios.append(parse_throughput(line))
    return ios


def pick_io_type(ios, type, pattern):
    picked = []
    for io in ios:
        if io['type'] != type:
            continue
        picked_io = dict(
            time_s = io['time_s'],
            value = io.get(pattern)
        )
        picked.append(picked_io)
    return picked


def draw_line(disk_io):
    for i in range(len(patterns)):
        pattern = patterns[i]
        labels = []
        accesses = []
        for s in sorted(disk_io.keys()):
            ios = disk_io.get(s)
            for type in types:
                picked_io = pick_io_type(ios, type, pattern)
                labels.append(s + '_' + type)
                accesses.append(picked_io)
                info = 'type: %s, pattern: %s, len: %d' % (type, pattern, len(picked_io))
                print(info)

        ax = plt.subplot(fig_row, len(patterns) / fig_row, i + 1)
        for i in range(len(accesses)):
            x = [io['time_s'] for io in accesses[i]]
            y = [io['value'] for io in accesses[i]]
            style = get_style()
            ax.plot(x, y, style)
        ax.set_xlim([0, time_limit_s])
        ax.grid(True)
        ax.set_xlabel('time (second)')
        ax.set_ylabel(pattern)
        ax.set_title(pattern + ' on startup')
        # ax.legend(labels, ncol=2, bbox_to_anchor=(1.05, 1), loc='best', shadow=True, fancybox=True)
        ax.legend(labels, ncol=1, loc='best', shadow=True, fancybox=True)

    # with PdfPages('access_point.pdf') as pdf:
        # pdf.savefig(fig)
    fig = plt.gcf()
    fig.set_size_inches(fig_size_inches)
    plt.savefig('disk_throughput.png')


def sum_io_mtrics(io_metrics):
    ios = []
    for type in types:
        sum_io = dict()
        for io in io_metrics:
            if io['type'] != type:
                continue
            timestamp = io['date'].replace(second=0, microsecond=0)
            minute_io = sum_io.get(timestamp)
            if not minute_io:
                sum_io[timestamp] = io
            else:
                minute_io['read_throughput'] += io['read_throughput']
                minute_io['write_throughput'] += io['write_throughput']
                minute_io['read_iops'] += io['read_iops']
                minute_io['write_iops'] += io['write_iops']
        for key in sorted(sum_io.keys()):
            ios.append(sum_io.get(key))
    return ios


def get_io(dir_path):
    io_metrics = []
    for file_name in os.listdir(dir_path):
        if file_name == '.' or file_name == '..':
            continue
        if 'blockserver.log' not in file_name:
            continue
        info = 'process %s' % file_name
        print(info)
        path = os.path.join(dir_path, file_name)
        ios = get_throughput(path)
        io_metrics.extend(ios)
    io_metrics = sum_io_mtrics(io_metrics)
    start_time = io_metrics[0].get('date')
    io_metrics = add_relative_time(start_time, io_metrics)
    return io_metrics


def sum_io(ios):
    delta_time_s = 300
    sum_ios = dict()
    for type in types:
        start_date = ios[0]['date']
        g_start_date = start_date
        my_sum = dict(
            type=type,
            read_mb=0.0,
            write_mb=0.0,
            read_io=0,
            write_io=0
        )
        sum_ios[type] = my_sum
        for io in ios:
            if io['type'] != type:
                continue
            delta_date = io['date'] - g_start_date
            if delta_date.total_seconds() > time_limit_s:
                break
            delta_date = io['date'] - start_date
            if delta_date.total_seconds() < delta_time_s:
                continue
            start_date = io['date']
            my_sum['read_mb'] += (io['read_throughput'] * delta_time_s)
            my_sum['write_mb'] += (io['write_throughput'] * delta_time_s)
            my_sum['read_io'] += (io['read_iops'] * delta_time_s)
            my_sum['write_io'] += (io['write_iops'] * delta_time_s)
    return sum_ios


def get_cdf_io(dir_path):
    node_sum_ios = dict()
    for file_name in os.listdir(dir_path):
        if file_name == '.' or file_name == '..':
            continue
        if 'blockserver.log' not in file_name:
            continue
        info = 'process %s' % file_name
        print(info)
        path = os.path.join(dir_path, file_name)
        ios = get_throughput(path)
        sum_ios = sum_io(ios)
        for key in sum_ios.keys():
            node_sum = node_sum_ios.get(key)
            if not node_sum:
                node_sum_ios[key] = sum_ios.get(key)
            else:
                this_node_sum = sum_ios.get(key)
                node_sum['read_mb'] += this_node_sum['read_mb']
                node_sum['write_mb'] += this_node_sum['write_mb']
                node_sum['read_io'] += this_node_sum['read_io']
                node_sum['write_io'] += this_node_sum['write_io']
    return node_sum_ios


def draw_cdf(disk_io):
    for i in range(len(cdf_patterns)):
        pattern = cdf_patterns[i]
        labels = []
        accesses = []
        for s in sorted(disk_io.keys()):
            node_sum_io = disk_io.get(s)
            for type in types:
                sum_io = node_sum_io.get(type)
                target_io = sum_io.get(pattern)
                labels.append(s + '_' + type)
                accesses.append(target_io)
                info = 'type: %s, pattern: %s, len: %d' % (type, pattern, int(target_io))
                print(info)

        ax = plt.subplot(fig_row, len(patterns) / fig_row, i + 1)
        y_pos = np.arange(len(accesses))
        ax.barh(y_pos, accesses, align='center',
                color='green', ecolor='black')
        ax.set_yticks(y_pos)
        ax.set_yticklabels(labels)
        ax.invert_yaxis()  # labels read top-to-bottom
        for x, y in zip(y_pos, accesses):
            ax.text(y + 40, x + 0.4, '%.2f' % y, ha='center', va='bottom')
        # ax.set_xlabel('')
        ax.set_ylabel(pattern)
        # plt.tight_layout()

    # with PdfPages('access_point.pdf') as pdf:
        # pdf.savefig(fig)
    fig = plt.gcf()
    fig.set_size_inches(fig_size_inches)
    plt.savefig('disk_cdf.png')


def analyze(dir_path):
    '''

    :param dir_path:
    :return:
    disk_ios = dict()
    for file_name in os.listdir(dir_path):
        if file_name == '.' or file_name == '..':
            continue
        path = os.path.join(dir_path, file_name)
        if not os.path.isdir(path):
            continue
        disk_ios[file_name] = get_io(path)
    draw_line(disk_ios)
    '''

    disk_ios = dict()
    for file_name in os.listdir(dir_path):
        if file_name == '.' or file_name == '..':
            continue
        path = os.path.join(dir_path, file_name)
        if not os.path.isdir(path):
            continue
        disk_ios[file_name] = get_cdf_io(path)
    draw_cdf(disk_ios)


if __name__ == '__main__':
    analyze(os.getcwd())