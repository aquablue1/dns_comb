


FieldToLoc = {
    "timestamp" : 0,
    "uid"       : 1,
    "srcIP"     : 2,
    "srcPort"   : 3,
    "dstIP"     : 4,
    "dstPort"   : 5,
    "transProto": 6,
    "appProto"  : 7,
    "duration"  : 8,
    "sentByte"  : 9,
    "recvByte"  : 10,
    "endFlag"   : 11,
    #           : 12,
    #           : 13,
    #           : 14,
    #           : 15,
    #           : 16,
    #           : 17,
    #           : 18,
    #           : 19,
    #           : 20,
    #           : 21,
}

LocToField = {value:key for key, value in FieldToLoc.items()}