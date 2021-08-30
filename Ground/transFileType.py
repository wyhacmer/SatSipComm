import requests
import base64
import os
import json


def jsonTransferToBinary(filename):
    if os.path.getsize(filename) != 0:
        # TODO json文件转换为二进制文件格式
        with open(filename, "r") as f:
            fileContent = f.read()
        encodestr = base64.b64encode(fileContent.encode('utf - 8'))
        print(encodestr)
        binaryContent = str(encodestr, 'utf - 8')
        print(binaryContent)
        # base64转换成json（解码）
        # ww = base64.b64decode(encodestr)
        # print(str(ww, 'utf - 8'))
        with open(filename + "InBinary", "w") as f:
            f.write(binaryContent)
            f.close()
        return encodestr
    else:
        return "###"


def BinaryTransferToJson(filename):
    # TODO 二进制文件转换为json文件格式
    with open(filename, "r") as f:
        binaryContent = f.read()
    binaryContent = binaryContent.encode('utf - 8')
    print(binaryContent)
    # base64转成json
    jsonContent = base64.b64decode(binaryContent)
    with open(filename + "TransferToJson", 'w') as f:
        f.write(str(jsonContent, 'utf - 8'))
        f.close()


if __name__ == '__main__':
    jsonTransferToBinary("Files/serverFile")
    BinaryTransferToJson("Files/serverFileInBinary")
