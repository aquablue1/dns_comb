"""
" The purpose of this class is to draw the time series plot according to the given input file
" There are three major steps in order to do the visualization:
" First, load the json file.
" Second, decide the object and time period that will show in the figure
" Third, set all the suitable parameters and show the graph
" Loading is a easy task
" For object and time period selection, according to the methods defined in <code>JSDictToExchange</code>,
" time period is not defined so users need to define the time period by themselves. This (<code>timePlot</code>)
" class will only obey the defined time period if it matches the length of input data. There is no mechanism to verify
" if the time period is correct or not.
" This class will only support the visualization of one single graph in one round of running, i.e. sub-graph is not
" supported. However, multiple plots in one graph is supported by call <code>doDrawPlot</code> multiple times.
" Also, only time series plot is supported, the other formats such as log scale (in x-axis) graph or even Pie charts
" are not supported.
" By Zhengping on 2019-01-14
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
    # targetList = ["outcampus1"]
    for target in targetList:
        index = 1
        foldername = "../../exchange/total/"
        filename = "%sTotalOutClusterCollFull_trans.log" % target
        p = timePlot(foldername + filename, logRequ=True)
        objList1 = list(p.rawdata.keys())

        for objname in objList1:
            foldernametotal = "../../exchange/total/"
            filenametotal = "%sTotalOutClusterCollFull_trans.log" % target
            ptotal = timePlot(foldernametotal + filenametotal, logRequ=True)
            ptotal.doDrawPlot([objname], "total", "black", "-")

            # p.doShow()

            # p.doDrawPlot([objname], "weird", "r", "-")
            # p.doDrawPlot()
            p.setParams(title="%s" % (objname))
            p.doSave(index, target)
            index += 1
            # p.doShow()
