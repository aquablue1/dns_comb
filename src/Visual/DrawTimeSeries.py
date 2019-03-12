"""
" This script draws some random time Series graphs for final thesis report.
" Since the src data structure is very random and dynamic, hence
" this script is free to change.
" The input is required to have both the time and some counting information.
" The time will be used in x-axis and y will appears in y-axis.
" By Zhengping on 2019-03-06
"""

import os
import math
from datetime import date
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from src.util.FolderReader import folderReader
from src.util.FileReader import fileReader


class TimeSeriesPlot:
    def __init__(self, src_folder, module_name, date_range):
        self.src_folder = src_folder
        self.module_name = module_name
        self.date_range = {"start": date_range[0], "end": date_range[1]}
        self.ax = plt.figure().add_subplot(111)

    def _gen_date_list(self):
        start_date = self.date_range["start"]
        end_date = self.date_range["end"]
        # print(self.date_range)
        start_date = date(int(start_date.split("-")[0]),
                          int(start_date.split("-")[1]),
                          int(start_date.split("-")[2]))
        end_date = date(int(end_date.split("-")[0]),
                        int(end_date.split("-")[1]),
                        int(end_date.split("-")[2]))

        date_list = [str(date.fromordinal(i)) for i in range(start_date.toordinal(), end_date.toordinal())]

        return date_list

    def _get_data_key_list(self):
        """
        Generate the date Key List. These key is used to select values in data_dict
        The order ot this list is very important.
        :return:
        """
        date_key_list = []
        for date in self._gen_date_list():
            for hour in range(0, 24):
                date_key = date + "_%02d" % hour
                date_key_list.append(date_key)
        return date_key_list

    def _data_loader(self):
        """
        This method might be updated frequently in order to handle different
        data structures.
        :return:
        """
        data_dict = Counter()
        folder_list = folderReader(self.src_folder)
        for filename in folder_list:
            abs_filename = filename.split("/")[-1]
            if abs_filename.startswith(self.module_name):
                for line in fileReader(filename):
                    line_list = line.strip().split("\t")
                    # Most of the modifications happen here.

                    data_dict[line_list[0]] += (int(line_list[2]) + int(line_list[4]))
        return data_dict

    def paint(self):
        data_key_list = self._get_data_key_list()
        data_dict = self._data_loader()
        y_data = []
        for data_key in data_key_list:
            try:
                y_data.append(data_dict[data_key])
            except KeyError:
                print("Specified data key %s is not found from data dict" % data_key)
                print("Error data range or Error input src file")

        x_data = list(range(len(y_data)))

        self.ax.plot(x_data, y_data, color='black', label="Total Session Count")

    def decoration(self):
        # self.ax.set_xlim(self.time_range["start"], self.time_range["end"])
        # max_y_lim = max([int(raw[3]) for raw in self.load_raw_data()] +
        #                 [int(raw[4]) for raw in self.load_raw_data()])
        max_y_lim = 1_600_000
        max_x_lim = 240
        self.ax.set_ylim(0, max_y_lim)
        self.ax.set_xlim(0, max_x_lim)
        self.ax.set_xticks(list(range(0, max_x_lim+24, 24)))
        self.ax.set_xticklabels(["2018-09-%s" % str(d).zfill(2) for d in range(1, 12)], rotation=15)

        self.ax.set_yticks(list(range(0, max_y_lim+1, 200_000)))
        self.ax.set_yticklabels(["0"] + ["$%dx10^{5}$" % base for base in range(2, 18, 2)])

        self.ax.set_ylabel("Session Count (per hour)")
        handles, labels = plt.gca().get_legend_handles_labels()
        i = 1
        while i < len(labels):
            if labels[i] in labels[:i]:
                del (labels[i])
                del (handles[i])
            else:
                i += 1
        plt.legend(handles, labels, loc="best")
        # self.ax.legend(loc="best")

        plt.show()

    def statistics(self):
        data_key_list = self._get_data_key_list()
        data_dict = self._data_loader()
        y_data = []
        for data_key in data_key_list:
            try:
                y_data.append(data_dict[data_key])
            except KeyError:
                print("Specified data key %s is not found from data dict" % data_key)
                print("Error data range or Error input src file")
        y_data_np = np.array(y_data)
        print("Total witnessed amount is %d" % sum(y_data))
        print("Max witnessed value is %d" % y_data_np.max())
        print("Min witnessed value is %d" % y_data_np.min())
        print("Mean value is %f" % y_data_np.mean())
        print("Population Standard Deviation is %d" % y_data_np.std())


if __name__ == '__main__':
    # src_folder_t = "../../exchange/totalCount"
    src_folder_t = "../../exchange/OverallVolumeCollector/"
    date_range_t = ["2018-09-01", "2018-09-11"]
    module_name_t = ""
    tsp = TimeSeriesPlot(src_folder_t, module_name_t, date_range_t)
    # tsp.paint()
    # tsp.decoration()
    tsp.statistics()
