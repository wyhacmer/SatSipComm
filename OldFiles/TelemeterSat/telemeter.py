import socket
import logging
import numpy
import crcmod
import os
# TODO 修改config路径
from TelemeterSat.config import pi_port


class TelemeterSipData:
    def __init__(self):
        self.run_number = numpy.uint8(0)
        self.has_input_file = numpy.uint8(0)
        self.is_decode = numpy.uint8(0)
        self.is_encode = numpy.uint8(0)
        self.has_output_file = numpy.uint8(0)
        self.cpu_temperature = numpy.uint8(0)
        self.encode_file_len = numpy.uint8(0)

    def concat_data(self):
        sip_data = numpy.uint32(0)
        sip_data = numpy.uint32(self.run_number << 24) | sip_data
        sip_data = numpy.uint32(self.has_input_file << 22) | sip_data
        sip_data = numpy.uint32(self.is_decode << 20) | sip_data
        sip_data = numpy.uint32(self.is_encode << 18) | sip_data
        sip_data = numpy.uint32(self.has_output_file << 16) | sip_data
        sip_data = numpy.uint32(self.cpu_temperature << 8) | sip_data
        sip_data = numpy.uint32(self.encode_file_len) | sip_data
        return int(sip_data).to_bytes(length=4, byteorder='big', signed=False)


class Telemeter:
    def __init__(self):
        self.header = b'\x1a\xcf\xfc\x1d'
        self.packet_type = b'\x00\x00\x00\x03'
        self.sequence_num = numpy.uint8(0)  # 4
        self.file_num = b'\x00\x00\x17\x70'
        self.file_length = b'\x00\x00\x00\x00'
        self.data_offset = b'\x00\x00\x00\x00\x00\x00'
        self.data_length = b'\x00\x00\x00\x00\x00\x00'
        self.crc = bytes()
        self.data = b'\xff' * 1024


def get_cpu_temperature() -> int:
    ##### Ubuntu 获取cpu温度 #####
    res = os.popen('vcgencmd measure_temp').readline()
    return int(float(res.replace("temp=", "").replace("'C\n", "")))


def modify_sip_data(_telemeter_sip_data, last_lab_num):
    ##### 一轮实验结束 & 新实验重置各数据段 #####
    lab_num = os.path.getsize("Files/calculator") if os.path.exists("Files/calculator") else 0
    if lab_num != last_lab_num and not os.path.exists("Files/uploadJson") and not os.path.exists("Files/downloadJson"):
        last_lab_num = lab_num
        _telemeter_sip_data = TelemeterSipData()
        telemeter_sip_data = bytes(_telemeter_sip_data.concat_data())
        print("Round Over", _telemeter_sip_data.__dict__)
        return telemeter_sip_data, last_lab_num, _telemeter_sip_data

    ##### 遥测运行次数叠加 #####
    _telemeter_sip_data.run_number += 1

    ##### 判断是否有输入文件 #####
    if os.path.exists("Files/uploadJson"):
        _telemeter_sip_data.has_input_file = numpy.uint8(1)
    else:
        _telemeter_sip_data.has_input_file = numpy.uint8(2)

    ##### 判断encode decode是否成功(有输入就视为成功) #####
    if os.path.exists("Files/uploadJson"):
        _telemeter_sip_data.is_decode = numpy.uint8(1)
        _telemeter_sip_data.is_encode = numpy.uint8(1)
    else:
        _telemeter_sip_data.is_decode = numpy.uint8(2)
        _telemeter_sip_data.is_encode = numpy.uint8(2)

    ##### 判断是否有输出文件 #####
    if os.path.exists("Files/downloadJson"):
        _telemeter_sip_data.has_output_file = numpy.uint8(1)
    else:
        _telemeter_sip_data.has_output_file = numpy.uint8(2)

    ##### CPU温度(Windows和Ubuntu获取CPU温度方法不同) #####
    # TODO _telemeter_sip_data.cpu_temperature = numpy.uint8(get_cpu_temperature())
    _telemeter_sip_data.cpu_temperature = numpy.uint8(50)

    ##### 下传文件长度(单位为字节) #####
    try:
        _telemeter_sip_data.encode_file_len = numpy.uint8(os.path.getsize("Files/downloadJson"))
    except OSError:
        _telemeter_sip_data.encode_file_len = numpy.uint8(0)

    ##### sip data输出 #####
    print(_telemeter_sip_data.__dict__)

    telemeter_sip_data = bytes(_telemeter_sip_data.concat_data())
    return telemeter_sip_data, last_lab_num, _telemeter_sip_data


def create_telemeter(telemeter, _telemeter_sip_data, last_lab_num):
    ##### 序列号累加 #####
    telemeter.sequence_num += 1
    sequence_num_concat = int(telemeter.sequence_num).to_bytes(length=4, byteorder='big', signed=False)

    ##### 传输的文件长度 #####

    ##### 数据长度(sip + ai = 8 bit) #####
    telemeter.data_length = b'\x00\x00\x00\x08'

    ##### DATA(更新sip data) #####
    telemeter_sip_data, last_lab_num, _telemeter_sip_data = modify_sip_data(_telemeter_sip_data, last_lab_num)
    telemeter.data = telemeter_sip_data + b'\xff' * 1020

    ##### CRC(DATA 1024作为输入) #####
    crc32_func = crcmod.mkCrcFun(poly=0x11EDC6F41, initCrc=0x0, rev=True, xorOut=0xffffffff)
    _crc = hex(crc32_func(telemeter.data)).replace('0x', '').zfill(8)
    telemeter.crc = bytes.fromhex(_crc)

    resp = telemeter.header + telemeter.packet_type + sequence_num_concat + telemeter.file_num + telemeter.file_length + telemeter.data_offset + telemeter.data_length + telemeter.crc + telemeter.data
    return resp, last_lab_num, _telemeter_sip_data


def main_logic():
    ##### 设置logging的文件和存储级别 #####
    logging.basicConfig(level=logging.INFO,
                        filename="telemeter_log.log",
                        filemode="w+")

    ##### 获取当前树莓派的ip #####
    hostname = socket.gethostname()
    pi_ip = socket.gethostbyname(hostname)

    ##### 初始化树莓派的socket通信 #####
    pi_address = (pi_ip, pi_port)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(pi_address)

    ##### 初始化回复的遥测包 #####
    telemeter = Telemeter()

    ##### 初始化回复的sip数据段 #####
    _telemeterSipData = TelemeterSipData()

    ##### 初始化实验次数 #####
    last_lab_num = os.path.getsize("Files/calculator") if os.path.exists("Files/calculator") else 0

    while True:
        ##### 监听来自OBC的遥测请求 #####
        telemeter_req, obc_address = s.recvfrom(1024)
        logging.info("telemeter request = %s; obc address = %s; pi address = %s", telemeter_req, obc_address, pi_address)

        ##### 生成遥测回复 #####
        telemeter_resp, last_lab_num, _telemeterSipData = create_telemeter(telemeter, _telemeterSipData, last_lab_num)

        ##### 发送遥测回复给OBC #####
        s.sendto(telemeter_resp, obc_address)
        logging.info("telemeter response = %s", telemeter_resp)


if __name__ == '__main__':
    main_logic()
