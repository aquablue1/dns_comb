"""
" The purpose of this script is build a connection between source JS file and data which is prepared for
" result visualization.
" For all the JSON files generated by Collect workers, their key should be a timestamp: %date_%hour.
" and all the values are also a dict with each K as the collected object and value as the counting of the corresponding
" Key.
" For this script, it will read one or more JSON files, convert it/them into the following format:
" obj-name1 \t count_at_time1 \t count_at_time2 ... count_at_timeN \n
" obj-name2 \t count_at_time1 \t count_at_time2 ... count_at_timeN \n
" ....
" obj-nameN \t count_at_time1 \t count_at_time2 ... count_at_timeN \n
" where obj-name can be either user-defined or generated from source files.
" ==> Problem 1:
" The selection of obj-name is not easy since the data at different time may contain completely different obj set.
" In this situation, the user-defined obj-name set might help, but it is not enough if the number of distinct
" obj-name is large.
" A potential good solution is select the topK popular obj-name based on the overall static.
" But this means a pre-process to collect the total occurance for each obj is necessary. This will increase
" the execution time.
" In this script all the mentioned solutions are implemented. But the topK method is suggested.
" ==> Problem 2:
" The second problem is single file vs multiple files.
" In some scenario data is stored in multiple files since they used to belong to different Objects (e.g. outcampus1
" and outcampus2), when an integrated analysis is required, (To be continued...)
" By Zhengping on 2019-01-10
"""


import sys
import json
# from src.util.FileWriter import fileWriter
from collections import OrderedDict, Counter
sys.path.append('/home/zhengping/DNS/DNSPythonWorkspace')

# Warning! at this stage, only a single file is handled. Means it will only accept a single file, and then dump it
# to a single Line RecordFile


def doSingleTrans(filename, outputFilename, topK=None, assigObject=None):
    """
    trans a single file into the second-level exchange format and store it into the storage folder.
    :param filename: input single filename, only the filename, no folder info
    :param outputFilename: the outputFilename
    :param topK: topK objects that wants to be translated
    :param assigObject: a list of assigned obj (if this field is assigned, topK selection becomes useless)
    :return: output the translated result as json file.
    """
    fatherFolder = "batchedCollectWork"
    storageFolder = "../../analResult/%s/" % (fatherFolder)
    with open(storageFolder+filename, 'r') as f:
        sigdict = json.load(f, object_pairs_hook=OrderedDict)
    transObjectCounter = Counter()

    if not assigObject:
        # if Objects are not assigned, select the topK
        for time in sigdict:
            # First traversals the dict to get all the distinct Object name and the corresponding count.
            for ObjectName in sigdict[time]:
                transObjectCounter[ObjectName] += sigdict[time][ObjectName]
        selectedObjects = [tup[0] for tup in transObjectCounter.most_common(topK)]
    else:
        selectedObjects = assigObject

    # Init all the values as an empty list
    transdict = dict([(obj, []) for obj in selectedObjects])
    for time in sigdict:
        for obj in selectedObjects:
            if obj in sigdict[time].keys():
                transdict[obj].append(sigdict[time][obj])
            else:
                # If Object does not exist at current time.
                transdict[obj].append(0)

    outputFoldername = "../../exchange"
    outputFile = outputFoldername + "/" + outputFilename
    with open(outputFile, 'a') as f:
        json.dump(transdict, f)


def doMultipleTrans(filenameList, outputFilename, topK=None, assigObject=None):
    """
    The <code>doSingleTrans</code> is able to handle most of the situations.
    But in some situation, we need to merge some related files and output them into one file.
    There are two different kinds of inosculations.
    First, two files store the same module but focus on different time duration.
    Second, two files focus on the same time duration but store the different modules (e.g. campus1 and campus2)
    Both these two situations need to be handled.
    Warning! the <code>doSingleTrans</code> will not check if it is legal or reasonable to inosculate two files.
    It will only do the inosculation and return the corresponding result.
    :param filename: input single filename, only the filename, no folder info
    :param outputFilename: the outputFilename
    :param topK: topK objects that wants to be translated
    :param assigObject: a list of assigned obj (if this field is assigned, topK selection becomes useless)
    :return:
    """
    fatherFolder = "batchedCollectWork"
    storageFolder = "../../analResult/%s/" % (fatherFolder)
    sigdict = OrderedDict()
    for filename in filenameList:
        with open(storageFolder+filename, 'r') as f:
            sigdict_tmp = json.load(f, object_pairs_hook=OrderedDict)
        for tmpKey in sigdict_tmp:
            if tmpKey in sigdict:
                sigdict[tmpKey] = sigdict[tmpKey] + Counter(sigdict_tmp[tmpKey])

    transObjectCounter = Counter()
    if not assigObject:
        # if Objects are not assigned, select the topK
        for time in sigdict:
            # First traversals the dict to get all the distinct Object name and the corresponding count.
            for ObjectName in sigdict[time]:
                transObjectCounter[ObjectName] += sigdict[time][ObjectName]
        selectedObjects = [tup[0] for tup in transObjectCounter.most_common(topK)]
    else:
        selectedObjects = assigObject

    # Init all the values as an empty list
    transdict = dict([(obj, []) for obj in selectedObjects])
    for time in sigdict:
        for obj in selectedObjects:
            if obj in sigdict[time].keys():
                transdict[obj].append(sigdict[time][obj])
            else:
                # If Object does not exist at current time.
                transdict[obj].append(0)

    outputFoldername = "../../exchange/"
    outputFile = outputFoldername + "/" + outputFilename
    with open(outputFile, 'a') as f:
        json.dump(transdict, f)

