"""
" Similar script with worker2D2, but the Outer Server is classified based on cluster.
" The cluster is basically the class A, B or C IP address.
" The logic is defined under src.util.IPCluster
" Input: the target filename
" Output: the topK result collected  from target file
" By Zhengping on 2019-01-10
"""

import sys
sys.path.append('/home/zhengping/DNS/DNSPythonWorkspace')
from src.util.IPCluster import getIPCluster
from collections import Counter
import json

def doCollectTask(filename, topK):
    """
    Collect the topK result from filename
    :param filename: target filename
    :param topK: topK wants to select, by default is None.
    :return: top K count result.
    """
    f = open(filename)
    dataDict = json.load(f)
    weirdOutCollect = Counter()
    for key in dataDict:
        if dataDict[key]["weird"]:
            # Check direction first to get the inner server.
            srcIP = dataDict[key]["addr"][0]
            dstIP = dataDict[key]["addr"][2]
            if srcIP.startswith("136.159."):
                # Which means srcIP is within our campus. it should be an outbound traffic
                weirdOutCollect[getIPCluster(dstIP)] += 1
            else:
                weirdOutCollect[getIPCluster(srcIP)] += 1

    return Counter(dict(weirdOutCollect.most_common(topK)))
