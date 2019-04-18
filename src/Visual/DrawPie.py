"""
" Generate Pie chart based on the data provided by one/multiple JSON files.
" By Zhengping on 2019-03-14
"""

import json
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from src.util.FolderReader import folderReader


class PieChart:
    def __init__(self, src_folder, module_name, ax):
        self.src_folder_name = src_folder
        self.module_name = module_name
        self.ax = ax

    def _data_loader(self):
        total_counter = Counter()
        for filename in folderReader(self.src_folder_name):
            if filename.split("/")[-1].startswith(self.module_name):
                with open(filename, 'r') as f:
                    src_data = json.load(f)
                for key in src_data:
                    hourly_counter = Counter(src_data[key])
                    total_counter += hourly_counter
        return total_counter

    def paint(self):
        data_counter = self._data_loader()
        print(data_counter)
        candidate_list = ["A", "AAAA", "PTR", "NS", "MX", "TXT"]
        candidate_list = ["A", "AAAA", "PTR", "NS"]
        candidate_list = ["NOERROR", "NXDOMAIN", "SERVFAIL", "REFUSED"]
        color_list = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d42728",
                      "#9467bd", "#8c564b", "#e377c2", "#7f7f7f"]
        color_dict = {k: v for k, v in zip(candidate_list, color_list)}
        color_dict.update({"Others": "#7f7f7f"})
        to_draw_dict = {}
        for key in candidate_list:
            if key in data_counter:
                if data_counter[key] > 100:
                    to_draw_dict[key] = data_counter[key]
        for key in data_counter:
            if key not in candidate_list:
                try:
                    to_draw_dict["Others"] += data_counter[key]
                except KeyError:
                    to_draw_dict["Others"] = data_counter[key]

        prc_list = [float(i/sum(to_draw_dict.values())) for i in to_draw_dict.values()]
        patches, texts = self.ax.pie([to_draw_dict[k] for k in to_draw_dict],
                                     colors=[color_dict[k] for k in to_draw_dict], shadow=True,
                                     startangle=90)
        labels = ["{0} - {1:1.2f}%".format(k, prc*100) for k, prc in zip(to_draw_dict.keys(), prc_list)]
        plt.legend(patches, labels, bbox_transform=plt.gcf().transFigure, loc="upper left")

    def decoration(self):
        self.ax.set_title(self.module_name)
        # plt.savefig("../../figure/rtype/rtype-%s" % self.module_name)
        # plt.close()

        plt.show()


if __name__ == '__main__':
    module_list = ["incampus",  "incpsc", "inothers", "inakamai",
                   "incampusNew", "inphys", "inunknown205"]
    module_list += ["outakamai", "outcampus1", "outcampus2",
                    "outcpsc", "outothers"]
    # module_list += ["in", "out"]

    # color_list = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    # color_list = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d42728",
    #               "#9467bd", "#8c564b", "#e377c2", "#7f7f7f"]
    # color_dict = dict([(module, color) for module, color in zip(module_list, color_list)])

    for module_name_t in module_list:
        ax_t = plt.figure(figsize=(4, 4)).add_subplot(111)
        src_folder_t = "../../exchange/Rtype/"
        pie = PieChart(src_folder_t, module_name_t, ax_t)
        pie.paint()
        pie.decoration()
