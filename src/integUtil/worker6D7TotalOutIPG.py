"""
" Get the count of IP address in each distinct hours.
" By Zhengping on 2019-01-21
"""

import json
from collections import Counter


def doCollectTask(filename, topK):
    """
    Collect the topK result from filename
    :param filename: target filename
    :param topK: topK wants to select, by default is None.
    :return: top K count result.
    """
    f = open(filename)
    dataDict = json.load(f)
    allOutIPCollect = Counter()
    for key in dataDict:
        # Check direction first to get the inner server.
        srcIP = dataDict[key]["addr"][0]
        dstIP = dataDict[key]["addr"][2]
        if srcIP.startswith("136.159."):
            # Which means srcIP is within our campus. it should be an outbound traffic
            allOutIPCollect[dstIP] += 1
        else:
            allOutIPCollect[srcIP] += 1

    return Counter(dict(allOutIPCollect.most_common(topK)))
