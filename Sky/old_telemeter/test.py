import numpy

class TelemeterAiData:
    def __init__(self):
        self.state = numpy.uint8(0)
        self.cpu = numpy.uint8(0)
        self.run_number = numpy.uint8(0)
        self.output_file_number = numpy.uint8(0)
        self.crc = numpy.uint8(0)

    def concat_data(self):
        ai_data = numpy.uint8(0)
        ai_data = numpy.uint8(self.state << 7) | ai_data
        ai_data = numpy.uint8(self.cpu) | ai_data
        # ai_data = numpy.uint32(self.run_number << 16) | ai_data
        # ai_data = numpy.uint32(self.output_file_number << 8) | ai_data
        # ai_data = numpy.uint32(self.crc) | ai_data
        return int(ai_data).to_bytes(length=1, byteorder='big', signed=False)

if __name__ == '__main__':
    a = TelemeterAiData()
    a.state = numpy.uint8(0)
    a.cpu = numpy.uint8(13)
    result = a.concat_data()
    res = result.hex()
    print(res)
