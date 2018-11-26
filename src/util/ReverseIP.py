"""
" Get the real IP based on reverse IP or vice verse.
" Only Accept normal IPv4 IP addresses.
" Ignore all the DNS Discovery messages and other types.
" Warning: In order to increase efficiency, all errors are ignored in this method.
" By Zhengping on 2018-08-17
"""


def getNormByReverse(reverseIP):
    return ".".join(reversed(reverseIP[:-13].split(".")))


if __name__ == '__main__':
    reverseIP = "4.2.159.136.in-addr.arpa"
    print(getNormByReverse(reverseIP))
