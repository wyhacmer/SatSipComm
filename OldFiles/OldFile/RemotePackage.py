import numpy

class RemotePackage:
    def __init__(self):
        self.header = b'\x1a\xcf\xfc\x1d'
        self.type = b'\x00\x00\x00\x03'
        self.seqNum = numpy.uint8(0)  # 4
        self.fileNum = b'\x00\x00\x17\x70'
        self.fileLen = b'\x00\x00\x00\x00'
        self.offset = b'\x00\x00\x00\x00\x00\x00'
        self.dataLen = b'\x00\x00\x00\x00\x00\x12'
        self.crc = bytes()

