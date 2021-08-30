import os
import time
import json


def handle_output_file():
    ##### 生成输出文件 #####
    download_json_content = [{
        "call": "input.py",
        "command": ["+a", "sip:1000@10.112.244.60", "sip:10.112.244.60", "*", "1000", "1000", "m",
                    "sip:2000@10.112.244.60"]
    },
        {
            "call": "output.py",
            "command": ["+a", "sip:1000@10.112.244.60", "sip:10.112.244.60", "*", "2000", "2000", "a", "200"]
        }
    ]

    with open("Files/downloadJson", "w+") as f:
        download_json_content = json.dumps(download_json_content, sort_keys=True, indent=10, separators=(',', ': '))
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
