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
import json
import matplotlib.pyplot as plt
import math


class timePlot():
    def __init__(self, filename):
        # read the filename from exchange/***
        self.filename = filename
        self.rawdata = self._load()

    def _load(self):
        with open(self.filename, 'r') as f:
            rawData = json.load(f)
        return rawData

    def _ydataExtract(self, objectName, logRequ=False):
        """
        Extract the data which is used to draw plot.
        One call of _ydataExcract will return a list of y-axis data which can be used to draw the plot directly
        i.e. the return value should be able to be sent to the plt.plot method directly.
        No further execution is required.
        If multiple plots in one graph is required, each plot requires one call of this method to get
        its corresponding y data.
        :param objectName: The name of target object, should be simply one of the keyword from self.rowdata
        :param islog: define if log-scale is required
        :return: y data as a list which can be used to draw the plot.
        """
        if not logRequ:
            return self.rawdata[objectName]
        else:
            return [math.log10(data) for data in self.rawdata[objectName]]

    def _ydataExtractG(self, objectList, logRequ):
        """
        Extract the data which is used to draw plot.
        This method is very similar with <code>_ydataExtract</code> except that this method accept a list of objects
        instead of only one.
        :param objectList: a list of the name of target object
        :param logRequ: define if log-scale is required
        :return: y data as a list which can be used to draw the plot.
        """
        summarydata = None
        for objectName in objectList:
            tmpdata = self._ydataExtract(objectName)
            if not summarydata:
                summarydata = [x+y for x, y in zip(summarydata, tmpdata)]

        if summarydata:
            if logRequ:
                return [math.log10(data) for data in summarydata]
            else:
                return summarydata
        else:
            return None