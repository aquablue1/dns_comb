


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
    "local_orig"           : 12,
    "local_resp"           : 13,
    "missed_bytes"           : 14,
    "history"           : 15,
    "ipSentPack"           : 16,
    "ipSentByte"           : 17,
    "ipRecvPack"           : 18,
    "ipRecvByte"           : 19,
    #           : 20,
    #           : 21,
}

LocToField = {value:key for key, value in FieldToLoc.items()}