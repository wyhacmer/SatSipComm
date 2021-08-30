import binascii
from ctypes import *

import numpy
import socket
import fcntl, struct
from config import remoteHeader


def crc32asii(v):
    return '0x%8x' % (binascii.crc32(v) & 0xffffffff)


def crc2hex(crc):
    return '%08x' % (binascii.crc32(binascii.a2b_hex(crc)) & 0xffffffff)


def get_local_ip(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    inet = fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))
    ret = socket.inet_ntoa(inet[20:24])
    return ret


if __name__ == '__main__':
    print(get_local_ip("eth0"))
    # adder = CDLL("./crc.dll")
    # data = c_uint8(numpy.uint8(b'\xff\xff\xff\xff'))
    # length = c_uint32(8)
    # csp_crc32_memory = adder.csp_crc32_memory
    # # csp_crc32_memory.restype = c_uint8
    # crc = csp_crc32_memory(data, length)
    # adder.csp_crc32_memory.restype = c_char_p
    # str = adder.csp_crc32_memory(numpy.uint8(b'\xff\xff\xff\xff'), 8)
# print(crc32asii(remoteHeader))

# num = 0x00000013
# by = num.to_bytes(length=4, byteorder='big', signed=False)
# print(int.from_bytes(by, 'big', signed=False))
