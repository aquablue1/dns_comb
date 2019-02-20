"""
" Create the IP Database based on the IP address and Info We witness
" By Zhengping on 2019-01-21
"""

import sys
import json
from src.util.IPInfo import getIPInfo
# sys.path.append('/home/zhengping/DNS/DNSPythonWorkspace')


def loadIPDatabase():
    IPDBFilename = "../../data/IPDB.log"
    with open(IPDBFilename, 'r') as f:
        IPDict = json.load(f)
    return IPDict


def updateIPDB():
    IPDict = loadIPDatabase()
    moduleList = ["inakamai", "inaurora", "incampus", "incampusNew",
                  "incpsc", "inothers", "inphys", "inunknown205"]

    moduleList += ["outakamai", "outcampus1", "outcampus2",
                  "outcpsc", "outothers", "outwebpax"]

    IPCheckList = set()

    for module in moduleList:
        taskFilename = "../../exchange/ip/%sTotalOutIPCounterTen_trans.log" % module
        with open(taskFilename, 'r') as f:
            ipstatics = json.load(f)
        for ip in ipstatics:
            IPCheckList.add(ip)
    print("len of ipchecklist is %d" % len(IPCheckList))
    print("Index of curr is %d" % list(IPCheckList).index("199.119.235.212"))
    # exit(-1)
    print("cur IPDict len %d" % len(IPDict))
    # print(len(IPDict["128.1.233.242"]))
    # exit(-1)
    newIndex = 0
    for ip in IPCheckList:
        if ip not in IPDict:
            IPInfo = getIPInfo(ip)
            if IPInfo:
                IPDict[ip] = IPInfo
                newIndex += 1
                print("cur new member # %s" % (newIndex))

    with open("../../data/IPDB.log", 'w') as f:
        json.dump(IPDict, f)


if __name__ == '__main__':
    updateIPDB()

