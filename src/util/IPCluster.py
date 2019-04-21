"""
" Cluster IPs which belong to the same IP set.
" According to the IP classification from IPv4 standard,
" All IP addresses from 0.0.0.0 to 254.255.255.255 are divided into five different classes, i.e.:
" Class A: 1.x.x.x to 126.x.x.x, mask: 255.0.0.0
" Class B: 128.?.x.x to 191.?.x.x, mask: 255.255.0.0
" Class C:  192.?.?.x to 223.?.?.0, mask: 255.255.255.0
" Class D: 224.?.?.? to 239.?.?.?, reserved for multicast (mask can be treated as 255.255.255.255)
" Class E: 240.?.?.? to 254.?.?.?, reserved for research (mask can be treated as 255.255.255.255)
" This script translate the IP address into their IP group based on the above rules.
" return string to identify the IP class
" By Zhengping on 2019-01-10
"""

def getIPCluster(IP):
    ipList = IP.split(".")
    ipcluster = "x.x.x.x"
    if len(ipList) == 4:
        # do find cluster
        fir = int(ipList[0])
        if 1<= fir <= 127:
            # Class A
            ipcluster = "%s.x.x.x" % ipList[0]
        elif 128 <= fir <= 191:
            # Class B
            ipcluster = "%s.%s.x.x" % (ipList[0], ipList[1])
        elif 192 <= fir <= 223:
            # Class C
            ipcluster = "%s.%s.%s.x" % (ipList[0], ipList[1], ipList[2])
        elif 224 <= fir <= 239:
            # Class D
            ipcluster = IP
        elif 240 <= fir <= 254:
            # Class D
            ipcluster = IP
    else:
        # IP format is not correct
        ipcluster = "x.x.x.x"
    return ipcluster


if __name__ == '__main__':
    ip = "173.252.85.192"
    print(getIPCluster(ip))