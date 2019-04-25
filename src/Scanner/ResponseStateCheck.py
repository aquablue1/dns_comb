"""
" Detect the DNS scans with actual response.
" By Zhengping on 2019-04-23
"""

import json
from collections import Counter


class ResponseStateChecker:
    def __init__(self, src_ip):
        self.s_ip = src_ip
        self.response_state_counter = None
        self.no_s0_set = None
        self.response_type_counter = None
        self.no_dash_set = None

        self.scan_hit_counter = None

    def checker_s0(self):
        src_filename = "../../exchange/Scanner/targetIPs/%s.log" % self.s_ip
        self.response_state_counter = Counter()
        # ts_list = []
        self.no_s0_set = set()
        with open(src_filename, 'r') as f:
            data_dict = json.load(f)

        for uid in data_dict:
            response_state = data_dict[uid]["conn"][3]
            self.response_state_counter[response_state] += 1
            if "S0" not in response_state:
                dst_ip = data_dict[uid]["addr"][2]
                self.no_s0_set.add(dst_ip)

        print(self.response_state_counter)
        print(self.no_s0_set)
        print(len(self.no_s0_set))

    def checker_no_dash(self):
        src_filename = "../../exchange/Scanner/targetIPs/%s.log" % self.s_ip
        self.response_type_counter = Counter()
        # ts_list = []
        self.no_dash_set = set()
        self.scan_hit_counter = Counter()
        with open(src_filename, 'r') as f:
            data_dict = json.load(f)

        for uid in data_dict:
            if data_dict[uid]["dns"]:
                dst_ip = data_dict[uid]["addr"][2]
                for dns in data_dict[uid]["dns"]:
                    state = dns[6]
                    self.response_type_counter[state] += 1
                    if state != "-":
                        self.no_dash_set.add(dst_ip)
                        self.scan_hit_counter[dst_ip] += 1

        # print(self.response_type_counter)
        # print(self.no_dash_set)
        # print(len(self.no_dash_set))

    def get_hit_counter(self):
        return self.scan_hit_counter

    def resolver_checker(self):
        src_filename = "../../exchange/Scanner/targetIPs/%s.log" % self.s_ip
        self.response_type_counter = Counter()
        # ts_list = []
        self.no_dash_set = set()
        self.scan_hit_counter = Counter()
        with open(src_filename, 'r') as f:
            data_dict = json.load(f)
        resolver_dict = ["136.159.2.1", "136.159.2.4", "136.159.1.21", "136.159.34.201"]
        for uid in data_dict:
            print(data_dict[uid]["addr"][2])
            if data_dict[uid]["addr"][2] in resolver_dict:
                print(data_dict[uid])


if __name__ == '__main__':
    with open("../../exchange/Scanner/TargetExact.log", 'r') as f:
        target_ip_list = json.load(f)["target"]
    total_query_counter = Counter()
    # total_hit_counter = Counter()
    for target_ip_t in target_ip_list:
        # target_ip_t = "111.13.148.44"
        print(target_ip_t)
        rs_checker = ResponseStateChecker(target_ip_t)
        # rs_checker.checker_no_dash()
        rs_checker.resolver_checker()
        # print("=====================")
        # total_hit_counter += rs_checker.get_hit_counter()
    # print(total_hit_counter)
    # output_filename = "../../exchange/Scanner/HitCounter.log"
    # with open(output_filename, 'w') as f:
    #     json.dump(total_hit_counter, f)


