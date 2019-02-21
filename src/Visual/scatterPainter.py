"""
" Draft version for timePlot
" Used for simple and random tasks
" By Zhengping on 2019-01-17
"""

import sys
import os
import json
import matplotlib.pyplot as plt
import math
import numpy as np
from src.util.AutoCorr import getAutoCorr
from src.util.CoeffVar import getCoeffVar



class timePlot():
    def __init__(self, filename, logRequ=False):
        # read the filename from exchange/***
        self.filename = filename
        self.rawdata = self._load()
        self.logRequ = logRequ
        # self.fig = plt.figure(figsize=(100, 120))

    def _load(self):
        with open(self.filename, 'r') as f:
            rawData = json.load(f)
        return rawData

    def _ydataExtract(self, objectName):
        """
        Extract the data which is used to draw plot.
        One call of _ydataExcract will return a list of y-axis data which can be used to draw the plot directly
        i.e. the return value should be able to be sent to the plt.plot method directly.
        No further execution is required.
        If multiple plots in one graph is required, each plot requires one call of this method to get
        its corresponding y data.
        :param objectName: The name of target object, should be simply one of the keyword from self.rowdata
        :return: y data as a list which can be used to draw the plot.
        """
        try:
            return self.rawdata[objectName]
        except KeyError:
            return None

    def _ydataExtractG(self, objectList):
        """
        Extract the data which is used to draw plot.
        This method is very similar with <code>_ydataExtract</code> except that this method accept a list of objects
        instead of only one.
        :param objectList: a list of the name of target object
        :return: y data as a list which can be used to draw the plot.
        """
        if objectList == "all":
            objectList = list(self.rawdata.keys())
        summarydata = None
        # objectList = list(self.rawdata.keys())[i:i+1]
        self.objname = objectList[0]
        print(objectList)
        for objectName in objectList:
            tmpdata = self._ydataExtract(objectName)
            if summarydata and tmpdata:
                summarydata = [x+y for x, y in zip(summarydata, tmpdata)]
            elif tmpdata:
                summarydata = tmpdata
            else:
                summarydata = summarydata

        if summarydata:
            if self.logRequ:
                return [math.log10(data+0.1) for data in summarydata]
            else:
                return summarydata
        else:
            return None

    def doDrawPlot(self, objectList, label, color, linestyle):
        ydata = self._ydataExtractG(objectList)
        if not ydata:
            return None
        xdata = list(range(1, len(ydata)+1))

        if not label:
            label = self.objname
        plt.plot(xdata, ydata, label=label, color=color, linestyle=linestyle)

    def setParams(self,xLabel=None, yLabel=None, title=None):
        """
        Make the consistent label parameters
        :param xTick: Cur range from Sept 1st to Sept 10th
        :param yTick: Range from 0 to 100_000
        :param xLabel: time in hour
        :param yLabel: # of queries.
        :return: None
        """
        # xloc, _ = plt.xticks()
        plt.xticks(list(range(1, 24*10+1, 24)), ["2018-09-%s" % str(day).zfill(2) for day in range(1, 11)],
                   rotation=24)

        plt.yticks([math.log10(0.1), math.log10(1), math.log10(10), math.log10(100),
                    math.log10(1_000), math.log10(10_000), math.log10(100_000)],
                   ["0"]+["$10^{%d}$" % exp for exp in range(0, 6)])

        if xLabel:
            plt.xlabel(xLabel)

        if yLabel:
            plt.ylabel(yLabel)

        if title:
            plt.title(title)

        plt.legend(loc="best")

    def doShow(self):
        plt.show()

    def doSave(self, index, target):
        if not os.path.isdir("../../figure/mean-std-Scatter/New/"):
            os.mkdir("../../figure/mean-std-Scatter/New/")
        # plt.savefig("../../figure/mean-std-Scatter/log_%s_ByIPCluster_TotalSessionCount.pdf" % (target), format='pdf')
        plt.savefig("../../figure/LogMeanSTD_scatters/TopThousandOutbound/%s_ByIPCluster_TotalOutboundVolume.pdf" % (target), format='pdf')

        # plt.close(self.fig)
        plt.close()


