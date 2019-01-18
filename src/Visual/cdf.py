"""
"
"""


import matplotlib.pyplot as plt
import math
import numpy as np
import json


def doCDF():
    targetList = ["inakamai", "inaurora", "incampus", "incampusNew",
                  "incpsc", "inothers", "inphys", "inunknown205"]

    targetList += ["outakamai", "outcampus1", "outcampus2",
                   "outcpsc", "outothers", "outwebpax"]
    targetList = ['outothers']
    for target in targetList:
        filenameIn = "../../exchange/totalSizeE/%sTotalInByteClusterExtrOne.log" % target
        with open(filenameIn, 'r') as f:
            rawDict = json.load(f)
        globalInList = []
        for time in rawDict:
            for key in rawDict[time]:
                if rawDict[time][key]:
                    globalInList += rawDict[time][key]

        globalInList = [int(i) for i in globalInList]
        globalInList.sort()
        xdata = np.array(globalInList)
        a_norm = np.divide(xdata, xdata.sum())
        ydata = np.cumsum(a_norm)
        logxdata = []
        for i in xdata:
            logxdata.append(i if i==0 else math.log10(i))
        plt.plot(logxdata, ydata, label="Inbound", color="red")


        filename = "../../exchange/totalSizeE/%sTotalOutByteClusterExtrOne.log" % target
        with open(filename, 'r') as f:
            rawDict = json.load(f)
        globalOutList = []
        for time in rawDict:
            for key in rawDict[time]:
                if rawDict[time][key]:
                    globalOutList += rawDict[time][key]

        globalOutList = [int(i) for i in globalOutList]
        globalOutList.sort()
        xdata = np.array(globalOutList)
        a_norm = np.divide(xdata, xdata.sum())
        ydata = np.cumsum(a_norm)
        logxdata = []
        for i in xdata:
            logxdata.append(i if i==0 else math.log10(i))
        # logxdata = [math.log10(i) for i in xdata]
        plt.plot(logxdata, ydata, label="Outbound", color="blue")

        plt.xticks([0, 1, 2, 3, 4, 5, 6], ['0']+["$10^{%d}$"% i for i in range(1, 7)])
        plt.xlim((0, 6))
        plt.xlabel("Message Size (in Byte)")

        plt.ylim((0, 1.05))
        plt.ylabel("CDF")

        plt.title(target)
        plt.legend(loc="best")

        plt.savefig("../../figure/totalIOSize/%s_%s.pdf" % (target, "totalIOSize"), format='pdf')
        plt.close()
        # plt.show()
        # print(b)
        print("job done %s" % target)


if __name__ == '__main__':
    doCDF()
