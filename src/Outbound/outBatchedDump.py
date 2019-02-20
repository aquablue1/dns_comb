"""
" Read Conn, DNS and weird files
" Dump them into one integrated json file.
" Divide them into
" campus1 (136.159.222.2),
" campus2 (136.159.222.10),
" akamai (136.159.222.244),
" cpsc (136.159.5.75, 136.159.5.76)
" webpax (136.159.190.37) and
" others.
" By Zhengping on 2019-01-05
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
        if checkedIP in Campus1List:
            targetDict = campus1Dict
        elif checkedIP in Campus2List:
            targetDict = campus2Dict
        elif checkedIP in AkamaiList:
            targetDict = akamaiDict
        elif checkedIP in CPSCList:
            targetDict = cpscDict
        elif checkedIP in WebpaxList:
            targetDict = webpaxDict

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
    Campus1List = ["136.159.222.2"]
    Campus2List = ["136.159.222.10"]
    CPSCList = ["136.159.5.75", "136.159.5.76"]
    WebpaxList = ["136.159.190.37"]

    # Others

    for hour in range(0, 24):

        # Init CLNS related dicts
        akamaiDict = {}
        campus1Dict = {}
        campus2Dict = {}
        cpscDict = {}
        webpaxDict = {}

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
            checkedIP = line_list[connFTL["srcIP"]]
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
        dnsfile = fileReader(dnsFilename)
        for line in dnsfile:
            line_list = line.strip().split("\t")
            uid = line_list[dnsFTL["uid"]]
            checkedIP = line_list[dnsFTL["srcIP"]]
            targetDict = dictSelection(checkedIP)
            dnsList = [line_list[dnsFTL["transID"]], line_list[dnsFTL["rtt"]],
                       line_list[dnsFTL["query"]], line_list[dnsFTL["answers"]],
                       line_list[dnsFTL["ttls"]], line_list[dnsFTL["type"]],
                       line_list[dnsFTL["error"]]]
            try:
                if not targetDict[uid]["dns"]:
                    targetDict[uid]["dns"] = []
                    targetDict[uid]["dns"].append(dnsList)
                else:
                    # Remove duplicated dns traces.
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
            checkedIP = line_list[weirdFTL["srcIP"]]
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
        akamaiOutputFolder = "../../structNew/outakamai/%s/" % (date)
        if not os.path.exists(akamaiOutputFolder):
            os.makedirs(akamaiOutputFolder)
        with open(akamaiOutputFolder+outputilename, 'a') as f:
            json.dump(akamaiDict, f)

        campus1OutputFolder = "../../structNew/outcampus1/%s/" % (date)
        if not os.path.exists(campus1OutputFolder):
            os.makedirs(campus1OutputFolder)
        with open(campus1OutputFolder+outputilename, 'a') as f:
            json.dump(campus1Dict, f)

        campus2OutputFolder = "../../structNew/outcampus2/%s/" % (date)
        if not os.path.exists(campus2OutputFolder):
            os.makedirs(campus2OutputFolder)
        with open(campus2OutputFolder+outputilename, 'a') as f:
            json.dump(campus2Dict, f)

        cpscOutputFolder = "../../structNew/outcpsc/%s/" % (date)
        if not os.path.exists(cpscOutputFolder):
            os.makedirs(cpscOutputFolder)
        with open(cpscOutputFolder+outputilename, 'a') as f:
            json.dump(cpscDict, f)

        webpaxOutputFolder = "../../structNew/outwebpax/%s/" % (date)
        if not os.path.exists(webpaxOutputFolder):
            os.makedirs(webpaxOutputFolder)
        with open(webpaxOutputFolder+outputilename, 'a') as f:
            json.dump(webpaxDict, f)

        othersOutputFolder = "../../structNew/outothers/%s/" % (date)
        if not os.path.exists(othersOutputFolder):
            os.makedirs(othersOutputFolder)
        with open(othersOutputFolder+outputilename, 'a') as f:
            json.dump(othersDict, f)

    errorOut.close()


if __name__ == '__main__':
    dateList = ["2018-09-%s" % str(d).zfill(2) for d in range(1, 11)]
    for date in dateList:
        _DIRECTION = "out"
        batchedDump(_DIRECTION, date)
