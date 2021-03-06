"""
" Similar with worker6D1, this method is used to collect and count all distinct Outer DNS Servers seen from our log.
" However, different from worker6D1, the Outer DNS Servers are clustered based on their IP in order to expose a more
" Clear logic.
" Also, this worker seems to be more useful than worker6D2 since the Outer Server are more interesting.
" By Zhengping on 2019-01-16
"""

import sys
from src.util.IPCluster import getIPCluster
from collections import Counter
import json
sys.path.append('/home/zhengping/DNS/DNSPythonWorkspace')


def doCollectTask(filename, topK):
    """
    Collect the topK result from filename
    :param filename: target filename
    :param topK: topK wants to select, by default is None.
    :return: top K count result.
    """
    f = open(filename)
    dataDict = json.load(f)
    allOutCollect = {}
    for key in dataDict:
        # Check direction first to get the inner server.
        srcIP = dataDict[key]["addr"][0]
        dstIP = dataDict[key]["addr"][2]
        if srcIP.startswith("136.159."):
            # Which means srcIP is within our campus. it should be an outbound traffic
            if dataDict[key]["conn"][1] != "-":
                try:
                    allOutCollect[getIPCluster(dstIP)].append(dataDict[key]["conn"][2])
                except KeyError:
                    allOutCollect[getIPCluster(dstIP)] = []
                    allOutCollect[getIPCluster(dstIP)].append(dataDict[key]["conn"][2])
        else:
            if dataDict[key]["conn"][2] != "-":
                try:
                    allOutCollect[getIPCluster(srcIP)].append(dataDict[key]["conn"][1])
                except KeyError:
                    allOutCollect[getIPCluster(srcIP)] = []
                    allOutCollect[getIPCluster(srcIP)].append(dataDict[key]["conn"][1])
    return allOutCollect
