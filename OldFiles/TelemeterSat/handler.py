import os
import time
from TelemeterSat.config import download_json_content


def handle_output_file():
    ##### 生成输出文件 #####
    with open("Files/downloadJson", "w+") as f:
        f.write(download_json_content)


def main_logic():
    while True:
        time.sleep(1)
        ##### 有上传无下传 #####
        if os.path.exists("Files/uploadJson") and not os.path.exists("Files/downloadJson"):
            handle_output_file()
            with open("Files/calculator", "a+") as f:
                f.write("1")
        else:
            pass


if __name__ == '__main__':
    main_logic()
