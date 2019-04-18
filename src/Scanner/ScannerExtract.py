import sys
sys.path.append('/home/zhengping/DNS/DNSPythonWorkspace')
from src.util.FileReader import fileReader
from src.util.FileWriter import fileWriter
from src.util.FolderReader import folderReader
from src.util.IsFileExist import isFileExist
import os
import importlib
import datetime
from datetime import time
import json


index = 1


def get_target_list(filename):
    with open(filename, 'r') as f:
        target_list = json.load(f)["target"]
    return target_list


class ScannerLocator:
    def __init__(self, target_sub, date_range=None):
        self.t_ip_list = target_sub
        self.data_dict = {}
        for ip in self.t_ip_list:
            self.data_dict[ip] = {}
        if date_range:
            self.date_range = {"start": date_range[0], "end": date_range[1]}
        else:
            self.date_range = {"start": "2015-01-01", "end": "2019-12-31"}

    def _get_folders_for_module(self, module_name="inothers"):
        target_daily_folders = []
        module_folder_name = "../../structNewNew/%s/" % module_name
        start, end = self.date_range["start"], self.date_range["end"]

        date_start = datetime.datetime(int(start.split("-")[0]),
                                       int(start.split("-")[1]),
                                       int(start.split("-")[2]))
        date_end = datetime.datetime(int(end.split("-")[0]),
                                     int(end.split("-")[1]),
                                     int(end.split("-")[2]))

        module_folder = folderReader(module_folder_name)
        for daily_folder in module_folder:
            # (daily_folder)
            date_string = daily_folder.split("/")[-1]
            date_current = datetime.datetime(int(date_string.split("-")[0]),
                                             int(date_string.split("-")[1]),
                                             int(date_string.split("-")[2]))
            if date_start <= date_current < date_end:
                target_daily_folders.append(daily_folder)

        return target_daily_folders

    def _hourly_collector(self, hourly_filename):
        with open(hourly_filename, 'r') as f:
            daily_dict = json.load(f)
        for uid in daily_dict:
            ip = daily_dict[uid]["addr"][0]
            if ip in self.t_ip_list:
                self.data_dict[ip][uid] = daily_dict[uid]
        # print("Done Hour %s" % hourly_filename)
        # return target_dict

    def daily_collector(self, daily_folder_name):
        daily_list = folderReader(daily_folder_name)
        for hourly_filename in daily_list:
            self._hourly_collector(hourly_filename)
            # daily_data_dict.update(hourly_dict)
        print("Done date: %s" % daily_folder_name)
        # return daily_data_dict

    def total_collector(self):
        daily_folder_list = self._get_folders_for_module()
        # total_dict = {}
        for daily_folder in daily_folder_list:
            self.daily_collector(daily_folder)
            # daily_data_tmp = self.daily_collector(daily_folder)
            # total_dict.update(daily_data_tmp)

    def dump(self):
        self.total_collector()
        for ip in self.t_ip_list:
            output_filename = "../../scanner/%s.log" % ip
            with open(output_filename, 'w') as f:
                json.dump(self.data_dict[ip], f)
            # print(self.data_dict[ip])
            # print("IP is %s" % ip)
            # input("Press Enter to continue...")
            print("========= ENE DUMP %d (%s) AT: %s==========" % (index, ip, datetime.datetime.now()))


if __name__ == '__main__':
    target_filename = "../../scanner/Target.log"
    target_list = get_target_list(target_filename)
    i = 0
    # for target_ip in target_list:
    while i < len(target_list):
        target_sub = target_list[i:min(i+20, len(target_list))]
        s_locator = ScannerLocator(target_sub, date_range=("2018-09-03", "2018-09-10"))
        s_locator.dump()
        i += 20
        index += 1
    print("========= ENE TASK ==========")
