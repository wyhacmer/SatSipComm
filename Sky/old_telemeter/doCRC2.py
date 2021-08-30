#!/usr/bin/python

import sys
import os
from zlib import crc32
import hashlib
import binascii
import crcmod


def getcrc32(filepath):
    file = open(filepath,'rb')
    return crc32(file.read())


def getbinasciiCRC(filepath):
    with open(filepath, 'rb') as f:
        file = f.read().decode()
        file = bytes.fromhex(file)
        crc32_func = crcmod.mkCrcFun(poly=0x11EDC6F41, initCrc=0x0, rev=True, xorOut=0xffffffff)
    result = hex(crc32_func(file)).replace('0x', '')
    result = result.zfill(8)
    print("result:", result)
    return bytes.fromhex(result)

def getmd5(filepath):
    file = open(filepath,'rb')
    md5func = hashlib.md5()
    md5func.update(file.read())
    return md5func.hexdigest()


def getsha1(filepath):
    file = open(filepath,'rb')
    sha1func = hashlib.sha1()
    sha1func.update(file.read())
    return sha1func.hexdigest()


if __name__ == '__main__':
    res = getbinasciiCRC("Files/remoteInfo")
    print(res)
    # path = sys.argv[1]
    # print(sys.argv[0], "  ", path)
    # print("crc32 value:%X" % (getcrc32(path) & 0xffffffff))
    # print("binascii crc32 value:%X" % (getbinasciiCRC(path)))
    # print("md5   value:%s" % (getmd5(path)))
    # print("sha1  value:%s" % (getsha1(path)))
