import socket
import struct
import ctypes
import sys


def int2ip(net_int):
    ip_int = ctypes.c_uint(net_int)
    host_int = socket.ntohl(ip_int.value)
    return socket.inet_ntoa(struct.pack("!I", host_int))


if __name__ == '__main__':
    # print(int2ip(sys.argv[1]))
    # print((int2ip(505298698)))
    print((int2ip(-1671454454)))
