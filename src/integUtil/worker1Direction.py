"""
" Get the hourly counting by direction.
" Since inbound and outbound data are stored separately,
" this method only returns the counting of current file.
" Outer worker (batchedWorker) will control the direction count by using different target names.
" By Zhengping on 2019-01-06
"""


import json

def doTask(filename):
    """
    count how many lines of record has return msg size equals 0
    :param filename: name of the searched file
    :return: List, [count]
    """
    f = open(filename)
    dataDict = json.load(f)
    count = len(dataDict)
    return [count]