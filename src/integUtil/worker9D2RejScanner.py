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
    data_dict = json.load(f)
    ip_counter = Counter()

    for key in data_dict:
        # Check direction first to get the inner server.
        src_ip = data_dict[key]["addr"][0]
        src_port = data_dict[key]["addr"][1]
        dst_ip = data_dict[key]["addr"][2]
        dst_port = data_dict[key]["addr"][3]
        if src_ip.startswith("136.159."):
            if data_dict[key]["dns"]:
                for dns in data_dict[key]["dns"]:
                    if dns[6] == "REFUSED" or dns[6] == "SERVFAIL":
                        ip_counter[dst_port] += 1
        else:
            if data_dict[key]["dns"]:
                for dns in data_dict[key]["dns"]:
                    if dns[6] == "REFUSED" or dns[6] == "SERVFAIL":
                        ip_counter[src_port] += 1

    return Counter(dict(ip_counter))
