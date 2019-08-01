import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import json
from matplotlib.backends.backend_pdf import PdfPages


with open('rg_io.log.gz.time_distributed.json', 'r') as f:
    data = json.load(f)

counter = [0.0] * 30000
for key, v in data.items():
    if 'ssd_pool_r2' not in key:
        continue
    index = int(key.split('_')[-1])
    counter[index] = v.get('write_iops')

min_io = int(min(counter))
max_op = int(max(counter)) + 1
y = [0] * max_op

for c in counter:
    y[int(c)] += 1

# y[0] = 0 # too many 0s

fig_size_inches = [18.5, 10.5]

fig, ax = plt.subplots()

x = range(0, max_op)

ax.bar(x, y)

# add a 'best fit' line
'''
y = ((1 / (np.sqrt(2 * np.pi) * sigma)) *
     np.exp(-0.5 * (1 / sigma * (bins - mu))**2))
ax.plot(x, y, '--')
'''
# ax.set_xlim((left, right))
ax.set_xlabel('rg index')
ax.set_ylabel('pool write-ps')
# ax.set_title(r'Block Num on RG')

# Tweak spacing to prevent clipping of ylabel
fig.tight_layout()
# plt.show()
fig = plt.gcf()
# fig.set_size_inches(fig_size_inches)
plt.savefig('rg_io.png')
with PdfPages('rg_io.pdf') as pdf:
    pdf.savefig(fig)