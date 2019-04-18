"""
"
"""


import matplotlib.pyplot as plt
import math
import numpy as np
import json
import random
from collections import Counter


def do_scatter(filename):
    with open(filename, 'r') as f:
        src_size_counter = json.load(f)

    total_size_counter = Counter()
    for time in src_size_counter:
        tmp_counter = Counter(src_size_counter[time])
        total_size_counter += tmp_counter
    max_count = math.log10(total_size_counter.most_common(1)[0][1])
    for size_info in total_size_counter:
        q_size, r_size = int(size_info.split("/")[0]), int(size_info.split("/")[1])
        occurance = total_size_counter[size_info]
        transparent = math.log10(occurance)/max_count
        color = (1, 0, 0, transparent)
        plt.scatter([q_size], [r_size], color=color, marker="o", s=8)
    plt.plot([0, 800], [0, 800], color="black", linewidth=1, linestyle="--")

    plt.xlim((0, 800))
    plt.ylim((0, 800))

    plt.xlabel("Query Size (Byte)")
    plt.ylabel("Response Size (Byte)")

    plt.show()


if __name__ == '__main__':
    module_list = ["inakamai", "incpsc", "incampus", "outakamai", "outcpsc", "outcampus1"]
    # module_list = [ "incpsc", "outcampus1"]
    for module_name in module_list:
        filename_t = "../../exchange/TotalQueryReply/%s_TotalQueryReplyE.log" % module_name
        do_scatter(filename_t)
