import sys
from src.util.IPCluster import getIPCluster
from collections import Counter
import json
sys.path.append('/home/zhengping/DNS/DNSPythonWorkspace')


def doCollectTask(filename, topK):
    """
    Collect the topK result from filename
    :param filename: target filename
    :param topK: topK wants to select, by default is None.
    :return: top K count result.
    """
    f = open(filename)
    dataDict = json.load(f)
    ReplyCollect = Counter()
    for key in dataDict:
        # Check direction first to get the inner server.
        if dataDict[key]["dns"]:
            for dns in dataDict[key]["dns"]:
                ttls = dns[4]
                for ttl in ttls.split(","):
                    ReplyCollect[ttl] += 1

    return ReplyCollect
