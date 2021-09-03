flags = [0, 0, 0]

ServerIp = "10.112.244.60"
ServerPortA = 31500
ServerPortB = 31501

SatServerIp = "192.168.200.17"
ServerJsonPort = 31503
ServerRemotePort = 20002

ClientAIp = "10.112.244.61"
ClientBIp = "10.112.244.62"

ObcIp = "192.168.200.100"
ObcPort = 20002

remoteHeader = b'\x1a\xcf\xfc\x1d\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x17p\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

pi_ip = "192.168.200.17"  # WLAN
pi_port = 20002

download_json_content = [{
        "call": "input.py",
        "command": ["+a", "sip:1000@10.112.244.60", "sip:10.112.244.60", "*", "1000", "1000", "m", "sip:2000@10.112.244.60"]
        },
        {
        "call": "output.py",
        "command": ["+a", "sip:1000@10.112.244.60", "sip:10.112.244.60", "*", "2000", "2000", "a", "200"]
        }
    ]

lab_num = [0, 0]

ip_list = [
    "192.168.200.202"
    "192.168.200.203"
]


