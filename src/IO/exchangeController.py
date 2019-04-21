"""
" This script is used to control the <code>JSDictToExchange</code>
" This script is required to assign a/multiple proper target filename as well as one outputFilename to
" the <code>do[Single/Multiple]Trans</code>.
" By Zhengping on 2019-01-14
"""

import json
import sys
sys.path.append('/home/zhengping/DNS/DNSPythonWorkspace')
from src.IO.JSDictToExchange import doMultipleTrans, doSingleTrans
from src.IO.easyMerger import doSingleMerger

def singleController():
    moduleList = ["inakamai", "inaurora", "incampus", "incampusNew",
                  "incpsc", "inothers", "inphys", "inunknown205"]
    moduleList += ["outakamai", "outcampus1", "outcampus2",
                  "outcpsc", "outothers", "outwebpax"]

    taskList = ["%sTotalOutClusterCollFull" % module for module in moduleList]
    for taskname in taskList:
        filename = "%s.log" % taskname
        outputFilename = "%s_trans.log" % taskname
        topK = None
        assigObject = None
        doSingleTrans(filename, outputFilename, topK, assigObject)

def multipleController():
    tasknameList = []
    filenameList = []
    for taskname in tasknameList:
        filenameList.append("%s.log" % taskname)
    outputFilename = ""
    topK = None
    assigObject = None
    doMultipleTrans(filenameList, outputFilename, topK, assigObject)

def easyMergerController():
    moduleList = ["inakamai", "inaurora", "incampus", "incampusNew",
                  "incpsc", "inothers", "inphys", "inunknown205"]
    moduleList += ["outakamai", "outcampus1", "outcampus2",
                  "outcpsc", "outothers", "outwebpax"]

    taskList = ["%sTotalOutIPG" % module for module in moduleList]
    for taskname in taskList:
        filename = "%s.log" % taskname
        outputFilename = "%s_trans.log" % taskname
        topK = None
        assigObject = None
        doSingleTrans(filename, outputFilename, topK, assigObject)


if __name__ == '__main__':
    singleController()
    # multipleController()

 