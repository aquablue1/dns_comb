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
"""

import os
import sys
import math
import matplotlib.pyplot as plt
from collections import Counter
sys.path.append('/home/zhengping/DNS/DNSPythonWorkspace')
from src.util.FileReader import fileReader


class ValidRateScatter:
    def __init__(self, module_name, target, date_range, style="Rank", qualify_num=10):
        self.module_name = module_name
        self.target = target
        self.style = style
        self.date_range = {"start": date_range[0], "end": date_range[1]}
        self.ax = plt.figure().add_subplot(111)
        self.paint_length = 0
        self.qualify_num = qualify_num

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
        for query_tuple in query_counter.most_common():
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
            # if 0.3 < valid/total < 0.8:
            #     print("%s - %s" % (query, query_dict[query]))
        if self.style == "Rank":
            self.paint_length = index
        elif self.style == "Count":
            self.paint_length = math.log10(query_counter.most_common(1)[0][1])
        self.ax.scatter(x_data, y_data, color="black", marker="x", linewidths=1,
                        label="%s_%s_positive_rate" % (self.module_name, self.target))

        self.decoration()

    def decoration(self):
        if self.style == "Rank":
            self.ax.set_xlim(self.qualify_num, self.paint_length)
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
            self.ax.plot([0, self.paint_length+10], [0.98, 0.98], linestyle="--",
                         color="black", linewidth=1)
            self.ax.plot([0, self.paint_length+10], [0.02, 0.02], linestyle="--",
                         color="black", linewidth=1)
        elif self.module_name.startswith("out"):
            self.ax.plot([0, self.paint_length+10], [0.90, 0.90], linestyle="--",
                         color="black", linewidth=2)
            self.ax.plot([0, self.paint_length+10], [0.1, 0.1], linestyle="--",
                         color="black", linewidth=2)

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
        # plt.savefig("../../ResponseAnalysis/Fig%s_ValidInvalidStatistics/%s_%s_%sTo%s.pdf"
        #             % (self.style, self.module_name, self.target,
        #                self.date_range["start"], self.date_range["end"]),
        #             format='pdf')
        # plt.close()


if __name__ == '__main__':
    module_list = ["inakamai", "inaurora", "inphys", "incampus", "incampusNew",
                   "incpsc", "inothers", "inunknown205"]

    module_list += ["outakamai", "outcampus1", "outcampus2",
                    "outcpsc", "outothers", "outwebpax"]

    for module_name_t in module_list:
        target_t = "isError"
        date_range_t = ["2018-09-01", "2018-09-11"]
        VRScatter = ValidRateScatter(module_name_t, target_t, date_range_t, style="Count")
        VRScatter.paint()

