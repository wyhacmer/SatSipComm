import socket
import os
import time
from config import ClientBIp, ServerIp, ServerPortB

def createJsonContent():
    ip = ClientBIp
    clientname = "clientB"
    # with open("Files/requestA", "w") as f:
    #     f.write("ip:" + ip + "\n")
    #     f.write("serverName:" + clientname + "\n")
    #     f.close()
    return "ip:" + ip + "\n" + "clientName:" + clientname + "\n"


address = (ServerIp, ServerPortB)  # 服务端地址和端口
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
