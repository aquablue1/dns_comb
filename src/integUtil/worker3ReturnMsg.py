"""
" check if the return message is 0 or not.
" for inbound traffic, sender is outer host, the return message is sent by receiver, so we should count resp_byte.
" for outbound traffic, sender is inner host, the return message is sent by receiver, so we still count resp_byte.
" dict["conn"][2]
" Return
" By Zhengping
"""

import json

def doTask(filename):
    """
    count how many lines of record has return msg size equals 0
    :param filename: name of the searched file
    :return: List, [nonemptyCount, emptyCount]
    """
    f = open(filename)
    dataDict = json.load(f)
    emptyCount = 0
    nonemptyCount = 0
    for key in dataDict:
        retmsg = int(dataDict[key]["conn"][2])
        if retmsg == 0:
            emptyCount += 1
        else:
            nonemptyCount += 1
    return [nonemptyCount, emptyCount]