"""
" Warning! This is a one-time runnable script!
" Used to collect and cluster the distinct weird type in different module and different OuterHost at different time.
" By Zhengping on 2019-01-16
"""


import sys
# sys.path.append('/home/zhengping/DNS/DNSPythonWorkspace')
from src.util.FileReader import fileReader
from src.util.FileWriter import fileWriter
from src.util.FolderReader import folderReader
from src.util.IPCluster import getIPCluster

import importlib
import datetime
import json

class batchedWorker():
    def __init__(self, targetList, taskname, outputname):
        self.targetList = targetList
        self.taskname = taskname
        self.staticCount = {}
        self.staticCollector = {}
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

    def actLevel2CollectWorker(self, filename):
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
        staticDict = doLevel2CollectTask(filename)
        datetimeKey = filename.split("/")[-1].split(".")[0]
        # try:
        #     self.staticCollector[datetimeKey] += static
        # except KeyError:
        self.staticCollector[datetimeKey] = staticDict
        targetname = filename.split("/")[-3] # influenced by line: targetFatherFolder = "../../%s/%s" % (repository, target)
        print("Job Done %s: %s===%s" % (self.taskname, targetname, datetimeKey))

    def dumpLevel2Collector(self):
        outputFilename = "../../analResult/batchedLevel2CollectWork/%s.log" % (self.outputname)
        with open(outputFilename, 'a') as f:
            json.dump(self.staticCollector, f)
        currentDT = datetime.datetime.now()
        print("All Job Done: %s. At: %s" % (self.taskname, str(currentDT)))


def doLevel2CollectTask(filename):
    """
    Collect the topK result from filename
    :param filename: target filename
    :param topK: topK wants to select, by default is None.
    :return: top K count result.
    """
    Type0 = "dns_unmatched_msg"
    Type1 = "dns_unmatched_reply"
    Type2 = "DNS_RR_unknown_type"
    f = open(filename)
    dataDict = json.load(f)
    weirdByteCollect = {}
    for key in dataDict:
        if dataDict[key]["weird"]:
            # Check direction first to get the inner server.
            # Check direction first to get the inner server.
            srcIP = dataDict[key]["addr"][0]
            dstIP = dataDict[key]["addr"][2]
            for weird in dataDict[key]["weird"]:
                if weird[0] == "dns_unmatched_reply":
                    print(dataDict[key])
            if srcIP.startswith("136.159."):
                # Which means srcIP is within our campus. it should be an outbound traffic
                # Get the InByte First.
                byte = dataDict[key]["conn"][2]

                # print(dataDict[key])
                try:
                    weirdByteCollect[getIPCluster(dstIP)].append(byte)
                except KeyError:
                    weirdByteCollect[getIPCluster(dstIP)] = []
                    weirdByteCollect[getIPCluster(dstIP)].append(byte)
            else:
                byte = dataDict[key]["conn"][1]
                try:
                    weirdByteCollect[getIPCluster(srcIP)].append(byte)
                except KeyError:
                    weirdByteCollect[getIPCluster(srcIP)] = []
                    weirdByteCollect[getIPCluster(dstIP)].append(byte)
    print(weirdByteCollect)
    return weirdByteCollect

def collectorController():
    targetList = ["inakamai", "inaurora", "incampus", "incampusNew",
                  "incpsc", "inothers", "inphys", "inunknown205"]

    targetList += ["outakamai", "outcampus1", "outcampus2",
                  "outcpsc", "outothers", "outwebpax"]

    targetList = ["outcampus1"]

    for target in targetList:
        taskname = "worker2D6WeirdByteClusterG"
        outputname = "%sWeirdPopTypeClusterCollTest" % (target)

        bworker = batchedWorker([target], taskname, outputname)
        foldlist = bworker.getTargetFolderList("2018-09-01", "2018-09-02")
        # print(bworker.getTargetFileList(foldlist[0]))
        for fold in foldlist:
            fileList = bworker.getTargetFileList(fold)
            for filename in fileList:
                bworker.actLevel2CollectWorker(filename)
        bworker.dumpLevel2Collector()


if __name__ == '__main__':
    # counterColtroller()
    collectorController()
    print("Job Done! EXIT()")

