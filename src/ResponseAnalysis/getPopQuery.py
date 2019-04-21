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

    def pop_count(self):
        query_dict = self._data_loader()
        query_counter = Counter()
        for query in query_dict:
            query_counter[query] = query_dict[query][0] + query_dict[query][1]
        return query_counter

    def paint(self):
        query_counter = self.pop_count()
        index = 1
        x_data = []
        y_data = []
        for query_tuple in query_counter.most_common():
            x_data.append(index)
            index += 1
            y_data.append(query_tuple[1])
        log_x_data = [math.log10(x) for x in x_data]
        log_y_data = [math.log10(y) for y in y_data]
        plt.scatter(log_x_data, log_y_data, marker="x", color="black", linewidths=1)

        plt.xlim((0, 6.5))
        plt.ylim((0, 6))
        plt.xticks([0, 1, 2, 3, 4, 5, 6, 7],
                   ["$10^{0}$", "$10^{1}$", "$10^{2}$", "$10^{3}$", "$10^{4}$", "$10^{5}$", "$10^{6}$", "$10^{7}$"])
        plt.yticks([0, 1, 2, 3, 4, 5, 6],
                   ["$10^{0}$", "$10^{1}$", "$10^{2}$", "$10^{3}$", "$10^{4}$", "$10^{5}$", "$10^{6}$"])

        plt.xlabel("Rank of Queried Names")
        plt.ylabel("Number of Connections")

        plt.show()


if __name__ == '__main__':
    module_list = ["inakamai", "inaurora", "inphys", "incampus", "incampusNew",
                   "incpsc", "inothers", "inunknown205"]

    module_list += ["outakamai", "outcampus1", "outcampus2",
                    "outcpsc", "outothers", "outwebpax"]

    module_list = ["inakamai", "incpsc", "incampus", "outakamai", "outcpsc", "outcampus1"]
    for module_name_t in module_list:
        target_t = "isValid"
        date_range_t = ["2018-09-03", "2018-09-10"]
        VRScatter = ValidRateScatter(module_name_t, target_t, date_range_t, style="Rank")
        VRScatter.paint()

