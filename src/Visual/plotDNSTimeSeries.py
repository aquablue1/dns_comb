"""
" draw the DNS time series plot
" By Zhengping on 2019-02-07
"""

import matplotlib.pyplot as plt
import json


def getTTLV(curTTLV):
    if curTTLV <= -50:
        return 50
    else:
        return curTTLV-5


def getData(filename):
    targetIPC = "207.204.213.x"
    targetIPC = "64.x.x.x"
    # targetIPC = "218.248.112.x"
    targetIPC = "190.157.x.x"
    targetIPC = "198.134.2.x"
    # targetIPC = "208.69.32.x"
    # targetIPC = "195.175.122.x"
    with open(filename, 'r') as f:
        rawData = json.load(f)[targetIPC]
    print(len(rawData))
    print(rawData)
    reversedCount = 0
    NSCount = 0
    PhysNSCount = 0
    for row in rawData:
        if "arpa" in row[5]:
            reversedCount += 1
        elif ".auroralimaging.com" in row[5]:
            NSCount += 1
        elif "phys" in row[5]:
            PhysNSCount += 1
    print(str(reversedCount) + "\t" + str(NSCount) + "\t" + str(PhysNSCount))
    # exit(0)
    # 1535781600 or 1535760000
    timeStart = 1535781600 + 3600*24*3
    timeEnd = 1535781600 + 3600*24*6

    # timeStart = 1536573960
    # timeEnd = 1536574080
    ttlLevel = 30
    srcIP = "208.69.32.x"
    query = "mirror.cpsc.ucalgary.ca"
    query = "fsa.cpsc.ucalgary.ca"
    # query = "subitaneous.cpsc.ucalgary.ca"
    query = "pages.cs.ucalgary.ca"
    # query = "pool.ntp.org"
    # query = "ntp.cpsc.ucalgary.ca"
    # query = "248.156.159.136.in-addr.arpa"
    # query = "179.118.159.136.in-addr.arpa"
    # query = "ns1.cs.cpsc.ucalgary.ca"
    # query = "1.2.159.136.in-addr.arpa"

    # ns1
    inquirerSet = set()
    replyList = []
    emptyList = []

    for recocrd in rawData:
        print(recocrd)
        ts = float(recocrd[0])
        if timeStart <= ts <= timeEnd and recocrd[2] == "136.159..1"\
                and recocrd[5] == query:
            inquirerSet.add(recocrd[1])
            reply = [recocrd[0], recocrd[3], recocrd[4], recocrd[7].split(",")[0]]
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
                 color=replyClr, linewidth=2, label="NS1 Succeed")
        ttlLevel = getTTLV(ttlLevel)
        plt.plot([float(elem[0]), float(elem[0])+float(elem[3])], [ttlLevel, ttlLevel])

    emptyClr = (0.0, 0.6, 0.0, 0.2)
    for elem in emptyList:
        if elem[0] == "-" or elem[1] == "-" or elem[2] == "-":
            continue
        print(elem)
        plt.plot([float(elem[0]), float(elem[0])], [float(elem[1]), 0-float(elem[2])],
                 color=emptyClr, linewidth=2, label="NS1 Failed")
        # plt.plot([float(elem[0]), float(elem[0])+3600], [25, 25])

    print(len(replyList))
    print(len(emptyList))

    # ns2
    replyList = []
    emptyList = []

    for recocrd in rawData:
        print(recocrd)
        ts = float(recocrd[0])
        if timeStart <= ts <= timeEnd and recocrd[2] == "136.159.2.4"\
                and recocrd[5] == query:
            inquirerSet.add(recocrd[1])
            reply = [recocrd[0], recocrd[3], recocrd[4], recocrd[7].split(",")[0]]
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
                 color=replyClr, linewidth=2, linestyle="--", label="NS2 Succeed")
        plt.plot([float(elem[0]), float(elem[0])+float(elem[3])], [ttlLevel, ttlLevel])
    emptyClr = (0.0, 0.6, 0.0, 0.2)
    for elem in emptyList:
        if elem[0] == "-" or elem[1] == "-" or elem[2] == "-":
            continue
        print(elem)
        plt.plot([float(elem[0]), float(elem[0])], [float(elem[1]), 0-float(elem[2])],
                 color=emptyClr, linewidth=2, linestyle="--", label="NS2 Failed")
    print(len(replyList))
    print(len(emptyList))



    plt.plot([timeStart-3600, timeEnd+3600], [0,0], linestyle="-.", color="black", linewidth=1)
    plt.xlim((timeStart, timeEnd))

    plt.xticks(list(range(timeStart, timeEnd+3600*24, 3600*24)),
               ["2018-09-%s" % str(d).zfill(2) for d in range(4, 8)], rotation=15)
    # plt.xticks([1536573960, 1536573960+60, 1536573960+120],
    #            ["2018-09-10 10:06", "2018-09-10 10:07", "2018-09-10 10:08"], rotation=15)
    plt.title("Queried NS: "+query)
    # plt.ylim((-400, 400))

    handles, labels = plt.gca().get_legend_handles_labels()
    i = 1
    while i < len(labels):
        if labels[i] in labels[:i]:
            del (labels[i])
            del (handles[i])
        else:
            i += 1
    plt.legend(handles, labels, loc="lower right")
    plt.text(timeStart+3000, -75, "Inquirer: "+srcIP, fontsize=10)
    plt.text(timeStart+3000, -85, "Queried NS: "+query, fontsize=10 )

    print(inquirerSet)
    print(len(inquirerSet))
    plt.show()



if __name__ == '__main__':
    targetList = ["inakamai", "inaurora", "incampus", "incampusNew",
                  "incpsc", "inothers", "inphys", "inunknown205"]

    targetList += ["outakamai", "outcampus1", "outcampus2",
                  "outcpsc", "outothers", "outwebpax"]
    targetList = ["inaurora"]
    for target in targetList:
        filename = "../../exchange/batchedTransWork/%sTransTop100TSpecial.log" % target
        getData(filename)