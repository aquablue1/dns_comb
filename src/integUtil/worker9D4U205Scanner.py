import sys
from src.util.IPCluster import getIPCluster
from collections import Counter
import json

sys.path.append('/home/zhengping/DNS/DNSPythonWorkspace')


def doCollectTask(filename, topK):
    """
    Collect the topK result from filename
    # Warning: Needs cooperation from workerController
    :param filename: target filename
    :param topK: topK wants to select, by default is None.
    :return: top K count result.
    """
    f = open(filename)
    data_dict = json.load(f)
    ip_counter = Counter()

    for key in data_dict:
        # Check direction first to get the inner server.
        src_ip = data_dict[key]["addr"][0]
        # dst_ip = data_dict[key]["addr"][2]

        if data_dict[key]["dns"]:
            ip_counter[src_ip] += len(data_dict[key]["dns"])
        else:
            ip_counter[src_ip] += 1

    return Counter(dict(ip_counter))
