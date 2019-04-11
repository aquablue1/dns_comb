"""
" This script aims to get the statistics of Error/NoError, valid/invalid, Reply/NoReply DNS message in each DNS Module.
" *NoError* means the DNS reply contains the NOERROR for session status,
" *Error* means the DNS reply has some errors, e.g. MXDOMAIN.
" *VALID* means the DNS response is visible in Bro log.
" *INVALID* means the response and TTL fields are both a dash ("-"), which means no response is witnessed
" or Bro cannot understand it.
" *Reply* means the response size is non-zero, at least there is some responded content in IP layer.
" *NoReply* means even in IP layer, there is no data size info witnessed.
" This script accept the data from structNew as input,
" analysis the response status in each Module.
" For each Module, it outputs three report files namely:
" ModuleName_isError_TimeRange.log,
" ModuleName_isValid_TimeRange.log and,
" ModuleName_isReply_TimeRange.log.
" valid and invalid -response corresponds to the valid and invalid we have mentioned above.
" the mix-response indicates for one certain queried name, both response and non-response is witnessed.
" For valid and invalid -response files, it records
" 1. queried name,
" 2. number of occurrence, (no_error count (from dns), valid (from dns), invalid (from dns),
                            non-request (from conn), non-response (from conn))
" 3. issued inner DNS Server.
" For mix-response files, it records both missed occurrence and caught occurrence.
" By Zhengping on 2019-03-03, Updated on 2019-03-04
"""

import sys
import os
import json
import datetime
from collections import Counter
sys.path.append('/home/zhengping/DNS/DNSPythonWorkspace')
from src.util.FolderReader import folderReader


class ResponseLoader:
    def __init__(self, module_list=None, date_range=None):
        self.module_list = module_list
        if date_range:
            self.date_range = {"start": date_range[0], "end": date_range[1]}
        else:
            self.date_range = {"start": "2015-01-01", "end": "2019-12-31"}

    def _get_folders_for_module(self, module_name):
        target_daily_folders = []
        module_folder_name = "../../structNew/%s" % module_name
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

    def _get_output_for_module(self, target, module_name):
        output_name = "../../ResponseAnalysis/ValidInvalidStatistics/%s_%s_%sTo%s.log" % (module_name, target,
                                                                                          self.date_range["start"],
                                                                                          self.date_range["end"])
        print(os.path.dirname(output_name))
        if not os.path.exists(os.path.dirname(output_name)):
            os.makedirs(os.path.dirname(output_name))
        return output_name

    # @staticmethod
    # def _get_files_for_module(daily_folder_name):
    #     daily_folder = folderReader(daily_folder_name)
    #     hourly_file_name_list = []
    #     for hourly_file_name in daily_folder:
    #         hourly_file_name_list.append(hourly_file_name)
    #     return hourly_file_name_list

    @staticmethod
    def hourly_collector(hourly_filename):
        with open(hourly_filename, 'r') as f:
            hourly_src = json.load(f)
        no_error_count = Counter()
        error_count = Counter()
        valid_count = Counter()
        invalid_count = Counter()
        reply_count = Counter()
        non_reply_count = Counter()
        for uid in hourly_src:
            dns_list = hourly_src[uid]["dns"]
            conn_list = hourly_src[uid]["conn"]
            if not dns_list:
                continue
            for dns_record in dns_list:
                qname = dns_record[2]+"/"+dns_record[5]
                # Check for response field in DNS log, "-" means invalid, otherwise valid
                if dns_record[3] == "-":
                    invalid_count[qname] += 1
                else:
                    valid_count[qname] += 1
                # Check for error field in DNS log. "NOERROR" means no error, otherwise error happens.
                if dns_record[6] == "NOERROR":
                    no_error_count[qname] += 1
                else:
                    error_count[qname] += 1
                # Check for response Size in IP-layer. "-" or 0 if no response, otherwise has response.
                if conn_list[6] == "-" or int(conn_list[6]) == 0:
                    non_reply_count[qname] += 1
                else:
                    reply_count[qname] += 1
        return {"no_error": no_error_count,
                "error": error_count,
                "valid": valid_count,
                "invalid": invalid_count,
                "reply": reply_count,
                "no_reply": non_reply_count}

    @staticmethod
    def daily_collector(daily_folder_name):
        daily_folder = folderReader(daily_folder_name)
        daily_statistics = {"no_error": Counter(), "error": Counter(),
                            "valid": Counter(), "invalid": Counter(),
                            "reply": Counter(), "no_reply": Counter()}
        for hourly_filename in daily_folder:
            hourly_statistics = ResponseLoader.hourly_collector(hourly_filename)
            for key in daily_statistics:
                daily_statistics[key] += hourly_statistics[key]

        return daily_statistics

    def executor(self, specify_module=None):
        if specify_module:
            module_name = specify_module
            print("Start Module: %s. At: %s" % (module_name, datetime.datetime.now()))
            module_statistics = {"no_error": Counter(), "error": Counter(),
                                 "valid": Counter(), "invalid": Counter(),
                                 "reply": Counter(), "no_reply": Counter()}
            daily_folder_name_list = self._get_folders_for_module(module_name)
            for daily_folder_name in daily_folder_name_list:
                daily_statistics_dict = ResponseLoader.daily_collector(daily_folder_name)
                for key in module_statistics:
                    module_statistics[key] += daily_statistics_dict[key]

            module_output_filename = self._get_output_for_module("isError", module_name)
            # Write to ISError files.
            with open(module_output_filename, 'w') as f:
                for key in set(module_statistics["no_error"]+module_statistics["error"]):
                    qname_info = "%s\t%d\t%d\n" % (key,
                                                   module_statistics["no_error"][key],
                                                   module_statistics["error"][key])
                    f.write(qname_info)
            # write to ISValid files.
            module_output_filename = self._get_output_for_module("isValid", module_name)
            with open(module_output_filename, 'w') as f:
                for key in set(module_statistics["valid"]+module_statistics["invalid"]):
                    qname_info = "%s\t%d\t%d\n" % (key,
                                                   module_statistics["valid"][key],
                                                   module_statistics["invalid"][key])
                    f.write(qname_info)
            # Write to ISReply files
            module_output_filename = self._get_output_for_module("isReply", module_name)
            with open(module_output_filename, 'w') as f:
                for key in set(module_statistics["reply"]+module_statistics["no_reply"]):
                    qname_info = "%s\t%d\t%d\n" % (key,
                                                   module_statistics["reply"][key],
                                                   module_statistics["no_reply"][key])
                    f.write(qname_info)
            print("Finish Module: %s. At: %s" % (module_name, datetime.datetime.now()))
        else:
            for module_name in self.module_list:
                self.executor(module_name)


if __name__ == '__main__':
    module_list_t = ["inakamai", "inaurora", "incampus", "incampusNew",
                     "incpsc", "inothers", "inphys", "inunknown205"]
    module_list_t += ["outakamai", "outcampus1", "outcampus2",
                      "outcpsc", "outothers", "outwebpax"]
    module_name_t = ["incpsc", "incampus", "inakamai", "outakamai", "outcampus1", "outcpsc"]
    # module_list_t = ["inaurora"]

    date_range_t = ["2018-09-03", "2018-09-10"]
    rl = ResponseLoader(module_list_t, date_range_t)
    print("======== Start Execution =========")
    for module_name_t in module_list_t:
        rl.executor(module_name_t)
    print("======== All Job Done =========")
