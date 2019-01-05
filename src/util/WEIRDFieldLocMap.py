"""
" Provides two maps to indicates the mapping between each field in weird file and its location
“ and vice verse.
"""


FieldToLoc = {
    "timestamp" : 0,
    "uid"       : 1,
    "srcIP"     : 2,
    "srcPort"   : 3,
    "dstIP"     : 4,
    "dstPort"   : 5,
    "weirdName"     : 6,
    "addl"   : 7,
    "notice"       : 8,
    "peer"     : 9,
}

LocToField = {v: k for k, v in FieldToLoc.items()}
