#!/usr/bin/env python

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

ssd_price = 0.0746
hdd_price = 0.0249
oversell = 1.5
occupy = 0.6


def cost3copies(price):
    p = price * 3 / occupy / oversell
    return p


def erasure1p5(price):
    p = price * 1.5 / occupy / oversell
    return p


def tiered3copies(front_price, backend_price, fraction, has_hole):
    if has_hole:
        backend_price = backend_price * (1 - fraction)
    p = (backend_price + front_price * fraction) * 3 / occupy / oversell
    return p


def tierederasure(front_price, backend_price, fraction, has_hole):
    if has_hole:
        backend_price = backend_price * (1 - fraction)
    p = (front_price * fraction * 3 + backend_price * 1.5) / occupy / oversell
    return p


def tiered_3copies_no_hole(front_price, backend_price, fraction):
    return tiered3copies(front_price, backend_price, fraction, False)


def tiered_3copies_with_hole(front_price, backend_price, fraction):
    return tiered3copies(front_price, backend_price, fraction, True)


def tiered_ec_with_hole(front_price, backend_price, fraction):
    return tiered3copies(front_price, backend_price, fraction, True)


def tiered_ec_no_hole(front_price, backend_price, fraction):
    return tierederasure(front_price, backend_price, fraction, False)


def tiered_ec_with_hole(front_price, backend_price, fraction):
    return tierederasure(front_price, backend_price, fraction, True)


def threecopies(front_price, backend_price, fraction):
    return cost3copies(backend_price)


def erasure_coding(front_price, backend_price, fraction):
    return erasure1p5(backend_price)

price_dict = dict(
    ssd=ssd_price,
    hdd=hdd_price
)

func_dict = dict(
    threecopies=threecopies,
    erasure_coding=erasure_coding,
    tiered_3copies_no_hole=tiered_3copies_no_hole,
    tiered_3copies_with_hole=tiered_3copies_with_hole,
    tiered_ec_no_hole=tiered_ec_no_hole,
    tiered_ec_with_hole=tiered_ec_with_hole
)

front_list = ['ssd']
backend_list = ['ssd', 'hdd']
storage_list = ['threecopies', 'erasure_coding']
tiered_list = ['tiered_3copies_no_hole', 'tiered_3copies_with_hole',
              'tiered_ec_no_hole', 'tiered_ec_with_hole']

labels = []
prices = []

for front in front_list:
    for backend in backend_list:
        for tier in storage_list:
            label = backend+'['+tier+']'
            labels.append(label)
            function = func_dict.get(tier)
            front_price = price_dict.get(front)
            backend_price = price_dict.get(backend)
            price = function(front_price, backend_price, 0.33)
            price = round(price, 3)
            prices.append(price)
        for tier in tiered_list:
            label = front+'+'+backend+'['+tier+']'
            labels.append(label)
            function = func_dict.get(tier)
            front_price = price_dict.get(front)
            backend_price = price_dict.get(backend)
            price = function(front_price, backend_price, 0.33)
            price = round(price, 3)
            prices.append(price)
fig, ax = plt.subplots()


def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


print(labels)
print(prices)
rects = ax.bar(labels, prices)
autolabel(rects)
plt.xticks(rotation=90)

# ax.set_xlim((left, right))
ax.set_xlabel('tiered method')
ax.set_ylabel('price (¥/GB)')
# ax.set_title(r'Block Num on RG')

# Tweak spacing to prevent clipping of ylabel
fig.tight_layout()
plt.show()
# fig = plt.gcf()
# fig.set_size_inches(fig_size_inches)
# plt.savefig('block_num.png')
# with PdfPages('block_num.pdf') as pdf:
#    pdf.savefig(fig)