"""
" A quick global sort script.
" Aim at get the general statistics of network traffic which goes through the campus edge router.
" The source data is stored under /data3/2018-09-[01-10], only the conn log is considered.
" Since all the src data sre compressed, zip lib should be included to actually conduct the analysis.
" The purpose of this script is to generate hourly, daily and general Proto/port usage report, as well as
" General statistics of overall traffic.
" By Zhengping on 2019-03-11
"""

import sys
sys.path.append('/home/zhengping/DNS/DNSPythonWorkspace')
import gzip
from collections import Counter
from src.util.FolderReader import folderReader


def get_date_list():
    date_list = ["2018-09-%s" % str(i).zfill(2) for i in range(1, 11)]
    # folder_name_dict = ["/data3/%s" % date for date in date_list]
    return date_list


def daily_analysis(date):
    folder_name = "/data3/%s" % date
    folder = folderReader(folder_name)
    daily_result = {}
    for i in range(0, 24):
        hour_key = str(i).zfill(2)
        daily_result[hour_key] = None
    daily_result["total"] = {"summary": [0, 0, 0, 0, 0, 0], "proto/port": Counter()}
    total_weird_count = 0
    for filename in folder:
        if "conn." not in filename:
            continue
        weird_count = 0
        total_in, total_out = 0, 0
        total_in_byte_trans, total_out_byte_trans = 0, 0
        total_in_byte_ip, total_out_byte_ip = 0, 0
        tcp_count, udp_count, icmp_count, non_trans_count = 0, 0, 0, 0
        proto_port_counter = Counter()
        with gzip.open(filename, 'rt') as f:
            for line in f:
                if line[0] == "#":
                    continue
                # print(line)
                line_list = line.strip().split("\t")
                src_ip = line_list[2]
                dst_ip = line_list[4]
                direct = "none"
                proto_port_key = line_list[6] + "/" + line_list[5]
                proto = line_list[6]
                if line_list[9] == "-":
                    src_bytes_trans = 0
                else:
                    src_bytes_trans = int(line_list[9])
                if line_list[10] == "-":
                    dst_bytes_trans = 0
                else:
                    dst_bytes_trans = int(line_list[10])
                src_bytes_ip = int(line_list[17])
                dst_bytes_ip = int(line_list[19])
                if src_bytes_ip*5 < src_bytes_trans:
                    weird_count += 1
                    # print("Abnormal: %d for IP but %d for Trans" % (src_bytes_ip, src_bytes_trans))
                    continue
                if proto == "tcp":
                    tcp_count += 1
                elif proto == "udp":
                    udp_count += 1
                elif proto == "icmp":
                    icmp_count += 1
                else:
                    non_trans_count += 1

                if src_ip.startswith("136.159."):
                    total_out += 1
                    total_out_byte_trans += src_bytes_trans
                    total_in_byte_trans += dst_bytes_trans
                    total_out_byte_ip += src_bytes_ip
                    total_in_byte_ip += dst_bytes_ip
                    proto_port_counter[proto_port_key] += 1
                elif dst_ip.startswith("136.159."):
                    total_in += 1
                    total_out_byte_trans += dst_bytes_trans
                    total_in_byte_trans += src_bytes_trans
                    total_out_byte_ip += dst_bytes_ip
                    total_in_byte_ip += src_bytes_ip
                    proto_port_counter[proto_port_key] += 1
        hour_target = filename.split("/")[-1][5:7]
        print("File Name: %s\nHour Target: %s" % (filename, hour_target))
        print("Weird Count is %d" % weird_count)
        total_weird_count += weird_count
        proto_port_counter_top = Counter(dict(proto_port_counter.most_common(100)))
        if daily_result[hour_target] is None:
            daily_result[hour_target] = {"summary": [total_in, total_out,
                                                     total_in_byte_trans, total_in_byte_ip,
                                                     total_out_byte_trans, total_out_byte_ip,
                                                     tcp_count, udp_count,
                                                     icmp_count, non_trans_count],
                                         "proto/port": proto_port_counter_top}
        else:
            summ_org = daily_result[hour_target]["summary"]
            summ_new = [total_in, total_out,
                        total_in_byte_trans, total_in_byte_ip,
                        total_out_byte_trans, total_out_byte_ip,
                        tcp_count, udp_count,
                        icmp_count, non_trans_count]
            summ_update = [value_org + value_new for value_org, value_new in zip(summ_org, summ_new)]
            proto_port_new = daily_result[hour_target]["proto/port"] + proto_port_counter_top
            daily_result[hour_target] = {"summary": summ_update,
                                         "proto/port": proto_port_new}
    for i in range(0, 24):
        hour_key = str(i).zfill(2)
        print("==>---------------------------------------------<==")
        print("Current Data and Hour: %s_%s" % (date, hour_key))
        print("Statistics Summary: %s" % daily_result[hour_key]["summary"])
        print("Proto/Port Popularity: %s" % daily_result[hour_key]["proto/port"])
        print("===================================================")
        daily_result["total"]["summary"] = [value_org + value_new for value_org, value_new in
                                            zip(daily_result["total"]["summary"],
                                                daily_result[hour_key]["summary"])]
        daily_result["total"]["proto/port"] += daily_result[hour_key]["proto/port"]
    print("==>--------------Daily Summary------------------<==")
    print("Output Daily Summary for %s" % date)
    print("Statistics Summary: %s" % daily_result["total"]["summary"])
    print("Proto/Port Popularity: %s" % daily_result["total"]["proto/port"])
    print("Total Weird Count: %s" % total_weird_count)
    print("===================================================")
    return daily_result


if __name__ == '__main__':
    total_statistics = {}
    for date in get_date_list():
        total_statistics[date] = daily_analysis(date)
    global_report = {"summary": [0, 0, 0, 0, 0, 0], "proto/port": Counter()}
    for date in get_date_list():
        summary_org = global_report["summary"]
        summary_new = total_statistics[date]["total"]["summary"]
        summary_update = [value_org + value_new for value_org, value_new in zip(summary_org, summary_new)]
        global_report["summary"] = summary_update
        global_report["proto/port"] += total_statistics[date]["total"]["proto/port"]
    print("==>--------------Global Summary------------------<==")
    # print(global_report)
    print("Here Output the Global Report")
    print("Statistics Summary: %s" % global_report["summary"])
    print("Proto/Port Popularity: %s" % global_report["proto/port"])
    print("===================================================")
    print("END OF JOB")
    # daily_analysis("2018-09-01")
    # print(get_date_list())
