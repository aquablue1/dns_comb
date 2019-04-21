"""
" Similar script with worker2D2, but the Outer Server is classified based on the Organization they belong to.
" The org info is get from the IP-DB and is cached in data/IPDB.log.
" The logic is defined under src.util.IPInfo.py
" Input: the target filename
" Output: the topK result collected  from target file
" By Zhengping on 2019-01-10
"""

from collections import Counter
import json

def doCollectTask(filename, topK):
    """
    Collect the topK result from filename
    :param filename: target filename
    :param topK: topK wants to select, by default is None.
    :return: top K count result.
    """
    IPDBFilename = "../../data/IPDB.log"
    with open(IPDBFilename, 'r') as f:
        IPDB = json.load(f)
    f = open(filename)
    dataDict = json.load(f)
    weirdOutCollect = Counter()
    for key in dataDict:
        if dataDict[key]["weird"]:
            # Check direction first to get the inner server.
            srcIP = dataDict[key]["addr"][0]
            dstIP = dataDict[key]["addr"][2]
            try:
                if srcIP.startswith("136.159."):
                    # Which means srcIP is within our campus. it should be an outbound traffic
                    weirdOutCollect[IPDB[dstIP]["org"]] += 1
                else:
                    weirdOutCollect[IPDB[srcIP]["org"]] += 1
            except KeyError:
                print("Info not found %s." % (dataDict[key]))

    return Counter(dict(weirdOutCollect.most_common(topK)))
