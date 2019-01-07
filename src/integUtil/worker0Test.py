"""
" A general test worker
" By Zhengping on 2019-01-06
"""


def doTask(filename=None):
    print(filename)
    return [10, 20]


if __name__ == '__main__':
    filename = "../helloworld"
    doTask(filename)