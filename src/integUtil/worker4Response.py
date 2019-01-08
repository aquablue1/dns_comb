"""
" check if the dns record has an actual response.
" The response info is stored in: dict["dns"][3]
" There are two main problems here when loading the response:
" 1. Some of the dns logs suffer from the duplication problem. So far the duplication avoidance plugin is not
"     added into the batchedWorker. Hence we should 1) avoid the duplication here; or 2) ignore the problem here and
"     and wait for the new source data.
" 2. One conn trace may contain multiple dns queries. we should 1) treated it as one or 2) treated it as multiple.
"     If we treated it as one, the duplication can be avoided, but the static is not accurate
"     or If we treated it as multiple, the duplication is still a problem.
"     So far, we treated is as <b>Multiple</b>.
" By Zhengping on 2019-01-07
"""

import json

def doCountTask(filename):
    """
    count how many dns queries have actual responses.
    :param filename: name of the searched file
    :return: List, [responseCount, responselessCount]
    """
    f = open(filename)
    dataDict = json.load(f)
    responselessCount = 0
    responseCount = 0
    for key in dataDict:
        if dataDict[key]["dns"]:
            for dnsmsg in dataDict[key]["dns"]:
                responsemsg = dnsmsg[3]
                if responsemsg == "-":
                    responselessCount += 1
                else:
                    responseCount += 1
    return [responseCount, responselessCount]
