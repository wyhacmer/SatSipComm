from config import ServerIp, SatServerIp, ServerRemotePort, ObcIp, ObcPort, remoteHeader
import socket, fcntl, struct
import _thread as thread
import base64
import os
import time
import numpy
import socket
from RemotePackage import RemotePackage
import binascii
import doCRC2
import transFileType


class RemoteObject:
    def __init__(self):
        self.runNum = numpy.uint8(0)
        self.hasInputFile = numpy.uint8(0)
        self.isDecode = numpy.uint8(0)
        self.isEncode = numpy.uint8(0)
        self.hasOutputFile = numpy.uint8(0)
        self.CpuTemperature = numpy.uint8(0)
        self.encodeFileLen = numpy.uint8(0)


def transferBinaryToJson(BinaryData):  # 输入其实为string类型
    binaryContent = BinaryData.encode('utf - 8')
    print(binaryContent)
    # base64转成json
    jsonContent = base64.b64decode(binaryContent)
    return jsonContent


def transferJsonToBinary(JsonData):
    binaryContent = base64.b64encode(JsonData.encode('utf - 8'))
    print(binaryContent)
    return binaryContent
    # binaryContent = str(encodestr, 'utf - 8')


def readResponseFromServer2(ResponseFromServer2):
    if os.path.getsize(ResponseFromServer2) != 0:
        with open(ResponseFromServer2, "r") as f:
            list = ''.join(f.readlines())
        binaryData = transferJsonToBinary(list)
        return binaryData
    else:
        return "###"


def writeFileFromSatToGround(data, address):
    with open(address, "w+") as f:
        f.write(data)
    f.close()


def readRemoteFile(address):
    with open(address, "r") as f:
        remoteInfo = f.read()
        return remoteInfo


def writeRemoteFile(address, remoteInfo):
    try:
        with open(address, "a") as f:
            f.write(remoteInfo)
    except IOError:
        return False
    else:
        return True


def getCPUtemperature() -> int:
    res = os.popen('vcgencmd measure_temp').readline()
    return int(float(res.replace("temp=", "").replace("'C\n", "")))


def isJsonOK(address, remoteObject):
    remoteObject.CpuTemperature = numpy.uint8(getCPUtemperature())
    if not os.path.exists(address):
        return remoteObject
    if not os.path.getsize(address) == 19:
        return remoteObject
    remoteObject.hasOutputFile = numpy.uint8(1)
    remoteObject.encodeFileLen = numpy.uint8(19)
    remoteObject.hasInputFile = numpy.uint8(1)
    remoteObject.isEncode = numpy.uint8(1)
    remoteObject.isDecode = numpy.uint8(1)
    remoteObject.runNum += 1
    print("RECEIVE JSON SUCCESSFULLY")
    return remoteObject


def transferRemoteToStr(remoteObject):
    remoteInfo = numpy.uint32(0)
    remoteInfo = numpy.uint32(remoteObject.runNum << 24) | remoteInfo
    remoteInfo = numpy.uint32(remoteObject.hasInputFile << 22) | remoteInfo
    remoteInfo = numpy.uint32(remoteObject.isDecode << 20) | remoteInfo
    remoteInfo = numpy.uint32(remoteObject.isEncode << 18) | remoteInfo
    remoteInfo = numpy.uint32(remoteObject.hasOutputFile << 16) | remoteInfo
    remoteInfo = numpy.uint32(remoteObject.CpuTemperature << 8) | remoteInfo
    remoteInfo = numpy.uint32(remoteObject.encodeFileLen) | remoteInfo
    return remoteInfo


def concatRemoteData(remoteInfo) -> bytes:
    return remoteInfo + b'\x02' * 14 + b'\xff' * 1006


def concatRemotePackage(remotePackage, remoteInfo) -> bytes:
    # remoteRemain = b'\x02' * 3 + b'\xff' * 1006
    remotePackage.seqNum = remotePackage.seqNum + 1
    remotePackage = remotePackage.header + remotePackage.type + \
        int(remotePackage.seqNum).to_bytes(length=4, byteorder='big', signed=False) + remotePackage.fileNum \
        + remotePackage.fileLen + remotePackage.offset + remotePackage.dataLen + \
        remotePackage.crc
    return remotePackage + remoteInfo


