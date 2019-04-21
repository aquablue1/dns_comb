"""
" Read a folder name and returns all the filenames under this folder that matches the searching cookie
" The search cookie usually is a date string or time string.
" By zhengping on 2018-08-09
"""

import os

class folderReader():
    def __init__(self, foldername, cookie=None):
        self.foldername = foldername
        if cookie is None:
            self.cookie = ""
        else:
            self.cookie = cookie
        self.selectedFileList = []

    def __iter__(self):
        try:
            for filename in os.listdir(self.foldername):
                if self.cookie in filename:
                    # select this filename and add its full name into selectedList
                    self.selectedFileList.append(self.foldername+"/"+filename)
        except OSError:
            print("Folder %s does not exists." % self.foldername)
        return self

    def __next__(self):
        try:
            return self.selectedFileList.pop(0)
        except IndexError:
            raise StopIteration



if __name__ == '__main__':
    foldername = "../../data/2018-03-07/inbound"
    folder = folderReader(foldername, "")
    for filename in folder:
        print(filename)