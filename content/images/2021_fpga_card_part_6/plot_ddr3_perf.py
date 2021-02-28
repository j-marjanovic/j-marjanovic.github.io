#! /usr/bin/env python3

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

"""

8
[mem check]   write throughput = 7816 MB/s
[mem check]   read throughput = 3138 MB/s

16
[mem check]   write throughput = 7816 MB/s
[mem check]   read throughput = 4898 MB/s

32
[mem check]   write throughput = 7816 MB/s
[mem check]   read throughput = 6854 MB/s

64
[mem check]   write throughput = 7816 MB/s
[mem check]   read throughput = 8583 MB/s

128
[mem check]   write throughput = 7816 MB/s
[mem check]   read throughput = 9790 MB/s


reordering turned on
[mem check]   write throughput = 7816 MB/s
[mem check]   read throughput = 9662 MB/s

"""


labels = ["8", "16", "32", "64", "128", "128 + reord"]
write_throughput_mbps = [7816, 7816, 7816, 7816, 7816, 7816]
read_throughput_mbps  = [3138, 4898, 6854, 8583, 9790, 9662]

max_speed_mbps = 64 * 1600e6 / 1e6 / 8

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, write_throughput_mbps, width, label='Write [MB/s]')
rects2 = ax.bar(x + width/2, read_throughput_mbps, width, label='Read [MB/s]')



# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('throughput')
ax.set_xlabel('burst length')

ax.set_title('DDR3 performance on Stratix V board')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.axhline(max_speed_mbps, linestyle='--', color='grey', alpha=0.8, linewidth=2, label="theoretical max [MB/s]")
ax.legend(loc="upper left")
ax.grid(True)


def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


autolabel(rects1)
autolabel(rects2)


fig.tight_layout()

#plt.show()

plt.savefig("plot_ddr3_perf.png")
