import socket
import struct


def int2ip(addr):
    return socket.inet_ntoa(struct.pack("!I", addr))