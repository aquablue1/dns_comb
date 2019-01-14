"""
" This script is used to control the <code>JSDictToExchange</code>
" This script is required to assign a/multiple proper target filename as well as one outputFilename to
" the <code>do[Single/Multiple]Trans</code>.
" By Zhengping on 2019-01-14
"""

import json
import sys
sys.path.append('/home/zhengping/DNS/DNSPythonWorkspace')
from src.IO.JSDictToExchange import doMultipleTrans,doSingleTrans

def singleController():
    taskname = ""
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

if __name__ == '__main__':
    singleController()
    # multipleController()