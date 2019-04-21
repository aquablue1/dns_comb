"""
"
"""


import matplotlib.pyplot as plt
import math
import numpy as np
import json
import random
from collections import Counter


def do_log_scatter(filename, target):
    with open(filename, 'r') as f:
        src_counter = json.load(f)

    total_counter = Counter()
    for time in src_counter:
        tmp_counter = Counter(src_counter[time])
        total_counter += tmp_counter

    index = 1
    x_data = []
    y_data = []
    for tuple_info in total_counter.most_common():
        key, occurrence = tuple_info[0], tuple_info[1]
        x_data.append(index)
        index += 1
        y_data.append(occurrence)
    print("=========================")
    print("The top-10 tuples for %s are:" % target)
    print("Length of counter is %d" % len(total_counter))
    for top_tuple_info in total_counter.most_common():
        count = top_tuple_info[1]
        print(top_tuple_info)
        if count < 1_000:
            break
    print("=========================")
    x_data_log = [math.log10(x) for x in x_data]
    y_data_log = [math.log10(y) for y in y_data]
    plt.scatter(x_data_log, y_data_log, color="black", marker="x", s=10)

    # plt.xlim((0, 1200))
    # plt.ylim((0, 1200))
    #
    # plt.xlabel("Query Size (Byte)")
    # plt.ylabel("Response Size (Byte)")

    plt.show()


if __name__ == '__main__':
    module_list = ["inakamai", "incpsc", "incampus", "incampusNew", "inothers"]
    # module_list = ["outakamai", "outcampus1", "outcampus2", "outcpsc", "outothers"]
    module_list = ["inothers"]
    for module_name in module_list:
        # filename_t = "../../exchange/Scanner/U205Scanner/%s_U205Scanner.log" % module_name
        filename_t = "../../exchange/Scanner/S0Scanner/%s_S0Scanner.log" % module_name
        do_log_scatter(filename_t, target=module_name)
