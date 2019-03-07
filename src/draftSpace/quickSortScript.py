"""
" Quick sort script
" By Zhengping on 2019-03-06
"""

import sys
# sys.path.append('/home/zhengping/DNS/DNSPythonWorkspace')
from collections import Counter
from src.util.FolderReader import folderReader
from src.util.FileReader import fileReader


def quick_sort(filename):
    key_counter = Counter()
    src_file = fileReader(filename)
    for line in src_file:
        line_list = line.split("\t")
        dst_port = line_list[5]
        trans_proto = line_list[6]
        app_proto = line_list[7]
        key = trans_proto + "/" + dst_port + "/" + app_proto
        key_counter[key] += 1
    return key_counter


def quick_daily_sort(folder_name):
    src_folder = folderReader(folder_name)
    daily_key_counter = Counter()
    for filename in src_folder:
        daily_key_counter += quick_sort(filename)
    print("Daily Result %s" % folder_name.split("/")[-1])
    print(daily_key_counter)
    return daily_key_counter


def aggregate_sort(date_list):
    aggregate_counter = Counter()
    for date in date_list:
        folder_name = "../../data/conn_inbound/%s" % date
        aggregate_counter += quick_daily_sort(folder_name)

    return aggregate_counter


if __name__ == '__main__':
    date_list = ["2018-09-%s" % str(i).zfill(2) for i in range(1, 11)]
    print("Overall Inbound Counting Result is: ")
    print(aggregate_sort(date_list))
    print("END OF SCRIPT")
