"""
"
"""


import matplotlib.pyplot as plt
import math
import numpy as np
import json
import random


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
    targetList = ['outcampus1']
    for target in targetList:
        filenameIn = "../../exchange/TotalQueryByte/%s_TotalQueryByteCount.log" % target
        with open(filenameIn, 'r') as f:
            rawDict = json.load(f)
        globalInList = []
        for time in rawDict:
            for key in rawDict[time]:
                if rawDict[time][key]:
                    globalInList += rawDict[time][key]

        globalInList = [int(i) for i in globalInList]
        # print(sum(globalInList))
        # globalInList = list(filter(lambda a: a != 0, globalInList))
        globalInList = random_sample(globalInList)
        globalInList.sort()
        x_indata = np.array(globalInList)
        # data_analysis(x_indata)
        a_norm = np.divide(x_indata, x_indata.sum())
        x_indata = list(x_indata)
        x_indata.append(1250)
        ydata = np.cumsum(a_norm)
        ydata = list(ydata)
        ydata.append(1)
        # logxdata = []
        # for i in xdata:
        #     logxdata.append(i if i==0 else math.log10(i))
        plt.plot(x_indata, ydata, label="Query", color="red", linestyle="-")


        filename = "../../exchange/TotalReplyByte/%s_TotalReplyByteCount.log" % target
        with open(filename, 'r') as f:
            rawDict = json.load(f)
        globalOutList = []
        for time in rawDict:
            for key in rawDict[time]:
                if rawDict[time][key]:
                    globalOutList += rawDict[time][key]

        globalOutList = [int(i) for i in globalOutList]
        globalOutList = random_sample(globalOutList)
        # print(sum(globalOutList))
        # globalOutList = list(filter(lambda a: a != 0, globalOutList))
        globalOutList.sort()
        x_outdata = np.array(globalOutList)
        # data_analysis(x_outdata)
        a_norm = np.divide(x_outdata, x_outdata.sum())
        x_outdata = list(x_outdata)
        x_outdata.append(1250)
        ydata = np.cumsum(a_norm)
        ydata = list(ydata)
        ydata.append(1)
        # logxdata = []
        # for i in xdata:
        #     logxdata.append(i if i==0 else math.log10(i))
        # logxdata = [math.log10(i) for i in xdata]
        plt.plot(x_outdata, ydata, label="Reply", color="blue", linestyle="--")

        # plt.xticks([0, 1, 2, 3, 4, 5, 6], ['0']+["$10^{%d}$"% i for i in range(1, 7)])
        # plt.xlim((0, 6))
        plt.xlim(0, 1250)
        plt.xlabel("Message Size (in Byte)")

        plt.ylim((0, 1.05))
        plt.ylabel("CDF")

        plt.title(target)
        plt.legend(loc="best")

        # plt.savefig("../../figure/totalIOSize/%s_%s.pdf" % (target, "totalIOSize"), format='pdf')
        # plt.close()
        plt.show()
        # print(b)
        print("job done %s" % target)


def doTTLCDF():
    targetList = ["inakamai", "inaurora", "incampus", "incampusNew",
                  "incpsc", "inothers", "inphys", "inunknown205"]

    targetList += ["outakamai", "outcampus1", "outcampus2",
                   "outcpsc", "outothers", "outwebpax"]
    targetList = ["incpsc", "inakamai", "incampus"]
    targetList = ["outcpsc",  "outakamai", "outcampus1"]

    color_dict = {"incpsc": 'red',
                  "inakamai": 'blue',
                  "incampus": 'yellow'}
    color_dict = {"outcpsc": 'red',
                  "outakamai": 'blue',
                  "outcampus1": 'yellow'}
    for target in targetList:
        filenameIn = "../../exchange/ReplyTTL/%s_ReplyTTL.log" % target
        with open(filenameIn, 'r') as f:
            rawDict = json.load(f)
        globalInList = []
        for time in rawDict:
            for key in rawDict[time]:
                if key != "-":
                    globalInList += [key]*rawDict[time][key]
        globalInList = list(filter(lambda a: a != "-", globalInList))
        globalInList = [int(float(i)) for i in globalInList]
        globalInList = list(filter(lambda a: a != 0, globalInList))
        # print(sum(globalInList))
        # globalInList = list(filter(lambda a: a != 0, globalInList))
        globalInList = random_sample(globalInList)
        globalInList.sort()
        x_indata = np.array(globalInList)
        # data_analysis(x_indata)
        a_norm = np.divide(x_indata, x_indata.sum())
        ydata = np.cumsum(a_norm)
        ydata = list(ydata)
        ydata.append(1)
        # logxdata = []
        # for i in xdata:
        #     logxdata.append(i if i==0 else math.log10(i))
        log_x_data = [math.log10(x) for x in x_indata]
        log_x_data.append(6)
        plt.plot(log_x_data, ydata, label=target, color=color_dict[target], linestyle="-")

        # plt.xticks([0, 1, 2, 3, 4, 5, 6, 7])
        # plt.plot([math.log10(60), math.log10(60)], [0, 2],
        #          color="black", linewidth=1, linestyle="--")
        # plt.plot([math.log10(3600), math.log10(3600)], [0, 2],
        #          color="black", linewidth=1, linestyle="--")
        # plt.plot([math.log10(14400), math.log10(14400)], [0, 2],
        #          color="black", linewidth=1, linestyle="--")
        # plt.plot([math.log10(86400), math.log10(86400)], [0, 2],
        #          color="black", linewidth=1, linestyle="--")
        # plt.plot([math.log10(86400 * 2), math.log10(86400 * 2)], [0, 2],
        #          color="black", linewidth=1, linestyle="--")
        # plt.plot([math.log10(86400 * 6), math.log10(86400 * 6)], [0, 2],
        #          color="black", linewidth=1, linestyle="--")
        # plt.plot([math.log10(86400 * 7), math.log10(86400 * 7)], [0, 2],
        #          color="black", linewidth=1, linestyle="--")
    plt.xlim((0, 6))
    plt.ylim((0, 1.05))
    plt.legend(loc="best")
    plt.show()

if __name__ == '__main__':
    # doCDF()
    doTTLCDF()

