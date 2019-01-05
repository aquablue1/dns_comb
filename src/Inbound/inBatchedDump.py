"""
" Read Conn, DNS and weird files
" Dump them into one integrated json file.
" By Zhengping on 2018-11-26
"""

# import sys
# sys.path.append('/home/zhengping/DNS/DNSPythonWorkSpace')
import json
import os
from src.util.FileReader import fileReader
from src.util.FileWriter import fileWriter
from src.util.DNSFieldLocMap import FieldToLoc as dnsFTL
from src.util.CONNFieldLocMap import FieldToLoc as connFTL
from src.util.WEIRDFieldLocMap import FieldToLoc as weirdFTL


def batchedDump(direction, date):
    def dictSelection(checkedIP):
        if checkedIP in CampusList:
            targetDict = campusDict
        elif checkedIP in AkamaiList:
            targetDict = akamaiDict
        elif checkedIP in CPSCList:
            targetDict = cpscDict
        elif checkedIP in Unknown205List:
            targetDict = unknown205Dict
        elif checkedIP in CampusNewList:
            targetDict = campusNewDict
        elif checkedIP in PhysList:
            targetDict = physDict
        elif checkedIP in AuroraList:
            targetDict = auroraDict
        else:
            targetDict = othersDict
        return targetDict

    print("Start date: %s" % date)
    errorLog = "../../result/error.log"
    errorOut = fileWriter(errorLog)

    connFoldername = "../../datasample/conn_%sbound/%s/" % (direction, date)
    dnsFoldername = "../../datasample/dns_%sbound/%s/" % (direction, date)
    weirdFoldername = "../../datasample/weird_%sbound/%s/" % (direction, date)


    # CLNS Lists and the corresponding IPs
    AkamaiList = ["136.159.222.244"]
    CampusList = ["136.159.1.21", "136.159.34.201"]
    CampusNewList = ["136.159.222.2", "136.159.222.10"]
    CPSCList = ["136.159.2.1", "136.159.2.4"]
    PhysList = ["136.159.51.4", "136.159.51.5", "136.159.52.10"]
    AuroraList = ["136.159.142.4", "136.159.142.5"]

    # UNS Lists
    Unknown205List = ["136.159.205.37", "136.159.205.38", "136.159.205.39"]
    # Others

    # Init CLNS related dicts
    akamaiDict = {}
    campusDict = {}
    campusNewDict = {}
    cpscDict = {}
    physDict = {}
    auroraDict = {}

    # Init UNS related dicts
    unknown205Dict = {}
    othersDict = {}
    for hour in range(0, 1):
        print("Start task: %s" % hour)

        hour = str(hour).zfill(2)
        connFilename = connFoldername + "%s_%s.log" % (date, hour)
        dnsFilename = dnsFoldername + "%s_%s.log" % (date, hour)
        weirdFilename = weirdFoldername + "%s_%s.log" % (date, hour)

        # handle all conn logs and init all the structures.
        connfile = fileReader(connFilename)
        for line in connfile:
            line_list = line.strip().split("\t")
            uid = line_list[connFTL["uid"]]
            checkedIP = line_list[connFTL["dstIP"]]
            # get the proper dict to store this info
            targetDict = dictSelection(checkedIP)
            targetDict[uid] = {"ts"   : line_list[connFTL["timestamp"]],
                                "addr" : (line_list[connFTL["srcIP"]],
                                       line_list[connFTL["srcPort"]],
                                       line_list[connFTL["dstIP"]],
                                       line_list[connFTL["dstPort"]]),
                                "conn" : None,
                                "dns"  : None,
                                "weird": None
                                }
            connList = [line_list[connFTL["duration"]], line_list[connFTL["sentByte"]],
                        line_list[connFTL["recvByte"]], line_list[connFTL["endFlag"]]]
            if targetDict[uid]["conn"]:
                print("duplicated uid! date:%s_%s, uid=%s" % (date, hour, uid))
            else:
                targetDict[uid]["conn"] = connList

        # handle all the dns files
        dnsfile = fileReader(dnsFilename)
        for line in dnsfile:
            line_list = line.strip().split("\t")
            uid = line_list[connFTL["uid"]]
            checkedIP = line_list[dnsFTL["dstIP"]]
            targetDict = dictSelection(checkedIP)
            dnsList = [line_list[dnsFTL["transID"]], line_list[dnsFTL["rtt"]],
                       line_list[dnsFTL["query"]], line_list[dnsFTL["answers"]],
                       line_list[dnsFTL["ttls"]], line_list[dnsFTL["type"]],
                       line_list[dnsFTL["error"]]]
            try:
                if not targetDict[uid]["dns"]:
                    targetDict[uid]["dns"] = []
                targetDict[uid]["dns"].append(dnsList)
            except KeyError as keyE:
                errorOut.writeString("DNS UID Not Found: %s.\n" % uid)
        # handle all the weird files
        weirdfile = fileReader(weirdFilename)
        for line in weirdfile:
            line_list = line.strip().split("\t")
            uid = line_list[connFTL["uid"]]
            checkedIP = line_list[dnsFTL["dstIP"]]
            targetDict = dictSelection(checkedIP)
            weirdList = [line_list[weirdFTL["weirdName"]], line_list[weirdFTL["addl"]],
                         line_list[weirdFTL["notice"]], line_list[weirdFTL["peer"]]]
            try:
                if not targetDict[uid]["weird"]:
                    targetDict[uid]["weird"] = []
                targetDict[uid]["weird"].append(weirdList)
            except KeyError as keyE:
                errorOut.writeString("Weird UID Not Found: %s.\n" % uid)
        print("Finish task: %s" % hour)

        print("Start dump: %s\n" %date)

        # output all the dicts as json file.
        outputilename = "%s_%s.log" % (date, hour)
        akamaiOutputFolder = "../../result/akamai/%s/" % (date)
        if not os.path.exists(akamaiOutputFolder):
            os.makedirs(akamaiOutputFolder)
        with open(akamaiOutputFolder+outputilename, 'a') as f:
            json.dump(akamaiDict, f)

        campusOutputFolder = "../../result/campus/%s/" % (date)
        if not os.path.exists(campusOutputFolder):
            os.makedirs(campusOutputFolder)
        with open(campusOutputFolder+outputilename, 'a') as f:
            json.dump(campusDict, f)

        campusNewOutputFolder = "../../result/campusNew/%s/" % (date)
        if not os.path.exists(campusNewOutputFolder):
            os.makedirs(campusNewOutputFolder)
        with open(campusNewOutputFolder+outputilename, 'a') as f:
            json.dump(campusNewDict, f)

        cpscOutputFolder = "../../result/cpsc/%s/" % (date)
        if not os.path.exists(cpscOutputFolder):
            os.makedirs(cpscOutputFolder)
        with open(cpscOutputFolder+outputilename, 'a') as f:
            json.dump(cpscDict, f)

        physOutputFolder = "../../result/phys/%s/" % (date)
        if not os.path.exists(physOutputFolder):
            os.makedirs(physOutputFolder)
        with open(physOutputFolder+outputilename, 'a') as f:
            json.dump(physDict, f)

        auroraOutputFolder = "../../result/aurora/%s/" % (date)
        if not os.path.exists(auroraOutputFolder):
            os.makedirs(auroraOutputFolder)
        with open(auroraOutputFolder+outputilename, 'a') as f:
            json.dump(auroraDict, f)

        unknown205OutputFolder = "../../result/unknown205/%s/" % (date)
        if not os.path.exists(unknown205OutputFolder):
            os.makedirs(unknown205OutputFolder)
        with open(unknown205OutputFolder+outputilename, 'a') as f:
            json.dump(unknown205Dict, f)

        othersOutputFolder = "../../result/others/%s/" % (date)
        if not os.path.exists(othersOutputFolder):
            os.makedirs(othersOutputFolder)
        with open(othersOutputFolder+outputilename, 'a') as f:
            json.dump(othersDict, f)


if __name__ == '__main__':
    date = "2018-09-01"
    direction = "in"
    batchedDump(direction, date)

