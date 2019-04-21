"""
" Class used to write files to a/multiple files.
" By Zhengping on 2019-01-04
"""


import os, errno


class fileWriter():
    def __init__(self, filename, isOverWrite=False):
        self.filename = filename
        try:
            if not isOverWrite:
                    self.outF = open(self.filename, 'a')
            else:
                self.outF = open(self.filename, 'w')
        except IOError as ioE:
            print(ioE)

    def writeString(self, string):
        self.outF.write(string)
        return True

    def close(self):
        self.outF.close()


# class batchFileWriter():
#     def __init__(self, foldername):
#         self.foldername = foldername
#
#     def writeString(self, filename, string, isOverWrite=False):
#         fullFilename = self.foldername + "/" + filename
#         if isOverWrite:
#             try:
#                 os.remove(fullFilename)
#             except OSError as osE:
#                 if osE.errno != errno.ENOENT:
#                     raise
#         with open(fullFilename, 'a') as outF:
#             outF.write(string)
#         return True
