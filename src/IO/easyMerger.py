"""
" Merge all the values from one JSON file.
" It is required that input file is a json file, which stores two-levels of dict, the key of the first level (outer)
" level should be the date_time, the second level must be a Counter so that add method can be used.
" The method will return the transferred result into a json file.
" By Zhengping on 2019-01-21
"""

import json
from collections import Counter

def doSingleMerger(filename, outputFilename):
    fatherFolder = "batchedCollectWork"
    storageFolder = "../../analResult/%s/" % (fatherFolder)
    fullfilename = storageFolder + filename
    with open(fullfilename, 'r') as f:
        sigMergerDict = json.load(f)

    overallCounter = Counter()
    for date_time in sigMergerDict:
        overallCounter += sigMergerDict[date_time]

    outputFoldername = "../../exchange"
    outputFile = outputFoldername + "/" + outputFilename
    with open(outputFile, 'a') as f:
        json.dump(overallCounter, f)
