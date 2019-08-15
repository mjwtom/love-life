#!/usr/bin/env python

import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime


fast_start_time_str = '20190723 16:00:00.000000'
fast_end_time_str = '20190728 09:00:00.000000'

# compare_start_time_str = '20190730 16:00:00.000000'
# compare_end_time_str = '20190804 09:00:00.000000'
compare_start_time_str = '20190716 16:00:00.000000'
compare_end_time_str = '20190721 09:00:00.000000'


def daytime(date):
    if date.hour < 9:
        return False
    return True


def str2datetime(date_str):
    return datetime.strptime(date_str, "%Y%m%d %H:%M:%S.%f")


def get_date_range_snapshot(start, end, snapshots,
                            volume_size_begin, volume_size_end):
    picked_snaps = dict()
    for id, snap in snapshots.items():
        created_at = str2datetime(snap.get('created_at'))
        if daytime(created_at):
            pass
            # continue
        if created_at < start:
            continue
        if created_at >= end:
            continue
        if snap.get('volume_size') < volume_size_begin:
            continue
        if snap.get('volume_size') >= volume_size_end:
            continue
        picked_snaps[id] = snap
    return picked_snaps


def average_time_s(snapshots):
    sum_s = 0.0
    num = 0
    for snap in snapshots.values():
        if snap.get('status') != 'available':
            print('not available, but %s' % snap.get('status'))
            continue
        start_datetime = str2datetime(snap.get('created_at'))
        end_datetime = str2datetime(snap.get('updated_at'))
        sum_s += (end_datetime - start_datetime).total_seconds()
        num += 1
    return sum_s, num, sum_s / num


def draw_figure():
    fast_start_datetime = str2datetime(fast_start_time_str)
    fast_end_datetime = str2datetime(fast_end_time_str)
    compare_start_datetime = str2datetime(compare_start_time_str)
    compare_end_datetime = str2datetime(compare_end_time_str)
    volume_size_begin = 0
    volume_size_end = 409600
    with open('snapshots.json', 'r') as f:
        snapshots = json.load(f)
    fast_snapshots = get_date_range_snapshot(fast_start_datetime, fast_end_datetime, snapshots,
                                             volume_size_begin, volume_size_end)
    compare_snapshots = get_date_range_snapshot(compare_start_datetime, compare_end_datetime, snapshots,
                                                volume_size_begin, volume_size_end)
    fast_total, fast_num, fast_average_time_s = average_time_s(fast_snapshots)
    compare_total, compare_num, compare_average_time_s = average_time_s(compare_snapshots)
    print(fast_total, fast_num, fast_average_time_s)
    print(compare_total, compare_num, compare_average_time_s)


if __name__ == '__main__':
    draw_figure()
