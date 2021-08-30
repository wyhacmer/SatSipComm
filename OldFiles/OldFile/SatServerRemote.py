from config import ServerIp, ServerRemotePort, ObcIp, ObcPort, remoteHeader
# import fcntl
import struct
import base64
import os
import time
import numpy
import socket
from RemotePackage import RemotePackage
import binascii
import doCRC2


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
    with open(address, "a") as f:
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
    remoteObject.encodeFileLen = numpy.uint(18)
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


def concatRemoteData(remoteInfo):
    result = remoteInfo + b'\x02' * 14 + b'\xff' * 1006
    return hex(result)


def concatRemotePackage(remotePackage, remoteInfo) -> bytes:
    # remoteRemain = b'\x02' * 3 + b'\xff' * 1006
    remotePackage.seqNum = remotePackage.seqNum + 1
    remotePackage = remotePackage.header + remotePackage.type + \
        int(remotePackage.seqNum).to_bytes(length=4, byteorder='big', signed=False) + remotePackage.fileNum \
        + remotePackage.fileLen + remotePackage.offset + remotePackage.dataLen + \
        remotePackage.crc
    return remotePackage + remoteInfo


def writeRemoteInfo(remoteInfo):
    with open("Files/remoteInfo", "a") as f:
        f.write(remoteInfo)
    f.close()


def SatServerRemoteRun():
    time_start = time.time()
    hostname = socket.gethostname()
    SatServerIp = socket.gethostbyname(hostname)
    print(SatServerIp)
    address = (SatServerIp, ServerRemotePort)  # OBC地址和端口
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(address)
    runtime = 0
    while True:
        remoteObject = RemoteObject()  # 新建对象
        remotePackage = RemotePackage()
        recvCtrlData, recvAddr = s.recvfrom(1024)
        print("recv: ", recvCtrlData)
        print("addr: ", recvAddr)
        # 判断内容是否正确
        if recvCtrlData == remoteHeader:
            pass
        else:
            break
        time.sleep(1)
        time_run = time.time() - time_start
        remoteFileName = "Files/remote"
        # 判断上传的文件存不存在
        if os.path.exists("Files/uploadJson") or time_run > 60:  # 超过60s发json包
            jsonFileName = "Files/downloadJson"
        else:
            jsonFileName = "Files/jsonBackup"
        remoteObject = isJsonOK(jsonFileName, remoteObject)  # 处理遥测包信息
        # 重复实验
        if 1627442047 > runtime > 600 and remoteObject.encodeFileLen == numpy.uint(18):
            remoteObject = RemoteObject()
            runtime = -1
            if os.path.exists("Files/uploadJson"):
                os.remove("Files/uploadJson")
        elif runtime != -1 and remoteObject.encodeFileLen == numpy.uint(18):
            runtime = time.time() - runtime
        elif runtime == 1 and remoteObject.encodeFileLen == numpy.uint(18):
            runtime = time.time()
        remoteInfo = transferRemoteToStr(remoteObject)  # 封装遥测包
        if writeRemoteFile(remoteFileName, str(remoteInfo)):
            try:
                send2 = int(remoteInfo)
                remoteInfo = send2.to_bytes(length=4, byteorder='big', signed=False)
                remoteInfo = concatRemoteData(remoteInfo)
                writeRemoteInfo(remoteInfo)
                remotePackage.crc = doCRC2.getbinasciiCRC("Files/remoteInfo")
                # remotePackage.crc = crc32asii(remoteInfo)
                sendToData = concatRemotePackage(remotePackage, remoteInfo)
                # print("send data: ", sendToData)
                address = (recvAddr[0], ObcPort)  # 局域网广播，防止OBC IP变动影响接收
                s.sendto(sendToData, address)
            except IOError:
                print("SENDTO ERROR")
        else:
            print("WRITE ERROR")
    s.close()


if __name__ == '__main__':
    SatServerRemoteRun()