def crc2hex(crc):
    return '%08x' % (binascii.crc32(binascii.a2b_hex(crc)) & 0xffffffff)


def crc32asii(v):
    return '0x%8x' % (binascii.crc32(v) & 0xffffffff)


def writeRemoteInfo(remoteInfo):
    with open("Files/remoteInfo", "w+") as f:
        f.write(remoteInfo)
    f.close()
def get_local_ip(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    inet = fcntl.ioctl(s.fileno(), 0x8915, struct.pack("256s", ifname[:15]))
    ret = socket.inet_ntoa(inet[20:24])
    return ret
def GetLocalIPByPrefix(prefix):
    localIP = ''
    for ip in socket.gethostbyname_ex(socket.gethostname())[2]:
        if ip.startswith(prefix):
            localIP = ip
    return localIP
def SatServerRemoteRun():
    time_start = time.time()
    # hostname = socket.gethostname()
    # SatServerIp = socket.gethostbyname(hostname)
    SatServerIp = GetLocalIPByPrefix("192.168.200")
    print(SatServerIp)
    address = (SatServerIp, ServerRemotePort)  # OBC地址和端口
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(address)
    remoteObject = RemoteObject()
    remotePackage = RemotePackage()
    while True:
        recvCtrlData, recvAddr = s.recvfrom(1024)
        print("recv: ", recvCtrlData)
        print("addr: ", recvAddr)
        # TODO 判断内容是否正确
        if recvCtrlData == remoteHeader:
            pass
        else:
            break
        time.sleep(1)
        time_run = time.time() - time_start
        remoteFileName = "Files/remote"
        if time_run > 5:  # 超过60s发json包
            jsonFileName = "Files/downloadJson"
        else:
            jsonFileName = "Files/jsonBackup"
        remoteObject = isJsonOK(jsonFileName, remoteObject)  # 处理遥测包信息
        remoteInfo = transferRemoteToStr(remoteObject)  # 封装遥测包
        if writeRemoteFile(remoteFileName, str(remoteInfo)):
            try:
                send2 = int(remoteInfo)
                remoteInfo = send2.to_bytes(length=4, byteorder='big', signed=False)
                remoteInfo = concatRemoteData(remoteInfo)
                print("remoteInfo: ", remoteInfo)
                writeRemoteInfo(str(remoteInfo))
                remotePackage.crc = doCRC2.getbinasciiCRC("Files/remoteInfo").to_bytes(length=4, byteorder='big', signed=False)
                # remotePackage.crc = crc32asii(remoteInfo)
                sendToData = concatRemotePackage(remotePackage, remoteInfo)
                # print("send data: ", sendToData)
                address = (recvAddr[0], ObcPort) # 局域网广播，防止OBC IP变动影响接收
                s.sendto(sendToData, address)
            except IOError:
                print("SENDTO ERROR")
        else:
            print("WRITE ERROR")
    s.close()


# def SatServerRemoteRunBackup():
#     address = (SatServerIp, ServerRemotePort)  # 卫星服务端地址和端口
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     s.bind(address)  # 绑定服务端地址和端口
#     while True:
#         # data, addr = s.recvfrom(1024)  # 返回数据和接入连接的（客户端）地址 data是string
#         # data = str(data, 'utf - 8')
#         # if not data:
#         #     break
#         # print('[Received]', data)
#
#         # 遥测包判断
#         data = isJsonOK("Files/remote")
#
#         # TODO 处理遥测包信息
#         # writeContent = "input.py\noutput.py\n"
#         # writeFileFromSatToGround(writeContent, "Files/ResponseFromServer2")
#         ObcAddress = (ObcIp, ObcPort)
#         s2obc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         s2obc.bind(ObcAddress)
#         # send = readResponseFromServer2("Files/ResponseFromServer2")  # send = input.py\n output.py
#         send = transferJsonToBinary(data)
#         if send != "###":
#             s2obc.sendto(send, addr)  # UDP 是无状态连接，所以每次连接都需要给出目的地址
#     s.close()


if __name__ == '__main__':
    SatServerRemoteRun()