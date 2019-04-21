"""
" Merge one or multiple dicts based on the key values.
" It is required that if two dicts contain the same key, the corresponding values should also be the same.
" However, this method does not stop the merging process if values are not same,
" Instead, it prints warning information, and use the first defined dict as the chief role.
" The other values with the same key will simply be overlapped.
" Return the merged Dict.
" The original purpose if this function is to merge the IPDB, since more than 5 workers are involved in this work
" Each worker will collect partial of the IP information.
" So a manual merger is required.
" Input, all the dicts are stored in JSON files, hence a list of JSON path should be given.
"
" By Zhengping on 2019-01-24
"""

import json


def doDictMerge(filenameList):
    """
    Warning, the implementation of diDictMerge does not meet the requirements from script
    description, it simply calls the update methods in dict class
    :param filenameList:
    :return:
    """
    clusterDict = {}
    for filename in filenameList:
        with open(filename, 'r') as f:
            tmpDict = json.load(f)
        clusterDict.update(tmpDict)
    return clusterDict
