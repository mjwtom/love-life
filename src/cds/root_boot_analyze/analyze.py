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
time_limit_s = 100
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
cl = ['win', 'debian', 'ubuntu', 'centos']
fig_size_inches = [18.5, 10.5]


def get_style():
    global shape_index
    global color_index
    style = shapes[shape_index] + colors[color_index]
    shape_index = (shape_index+1) % len(shapes)
    color_index = (color_index+1) % len(colors)
    return style


def reset_style():
    global shape_index
    global color_index


def sepearate_rw(hints):
    r_io = []
    w_io = []
    for io in hints:
        if io['type'] == 'read':
            r_io.append(io)
        else:
            w_io.append(io)
    return r_io, w_io


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
            io['slice_index'] = int(io['offset']) / slice_size
        elif 'length' in part:
            io['length'] = get_value(part)
    return io


def add_relative_time(attach_date, ios):
    out_ios = []
    for io in ios:
        delta = io['date'] - attach_date
        io['time_s'] = delta.total_seconds()
        if io['time_s'] <= time_limit_s:
            out_ios.append(io)
    return out_ios


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


def io_size_distribution(ios):
    length = int(math.log(slice_size, 2))
    sizes = [0] * (length + 1)
    for io in ios:
        io_length = int(math.log(int(io['length']), 2))
        if io_length >= length:
            sizes[length] += 1
        else:
            sizes[io_length] += 1
    return sizes


def io_to_slice(ios):
    slices = set()
    for io in ios:
        start_slice = int(io['offset']) / slice_size
        slices.add(start_slice)
        for i in range(int(io['length']) / (slice_size + 1)): # if read size equals to slice_size, it is till one slice
            slices.add(start_slice + i)
    return slices


def sum_request_size(ios):
    sum = 0
    for io in ios:
        sum += int(io['length'])
    return sum


def calculate_iops(ios):
    iops = [0] * time_limit_s
    for io in ios:
        time_s = int(io['time_s'])
        iops[time_s] += 1
    return iops


def calculate_size_ps(ios):
    sizes = [0] * time_limit_s
    for io in ios:
        time_s = int(io['time_s'])
        sizes[time_s] += int(io['length'])
    return sizes


def accessed_slice(ios):
    cur_time = 0
    sizes = [0] * time_limit_s
    slices = set()
    for io in ios:
        time_s = int(io['time_s'])
        if cur_time != time_s:
            for i in range(cur_time, time_s):
                slice_number = len(slices)
                if sizes[i] == 0:
                    sizes[i] = slice_number
            cur_time = time_s
        slice = int(io['offset']) / slice_size
        if slice not in slices:
            slices.add(slice)
    for i in range(cur_time, len(sizes)):
        slice_number = len(slices)
        if sizes[i] == 0:
            sizes[i] = slice_number
    return sizes


def continuous_io(ios):
    out_ios = []
    counter = []
    o_io = None
    offset = -1
    c_numer = 0
    for io in ios:
        if io['type'] != 'read':
            continue
        if int(io['offset']) == offset:
            o_io['length'] += int(io['length'])
            c_numer += 1
            print('find continuous read, size: %d' % o_io['length'])
        else:
            o_io = io
            o_io['length'] = int(io['length'])
            out_ios.append(o_io)
            for i in range(len(counter), c_numer + 1):
                counter.append(0)
            counter[c_numer] += 1
            c_numer = 0
        offset = int(io['offset']) + int(io['length'])
    return out_ios, counter


