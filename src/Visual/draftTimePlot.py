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
                    math.log10(1000), math.log10(10000), math.log10(100000)],
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
        if not os.path.isdir("../../figure/comb/%s/" % target):
            os.mkdir("../../figure/comb/%s/" % target)
        plt.savefig("../../figure/comb/%s/%s_%s.pdf" % (target, target, str(index)), format='pdf')
        # plt.close(self.fig)
        plt.close()



if __name__ == '__main__':
    targetList = ["inakamai", "inaurora", "incampus", "incampusNew",
                  "incpsc", "inothers", "inphys", "inunknown205"]

    targetList += ["outakamai", "outcampus1", "outcampus2",
                  "outcpsc", "outothers", "outwebpax"]
    # targetList = ["inakamai"]
    for target in targetList:
        index = 1
        foldername = "../../exchange/total/"
        filename = "%sTotalOutByteClusterCollTen_trans.log" % target
        pout = timePlot(foldername + filename, logRequ=True)
        valueList1 = list(pout.rawdata.values())
        totalOut = valueList1[0]
        for valuelist in valueList1[1:]:
            for i in range(len(totalOut)):
                totalOut[i] += valuelist[i]

        foldernametotal = "../../exchange/total/"
        filenametotal = "%sTotalInByteClusterCollTen_trans.log" % target
        pin = timePlot(foldernametotal + filenametotal, logRequ=True)
        valueList2 = list(pin.rawdata.values())
        totalIn = valueList2[0]
        for valuelist in valueList2[1:]:
            for i in range(len(totalIn)):
                totalIn[i] += valuelist[i]

        # print(totalweird)
        # print(totaltotal)

        logtotalIn = [math.log10(i+1)-3 for i in totalIn]
        logtotalOut = [math.log10(i+1)-3 for i in totalOut]
        xdata = list(range(1, 1+len(totalIn)))
        plt.plot(xdata, logtotalIn, color="red", label="Inbound Volume")
        plt.plot(xdata, logtotalOut, color="blue", label="Outbound Volume")
        plt.xticks(list(range(1, 24*10+1, 24)), ["2018-09-%s" % str(day).zfill(2) for day in range(1, 11)],
                   rotation=24)

        ysrc = [1, 10, 100, 1000, 10000, 100000, 1000000, 10000000, 100000000]
        plt.yticks([math.log10(i) for i in ysrc],
                   ["0"]+["$10^{%d}$" % exp for exp in range(1, 9)])
        #
        plt.ylim((0,math.log10(100000000)))
        plt.title(target)
        plt.legend(loc="best")
        plt.ylabel("Size (in KB)")
        plt.savefig("../../figure/totalIO/%s_%s.pdf" % (target, "totalIO"), format='pdf')
        plt.close()
        # plt.show()
        # p.doShow()
        #
        # p.doDrawPlot([objname], "weird", "r", "-")
        # # p.doDrawPlot()
        # p.setParams(title="%s" % (objname))
        # p.doSave(index, target)
        # index += 1
        # # p.doShow()
