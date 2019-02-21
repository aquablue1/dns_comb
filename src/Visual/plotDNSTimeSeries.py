"""
" draw the DNS time series plot
" By Zhengping on 2019-02-07
"""

import matplotlib.pyplot as plt
import json


def getTTLV(curTTLV):
    if curTTLV <= -25:
        return 25
    else:
        return curTTLV-5


def getData(filename):
    targetIPC = "207.204.213.x"
    targetIPC = "64.x.x.x"
    # targetIPC = "218.248.112.x"
    targetIPC = "190.157.x.x"
    targetIPC = "198.134.2.x"
    with open(filename, 'r') as f:
        rawData = json.load(f)[targetIPC]
    # 1535781600 or 1535760000
    timeStart = 1535781600 + 3600*24*3
    timeEnd = 1535781600 + 3600*24*6

    # timeStart = 1536573960
    # timeEnd = 1536574080
    ttlLevel = 30
    query = "ns1.phys.ucalgary.ca"
    query = "ns2.phys.ucalgary.ca"
    query = "smtp.phys.ucalgary.ca"

    # ns1
    replyList = []
    emptyList = []

    for recocrd in rawData:
        print(recocrd)
        ts = float(recocrd[0])
        if timeStart <= ts <= timeEnd and recocrd[2] == "136.159.51.4"\
                and recocrd[5] == query:
            reply = [recocrd[0], recocrd[3], recocrd[4]]
            if recocrd[6]!="-":
                replyList.append(reply)
            else:
                emptyList.append(reply)

    # print(ip1List)
    replyClr = (0.6, 0.0, 0.0, 0.2)
    for elem in replyList:
        if elem[0] == "-" or elem[1] == "-" or elem[2] == "-":
            continue
        print(elem)
        plt.plot([float(elem[0]), float(elem[0])], [float(elem[1]), 0-float(elem[2])],
                 color=replyClr, linewidth=2)
        ttlLevel = getTTLV(ttlLevel)
        plt.plot([float(elem[0]), float(elem[0])+3600], [ttlLevel, ttlLevel])

    emptyClr = (0.0, 0.6, 0.0, 0.2)
    for elem in emptyList:
        if elem[0] == "-" or elem[1] == "-" or elem[2] == "-":
            continue
        print(elem)
        plt.plot([float(elem[0]), float(elem[0])], [float(elem[1]), 0-float(elem[2])],
                 color=emptyClr, linewidth=2)
        # plt.plot([float(elem[0]), float(elem[0])+3600], [25, 25])

    print(len(replyList))
    print(len(emptyList))

    # ns2
    replyList = []
    emptyList = []

    for recocrd in rawData:
        print(recocrd)
        ts = float(recocrd[0])
        if timeStart <= ts <= timeEnd and recocrd[2] == "136.159.51.5"\
                and recocrd[5] == query:
            reply = [recocrd[0], recocrd[3], recocrd[4]]
            if recocrd[6]!="-":
                replyList.append(reply)
            else:
                emptyList.append(reply)
    # print(ip1List)
    replyClr = (0.6, 0.0, 0.0, 0.2)
    for elem in replyList:
        if elem[0] == "-" or elem[1] == "-" or elem[2] == "-":
            continue
        print(elem)
        ttlLevel = getTTLV(ttlLevel)
        plt.plot([float(elem[0]), float(elem[0])], [float(elem[1]), 0-float(elem[2])],
                 color=replyClr, linewidth=2, linestyle="--")
        plt.plot([float(elem[0]), float(elem[0])+3600], [ttlLevel, ttlLevel])
    emptyClr = (0.0, 0.6, 0.0, 0.2)
    for elem in emptyList:
        if elem[0] == "-" or elem[1] == "-" or elem[2] == "-":
            continue
        print(elem)
        plt.plot([float(elem[0]), float(elem[0])], [float(elem[1]), 0-float(elem[2])],
                 color=emptyClr, linewidth=2, linestyle="--")
    print(len(replyList))
    print(len(emptyList))

    # smtp (ns3)
    replyList = []
    emptyList = []

    for recocrd in rawData:
        print(recocrd)
        ts = float(recocrd[0])
        if timeStart <= ts <= timeEnd and recocrd[2] == "136.159.52.10"\
                and recocrd[5] == query:
            reply = [recocrd[0], recocrd[3], recocrd[4]]
            if recocrd[6]!="-":
                replyList.append(reply)
            else:
                emptyList.append(reply)

    # print(ip1List)
    replyClr = (0.6, 0.0, 0.0, 0.2)
    for elem in replyList:
        if elem[0] == "-" or elem[1] == "-" or elem[2] == "-":
            continue
        print(elem)
        ttlLevel = getTTLV(ttlLevel)
        plt.plot([float(elem[0]), float(elem[0])], [float(elem[1]), 0-float(elem[2])],
                 color=replyClr, linewidth=2, linestyle="--")
        plt.plot([float(elem[0]), float(elem[0])+3600], [ttlLevel, ttlLevel])

    emptyClr = (0.0, 0.6, 0.0, 0.2)
    for elem in emptyList:
        if elem[0] == "-" or elem[1] == "-" or elem[2] == "-":
            continue
        print(elem)
        plt.plot([float(elem[0]), float(elem[0])], [float(elem[1]), 0-float(elem[2])],
                 color=emptyClr, linewidth=2, linestyle="-.")
    print(len(replyList))
    print(len(emptyList))

    plt.plot([timeStart-3600, timeEnd+3600], [0,0], linestyle="-.", color="black", linewidth=1)
    plt.xlim((timeStart, timeEnd))

    plt.xticks(list(range(timeStart, timeEnd+3600*24, 3600*24)),
               ["2018-09-%s" % str(d).zfill(2) for d in range(4, 8)], rotation=15)
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
        filename = "../../exchange/batchedTransWork/%sTransTop100TSpecial.log" % target
        getData(filename)