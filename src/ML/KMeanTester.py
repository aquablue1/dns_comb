

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
from sklearn import datasets
from sklearn.cluster import KMeans


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
        if not os.path.isdir("../../figure/TLD/%s/" % target):
            os.mkdir("../../figure/TLD/%s/" % target)
        plt.savefig("../../figure/TLD/%s/%s_%s.pdf" % (target, target, str(index)), format='pdf')
        # plt.close(self.fig)
        plt.close()



if __name__ == '__main__':
    targetList = ["inakamai", "inaurora", "incampus", "incampusNew",
                  "incpsc", "inothers", "inphys", "inunknown205"]

    targetList += ["outakamai", "outcampus1", "outcampus2",
                  "outcpsc", "outothers", "outwebpax"]
    targetList = ["incampus"]
    for target in targetList:
        foldernametotal = "../../exchange/Total/"
        filenametotal = "%sTotalOutClusterCollFull_trans.log" % target
        pResponse = timePlot(foldernametotal + filenametotal, logRequ=True)
        pTotal = timePlot(foldernametotal + filenametotal, logRequ=True)
        index = 0
        keyList = []
        featureList = []
        infoDict = {}
        for TLDname in list(pTotal.rawdata.keys()):
            valueListTotal = np.array(list(pTotal.rawdata[TLDname]))
            # curFeatureList = []

            # print(valueListTotal.mean())
            # varUPD1 = np.array([math.log10(x + 1) for x in valueListTotal])
            # varUPD2 = np.array([math.log10(x + 0.01) for x in valueListTotal])
            # mean = varUPD1.mean()
            # std = varUPD2.std()
            mean = math.log10(valueListTotal.mean())
            std = math.log10(valueListTotal.std()+1)
            # mean = valueListTotal.mean()
            # std = valueListTotal.std()
            ac = getAutoCorr(valueListTotal, 12)
            cov = getCoeffVar(valueListTotal)/20
            actRate = len(valueListTotal.nonzero()[0])/len(valueListTotal) * 2
            curFeatureList = [mean, std, ac,  cov, actRate]
            infoDict[TLDname] = curFeatureList
            keyList.append(TLDname)
            featureList.append(curFeatureList)

        # Loading dataset

        # Declaring Model
        for i in range(2, 16):
            model = KMeans(n_clusters=i)
            # Fitting Model
            # print(featureList)
            model.fit(featureList)

            # Predicitng a single input
            # predicted_label = model.predict([[7.2, 3.5, 0.8, 1.6], [1000, 1000, 1000, 1000]])

            # Prediction on the entire data
            all_predictions = model.predict(featureList)
            predDict = {}
            for pred, tld in zip(all_predictions, keyList):
                predDict[tld] = int(pred)
                # if pred == 1:
                #     print(tld)
            # print(predDict)
            with open("../../prediction/outcpsc/prediction_logAfter/total_%d.json" % i, 'w') as f:
                print(predDict)
                json.dump(predDict, f)
                print("Job Done for %d." % i)

        with open("../../prediction/outcpsc/prediction_logAfter/total_feature.json", 'w') as f:
            json.dump(infoDict, f)