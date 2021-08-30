import socket,os
import time
import json
import _thread as thread
import config
from config import ServerIp, ServerPortB


def readFile(filecontent):
    with open("Files/serverFile", "a+") as f:
        f.read()
        f.write(str(filecontent))


def readResponseFromServer2(ResponseFromServer2):
    if os.path.getsize(ResponseFromServer2) != 0:
        with open(ResponseFromServer2, "r") as f:
            content = f.read()
            content = json.loads(content)
            return content[1].get("call")
    else:
        return "###"


def ServerBRun():
    address = (ServerIp, ServerPortB)  # 服务端地址和端口
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(address)  # 绑定服务端地址和端口
    while True:
        data, addr = s.recvfrom(1024)  # 返回数据和接入连接的（客户端）地址
        data = data.decode()

        if not data:
            break
        print('[Received]', data)

        # tempDataRcvFromB = "ClientB:" + data
        #thread.start_new_thread(readFile, (data.encode('utf - 8'),))
        # TODO 写入上传文件
        # with open("Files/uploadJson", "a+") as f:
        #     f.write(data)
        #     f.close()

        while True:
            if os.path.exists("Files/downloadJson"):
                config.flags[1] = 1
                config.flags = [config.flags[0], config.flags[1]]
                break
            print("wait for file")
        print("Server B ", config.flags)
        time.sleep(2)
        while True:
            if config.flags[0] == 1:
                send = readResponseFromServer2("Files/downloadJson")
                if send != "###":
                    s.sendto(send.encode(), addr)  # UDP 是无状态连接，所以每次连接都需要给出目的地址
    s.close()

if __name__ == '__main__':
    ServerBRun()
