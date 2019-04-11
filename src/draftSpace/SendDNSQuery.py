
import sys
import time
import dns.resolver
import csv
#
# # domain = 'www.google.com'
# # domain = 'auroralimaging.com'
# # domain = 'cpsc.ucalgary.ca'
# domain = "phys.ucalgary.ca"
# my_resolver = dns.resolver.Resolver(configure=False)
# my_resolver.nameservers = ["136.159.51.4"]
# for _ in range(0, 60):
#     try:
#         answers = my_resolver.query(domain,'NS')
#         # print(answers)
#         for server in answers:
#             print(server)
#         # print(answers.response)
#     except:
#         print("Error Info")
#     finally:
#         time.sleep(1)
#         # dns.resolver.reset_default_resolver()

def read_from_csv(file_name, m=80, n=12):
    num = []
    with open(file_name) as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            # print(line)
            line = [float(str) for str in line]
            num.append(line)
    label_list = []
    for array in num:
        label_list.append([array[-1]])
    # print(label_list)
    features = get_array_top_m_n(num, m, n)
    return features, label_list

def get_array_top_m_n(array, m, n):
    if len(array) < m:
        raise IndexError("Array does not have more than m rows")
    top_m_n_array = []
    for i in range(0, m):
        if len(array[i]) < n:
            raise IndexError("Array does not have more than n columns")
        top_m_n_array.append(array[i][0:n])
    return top_m_n_array


if __name__ == '__main__':
    a = [[1,2,3,4,5], [44,5,3,4,4,4,6], [23,4,4,56,6,7,78]]
    print(get_array_top_m_n(a, 10, 2))

