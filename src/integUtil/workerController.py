"""
" Control all the workers
"""

import sys
sys.path.append('/home/zhengping/DNS/DNSPythonWorkspace')
from src.integUtil.batchedWorker import batchedWorker

if __name__ == '__main__':
    # Test tasklist
    targetList = ["phys"]
    # # Inbound global taskList
    # targetList = ["akamai", "aurora", "campus", "campusNew", "cpsc", "others", "phys", "unknown205"]
    # # Outbound global taskList
    # targetList = ["akamaiOut", "campus1Out", "campus2Out", "cpscOut", "othersOut", "webpaxOut"]
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
    # outputname = "weordG"
    #
    # # task3 tuple
    # taskname = "worker3ReturnMsg"
    # outputname = "retMsgG"
    #
    # # task4 tuple
    # taskname = "worker4Response"
    # outputname = "responseG"

    bworker = batchedWorker(targetList, taskname, outputname)
    foldlist = bworker.getTargetFolderList()
    # print(bworker.getTargetFileList(foldlist[0]))
    for fold in foldlist:
        fileList = bworker.getTargetFileList(fold)
        for filename in fileList:
            bworker.actWorker(filename)