def draw_access_slice_growth(hints, pattern):
    for i in range(len(cl)):
        title_prefix = cl[i]
        op_sys = []
        iops = []
        for s in sorted(hints.keys()):
            if not s.lower().startswith(title_prefix):
                continue
            op_sys.append(s)
            r, w = sepearate_rw(hints[s])
            if pattern == 'mix':
                volume_iops = accessed_slice(hints[s])
                iops.append(volume_iops)
            elif pattern == 'read':
                volume_iops = accessed_slice(r)
                iops.append(volume_iops)
            elif pattern == 'write':
                volume_iops = accessed_slice(w)
                iops.append(volume_iops)

        ax = plt.subplot(fig_row, len(cl) / fig_row, i + 1)
        for i in range(len(op_sys)):
            volume_iops = iops[i]
            x = range(len(volume_iops))
            style = get_style() + '-'
            ax.plot(x, volume_iops, style)
        ax.set_xlim([0, time_limit_s])
        ax.grid(True)
        ax.set_xlabel('time (second)')
        ax.set_ylabel('accessed slice number')
        ax.set_title(title_prefix + ' ' + pattern + ' accessed slice growth')
        # ax.legend(op_sys, ncol=2, bbox_to_anchor=(1.05, 1), loc='best', shadow=True, fancybox=True)
        ax.legend(op_sys, ncol=2, loc='best', shadow=True, fancybox=True)

    # with PdfPages('iops.pdf') as pdf:
        # pdf.savefig(fig)
    fig = plt.gcf()
    fig.set_size_inches(fig_size_inches)
    plt.savefig(pattern + '_accessed_slice.png')


def draw_io_size_distribution(hints, pattern):
    for i in range(len(cl)):
        title_prefix = cl[i]
        op_sys = []
        iops = []
        for s in sorted(hints.keys()):
            if not s.lower().startswith(title_prefix):
                continue
            op_sys.append(s)
            r, w = sepearate_rw(hints[s])
            if pattern == 'mix':
                volume_iops = io_size_distribution(hints[s])
                iops.append(volume_iops)
            elif pattern == 'read':
                volume_iops = io_size_distribution(r)
                iops.append(volume_iops)
            elif pattern == 'write':
                volume_iops = io_size_distribution(w)
                iops.append(volume_iops)

        ax = plt.subplot(fig_row, len(cl) / fig_row, i + 1)
        for i in range(len(op_sys)):
            volume_iops = iops[i]
            x = range(len(volume_iops))
            style = get_style() + '-'
            ax.plot(x, volume_iops, style)
        ax.set_xlim([0, int(math.log(slice_size, 2)) + 1])
        ax.grid(True)
        ax.set_xlabel('log(io_size, 2)')
        ax.set_ylabel('count')
        ax.set_title(title_prefix + ' ' + pattern + ' io size distribution on startup')
        # ax.legend(op_sys, ncol=2, bbox_to_anchor=(1.05, 1), loc='best', shadow=True, fancybox=True)
        ax.legend(op_sys, ncol=1, loc='best', shadow=True, fancybox=True)

    # with PdfPages('iops.pdf') as pdf:
        # pdf.savefig(fig)
    fig = plt.gcf()
    fig.set_size_inches(fig_size_inches)
    plt.savefig(pattern + '_io_size_distribution.png')


def draw_sequential_io(hints):
    for i in range(len(cl)):
        title_prefix = cl[i]
        op_sys = []
        iops = []
        for s in sorted(hints.keys()):
            if not s.lower().startswith(title_prefix):
                continue
            op_sys.append(s)
            volume_iops, _ = continuous_io(hints[s])
            volume_iops = io_size_distribution(volume_iops)
            iops.append(volume_iops)

        ax = plt.subplot(fig_row, len(cl) / fig_row, i + 1)
        for i in range(len(op_sys)):
            volume_iops = iops[i]
            x = range(len(volume_iops))
            style = get_style() + '-'
            ax.plot(x, volume_iops, style)
        ax.set_xlim([0, int(math.log(slice_size, 2)) + 1])
        ax.grid(True)
        ax.set_xlabel('log(io_size, 2)')
        ax.set_ylabel('count')
        ax.set_title(title_prefix  + ' sequential read io_size on startup')
        # ax.legend(op_sys, ncol=2, bbox_to_anchor=(1.05, 1), loc='best', shadow=True, fancybox=True)
        ax.legend(op_sys, ncol=1, loc='best', shadow=True, fancybox=True)

    # with PdfPages('iops.pdf') as pdf:
        # pdf.savefig(fig)
    fig = plt.gcf()
    fig.set_size_inches(fig_size_inches)
    plt.savefig('sequetial_read_io.png')


