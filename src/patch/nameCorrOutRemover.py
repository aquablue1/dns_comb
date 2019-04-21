"""
" In the first version of outbound generation script, the all the output files have the prefix
" "out_", which make them not consist with inbound logs. The goal of this patch is to remove these
" prefix, i.e. remove all "out_" from filename
"""

import sys
sys.path.append('/home/zhengping/DNS/DNSPythonWorkspace')
import os
from src.util.FolderReader import folderReader


def doMove(filename):
    if "out_" in filename:
        newfname = filename.replace("out_", "")
        os.rename(filename, newfname)
        return True
    return False

def doGroupRemove(foldername):
    folder = folderReader(foldername)
    for filename in folder:
        doMove(filename)

def doModuleRemove(moduleName):
    moduleFoldername = "../../result/%s/" % (moduleName)
    mfolder = folderReader(moduleFoldername)
    for ffolder in mfolder:
        doGroupRemove(ffolder)

if __name__ == '__main__':
    moduleName = "akamaiOut"
    doModuleRemove(moduleName)
