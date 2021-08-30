import socket
import os
import time
import json
from config import ClientAIp, ServerIp, ServerPortA


# 启动客户机
def startClientSip(data):
    startClient = os.system(r"cd F:\VirtualStudioProgram\pjproject-wyh\pjsip-apps\bin")
    startClient = os.system(r"pjsua-i386-Win32-vc14-Debug.exe")
    print(startClient)


def createJsonContent():
    ip = ClientAIp
    clientname = "clientA"
    # with open("Files/requestA", "w") as f:
    #     f.write("ip:" + ip + "\n")
    #     f.write("serverName:" + clientname + "\n")
    #     f.close()
    return "ip:" + ip + "\n" + "clientName:" + clientname + "\n"


address = (ServerIp, ServerPortA)  # 服务端地址和端口
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while True:
    trigger = createJsonContent()
    s.sendto(trigger.encode(), address)
    filename, addr = s.recvfrom(1024)  # 返回数据和接入连接的（服务端）地址
    filename = filename.decode()
    print('[Recieved]', filename)
    # time.sleep(2)
    # os.system(r"python " + filename)  # filename带py
    # # startClientSip(filename)
    # if trigger == '###':  # 自定义结束字符串
    #     break
s.close()
