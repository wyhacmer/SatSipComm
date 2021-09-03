import socket
import logging
import time
# TODO 修改config路径
from config import pi_port

import config

def main_socket():
    ##### 设置logging的文件和存储级别 #####
    logging.basicConfig(level=logging.INFO,
                        filename="log/telemeter_log.log",
                        filemode="w+")

    ##### 获取当前树莓派的ip #####
    hostname = socket.gethostname()
    pi_ip = socket.gethostbyname(hostname)

    ##### 初始化树莓派的socket通信 #####
    pi_address = (pi_ip, pi_port)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(pi_address)

    while True:
        now = int(time.time())
        timeArray = time.localtime(now)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        print(otherStyleTime)
        ##### 监听来自OBC的遥测请求 #####
        telemeter_req, obc_address = s.recvfrom(1024)
        # logging.info("telemeter request = %s; obc address = %s; pi address = %s", telemeter_req, obc_address, pi_address)

        ##### 判断端口是否为20002 #####
        obc_ip = obc_address[0]
        obc_port = int(obc_address[1])
        # if obc_port == 20002:
        #  pass
        # else:
        #    logging.info("obc port error")
        #   continue

        ##### 判断遥测请求是否正确 #####
        if len(telemeter_req) == 36:
            pass
        else:
            logging.info("length error: %s", str(telemeter_req))
            continue

        if telemeter_req[0:4] == b'\x1a\xcf\xfc\x1d':
            pass
        else:
            logging.info("head error: %s", str(telemeter_req))
            continue

        if telemeter_req[4:8] == b'\x00\x00\x00\x03':
            pass
        else:
            logging.info("type error: %s", str(telemeter_req))
            continue

        # TODO 6000
        if telemeter_req[12:16] == b'\x00\x00\x17\x70':
            pass
        else:
            logging.info("file number error: %s", str(telemeter_req))
            continue


        ##### 发送遥测回复给OBC #####
        obc_address = (obc_ip, 20002)
        s.sendto(config.telemeter_resp, obc_address)
        # logging.info("telemeter response = %s", config.telemeter_resp)


if __name__ == '__main__':
    main_socket()
