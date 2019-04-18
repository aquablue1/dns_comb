"""
"
"""


import matplotlib.pyplot as plt
import math
import numpy as np
import json
import random
from collections import Counter


def random_sample(n_array):
    selected_list = []
    for k in n_array:
        rand_int = random.randint(0, 50)
        if rand_int == 1:
            selected_list.append(k)
    return selected_list


def data_analysis(n_array):
    print("The length of array is %d" % len(n_array))
    print("The maximum witnessed Value is %d" % np.max(n_array))
    print("The minimum witnessed value is %d" % np.min(n_array))
    print("The mean value is %f" % n_array.mean())
    print(sum(list(n_array)))

def doCDF():
    targetList = ["inakamai", "inaurora", "incampus", "incampusNew",
                  "incpsc", "inothers", "inphys", "inunknown205"]

    targetList += ["outakamai", "outcampus1", "outcampus2",
                   "outcpsc", "outothers", "outwebpax"]
    targetList = ['outakamai', 'outcpsc', 'outcampus1']
    color_dict = {"outakamai": "blue",
                  "outcpsc": "red",
                  "outcampus1": "green"}
    # targetList = ['inakamai', 'incpsc', 'incampus']
    # color_dict = {"inakamai": "blue",
    #               "incpsc": "red",
    #               "incampus": "green"}
    for target in targetList:

        #     filenameIn = "../../exchange/TotalQueryByte/%s_TotalQueryByteCount.log" % target
        #     with open(filenameIn, 'r') as f:
        #         rawDict = json.load(f)
        #     globalInList = []
        #     for time in rawDict:
        #         for key in rawDict[time]:
        #             if rawDict[time][key]:
        #                 globalInList += rawDict[time][key]
        #
        #     globalInList = [int(i) for i in globalInList]
        #     # print(sum(globalInList))
        #     # globalInList = list(filter(lambda a: a != 0, globalInList))
        #     globalInList = random_sample(globalInList)
        #     globalInList.sort()
        #     x_indata = np.array(globalInList)
        #     # data_analysis(x_indata)
        #     a_norm = np.divide(x_indata, x_indata.sum())
        #     x_indata = list(x_indata)
        #     x_indata.append(1250)
        #     ydata = np.cumsum(a_norm)
        #     ydata = list(ydata)
        #     ydata.append(1)
        #     # logxdata = []
        #     # for i in xdata:
        #     #     logxdata.append(i if i==0 else math.log10(i))
        #     plt.plot(x_indata, ydata, label="Query", color="red", linestyle="-")

        filename = "../../exchange/ReplyTTL/%s_ReplyTTL.log" % target
        with open(filename, 'r') as f:
            rawDict = json.load(f)
        total_counter = Counter()
        globalOutList = []
        for time in rawDict:
            total_counter += Counter(rawDict[time])
        print(total_counter.most_common(5))
        print(total_counter["518400.000000"])
        for key in total_counter:
            if key != "-":
                globalOutList += ([int(float(key))] * int(total_counter[key]))
        # globalOutList = [int(float(i)) for i in globalOutList]
        # print(globalOutList[2456090:2456100])
        print(len(globalOutList))
        # globalOutList = random_sample(globalOutList)
        # print(sum(globalOutList))
        globalOutList = list(filter(lambda a: a != 0, globalOutList))
        globalOutList.sort()

        x_outdata = np.array(globalOutList)
        # data_analysis(x_outdata)
        x_total = sum(globalOutList)
        # a_norm = np.divide(x_outdata, x_outdata.sum())
        a_norm = [x/x_total for x in globalOutList]
        # x_outdata = list(x_outdata)
        # x_outdata.append(1250)
        a_norm = np.array(a_norm)
        y_base = [1] * len(globalOutList)
        y_base_np = np.array(y_base)
        ybase_norm = np.divide(y_base_np, y_base_np.sum())
        ydata = np.cumsum(ybase_norm)

        # ydata = list(ydata)
        # ydata.append(1)
        # logxdata = []
        # for i in xdata:
        #     logxdata.append(i if i==0 else math.log10(i))
        logxdata = [math.log10(i) for i in x_outdata]
        plt.plot(logxdata, ydata, label=target, color=color_dict[target], linestyle="-")

        # plt.xticks([0, 1, 2, 3, 4, 5, 6], ['0']+["$10^{%d}$"% i for i in range(1, 7)])
        # plt.xlim((0, 6))
        # plt.xlim(0, 1250)
        # plt.xlabel("Message Size (in Byte)")

    plt.ylim((0, 1.05))
    plt.xlim((0, 6))
    plt.ylabel("CDF")

    # plt.title(target)
    plt.legend(loc="best")

    # plt.savefig("../../figure/totalIOSize/%s_%s.pdf" % (target, "totalIOSize"), format='pdf')
    # plt.close()
    plt.show()
    # print(b)
    # print("job done %s" % target)


if __name__ == '__main__':
    doCDF()
