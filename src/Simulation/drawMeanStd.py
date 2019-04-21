"""
" Draw the Mean - Std graph based on the given mean value and data generation strategy.
" By Zhengping on 2019-01-30
"""

import math
import numpy as np
import matplotlib.pyplot as plt
from src.Simulation.dataGen import *


def doPaint(MeanStart, MeanEnd, MeanStep=100):
    meanList = []
    stdList = []
    for meanval in range(MeanStart, MeanEnd+MeanStep, MeanStep):
        dataSeries = np.array(genSinVals(meanval))
        mean = dataSeries.mean()
        std = dataSeries.std()
        meanList.append(mean)
        stdList.append(std)

    plt.scatter(meanList, stdList, color="black")
    plt.show()


def doLogPaint(MeanStart, MeanEnd, MeanStep=1):
    meanListLog = []
    stdListLog = []
    for meanval in range(MeanStart, MeanEnd+MeanStep, MeanStep):
        dataSeries = np.array(genSinVals(meanval))
        mean = dataSeries.mean()
        std = dataSeries.std()
        meanListLog.append(math.log10(mean+0.1))
        stdListLog.append(math.log10(std+0.1))

    plt.scatter(meanListLog, stdListLog, color="black")
    plt.show()


if __name__ == '__main__':
    start = 101
    end = 5000
    doPaint(start, end)
    doLogPaint(start, end)