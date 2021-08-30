import base64
import os
from config import remoteHeader
import time
import SatServerRemote

def a():
    b = os.path.getsize("Files/json")
    print(b)
    c = b'\x02' * 3
    print(c)

def u():
    i = remoteHeader + b'\xff\xff\x00\x00'
    print(i)

if __name__ == '__main__':
    # t = time.time()
    # print(t)
    # for i in range(3):
    #     time.sleep(1)
    # print(time.time() - t)

    a = bytes(1)
    print(a)

    # time_start = time.time()
    # with open("Files/ResponseFromServer2", "r") as f:
    #     print(len("input.py\noutput.py\n"))
    #     print(os.path.getsize("Files/ResponseFromServer2"))
    #     list = ''.join(f.readlines())
    #     list = base64.b64encode(list.encode('utf - 8'))
    #     print(list)
    #     output = base64.b64decode(list)
    #     print(type(output))
    #     output = str(output, 'utf - 8')
    #     print(output)
    # for i in range(10000000):
    #     pass
    # time_run = time.time() - time_start
    # print("time: ", time_run)
    # with open("Files/ResponseFromServer2", "r") as f:
    #     jsonData = f.read()
    #     binaryData = SatServerRemote.transferJsonToBinary(jsonData)
    # with open("Files/downloadJson", "a") as f:
    #     f.write(str(binaryData))
    # f.close()