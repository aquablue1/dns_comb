"""
" Trans the storage format for popular IPs.
" By Zhengping on 2019-02-06
"""


import json
import sys
sys.path.append('/home/zhengping/DNS/DNSPythonWorkspace')
from src.util.IPCluster import getIPCluster

def doTransTask(filename, topK):
    """
    Collect the topK result from filename
    :param filename: target filename
    :param topK: topK wants to select, by default is None.
    :return: top K count result.
    """
    f = open(filename)
    dataDict = json.load(f)
    popIPList = []
    transResult = {}
    for key in dataDict:
        # Check direction first to get the inner server.
        srcIP = dataDict[key]["addr"][0]
        dstIP = dataDict[key]["addr"][2]
        if srcIP.startswith("136.159."):
            # Which means srcIP is within our campus. it should be an outbound traffic
            externalIP = dstIP
        else:
            externalIP = srcIP
        externalIPC = getIPCluster(externalIP)
        if externalIPC not in popIPList:
            continue
        try:
            transResult[externalIPC].append([dataDict[key]["ts"],
                                             dataDict[key]["addr"][0], dataDict[key]["addr"][2],
                                             dataDict[key]["conn"][4], dataDict[key]["conn"][6]],
                                             dataDict[key]['dns'][2], dataDict[key]["dns"][3])
        except KeyError:
            transResult[externalIPC] = [[dataDict[key]["ts"],
                                         dataDict[key]["addr"][0], dataDict[key]["addr"][2],
                                         dataDict[key]["conn"][4], dataDict[key]["conn"][6]],
                                         dataDict[key]['dns'][2], dataDict[key]["dns"][3]]
    # print(transResult)
    return transResult
