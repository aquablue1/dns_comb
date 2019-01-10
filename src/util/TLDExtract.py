"""
" Extract and return the TLD from an URL.
" Method does not include the situation where input is not a legal URL.
" Even though in the $10 of an DNS record, it should contain a legal URL.
" But for some scanning activities, they do not assign this field with an URL.
" E.g. in some NETBIOS based scanning, *\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00 is assigned.
" In this situation, since \x00 is recognized as non-symbol in ASCII. it is simply recognized as "*"
" The idea of this function is 1. separate the url with "." then extract the last field from the
" seperated list.
"""


def getTLD(url):
    return url.split(".")[-1]


if __name__ == '__main__':
    urltest1 = "*\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    urltest2 = "www.ucalgary.ca"
    print(getTLD(urltest2))