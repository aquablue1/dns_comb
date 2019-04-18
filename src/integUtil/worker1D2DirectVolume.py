

import json


def doCountTask(filename):
    """
    count how many lines of record has return msg size equals 0
    :param filename: name of the searched file
    :return: List, [count]
    """
    f = open(filename)
    data_dict = json.load(f)
    inbound_query = 0
    inbound_reply = 0
    outbound_query = 0
    outbound_reply = 0
    for key in data_dict:
        # Check direction first to get the inner server.
        src_IP = data_dict[key]["addr"][0]
        # dst_IP = data_dict[key]["addr"][2]
        if src_IP.startswith("136.159."):
            # Which means srcIP is within our campus. it should be an outbound traffic
            outbound_query += int(data_dict[key]["conn"][4])
            outbound_reply += int(data_dict[key]["conn"][6])
        else:
            inbound_query += int(data_dict[key]["conn"][4])
            inbound_reply += int(data_dict[key]["conn"][6])

    return [inbound_query, inbound_reply, outbound_query, outbound_reply]
