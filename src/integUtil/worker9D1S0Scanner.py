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
    # skipped_list = ["136.159.205.37", "136.159.205.38", "136.159.205.39"]
    for key in data_dict:
        # Check direction first to get the inner server.
        src_ip = data_dict[key]["addr"][0]
        src_port = data_dict[key]["addr"][1]
        dst_ip = data_dict[key]["addr"][2]
        dst_port = data_dict[key]["addr"][3]
        if data_dict[key]["conn"][3] == "S0":
            # if dst_ip not in skipped_list:
            if src_ip.startswith("136.159."):
                # Outbound traffic -> get external IP from dst_ip field.
                if data_dict[key]["dns"]:
                    ip_counter[dst_port] += len(data_dict[key]["dns"])
                else:
                    # (data_dict[key])
                    ip_counter[dst_port] += 1
            else:
                # Outbound traffic -> get external IP from dst_ip field.
                if data_dict[key]["dns"]:
                    ip_counter[src_port] += len(data_dict[key]["dns"])
                else:
                    # (data_dict[key])
                    ip_counter[src_port] += 1

    return Counter(dict(ip_counter))
