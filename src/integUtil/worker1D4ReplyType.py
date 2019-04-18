
import sys
sys.path.append('/home/zhengping/DNS/DNSPythonWorkspace')
from src.util.IPCluster import getIPCluster
from collections import Counter
import json


def doCollectTask(filename, topK):
    """
    Collect the topK result from filename
    :param filename: target filename
    :param topK: topK wants to select, by default is None.
    :return: top K count result.
    """
    f = open(filename)
    dataDict = json.load(f)
    typeCollector = Counter()
    for key in dataDict:
        if dataDict[key]["dns"]:
            for dns in dataDict[key]["dns"]:
                q_type = dns[6]
                typeCollector[q_type] += 1
    return Counter(dict(typeCollector.most_common(topK)))
