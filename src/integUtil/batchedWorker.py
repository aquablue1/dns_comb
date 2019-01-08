"""
" Batched worker, used to analysis data in batched manner
" accept a list of targets, a task and an output path.
" output the analysis result into output path.
"""


import sys
sys.path.append('/home/zhengping/DNS/DNSPythonWorkspace')
from src.util.FileReader import fileReader
from src.util.FileWriter import fileWriter
from src.util.FolderReader import folderReader
from src.util.IsFileExist import isFileExist
import os
import importlib
import datetime
from datetime import time
from collections import Counter
import json

class batchedWorker():
    def __init__(self, targetList, taskname, outputname):
        self.targetList = targetList
        self.taskname = taskname
        self.staticCount = {}
        self.staticCollector = Counter()
        self.outputname = outputname

    def getTargetFolderList(self, start="2015-01-01", end="2100-12-31"):
        targetFolderList = []
        repository = "struct"
        dateStart = datetime.datetime(int(start.split("-")[0]),
                                      int(start.split("-")[1]),
                                      int(start.split("-")[2]))
        dateEnd = datetime.datetime(int(end.split("-")[0]),
                                      int(end.split("-")[1]),
                                      int(end.split("-")[2]))
        for target in self.targetList:
            targetFatherFolder = "../../%s/%s" % (repository, target)
            fatherFolder = folderReader(targetFatherFolder)
            for folder in fatherFolder:
                # print(folder)
                dateCurStr = folder.split("/")[-1]
                dateCur = datetime.datetime(int(dateCurStr.split("-")[0]),
                                            int(dateCurStr.split("-")[1]),
                                            int(dateCurStr.split("-")[2]))
                if dateStart <= dateCur < dateEnd:
                    # add range control (start, end) here if necessary.
                    targetFolderList.append(folder)
                else:
                    # ignore those not in the target range
                    pass
        targetFolderList.sort()
        return targetFolderList

    def getTargetFileList(self, foldername):
        targetFileList = []
        targetFolder = folderReader(foldername)
        for filename in targetFolder:
            targetFileList.append(filename)
        targetFileList.sort()
        return targetFileList

    def actCountWorker(self, filename):
        module = importlib.import_module("src.integUtil.%s" % (self.taskname))
        func = getattr(module, "doCountTask")
        static = func(filename)
        datetimeKey = filename.split("/")[-1].split(".")[0]
        try:
            self.staticCount[datetimeKey] = [a+b for a, b in zip(self.staticCount[datetimeKey], static)]
        except KeyError:
            self.staticCount[datetimeKey] = static
        targetname = filename.split("/")[-3] # influenced by line: targetFatherFolder = "../../%s/%s" % (repository, target)
        print("Job Done %s: %s===%s" % (self.taskname, targetname, datetimeKey))

    def dumpCount(self):
        outputFilename = "../../analResult/batchedWork/%s.log" % (self.outputname)
        outputF = fileWriter(outputFilename)
        for key in self.staticCount.keys():
            valuestr = ""
            for value in self.staticCount[key]:
                valuestr += "%d\t" % (value)
            outputF.writeString("%s\t%s\n" % (key, valuestr))
        outputF.close()
        currentDT = datetime.datetime.now()
        print("All Job Done: %s. At: %s" % (self.taskname, str(currentDT)))


    def actCollectWorker(self, filename, topK=None):
        """
        " Define the behavior of a collector here
        " Unlike the counter which only returns the static result (count)
        " The collector records both infomation and its counter, in the format of a dict.
        " It calls all the collect workers with has a capital letter G as the end in their module names.
        " Since the counter is used. In order to reduce the output size, another parameter topK is used
        " To control top-K result from output.
        " the output is a collector dict. which hires the date as key and top-k dict as value.
        :param filename: the target filename
        :param topK: topK result that want to collect from target filename.
        :return: a collector dict which stored as a global parameter, i.e. self.staticCollector
        """
        module = importlib.import_module("src.integUtil.%s" % (self.taskname))
        func = getattr(module, "doCollectTask")
        static = func(filename, topK)
        datetimeKey = filename.split("/")[-1].split(".")[0]
        try:
            self.staticCollector[datetimeKey] += static
        except KeyError:
            self.staticCount[datetimeKey] = static
        targetname = filename.split("/")[-3] # influenced by line: targetFatherFolder = "../../%s/%s" % (repository, target)
        print("Job Done %s: %s===%s" % (self.taskname, targetname, datetimeKey))

    def dumpCollector(self):
        outputFilename = "../../analResult/batchedCollectWork/%s.log" % (self.outputname)
        with open(outputFilename, 'a') as f:
            json.dump(self.staticCollector, f)
        currentDT = datetime.datetime.now()
        print("All Job Done: %s. At: %s" % (self.taskname, str(currentDT)))


if __name__ == '__main__':
    bworker = batchedWorker([sys.argv[1]], "worker0Test", "test")
    foldlist = bworker.getTargetFolderList()
    print(bworker.getTargetFileList(foldlist[0]))
    for fold in foldlist:
        fileList = bworker.getTargetFileList(fold)
        for filename in fileList:
            bworker.actCountWorker(filename)
    # bworker.dump()
