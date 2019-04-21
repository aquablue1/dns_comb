"""
" Generate the data needed for Mean and Std analysis.
" By Zhengping on 2019-01-30
"""

import math
import numpy as np


def genZeroAndFix(x_mean, k=120):
    n = 24 * 10
    x_fix = (n*x_mean) / k
    return [0]*(n-k) + [x_fix]*k


def genProbBasedFix(x_mean, k=120):
    n = 240
    p = 0.3
    x_1 = (1-p) * x_mean
    x_2 = (1+p) * x_mean
    return [x_1]*(n-k) + [x_2]*k


def genSinVals(x_mean, k=120):
    degreeList = list(range(0, 3615, 15))
    valList = [math.sin(degree) * 100+x_mean for degree in degreeList]
    return valList



if __name__ == '__main__':
    x_mean = 10
    # print(genZeroAndFix(x_mean))
    print(genSinVals(180))