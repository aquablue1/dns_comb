"""
" Check if a file exists
" True if exists
" Else false
"""

import os


def isFileExist(filename):
    return os.path.isfile(filename)


if __name__ == '__main__':
    path = "../../result/ToCPSC/"
    print(isFileExist(path))