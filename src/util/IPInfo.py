"""
" Get the IP information by IP-API (http://ip-api.com/docs/api:json)
By Zhengping on 2019-01-21
"""



import sys
import urllib.request
import json
import time


def getIPInfo(ip):
    api = "http://ip-api.com/json/%s?fields=53247" % ip
    # api = "http://extreme-ip-lookup.com/json/%s" % ip
    try:
        result = urllib.request.urlopen(api).read()
        result = json.loads(result)
        print("GET IP %s, INFO %s" % (ip, result))
    except:
        print("Cannot find: %s" % api)
        return None
    time.sleep(0.3)
    return result



if __name__ == '__main__':
    ip = "205.251.197.20"
    print(getIPInfo(ip))