def draw_sequential_number(hints):
    for i in range(len(cl)):
        title_prefix = cl[i]
        op_sys = []
        iops = []
        for s in sorted(hints.keys()):
            if not s.lower().startswith(title_prefix):
                continue
            op_sys.append(s)
            _, volume_iops = continuous_io(hints[s])
            iops.append(volume_iops)

        ax = plt.subplot(fig_row, len(cl) / fig_row, i + 1)
        for i in range(len(op_sys)):
            volume_iops = iops[i]
            x = range(len(volume_iops))
            style = get_style() + '-'
            ax.plot(x, volume_iops, style)
        # ax.set_xlim([0, len(volume_iops)])
        ax.set_ylim([0, 100])
        ax.set_xlim([0, 100])
        ax.grid(True)
        ax.set_xlabel('countinuous read number')
        ax.set_ylabel('count')
        ax.set_title(title_prefix  + ' sequential read io number on startup')
        # ax.legend(op_sys, ncol=2, bbox_to_anchor=(1.05, 1), loc='best', shadow=True, fancybox=True)
        ax.legend(op_sys, ncol=1, loc='best', shadow=True, fancybox=True)

    # with PdfPages('iops.pdf') as pdf:
        # pdf.savefig(fig)
    fig = plt.gcf()
    fig.set_size_inches(fig_size_inches)
    plt.savefig('sequetial_io_number.png')


def draw_iops(hints, pattern):
    for i in range(len(cl)):
        title_prefix = cl[i]
        op_sys = []
        iops = []
        for s in sorted(hints.keys()):
            if not s.lower().startswith(title_prefix):
                continue
            op_sys.append(s)
            r, w = sepearate_rw(hints[s])
            if pattern == 'mix':
                volume_iops = calculate_iops(hints[s])
                iops.append(volume_iops)
            elif pattern == 'read':
                volume_iops = calculate_iops(r)
                iops.append(volume_iops)
            elif pattern == 'write':
                volume_iops = calculate_iops(w)
                iops.append(volume_iops)

        ax = plt.subplot(fig_row, len(cl) / fig_row, i + 1)
        for i in range(len(op_sys)):
            volume_iops = iops[i]
            x = range(len(volume_iops))
            style = get_style() + '-'
            ax.plot(x, volume_iops, style)
        ax.set_xlim([0, time_limit_s])
        ax.grid(True)
        ax.set_xlabel('time (second)')
        ax.set_ylabel('iops')
        ax.set_title(title_prefix + ' ' + pattern + ' iops on startup')
        # ax.legend(op_sys, ncol=2, bbox_to_anchor=(1.05, 1), loc='best', shadow=True, fancybox=True)
        ax.legend(op_sys, ncol=2, loc='best', shadow=True, fancybox=True)

    # with PdfPages('iops.pdf') as pdf:
        # pdf.savefig(fig)
    fig = plt.gcf()
    fig.set_size_inches(fig_size_inches)
    plt.savefig(pattern + '_iops.png')


def draw_size_ps(hints, pattern):
    for i in range(len(cl)):
        title_prefix = cl[i]
        op_sys = []
        iops = []
        for s in sorted(hints.keys()):
            if not s.lower().startswith(title_prefix):
                continue
            op_sys.append(s)
            r, w = sepearate_rw(hints[s])
            if pattern == 'mix':
                volume_iops = calculate_size_ps(hints[s])
                iops.append(volume_iops)
            elif pattern == 'read':
                volume_iops = calculate_size_ps(r)
                iops.append(volume_iops)
            elif pattern == 'write':
                volume_iops = calculate_size_ps(w)
                iops.append(volume_iops)

        ax = plt.subplot(fig_row, len(cl) / fig_row, i + 1)
        for i in range(len(op_sys)):
            volume_iops = iops[i]
            x = range(len(volume_iops))
            style = get_style() + '-'
            ax.plot(x, volume_iops, style)
        ax.set_xlim([0, time_limit_s])
        ax.grid(True)
        ax.set_xlabel('time (second)')
        ax.set_ylabel('size ps')
        ax.set_title(title_prefix + ' ' + pattern + ' io_size per second on startup')
        # ax.legend(op_sys, ncol=2, bbox_to_anchor=(1.05, 1), loc='best', shadow=True, fancybox=True)
        ax.legend(op_sys, ncol=2, loc='best', shadow=True, fancybox=True)

    # with PdfPages('iops.pdf') as pdf:
        # pdf.savefig(fig)
    fig = plt.gcf()
    fig.set_size_inches(fig_size_inches)
    plt.savefig(pattern + '_size_ps.png')


