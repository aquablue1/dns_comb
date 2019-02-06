"""
" Collect the different type of TLD which has a valid response.
" The response is verified by the "response" field under "dns" entry of each trace.
" As long as one of the dns record has a valid response, it is treated as responsible.
" If neither dns entries from a trace has valid response, it is treated as responseless.
" The size of the session is recorded.
" By Zhengping on 2019-01-24
"""

import sys
sys.path.append('/home/zhengping/DNS/DNSPythonWorkspace')
import json
from collections import Counter
from src.util.TLDExtract import getTLD

def doCollectTask(filename, topK):
    """
    collect all the TLD records which have a valid response
    :param filename: file to be executed
    :param topK: topK returned result
    :return:
    """
    f = open(filename)
    dataDict = json.load(f)
    tldCollect = Counter()
    for key in dataDict:
        if dataDict[key]["dns"]:
            for dns in dataDict[key]["dns"]:
                if dns[3] != "-":
                    tld = getTLD(dns[2])
                    answerSize = dataDict[key]["conn"][2]
                    if answerSize == "-":
                        answerSize = 0
                    tldCollect[tld] += int(answerSize)
    return Counter(dict(tldCollect.most_common(topK)))
