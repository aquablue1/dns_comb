"""
" By Zhengping on 2019-02-13
"""

import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def do3DDraw():
    """
    Draw 3D scatter with std, mean and activeRate as three features,
    Paint different colors for different cluster
    :return:
    """
    with open("../../prediction/outcpsc/prediction_logPre/total_feature.json", 'r') as f:
        featureDict = json.load(f)
    n_clusters = 8
    with open("../../prediction/outcpsc/prediction_logPre/total_%d.json" % n_clusters, 'r') as f:
        classDict = json.load(f)

    transClassDict = {}
    for key in classDict:
        try:
            transClassDict[classDict[key]].append(key)
        except KeyError:
            transClassDict[classDict[key]] = [key]

    # print(transClassDict)
    clusterTOColor = {0: "red", 1: "blue", 2: "orange", 3: "yellow", 4: "green", 5: "m", 6: "pink",
                      7: "gold", 8: "palegreen", 9: "slategray", 10: "aqua", 11: "darkcyan", 12: "bisque",
                      13: "silver",}

    fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    ax = Axes3D(fig)
    for cluster in transClassDict:
        keyList = transClassDict[cluster]
        color = clusterTOColor[cluster]
        fir = []
        sec = []
        thi = []
        for key in keyList:
            fir.append(featureDict[key][0])   # mean
            sec.append(featureDict[key][1])   # std
            thi.append(featureDict[key][4])   # actRate
        # print(color)
        ax.scatter(fir, sec, thi, marker='+', color=color)
    ax.set_xlabel("mean")
    ax.set_ylabel("std")
    ax.set_zlabel("active rate")
    plt.show()


def do2DDraw(label1, label2):
    """
    Draw 3D scatter with std, mean and activeRate as three features,
    Paint different colors for different cluster
    :return:
    """
    labelDict = {"mean":0, "std":1, "AC":2, "CoV/20":3, "2 * Active Rate":4}
    with open("../../prediction/outcpsc/prediction_logPre/total_feature.json", 'r') as f:
        featureDict = json.load(f)
    n_clusters = 8
    with open("../../prediction/outcpsc/prediction_logPre/total_%d.json" % n_clusters, 'r') as f:
        classDict = json.load(f)

    transClassDict = {}
    for key in classDict:
        try:
            transClassDict[classDict[key]].append(key)
        except KeyError:
            transClassDict[classDict[key]] = [key]

    # print(transClassDict)
    clusterTOColor = {0: "red", 1: "blue", 2: "orange", 3: "yellow", 4: "green", 5: "m", 6: "pink",
                      7: "gold", 8: "palegreen", 9: "slategray", 10: "aqua", 11: "darkcyan", 12: "bisque",
                      13: "silver",}

    fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # ax = Axes3D(fig)
    ax = fig.add_subplot(111)
    for cluster in transClassDict:
        keyList = transClassDict[cluster]
        color = clusterTOColor[cluster]
        fir = []
        sec = []
        for key in keyList:
            fir.append(featureDict[key][labelDict[label1]])   # CoV
            sec.append(featureDict[key][labelDict[label2]])   # AC
        # print(color)
        ax.scatter(fir, sec, marker='+', color=color)
    ax.set_xlabel(label1)
    ax.set_ylabel(label2)
    # ax.set_ylim(-1, 1)
    ax.set_title("outcpsc")
    plt.show()



if __name__ == '__main__':
    # do3DDraw()
    label1 = "std"
    label2 = "2 * Active Rate"
    # label1 = "CoV/20"
    # label2 = "AC"
    do2DDraw(label1, label2)