"""
" Check if a potential IP is scanning or not.
" By Zhengping on 2019-04-17
"""

import json
import matplotlib.pyplot as plt


class ScannerChecker:
    def __init__(self, ip):
        self.ip = ip
        self.src_dict = None

    def data_loader(self):
        src_filename = "../../exchange/Scanner/%s.log" % self.ip
        with open(src_filename, 'r') as f:
            self.src_dict = json.load(f)

    def analysis(self):
        self.data_loader()
        target_ips = set()
        queries = set()
        for uid in self.src_dict:
            # For Inbound traffic: field 0 for external IPs, field 2 for internal IPs
            # We choose internal IPs here, since they are the targets.
            target_ips.add(self.src_dict[uid]["addr"][2])
            if self.src_dict[uid]["dns"]:
                for dns in self.src_dict[uid]["dns"]:
                    # field 2 for detailed query domain
                    queries.add(dns[2])
        return len(self.src_dict), len(target_ips), len(queries)


class Painter:
    def __init__(self, src_fname):
        self.src_fname = src_fname
        with open(self.src_fname, 'r') as f:
            self.src_ip_list = json.load(f)["target"]
        self.statistics = {}

    def painter(self):
        x_data = []
        y_data = []
        for ip in self.src_ip_list:
            total_length, target_length, query_length = ScannerChecker(ip).analysis()
            self.statistics[ip] = [total_length, target_length, query_length]
            x_data.append(total_length)
            y_data.append(target_length)
            print("Scann IP: %s, total: %d, target: %d" % (ip, total_length, target_length))
        plt.scatter(x_data, y_data, color="black", marker="x", s=20)
        plt.plot([0, 65_535], [0, 65_535], linestyle="--", color="black")

        limitation = max(max(x_data), max(y_data))
        plt.xlim((0, limitation))
        plt.ylim((0, 65_535))
        plt.plot([65_535, limitation], [65_535, 65_535], linestyle="--", width="1",  color="black")

        plt.show()
        self.dump()

    def quick_painter(self):
        filename = "../../exchange/Scanner/Summary.log"
        with open(filename, 'r') as f:
            statistics = json.load(f)
        x_data = []
        y_data = []
        for ip in statistics:
            [total_length, target_length, query_length] = statistics[ip]
            x_data.append(total_length)
            y_data.append(target_length)
            print("Scann IP: %s, total: %d, target: %d" % (ip, total_length, target_length))
        plt.scatter(x_data, y_data, color="black", marker="x", s=20)
        plt.plot([0, 65_535], [0, 65_535], linestyle="--", color="black", linewidth=0.5)

        limitation = max(max(x_data), max(y_data))
        plt.xlim((0, limitation))
        plt.ylim((0, 66_535))
        plt.plot([65_535, limitation], [65_535, 65_535], linestyle="--", linewidth=0.5,  color="black")

        plt.show()

    def dump(self):
        output_filename = "../../exchange/Scanner/Summary.log"
        with open(output_filename, 'w') as f:
            json.dump(self.statistics, f)

if __name__ == '__main__':
    src_fname = "../../exchange/Scanner/Target.log"
    painter = Painter(src_fname)
    painter.quick_painter()