def doPaintNorm():
    targetList = ["inakamai", "inaurora", "incampus", "incampusNew",
                  "incpsc", "inothers", "inphys", "inunknown205"]

    targetList += ["outakamai", "outcampus1", "outcampus2",
                  "outcpsc", "outothers", "outwebpax"]
    # targetList = ["inakamai"]
    for target in targetList:
        # foldernametotal = "../../exchange/total/"
        # filenametotal = "%sTotalOutByteClusterCollTen_trans.log" % target
        # foldernametotal = "../../exchange/TLD/"
        # filenametotal = "%sTLDTotalG_trans.log" % target
        foldernametotal = "../../exchange/total/"
        filenametotal = "%sTotalOutByteClusterCollTen_trans.log" % target
        # filenametotal = "%sTotalInByteClusterCollTen_trans.log" % target
        # filenametotal = "%sTotalOutClusterCollFull_trans.log" % target

        pTotal = timePlot(foldernametotal + filenametotal)

        scatterMean = []
        scatterStd = []
        for TLDname in list(pTotal.rawdata.keys())[0:1000]:
            dataList = np.array([x for x in pTotal.rawdata[TLDname]])
            # dataList = np.array(pTotal.rawdata[TLDname])
            scatterMean.append(dataList.mean())
            scatterStd.append(dataList.std())
        logScatterMean = [math.log10(x+0.1) for x in scatterMean]
        logScatterStd = [math.log10(x+0.1) for x in scatterStd]
        plt.scatter(logScatterMean, logScatterStd, color="black", marker="x", linewidths=2)
        plt.title(target+" (Outbound Data Volume by each IPCluster, Top 1000)")
        plt.xlim((-1, 7))
        plt.xticks(list(range(-1, 8)), ["0"] + ["$10^{%d}$" % i for i in range(0, 8)])
        plt.xlabel("Mean Value (Bytes per hour)")
        plt.ylim((-1, 7))
        plt.text(-0.5, 6.5, "Total Point #: %s" % "{:,}".format(len(logScatterMean)), size=10)
        plt.yticks(list(range(-1, 8)), ["0"] + ["$10^{%d}$" % i for i in range(0, 8)])
        plt.ylabel("Standard Deviation")
        # plt.show()
        pTotal.doSave(0, target)


def doPaintLog():
    targetList = ["inakamai", "inaurora", "incampus", "incampusNew",
                  "incpsc", "inothers", "inphys", "inunknown205"]

    targetList += ["outakamai", "outcampus1", "outcampus2",
                  "outcpsc", "outothers", "outwebpax"]

    targetList = ["outcampus1"]
    for target in targetList:
        # foldernametotal = "../../exchange/total/"
        # filenametotal = "%sTotalOutByteClusterCollTen_trans.log" % target
        # foldernametotal = "../../exchange/TLD/"
        # filenametotal = "%sTLDTotalG_trans.log" % target
        foldernametotal = "../../exchange/total/"
        # filenametotal = "%sTotalOutByteClusterCollTen_trans.log" % target
        # filenametotal = "%sTotalInByteClusterCollTen_trans.log" % target
        filenametotal = "%sTotalOutClusterCollFull_trans.log" % target

        pTotal = timePlot(foldernametotal + filenametotal, logRequ=True)
        scatterMean = []
        scatterStd = []
        for TLDname in list(pTotal.rawdata.keys()):
            # print(pTotal.rawdata[TLDname])
            dataList = np.array([math.log10(x+1) for x in pTotal.rawdata[TLDname]])
            if TLDname == "103.x.x.x":
                print(pTotal.rawdata[TLDname])
            # dataList = np.array(pTotal.rawdata[TLDname])
            scatterMean.append(dataList.mean())
            scatterStd.append(dataList.std())
        plt.scatter(scatterMean, scatterStd, color="black", marker="x", linewidths=2)
        plt.title(target+" (Outbound Volume by each IPCluster Top 1000 - LogExtension)")
        plt.xlim((-0.2, 7))
        # plt.xticks(list(range(-1, 8)), ["0"] + ["$10^{%d}$" % i for i in range(0, 8)])
        plt.xlabel("Mean Value Log(Bytes) per hour")
        plt.ylim((0, 3))
        # plt.yticks(list(range(-1, 8)), ["0"] + ["$10^{%d}$" % i for i in range(0, 8)])
        plt.text(0.25, 2.85, "Total Point #: %s" % "{:,}".format(len(scatterMean)), size=10)
        plt.ylabel("Standard Deviation")
        # plt.show()
        # pTotal.doSave(0, target)


if __name__ == '__main__':

    # doPaintNorm()
    doPaintLog()