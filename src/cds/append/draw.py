#!/usr/bin/env python

from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import math
import os
from compaction import valid_rate


def draw(x, y, x_lable, titile):
    ax = plt.axes()
    ax.plot(x, y, '-')
    ax.set_xlim([0, 100])
    ax.set_ylim([0, 100])
    ax.grid(True)
    ax.set_xlabel(x_lable)
    ax.set_ylabel('valid_date_rate(%)')
    ax.set_title(titile)
    ax.legend(['validate'], ncol=2, loc='best', shadow=True, fancybox=True)

    # with PdfPages('iops.pdf') as pdf:
        # pdf.savefig(fig)
    # fig = plt.gcf()
    name = x_lable + '.png'
    path = os.path.join('/Users/majingwei/Downloads', name)
    plt.savefig(path)
    plt.show()


def comopaciton_start():
    rates = range(0, 100)
    y = []
    for x in rates:
        valid = valid_rate(u=x*1.0/100)
        y.append(valid*100)
    title = 'm=0,s=4K,o=1.0,P=3.5T,M=16G,u=changed'
    draw(rates, y, 'u(%)', title)


def comopaciton_start():
    rates = range(1, 100)
    y = []
    for x in rates:
        valid = valid_rate(o=x*1.0/100)
        y.append(valid*100)
    title = 'm=0,s=4K,o=changed,P=3.5T,M=16G,u=0.9'
    draw(rates, y, 'o(%)', title)


if __name__ == '__main__':
    comopaciton_start()