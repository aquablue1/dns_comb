"""
" draw the DNS time series plot
" By Zhengping on 2019-02-07
"""

import matplotlib.pyplot as plt
import json


def getData(filename):
    targetIPC = "207.204.213.x"
    targetIPC = "64.x.x.x"
    # targetIPC = "218.248.112.x"
    with open(filename, 'r') as f:
        rawData = json.load(f)[targetIPC]
    timeStart = 1535760000 + 3600*24*3 + 6*3600
    timeEnd = 1535760000 + 3600*24*4 + 6*3600

    # timeStart = 1536573960
    # timeEnd = 1536574080
    dstIP1 = "136.159.51.4"
    ip1List = []
    dstIP2 = "136.159.51.5"
    ip2List = []
    dstIP3 = "136.159.52.10"
    ip3List = []

    for recocrd in rawData:
        print(recocrd)
        ts = float(recocrd[0])
        if timeStart <= ts <= timeEnd:
            info = [recocrd[0], recocrd[3], recocrd[4]]
            if recocrd[2] == dstIP1:
                ip1List.append(info)
            elif recocrd[2] == dstIP2:
                ip2List.append(info)
            elif recocrd[2] == dstIP3:
                ip3List.append(info)
    # print(ip1List)
    for elem in ip1List:
        if elem[0] == "-" or elem[1] == "-" or elem[2] == "-":
            continue
        print(elem)
        plt.plot([float(elem[0]), float(elem[0])], [float(elem[1]), 0-float(elem[2])],
                 color="black")
    plt.plot([timeStart-3600, timeEnd+3600], [0,0], linestyle="--", color="black", linewidth=1)
    plt.xlim((timeStart, timeEnd))
    plt.xticks(list(range(timeStart, timeEnd+3600*24, 3600*24)),
               ["2018-09-%s" % str(d).zfill(2) for d in range(4, 11)], rotation=15)
    # plt.xticks([1536573960, 1536573960+60, 1536573960+120],
    #            ["2018-09-10 10:06", "2018-09-10 10:07", "2018-09-10 10:08"], rotation=15)
    plt.show()



if __name__ == '__main__':
    targetList = ["inakamai", "inaurora", "incampus", "incampusNew",
                  "incpsc", "inothers", "inphys", "inunknown205"]

    targetList += ["outakamai", "outcampus1", "outcampus2",
                  "outcpsc", "outothers", "outwebpax"]
    targetList = ["inphys"]
    for target in targetList:
        filename = "../../exchange/batchedTransWork/%sTransPop100T.log" % target
        getData(filename)