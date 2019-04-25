"""
" Check the query field in each scan activity.
" By Zhengping on 2019-04-18
"""

import math
import json
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter


class ScanTimeChecker:
    def __init__(self, target_ip):
        self.s_ip = target_ip
        self.time_list = []
        self.time_range = {"start": math.inf,
                           "end": 0}

    def checker(self):
        """

        :return:
        """
        src_filename = "../../exchange/Scanner/targetIPs/%s.log" % self.s_ip

        with open(src_filename, 'r') as f:
            data_dict = json.load(f)

        for uid in data_dict:
            time_stamp = float(data_dict[uid]["ts"])
            self.time_list.append(time_stamp)
            if time_stamp < self.time_range["start"]:
                self.time_range["start"] = time_stamp
            if time_stamp > self.time_range["end"]:
                self.time_range["end"] = time_stamp

        return self.time_list

    def paint(self):
        x_data = self.time_list
        y_data = [1] * len(x_data)
        color = (1, 0, 0, 0.2)
        plt.scatter(x_data, y_data, color=color, marker="o", s=10)
        plt.show()


def aov_painter():
    with open("../../exchange/Scanner/time_info.log", 'r') as f:
        time_info = json.load(f)
    y_data = []
    for ip in time_info:
        y_data.append(float(time_info[ip][2]))
    x_data = list(range(len(y_data)))
    plt.scatter(x_data, y_data, marker="x", s=10, color="black")
    plt.show()

if __name__ == '__main__':
    with open("../../exchange/Scanner/TargetExact.log", 'r') as f:
        target_ip_list = json.load(f)["target"]
    time_dict = {}
    y_data = []
    for target_ip_t in target_ip_list:
        # target_ip_t = "111.13.148.44"
        query_checker = ScanTimeChecker(target_ip_t)
        time_list = query_checker.checker()
        aoc = np.array(time_list).std()/len(time_list)
        time_dict[target_ip_t] = [query_checker.time_range["start"],
                                  query_checker.time_range["end"],
                                  aoc]
        if aoc > 40:
            query_checker.paint()

    # with open("../../exchange/Scanner/time_info.log", 'w') as f:
    #     json.dump(time_dict, f)

    # aov_painter()



