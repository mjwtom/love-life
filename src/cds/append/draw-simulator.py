#!/usr/bin/env python

import matplotlib as mpl
mpl.use('Agg')
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import json
from simulator import AppendSim, RandomWriteGenerator, GaussWriteGenerator
import os


def draw(offset_count, x, y_diff, y_no_diff, title_part):
    ax = plt.subplot(1, 2, 1)
    x_range = range(len(offset_count))
    ax.plot(x_range, offset_count, '-')
    ax.grid(True)
    ax.set_xlabel('write offset')
    ax.set_ylabel('count')
    ax.set_title(title_part+ '_write_distribution')
    ax.legend(['write_count'], ncol=2, loc='best', shadow=True, fancybox=True)

    ax = plt.subplot(1, 2, 2)
    ax.plot(x, y_diff, '+')
    ax.plot(x, y_no_diff, 'x')
    ax.grid(True)
    ax.set_xlabel('user writes')
    ax.set_ylabel('compaction writes')
    ax.set_title(title_part + '_compaction_writes')
    ax.legend(['separate', 'together'], ncol=2, loc='best', shadow=True, fancybox=True)

    # with PdfPages('iops.pdf') as pdf:
        # pdf.savefig(fig)
    # fig = plt.gcf()
    name = title_part + '.png'
    path = os.path.join('./', name)
    plt.savefig(path)
    # plt.show()


def write_and_draw():
    P = 48 * 1024 * 1024 * 1024  # physical size
    s = 4 * 1024  # write size
    o = 0.8  # oversell rate
    M = 16 * 1024 * 1024
    u = 0.9
    S = int(P*o)
    write_round = 2
    write_stat_step = int(S/s/100) # plot 10 times on one round write
    total_writes = write_round * S/s
    random_distribution = RandomWriteGenerator(S, s)
    gauss_distribution = GaussWriteGenerator(S, s, S / 2, S / 10)
    generator = random_distribution
    generator = gauss_distribution
    offset_count = [0] * int(S/s)
    sim_append_to_write = AppendSim(distribution=True  # writes distribution
                    , s=s
                    , o=o
                    , P=P
                    , M=M
                    , u=u  # compaction start point
                    , compaction_to_diff_seg=False
                    , check_after_compaction=False
                    )
    sim_append_to_separate = AppendSim(distribution=True  # writes distribution
                                    , s=s
                                    , o=o
                                    , P=P
                                    , M=M  # segment size
                                    , u=u  # compaction start point
                                    , compaction_to_diff_seg=True
                                    , check_after_compaction=False
                                    )
    i = 0
    x = []
    y_no_diff = []
    y_diff = []
    while i < total_writes:
        offset = generator.generate_offset()
        offset_count[offset] += 1
        sim_append_to_write.write_at(offset)
        sim_append_to_separate.write_at(offset)
        if i % write_stat_step == 0:
            print('run %d, total: %d, step: %d, progress %f' % (i, total_writes, write_stat_step, i*1.0/total_writes))
            x.append(i)
            y_no_diff.append(sim_append_to_write.compaction_count)
            y_diff.append(sim_append_to_separate.compaction_count)
            perf_dict = dict(
                offset_count=offset_count,
                x=x,
                y_no_diff=y_no_diff,
                y_diff=y_diff
            )
            with open('perf.json', 'w') as f:
                json.dump(perf_dict, f)
        i += 1
    print(offset_count)
    print(x)
    print(y_no_diff)
    print(y_diff)
    perf_dict = dict(
        offset_count=offset_count,
        x=x,
        y_no_diff=y_no_diff,
        y_diff=y_diff
    )
    with open('perf.json', 'w') as f:
        json.dump(perf_dict, f)
    draw(offset_count, x, y_diff, y_no_diff, 'random')


def read_and_draw():
    with open('gauss-perf.json') as f:
        data = json.load(f)
    draw(data.get('offset_count'), data.get('x'), data.get('y_diff'), data.get('y_no_diff'), 'gauss')
    with open('random-perf.json') as f:
        data = json.load(f)
    draw(data.get('offset_count'), data.get('x'), data.get('y_diff'), data.get('y_no_diff'), 'random')


if __name__ == '__main__':
    #write_and_draw()
    read_and_draw()
