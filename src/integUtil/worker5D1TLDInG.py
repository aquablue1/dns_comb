"""
" Collect and count the unique TLD from each DNS queries.
" There are at least two problems needed to be focused.
" First, further classification based on response/responseless should also be included.
" Second, the direction is an important factor of the analysis result. (e.g. all the
" Inbound traffic should be related to UofC, which means they should ended either with .ca or with .com)
" To be continued...
" By Zhengping on 2019-08-01
"""

import sys
sys.path.append('/home/zhengping/DNS/DNSPythonWorkspace')
import json
from collections import Counter
from src.util.TLDExtract import getTLD

def doCollectTask(filename, topK):
    """
    collect and count TLD from the input file.
    :param filename: name of the searched file
    :return: a dict which store the count result of topK TLD
    """
    f = open(filename)
    dataDict = json.load(f)
    tldCollect = Counter()
    for key in dataDict:
        if dataDict[key]["dns"]:
            for dns in dataDict[key]["dns"]:
                tld = getTLD(dns[2])
                tldCollect[tld] += 1
    return Counter(dict(tldCollect.most_common(topK)))

