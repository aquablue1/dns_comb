"""
" Control all the workers
"""

import sys
sys.path.append('/home/zhengping/DNS/DNSPythonWorkspace')
from src.integUtil.batchedWorker import batchedWorker


def collectorController():
    targetList = ["inakamai", "inaurora", "incampus", "incampusNew",
                  "incpsc", "inothers", "inphys", "inunknown205"]

    targetList += ["outakamai", "outcampus1", "outcampus2",
                  "outcpsc", "outothers", "outwebpax"]

    for target in targetList:
        taskname = "worker2D1WeirdIn"
        outputname = "%sWeirdInCollTen" % (target)

        bworker = batchedWorker([targetList], taskname, outputname)
        foldlist = bworker.getTargetFolderList("2018-09-01", "2018-09-11")
        # print(bworker.getTargetFileList(foldlist[0]))
        for fold in foldlist:
            fileList = bworker.getTargetFileList(fold)
            for filename in fileList:
                bworker.actCollectWorker(filename)
        bworker.dumpCollector()


def counterColtroller():
    # Test tasklist
    targetList = ["inphys"]
    # Inbound global taskList
    # targetList = ["inakamai", "inaurora", "incampus", "incampusNew",
    #               "incpsc", "inothers", "inphys", "inunknown205"]
    # # Outbound global taskList
    # targetList = ["outakamai", "outcampus1", "outcampus2",
    #               "outcpsc", "outothers", "outwebpax"]
    #
    # task0 tuple
    taskname = "worker0Test"
    outputname = "test"
    #
    # # task1 tuple
    # taskname = "worker1Direction"
    # outputname = "directionG" # G indicates global
    #
    # # task2 tuple Warning! issue with this task!
    # taskname = "worker2Weird"
    # outputname = "weirdG"
    #
    # # task3 tuple
    # taskname = "worker3ReturnMsg"
    # outputname = "retMsgG"
    #
    # # task4 tuple
    # taskname = "worker4Response"
    # outputname = "responseG"
    #
    # User Define Field:


    bworker = batchedWorker(targetList, taskname, outputname)
    foldlist = bworker.getTargetFolderList("2018-09-01", "2018-09-11")
    # print(bworker.getTargetFileList(foldlist[0]))
    for fold in foldlist:
        fileList = bworker.getTargetFileList(fold)
        for filename in fileList:
            bworker.actCountWorker(filename)
    bworker.dumpCount()


def transController():
    targetList = ["inakamai", "inaurora", "incampus", "incampusNew",
                  "incpsc", "inothers", "inphys", "inunknown205"]

    targetList += ["outakamai", "outcampus1", "outcampus2",
                  "outcpsc", "outothers", "outwebpax"]

    for target in targetList:
        taskname = "worker8D1TransPopT"
        outputname = "%sTransPop1000T" % (target)

        bworker = batchedWorker([targetList], taskname, outputname)
        foldlist = bworker.getTargetFolderList("2018-09-01", "2018-09-02")
        # print(bworker.getTargetFileList(foldlist[0]))
        for fold in foldlist:
            fileList = bworker.getTargetFileList(fold)
            for filename in fileList:
                bworker.actTransWorker(filename)
        bworker.dumpTrans()



if __name__ == '__main__':
    # counterColtroller()
    # collectorController()
    transController()
    print("Job Done! EXIT()")