def calculate_sliceps(ios):
    slices = []
    for _ in range(time_limit_s):
        slices.append(set())
    for io in ios:
        time_s = int(io['time_s'])
        slice_index = int(io['offset']) / slice_size
        if slice_index in slices[time_s]:
            continue
        else:
            slices[time_s].add(slice_index)
    slice_ps = [len(slice_num) for slice_num in slices]
    return slice_ps


def draw_sliceps(hints, pattern):
    for i in range(len(cl)):
        title_prefix = cl[i]
        labels = []
        iops = []
        for s in sorted(hints.keys()):
            if not s.lower().startswith(title_prefix):
                continue
            labels.append(s)
            r, w = sepearate_rw(hints[s])
            if pattern == 'mix':
                volume_iops = calculate_sliceps(hints[s])
                iops.append(volume_iops)
            elif pattern == 'read':
                volume_iops = calculate_sliceps(r)
                iops.append(volume_iops)
            elif pattern == 'write':
                volume_iops = calculate_sliceps(w)
                iops.append(volume_iops)
        ax = plt.subplot(fig_row, len(cl) / fig_row, i + 1)
        for i in range(len(labels)):
            volume_iops = iops[i]
            x = range(len(volume_iops))
            style = get_style() + '-'
            ax.plot(x, volume_iops, style)
        ax.set_xlim([0, time_limit_s])
        ax.grid(True)
        ax.set_xlabel('time (second)')
        ax.set_ylabel('slices per second')
        ax.set_title(title_prefix + ' ' + pattern + ' access slice number per second on startup')
        ax.legend(labels, ncol=2, loc='best', shadow=True, fancybox=True)
        # ax.legend(labels, bbox_to_anchor=(1.05, 1), loc='best', shadow=True, fancybox=True)
    # with PdfPages('iops.pdf') as pdf:
        # pdf.savefig(fig)
    fig = plt.gcf()
    fig.set_size_inches(fig_size_inches)
    plt.tight_layout()
    plt.savefig(pattern + '_slice_ps.png')
    reset_style()


def draw_hints(hints, pattern):
    for i in range(len(cl)):
        title_prefix = cl[i]
        labels = []
        accesses = []
        for s in sorted(hints.keys()):
            if not s.lower().startswith(title_prefix):
                continue
            labels.append(s)
            r, w = sepearate_rw(hints[s])
            if pattern == 'mix':
                accesses.append(hints[s])
            elif pattern == 'read':
                accesses.append(r)
            elif pattern == 'write':
                accesses.append(w)

        ax = plt.subplot(fig_row, len(cl) / fig_row, i + 1)
        for i in range(len(accesses)):
            x = [io['time_s'] for io in accesses[i]]
            y = [io['offset'] for io in accesses[i]]
            style = get_style()
            ax.plot(x, y, style)
        ax.set_xlim([0, time_limit_s])
        ax.grid(True)
        ax.set_xlabel('time (second)')
        ax.set_ylabel('access offset')
        ax.set_title(title_prefix + ' ' + pattern + ' access point on startup')
        # ax.legend(labels, ncol=2, bbox_to_anchor=(1.05, 1), loc='best', shadow=True, fancybox=True)
        ax.legend(labels, ncol=2, loc='best', shadow=True, fancybox=True)

    # with PdfPages('access_point.pdf') as pdf:
        # pdf.savefig(fig)
    fig = plt.gcf()
    fig.set_size_inches(fig_size_inches)
    plt.savefig(pattern + '_access_point.png')


def draw_slice_pos(hints, pattern):
    for i in range(len(cl)):
        title_prefix = cl[i]
        labels = []
        accesses = []
        for s in sorted(hints.keys()):
            if not s.lower().startswith(title_prefix):
                continue
            labels.append(s)
            r, w = sepearate_rw(hints[s])
            if pattern == 'mix':
                accesses.append(hints[s])
            elif pattern == 'read':
                accesses.append(r)
            elif pattern == 'write':
                accesses.append(w)

        ax = plt.subplot(fig_row, len(cl) / fig_row, i + 1)
        for i in range(len(accesses)):
            x = [io['time_s'] for io in accesses[i]]
            y = [io['offset'] for io in accesses[i]]
            style = get_style()
            ax.plot(x, y, style)
        ax.set_xlim([0, time_limit_s])
        ax.grid(True)
        ax.set_xlabel('time (second)')
        ax.set_ylabel('access offset')
        ax.set_title(title_prefix + ' ' + pattern + ' access point on startup')
        # ax.legend(labels, ncol=2, bbox_to_anchor=(1.05, 1), loc='best', shadow=True, fancybox=True)
        ax.legend(labels, ncol=2, loc='best', shadow=True, fancybox=True)

    # with PdfPages('access_point.pdf') as pdf:
        # pdf.savefig(fig)
    fig = plt.gcf()
    fig.set_size_inches(fig_size_inches)
    plt.savefig(pattern + '_access_point.png')


