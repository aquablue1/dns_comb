import matplotlib.pyplot as plt
import math
import numpy as np
import json
import random
from collections import Counter


def do_scatter(filename, target):
    with open(filename, 'r') as f:
        src_size_counter = json.load(f)

        total_outip_counter = Counter()
    for time in src_size_counter:
        tmp_counter = Counter(src_size_counter[time])
        total_outip_counter += tmp_counter

    index = 1
    x_data = []
    y_data = []
    print(target)
    print(total_outip_counter.most_common(10))
    print("=======================================")
    for out_IP_tuple in total_outip_counter.most_common():
        x_data.append(index)
        index += 1
        y_data.append(out_IP_tuple[1])
    # log_x_data = [math.log10(x) for x in x_data]
    # log_y_data = [math.log10(y) for y in y_data]
    # plt.scatter(log_x_data, log_y_data, color="black", label=target, marker="x", linewidths=1)

    # plt.xlim((0, 5))
    # plt.ylim((0, 6))
    # plt.xticks([0, 1, 2, 3, 4, 5], ["$10^{%d}$"%i for i in range(0, 6)])
    # plt.yticks([0, 1, 2, 3, 4, 5, 6], ["$10^{%d}$" % i for i in range(0, 7)])
    #
    # plt.xlabel("Rank of External IP")
    # plt.ylabel("Number of Connections")
    # plt.legend(loc="best")
    # plt.show()


if __name__ == '__main__':
    module_list = ["inakamai", "incpsc", "incampus", "outakamai", "outcpsc", "outcampus1"]
    # module_list = [ "outcpsc", "outcampus1"]
    for module_name in module_list:
        filename_t = "../../exchange/OutIP/%s_TotalOutIPG.log" % module_name
        do_scatter(filename_t, module_name)
