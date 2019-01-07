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

class batchedWorker():
    def __init__(self, targetList, taskname, outputname):
        self.targetList = targetList
        self.taskname = taskname
        self.staticCount = {}
        self.outputname = outputname

    def getTargetFolderList(self, start=0, end=0):
        targetFolderList = []
        repository = "result"
        for target in self.targetList:
            targetFatherFolder = "../../%s/%s" % (repository, target)
            fatherFolder = folderReader(targetFatherFolder)
            for folder in fatherFolder:
                print(folder)
                # add range control (start, end) here if necessary.
                targetFolderList.append(folder)
        targetFolderList.sort()
        return targetFolderList

    def getTargetFileList(self, foldername):
        targetFileList = []
        targetFolder = folderReader(foldername)
        for filename in targetFolder:
            targetFileList.append(filename)
        targetFileList.sort()
        return targetFileList

    def actWorker(self, filename):
        module = importlib.import_module("src.integUtil.%s" % (self.taskname))
        func = getattr(module, "doTask")
        static = func(filename)
        datetimeKey = filename.split("/")[-1].split(".")[0]
        try:
            self.staticCount[datetimeKey] = [a+b for a, b in zip(self.staticCount[datetimeKey], static)]
        except KeyError:
            self.staticCount[datetimeKey] = static
        targetname = filename.split("/")[-3] # influenced by line: 28
        print("Job Done %s: %s===%s" % (self.taskname, targetname, datetimeKey))

    def dump(self):
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


if __name__ == '__main__':
    bworker = batchedWorker([sys.argv[1]], "worker0Test", "test")
    foldlist = bworker.getTargetFolderList()
    print(bworker.getTargetFileList(foldlist[0]))
    for fold in foldlist:
        fileList = bworker.getTargetFileList(fold)
        for filename in fileList:
            bworker.actWorker(filename)
    # bworker.dump()
