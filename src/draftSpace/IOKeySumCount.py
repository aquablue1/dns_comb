"""
" Only usd to handle the files in exchange spaces.
" It is required that input is a json file, with each value as a list.
" all elements in the value list should be integer.
" The purpose of this script is to sum up the total numbers in this dict to get a Counter
" and dump it into a new JSON.
" By Zhegnping on 2019-01-24.
"""

from collections import Counter, OrderedDict
import json


def doKeySum(taskname, filename):
    fullFilename = "../../exchange/%s/%s.log" % (taskname, filename)

    with open(fullFilename, "r") as f:
        ioDict = json.load(f)

    sumDict = Counter()
    for key in ioDict:
        for val in ioDict[key]:
            sumDict[key] += val

    outputfilename = filename + "_sum"
    fullOutputFilename = "../../exchange/sumup/%s.log" % (outputfilename)
    with open(fullOutputFilename, 'w') as f:
        json.dump(sumDict, f)


def sumUpToLatex(filename, weirdFilename):
    """
    Print the result in latex table format to show in latex file.
    :param filename: sumUP Filename
    :return: None
    """
    fullFilename = "../../exchange/sumup/%s.log" % filename
    with open(fullFilename, 'r') as f:
        sumDict = Counter(json.load(f))
    fullWeirdFilename = "../../exchange/sumup/%s.log" % weirdFilename
    with open(fullWeirdFilename, 'r') as f:
        sumWeirdDict = Counter(json.load(f))
    index = 1
    for ele in sumDict.most_common(20):
        key = ele[0]
        val = ele[1]
        try:
            valWeird = sumWeirdDict[key]
        except KeyError:
            valWeird = 0
        weirdPercent = "{:.1%}".format(valWeird/val)
        weirdPercent = weirdPercent.replace("%", "\\%")
        print("%d\t& %s\t& %s\t& %s\t& %s\t \\\\ \hline" %
              (index, key, "{:,}".format(val),"{:,}".format(valWeird), weirdPercent))
        index += 1


if __name__ == '__main__':
    taskname = "ORG"
    modulename = "outothers"
    filename = "%sTotalOutORGCGTotal_trans" % modulename
    weirdFilename = "%sWeirdOutORGCGTotal_trans" % modulename
    doKeySum(taskname, filename)
    doKeySum(taskname, weirdFilename)
    sumUpToLatex(filename + "_sum", weirdFilename + "_sum")
