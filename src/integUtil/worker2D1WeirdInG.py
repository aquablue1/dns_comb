"""
" Analysis the inner server of weird DNS traffic based on the Weird Record
" The inner server means the inner Campus DNS server which involved in the weird behavior.
" Input: the target filename
" Output: the topK collected result from target file
" By Zhengping on 2019-01-08
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
    f = open(filename)
    dataDict = json.load(f)
    weirdInCollect = Counter()
    for key in dataDict:
        if dataDict[key]["weird"]:
            # Check direction first to get the inner server.
            srcIP = dataDict[key]["addr"][0]
            dstIP = dataDict[key]["addr"][2]
            if srcIP.startswith("136.159."):
                # Which means srcIP is within our campus. it should be an outbound traffic
                weirdInCollect[srcIP] += 1
            else:
                weirdInCollect[dstIP] += 1

    return Counter(dict(weirdInCollect.most_common(topK)))
