#!/usr/bin/env python

import os
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

slice_size = 1024 * 1024
log_dir = '/home/majingwei/download/root_read/'

shapes = ['o', 'v', '^', '<', '>',
          '1', '2', '3', '4', '8',
          's', 'p', '.', ',',
          '*', 'h', 'H', '+', 'x',
          'X', 'D', 'd', '|', '-']
shape_index = 0
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
color_index = 0


def get_style():
    global shape_index
    global color_index
    style = shapes[shape_index] + colors[color_index]
    shape_index = (shape_index+1) % len(shapes)
    color_index = (color_index+1) % len(colors)
    return style


def get_date(line):
    parts = line.split('cds-agent')
    parts = parts[0].split(':')
    time_str = ':'.join(parts[1: -1]).strip()
    return datetime.strptime(time_str, "%m-%d %H:%M:%S:%f")


def get_attach_date(file_path, volume_uuid):
    with open(file_path, 'r') as f:
        for line in f.readlines():
            if 'attach' in line and volume_uuid in line:
                return get_date(line)


def get_value(kv):
    parts = kv.split(':')
    return parts[-1].strip()


def parse_io(line):
    io = dict()
    io['date'] = get_date(line)
    parts = line.split(',')
    for part in parts:
        if 'type' in part:
            io['type'] = get_value(part)
        elif 'volume_offset' in part:
            io['offset'] = get_value(part)
        elif 'length' in part:
            io['length'] = get_value(part)
    return io


def add_relative_time(attach_date, ios):
    for io in ios:
        delta = io['date'] - attach_date
        io['time_s'] = delta.total_seconds()


def get_ios(file_path, volume_uuid):
    ios = []
    with open(file_path, 'r') as f:
        for line in f.readlines():
            if 'request' not in line:
                continue
            if volume_uuid not in line:
                continue
            if 'io_type' not in line:
                continue
            ios.append(parse_io(line))
    return ios


def io_to_slice(ios):
    slices = set()
    for io in ios:
        start_slice = int(io['offset']) / slice_size
        slices.add(start_slice)
        for i in range(int(io['length']) / (slice_size + 1)): # if read size equals to slice_size, it is till one slice
            slices.add(start_slice + i)
    return slices


def draw_hints(hints):
    cl = ['win', 'debian', 'ubuntu', 'centos']
    for c in cl:
        op_sys = []
        accesses = []
        for s in sorted(hints.keys()):
            if not s.lower().startswith(c):
                continue
            op_sys.append(s)
            accesses.append(hints[s])

        fig, ax = plt.subplots()
        for i in range(len(op_sys)):
            x = [io['time_s'] for io in accesses[i]]
            y = [io['offset'] for io in accesses[i]]
            style = get_style()
            ax.plot(x, y, style)
        ax.set_xlim([0, 240])
        ax.grid(True)
        ax.legend(op_sys, loc='best', shadow=True, fancybox=True)

        with PdfPages(c+'_access_point.pdf') as pdf:
            pdf.savefig(fig)


def draw_scale(fetch_data):
    os = []
    size = []
    for s in sorted(fetch_data.keys()):
        os.append(s)
        size.append(len(fetch_data[s]))

    fig, ax = plt.subplots()

    # Example data
    y_pos = np.arange(len(os))

    ax.barh(y_pos, size, align='center',
            color='green', ecolor='black')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(os)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Data size in MB')
    ax.set_title('Amount of data to fetch')
    plt.tight_layout()

    with PdfPages('fetch.pdf') as pdf:
        pdf.savefig(fig)


def analyze(dir_path):
    fetch_data = dict()
    io_hints = dict()
    for file_name in os.listdir(dir_path):
        if file_name == '.' or file_name == '..':
            continue
        parts = file_name.split('.')
        volume_uuid = parts[-1]
        op_sys = parts[-2]
        path = os.path.join(dir_path, file_name)
        print('parsing %s from %s' % (volume_uuid, path))
        ios = get_ios(path, volume_uuid)
        attach_date = get_attach_date(path, volume_uuid)
        print(attach_date)
        add_relative_time(attach_date, ios)
        slices = io_to_slice(ios)
        fetch_data[op_sys] = slices
        io_hints[op_sys] = ios
    draw_scale(fetch_data)
    draw_hints(io_hints)


if __name__ == '__main__':
    analyze(log_dir)