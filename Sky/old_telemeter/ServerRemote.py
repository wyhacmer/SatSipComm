import os
import socket
import transFileType
import base64
from config import SatServerIp, ServerRemotePort


def ServerRemoteRun():
    address = (SatServerIp, ServerRemotePort)  # 卫星服务端地址和端口
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    flag = 0
    while flag == 0:
        trigger = transFileType.jsonTransferToBinary("Files/remote")  # trigger是二进制流
        if trigger == '###':  # 自定义结束字符串
            continue
        s.sendto(trigger, address)
        flag += 1
    s.close()
