
import socket


def getNameByIP(ip):
    name = None
    try:
        name = socket.gethostbyaddr(ip)
    except socket.herror:
        print("Host name for IP: %s is not found" % ip)
    return name


if __name__ == '__main__':
    ip = "185.35.62.14"
    ip = "8.8.8.8"
    getNameByIP(ip)