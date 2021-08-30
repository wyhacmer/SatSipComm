#!/usr/bin/python
import crcmod


def getbinasciiCRC(filepath):
    with open(filepath, 'rb') as f:
        file = f.read().decode()
        file = bytes.fromhex(file)
        print("file:", file)
        crc32_func = crcmod.mkCrcFun(poly=0x11EDC6F41, initCrc=0x0, rev=True, xorOut=0xffffffff)
    # result = hex(crc32_func(file))[2:]
    result = hex(crc32_func(file)).replace('0x', '')
    result = result.zfill(8)
    return bytes.fromhex(result)


def test():
    # a = 0xeb900100010100000000000001000100002600000000000700000000094000
    str1 = "123456789"
    print(str1.encode())
    # a = 4812730177
    # print(hex(a))
    crc32_func = crcmod.mkCrcFun(poly=0x11EDC6F41, initCrc=0x0, rev=True, xorOut=0xffffffff)
    # crc32_func = crcmod.predefined.mkCrcFun("crc-32")
    print(hex(crc32_func(str1.encode())))


if __name__ == '__main__':
    test()
    res = getbinasciiCRC("Files/json")
    print(res)
