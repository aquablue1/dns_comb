"""
" Collect and count all the Inner Server in record file.
" Since there are only limited Inner server in each module (actually they are assigned in inBatchedDump.py and
" outBatchedDump.py)
" However, there are still at least two advantages of this script:
" First, we can get the actual statistics of each module
" Second, for others module only, we can all the distinct Inner DNS Servers.
" By Zhengping on 2019-01-10
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
    allInCollect = Counter()
    for key in dataDict:
        # Check direction first to get the inner server.
        srcIP = dataDict[key]["addr"][0]
        dstIP = dataDict[key]["addr"][2]
        if srcIP.startswith("136.159."):
            # Which means srcIP is within our campus. it should be an outbound traffic
            allInCollect[srcIP] += 1
        else:
            allInCollect[dstIP] += 1
    return Counter(dict(allInCollect.most_common(topK)))
