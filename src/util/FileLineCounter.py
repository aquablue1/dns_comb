"""
" A small script used to count the line of a given file
" By Zhengping on 2018-08-08
"""

def lineCount(filename):
    i = 0
    with open(filename, 'r') as f:
        for i, l in enumerate(f):
            pass
    return i + 1
