"""
" Get the hourly weird counting
" output: timestamp \t non-weird \t weird \n
" weird means the record has the corresponding weird log, dict["weird"] != "None"
" By Zhengping on 2019-01-06
"""

# Note: the below problem has been fixed.
# unWarning This worker does not work, since weird type is not properly loaded by the outer input data structure.
# Update is needed.


import json

def doCountTask(filename):
    """
    count how many dns queries have actual responses.
    :param filename: name of the searched file
    :return: List, [responseCount, responselessCount]
    """
    f = open(filename)
    dataDict = json.load(f)
    weridCount = 0
    unweridCount = 0
    for key in dataDict:
        if dataDict[key]["weird"]:
            weridCount += 1
        else:
            unweridCount += 1
    return [unweridCount, weridCount]
