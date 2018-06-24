import socket
import struct
import ctypes


def int2ip(net_int):
    ip_int = ctypes.c_uint(net_int)
    host_int = socket.ntohl(ip_int.value)
    return socket.inet_ntoa(struct.pack("!I", host_int))
