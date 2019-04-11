"""
" Read Conn, DNS and weird files
" Dump them into one integrated json file.
" By Zhengping on 2018-11-26
" Updated on 2019-03-25
"""

import sys
sys.path.append('/home/zhengping/DNS/DNSPythonWorkspace')
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

    connFoldername = "../../data/conn_%sbound/%s/" % (direction, date)
    dnsFoldername = "../../data/dns_%sbound/%s/" % (direction, date)
    weirdFoldername = "../../data/weird_%sbound/%s/" % (direction, date)


    # CLNS Lists and the corresponding IPs
    AkamaiList = ["136.159.222.244"]
    CampusList = ["136.159.1.21", "136.159.34.201"]
    CampusNewList = ["136.159.222.2", "136.159.222.10"]
    CPSCList = ["136.159.2.1", "136.159.2.4"]
    PhysList = ["136.159.51.4", "136.159.51.5", "136.159.52.6", "136.159.52.10", "136.159.52.164"]
    AuroraList = ["136.159.142.4", "136.159.142.5"]

    # UNS Lists
    Unknown205List = ["136.159.205.37", "136.159.205.38", "136.159.205.39"]
    # Others


    for hour in range(0, 24):
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
                        line_list[connFTL["recvByte"]], line_list[connFTL["endFlag"]],
                        line_list[connFTL["ipSentByte"]], line_list[connFTL["ipSentPack"]],
                        line_list[connFTL["ipRecvByte"]], line_list[connFTL["ipRecvPack"]]]
            if targetDict[uid]["conn"]:
                print("duplicated uid! date:%s_%s, uid=%s" % (date, hour, uid))
            else:
                targetDict[uid]["conn"] = connList

        # handle all the dns files
        # Done: Urgent! need to add the duplication avoidance plugin here to avoid the duplication problem.
        # The duplication can be checked by verify the transID field. However, this might affect some
        # DNS retransmission msgs, but since the retransmission is limited in number. This approach should
        # be acceptable.
        dnsfile = fileReader(dnsFilename)
        for line in dnsfile:
            line_list = line.strip().split("\t")
            uid = line_list[dnsFTL["uid"]]
            checkedIP = line_list[dnsFTL["dstIP"]]
            targetDict = dictSelection(checkedIP)
            dnsList = [line_list[dnsFTL["transID"]], line_list[dnsFTL["rtt"]],
                       line_list[dnsFTL["query"]], line_list[dnsFTL["answers"]],
                       line_list[dnsFTL["ttls"]], line_list[dnsFTL["type"]],
                       line_list[dnsFTL["error"]], line_list[dnsFTL["AA"]],
                       line_list[dnsFTL["TC"]], line_list[dnsFTL["RD"]],
                       line_list[dnsFTL["RA"]], line_list[dnsFTL["rejected"]]]
            try:
                if not targetDict[uid]["dns"]:
                    targetDict[uid]["dns"] = []
                # Done: add transID check here to avoid the duplication.
                    targetDict[uid]["dns"].append(dnsList)
                else:
                    existTIDList = [dnsr[0] for dnsr in targetDict[uid]["dns"]]
                    tID = dnsList[0]
                    if tID not in existTIDList:
                        targetDict[uid]["dns"].append(dnsList)

            except KeyError as keyE:
                # errorOut.writeString("DNS UID Not Found: %s.\n" % uid)
                pass
        # handle all the weird files
        weirdfile = fileReader(weirdFilename)
        for line in weirdfile:
            line_list = line.strip().split("\t")
            uid = line_list[weirdFTL["uid"]]
            checkedIP = line_list[weirdFTL["dstIP"]]
            targetDict = dictSelection(checkedIP)
            weirdList = [line_list[weirdFTL["weirdName"]], line_list[weirdFTL["addl"]],
                         line_list[weirdFTL["notice"]], line_list[weirdFTL["peer"]]]
            try:
                if not targetDict[uid]["weird"]:
                    targetDict[uid]["weird"] = []
                targetDict[uid]["weird"].append(weirdList)
            except KeyError as keyE:
                # errorOut.writeString("Weird UID Not Found: %s.\n" % uid)
                pass
        print("Finish task: %s" % hour)

        print("Start dump: %s\n" %date)

        # output all the dicts as json file.
        outputilename = "%s_%s.log" % (date, hour)
        akamaiOutputFolder = "../../structNewNew/inakamai/%s/" % (date)
        if not os.path.exists(akamaiOutputFolder):
            os.makedirs(akamaiOutputFolder)
        with open(akamaiOutputFolder+outputilename, 'a') as f:
            json.dump(akamaiDict, f)

        campusOutputFolder = "../../structNewNew/incampus/%s/" % (date)
        if not os.path.exists(campusOutputFolder):
            os.makedirs(campusOutputFolder)
        with open(campusOutputFolder+outputilename, 'a') as f:
            json.dump(campusDict, f)

        campusNewOutputFolder = "../../structNewNew/incampusNew/%s/" % (date)
        if not os.path.exists(campusNewOutputFolder):
            os.makedirs(campusNewOutputFolder)
        with open(campusNewOutputFolder+outputilename, 'a') as f:
            json.dump(campusNewDict, f)

        cpscOutputFolder = "../../structNewNew/incpsc/%s/" % (date)
        if not os.path.exists(cpscOutputFolder):
            os.makedirs(cpscOutputFolder)
        with open(cpscOutputFolder+outputilename, 'a') as f:
            json.dump(cpscDict, f)

        physOutputFolder = "../../structNewNew/inphys/%s/" % (date)
        if not os.path.exists(physOutputFolder):
            os.makedirs(physOutputFolder)
        with open(physOutputFolder+outputilename, 'a') as f:
            json.dump(physDict, f)

        auroraOutputFolder = "../../structNewNew/inaurora/%s/" % (date)
        if not os.path.exists(auroraOutputFolder):
            os.makedirs(auroraOutputFolder)
        with open(auroraOutputFolder+outputilename, 'a') as f:
            json.dump(auroraDict, f)

        unknown205OutputFolder = "../../structNewNew/inunknown205/%s/" % (date)
        if not os.path.exists(unknown205OutputFolder):
            os.makedirs(unknown205OutputFolder)
        with open(unknown205OutputFolder+outputilename, 'a') as f:
            json.dump(unknown205Dict, f)

        othersOutputFolder = "../../structNewNew/inothers/%s/" % (date)
        if not os.path.exists(othersOutputFolder):
            os.makedirs(othersOutputFolder)
        with open(othersOutputFolder+outputilename, 'a') as f:
            json.dump(othersDict, f)


if __name__ == '__main__':
    dateList = ["2018-09-%s" % str(d).zfill(2) for d in range(1, 11)]
    for date in dateList:
        # Warning! direction is fixed as “IN” here.
        _DIRECTION = "in"
        batchedDump(_DIRECTION, date)
