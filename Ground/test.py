import json

content = [{
            "client ip": "10.112.244.61",
            "client name": "client A",
            "server ip": "10.112.244.60",
            "server name": "server",
        },
            {
                "client ip": "10.112.244.62",
                "client name": "client B",
                "server ip": "10.112.244.60",
                "server name": "server",
            }]
content = json.dumps(content, sort_keys=True, indent=4, separators=(',', ': '))

with open("Files/uploadJson", "w+") as f:
    f.write(content)

with open("Files/downloadJson", "r") as f:
    content = f.read()
    content = json.loads(content)
    print(content[1].get("call"))
