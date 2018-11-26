"""
" Provides two maps to indicates the mapping between each field in dns file and its location
“ and vice verse.
"""

FieldToLoc = {
    "timestamp" : 0,
    "uid"       : 1,
    "srcIP"     : 2,
    "srcPort"   : 3,
    "dstIP"     : 4,
    "dstPort"   : 5,
    "proto"     : 6,
    "transID"   : 7,
    "rtt"       : 8,
    "query"     : 9,
    # ""        : 10,
    # ""        : 11,
    # ""        : 12,
    "type"      : 13,
    # ""        : 14,
    "error"     : 15,
    # ""        : 16,
    # ""        : 18,
    # ""        : 19,
    # ""        : 20,
    "answers"   : 21,
    "ttls"      : 22,
    # ""        : 23,
}

LocToField = {v: k for k, v in FieldToLoc.items()}