def draw_scale(io_hints):
    os = []
    size = []
    for s in sorted(io_hints.keys()):
        os.append(s)
        slices = io_to_slice(io_hints[s])
        size.append(len(slices))
        r, w = sepearate_rw(io_hints[s])
        os.append(s+'-read')
        slices = io_to_slice(r)
        size.append(len(slices))
        os.append(s + '-write')
        slices = io_to_slice(w)
        size.append(len(slices))

    fig, ax = plt.subplots()

    # Example data
    y_pos = np.arange(len(os))

    ax.barh(y_pos, size, align='center',
            color='green', ecolor='black')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(os)
    ax.invert_yaxis()  # labels read top-to-bottom
    for x, y in zip(y_pos, size):
        ax.text(y + 40, x + 0.4, '%.2f' % y, ha='center', va='bottom')
    ax.set_xlabel('number of accessed slices  (1 MB per slice)')
    ax.set_ylabel('operation system')
    ax.set_title('Number of Slices Accessed on startup')
    plt.tight_layout()

    # with PdfPages('fetch.pdf') as pdf:
    #    pdf.savefig(fig)
    fig = plt.gcf()
    fig.set_size_inches(fig_size_inches)
    plt.savefig('fetch.png')


def draw_total_io_size(io_hints):
    os = []
    size = []
    for s in sorted(io_hints.keys()):
        os.append(s)
        sum_size = sum_request_size(io_hints[s])
        size.append(sum_size / 1024 / 1024)
        r, w = sepearate_rw(io_hints[s])
        os.append(s+'-read')
        sum_size = sum_request_size(r)
        size.append(sum_size / 1024 / 1024)
        os.append(s + '-write')
        sum_size = sum_request_size(w)
        size.append(sum_size / 1024 / 1024)

    fig, ax = plt.subplots()

    # Example data
    y_pos = np.arange(len(os))

    ax.barh(y_pos, size, align='center',
            color='green', ecolor='black')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(os)
    ax.invert_yaxis()  # labels read top-to-bottom
    for x, y in zip(y_pos, size):
        ax.text(y + 40, x + 0.4, '%.2f' % y, ha='center', va='bottom')
    ax.set_xlabel('data size in (MB) in 240 seconds')
    ax.set_ylabel('opration system')
    ax.set_title('Total query data size on startup (240 s)')
    plt.tight_layout()

    # with PdfPages('fetch.pdf') as pdf:
    #    pdf.savefig(fig)
    fig = plt.gcf()
    fig.set_size_inches(fig_size_inches)
    plt.savefig('total_io_size.png')


def analyze(dir_path, type, pattern):
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
        ios = add_relative_time(attach_date, ios)
        io_hints[op_sys] = ios
    if type == 'fetch':
        draw_scale(io_hints)
    if type == 'sequential_io':
        draw_sequential_io(io_hints)
    if type == 'sequential_number':
        draw_sequential_number(io_hints)
    if type == 'access_slice_growth':
        draw_access_slice_growth(io_hints, pattern)
    elif type == 'hint':
        draw_hints(io_hints, pattern)
    elif type == 'total_size':
        draw_total_io_size(io_hints)
    elif type == 'qps_size':
        draw_size_ps(io_hints, pattern)
    elif type == 'io_size':
        draw_io_size_distribution(io_hints, pattern)
    elif type == 'iops':
        draw_iops(io_hints, pattern)
    elif type == 'sliceps':
        draw_sliceps(io_hints, pattern)


if __name__ == '__main__':
    analyze(log_dir, sys.argv[1], sys.argv[2])