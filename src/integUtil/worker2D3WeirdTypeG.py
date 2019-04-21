"""
" Similar script with worker2D1, but weird Type is focused here.
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
    weirdTypeCollect = Counter()
    for key in dataDict:
        if dataDict[key]["weird"]:
            # Check direction first to get the inner server.
            for weird in dataDict[key]["weird"]:
                weirdTypeCollect[weird[0]] += 1

    return Counter(dict(weirdTypeCollect.most_common(topK)))
