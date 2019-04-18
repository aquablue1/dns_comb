"""
" Dedicated method to draw Query Valid/Correct/Reply Rate scatters.
" This class accepts the output files from getValidInValidResponse.py as input.
" Generates the Valid/Correct/Reply Rate scatter plots as output.
" The generated scatter plots have two dimensions, i.e. x-Ranking, y-Rate
" or x-Total Session Count, y-Rate.
" For most of the top-ranked or popular Queries, the Valid/Error/Reply Rate should be
" either very low or very high.
" Since DNS server tends to always returns return the same answer for the same queries.
" This script is used to prove our assumption.
" By Zhengping on 2019-03-04
" ------------------------------------------------------------------------------------ "
" Update Version 0.1: add the collection functions for half-responsible queries.
" Major modification happens in paint() under Line: 'elif lower_bound <= valid/total <= upper_bound:'
"
"""

import os
import math
import matplotlib.pyplot as plt
from matplotlib.markers import MarkerStyle
from collections import Counter
# import sys
# sys.path.append('/home/zhengping/DNS/DNSPythonWorkspace')
from src.util.FileReader import fileReader


class ValidRateScatter:
    def __init__(self, module_name, target, date_range, style="Rank", qualify_num=50):
        self.module_name = module_name
        self.target = target
        self.style = style
        self.date_range = {"start": date_range[0], "end": date_range[1]}
        self.ax = plt.figure().add_subplot(111)
        self.paint_length = 0
        self.qualify_num = qualify_num
        self.real_always_f = open("../../ResponseAnalysis/MediumRecord/leq50_realAlways_%s_%s.log" %
                                  (self.module_name, self.target),
                                  'w')
        self.medium_f = open("../../ResponseAnalysis/MediumRecord/leq50_medium_%s_%s.log" %
                             (self.module_name, self.target),
                             'w')
        self.never_f = open("../../ResponseAnalysis/MediumRecord/leq50_never_%s_%s.log" %
                            (self.module_name, self.target),
                            'w')
        self.real_never_f = open("../../ResponseAnalysis/MediumRecord/leq50_never_%s_%s.log" %
                            (self.module_name, self.target),
                            'w')
        self.report = [0, 0, 0, 0, 0]

    def __del__(self):
        self.medium_f.close()
        self.real_never_f.close()
        self.real_always_f.close()
        self.never_f.close()

    def _get_input_filename(self):
        src_filename = "../../ResponseAnalysis/ValidInvalidStatistics/%s_%s_%sTo%s.log" % (self.module_name,
                                                                                           self.target,
                                                                                           self.date_range["start"],
                                                                                           self.date_range["end"])

        if not os.path.isfile(src_filename):
            print("File %s does not exists! Please check." % src_filename)
            raise FileNotFoundError

        return src_filename

    def _data_loader(self):
        input_filename = self._get_input_filename()
        input_file = fileReader(input_filename)
        query_dict = {}
        for line in input_file:
            line_list = line.strip().split("\t")
            query = line_list[0]
            valid_num = int(line_list[1])
            invalid_num = int(line_list[2])
            if query not in query_dict:
                query_dict[query] = [valid_num, invalid_num]
            else:
                print("Query %s already exists in previous records. Check for it" % query)
                raise KeyError
        return query_dict

    def paint(self):
        query_dict = self._data_loader()
        query_counter = Counter()
        for query in query_dict:
            query_counter[query] = query_dict[query][0] + query_dict[query][1]
        index = 1
        x_data = []
        y_data = []
        real_always_reply = 0
        always_reply = 0
        sometimes_reply = 0
        never_reply = 0
        real_never_reply = 0
        for query_tuple in query_counter.most_common(10000):
            total = int(query_tuple[1])
            if total < self.qualify_num:
                continue
            query = query_tuple[0]
            if self.style == "Rank":
                x_data.append(index)
            elif self.style == "Count":
                x_data.append(math.log10(total))
            else:
                print("Error, illegal style code, should be (rank/count).")
                raise ValueError
            index += 1
            valid = query_dict[query][0]

            if total != 0:
                y_data.append(valid/total)
            else:
                print("Total count is zero for query %s. Please Check" % query)
                raise ZeroDivisionError
            #
            upper_bound = 0
            lower_bound = 0
            if self.module_name.startswith("in"):
                upper_bound = 0.95
                lower_bound = 1 - upper_bound
            elif self.module_name.startswith("out"):
                upper_bound = 0.9
                lower_bound = 1 - upper_bound
            if valid/total > upper_bound:
                always_reply += 1
                if valid == total:
                    real_always_reply += 1
                    self.output_real_always_traces("%s\t%s\t%s\n" % (query,
                                                                    query_dict[query][0],
                                                                    query_dict[query][1]))
            elif lower_bound <= valid/total <= upper_bound:
                sometimes_reply += 1
                self.output_medium_traces("%s\t%s\t%s\n" % (query,
                                                            query_dict[query][0],
                                                            query_dict[query][1]))
            else:
                never_reply += 1
                self.output_never_traces("%s\t%s\t%s\n" % (query,
                                                           query_dict[query][0],
                                                           query_dict[query][1]))
                if valid == 0:
                    real_never_reply += 1
                    self.output_real_never_traces("%s\t%s\t%s\n" % (query,
                                                                    query_dict[query][0],
                                                                    query_dict[query][1]))
        print("======> Start Count %s <=====" % self.module_name)
        print("Count of Always Reply is: %d" % always_reply)
        print("Count of Sometimes Reply is: %d" % sometimes_reply)
        print("Count of Never Reply is: %d" % never_reply)
        print("Count of Real Always Reply is: %d" % real_always_reply)
        print("Count of Real Never Reply is: %d" % real_never_reply)
        self.report = [always_reply, sometimes_reply, never_reply, real_always_reply, real_never_reply]
        print("==============> END <===============")
        if self.style == "Rank":
            self.paint_length = index
        elif self.style == "Count":
            self.paint_length = math.log10(query_counter.most_common(1)[0][1])
        self.ax.scatter(x_data, y_data, color=(0, 0, 1, 0.25), marker=MarkerStyle('o', 'full'), linewidths=1,
                        label="%s_%s_positive_rate" % (self.module_name, self.target))

        self.decoration()

    def decoration(self):
        if self.style == "Rank":
            self.ax.set_xlim(0, self.paint_length)
        elif self.style == "Count":
            self.ax.set_xlim(self.paint_length, math.log10(self.qualify_num))
        self.ax.set_ylim(0, 1)

        if self.style == "Count":
            self.ax.set_xticks(list(range(int(self.paint_length)+1, 0, -1)))
            self.ax.set_xticklabels(["$10^{%d}$"
                                     % exp for exp in range(int(self.paint_length)+1, 0, -1)])

        self.ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1])
        self.ax.set_yticklabels(["%d%%" % Pe for Pe in range(0, 120, 20)])

        self.ax.set_xlabel("%sing" % self.style)
        self.ax.set_ylabel("Positive Percentage")

        # Draw some auxiliary lines
        if self.module_name.startswith("in"):
            self.ax.plot([0, self.paint_length+10], [0.95, 0.95], linestyle="--",
                         color="red", linewidth=1)
            self.ax.plot([0, self.paint_length+10], [0.05, 0.05], linestyle="--",
                         color="red", linewidth=1)
        elif self.module_name.startswith("out"):
            self.ax.plot([0, self.paint_length+10], [0.90, 0.90], linestyle="--",
                         color="red", linewidth=2)
            self.ax.plot([0, self.paint_length+10], [0.1, 0.1], linestyle="--",
                         color="red", linewidth=2)
        self.ax.text(self.paint_length/10, 0.2, "Always: %d\nSometimes: %d\nNever: %d" % (
                                                                        self.report[0],
                                                                        self.report[1],
                                                                        self.report[2]),
                     color='black')
        handles, labels = plt.gca().get_legend_handles_labels()
        i = 1
        while i < len(labels):
            if labels[i] in labels[:i]:
                del (labels[i])
                del (handles[i])
            else:
                i += 1
        plt.legend(handles, labels, loc="best")

        plt.show()
        # plt.savefig("../../ResponseAnalysis/Jpg%s_ValidInvalidStatistics_top100/%s_%s_%sTo%s.jpg"
        #             % (self.style, self.module_name, self.target,
        #                self.date_range["start"], self.date_range["end"]),
        #             format='jpg')
        # plt.close()

    def output_medium_traces(self, record):
        self.medium_f.write(record)

    def output_never_traces(self, record):
        self.never_f.write(record)

    def output_real_always_traces(self, record):
        self.real_always_f.write(record)

    def output_real_never_traces(self, record):
        self.real_never_f.write(record)


if __name__ == '__main__':
    module_list = ["inakamai", "inaurora", "inphys", "incampus", "incampusNew",
                   "incpsc", "inothers", "inunknown205"]

    module_list += ["outakamai", "outcampus1", "outcampus2",
                    "outcpsc", "outothers", "outwebpax"]

    for module_name_t in module_list:
        target_t = "isValid"
        date_range_t = ["2018-09-01", "2018-09-11"]
        VRScatter = ValidRateScatter(module_name_t, target_t, date_range_t, style="Rank")
        VRScatter.paint()

