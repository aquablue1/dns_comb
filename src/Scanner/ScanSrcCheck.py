"""
" Check the query field in each scan activity.
" By Zhengping on 2019-04-18
"""

import math
import json
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from src.util.IPInfo import getIPInfo
from src.util.IPName import getNameByIP


class ScanSrcChecker:
    def __init__(self, target_ip):
        self.s_ip = target_ip
        self.ip_info = None
        self.name_info = None

    def ip_checker(self):
        """

        :return:
        """
        target_ip = self.s_ip
        ip_info = getIPInfo(target_ip)
        if ip_info:
            self.ip_info = ip_info
        return ip_info

    def name_checker(self):
        target_ip = self.s_ip
        name_info = getNameByIP(target_ip)
        if name_info:
            self.name_info = name_info[0]
        return name_info

if __name__ == '__main__':
    with open("../../exchange/Scanner/TargetExact.log", 'r') as f:
        target_ip_list = json.load(f)["target"]
    src_dict = {}
    for target_ip_t in target_ip_list:
        # target_ip_t = "111.13.148.44"
        checker = ScanSrcChecker(target_ip_t)
        ip_info = checker.ip_checker()
        print(ip_info)
        name_info = checker.name_checker()
        print(name_info)
        src_dict[target_ip_t] = {"ip_info": ip_info,
                                 "name_info": name_info}
        # break

    with open("../../exchange/Scanner/src_info.log", 'w') as f:
        json.dump(src_dict, f)

    # aov_painter()



