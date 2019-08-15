import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import json
from matplotlib.backends.backend_pdf import PdfPages


with open('rg_io.log.gzblock_num.json', 'r') as f:
    data = json.load(f)

counter = [0] * 30000

for key, v in data.items():
    if 'ssd_pool_r2' not in key:
        continue
    index = v.get('block_num')
    counter[index] += 1


x = range(0, 30000)
fig_size_inches = [18.5, 10.5]
left = 0
while counter[left] == 0:
    left += 1
right = 30000
while counter[right-1] == 0:
    right -= 1

fig, ax = plt.subplots()

ax.bar(x, counter)

# add a 'best fit' line
'''
y = ((1 / (np.sqrt(2 * np.pi) * sigma)) *
     np.exp(-0.5 * (1 / sigma * (bins - mu))**2))
ax.plot(x, y, '--')
'''
ax.set_xlim((left, right))
ax.set_xlabel('block num')
ax.set_ylabel('rg num')
# ax.set_title(r'Block Num on RG')

# Tweak spacing to prevent clipping of ylabel
fig.tight_layout()
# plt.show()
fig = plt.gcf()
# fig.set_size_inches(fig_size_inches)
plt.savefig('block_num.png')
with PdfPages('block_num.pdf') as pdf:
    pdf.savefig(fig)