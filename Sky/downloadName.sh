#!/bin/bash
sudo chmod +x /home/ubuntu/SatSipComm/Files/downloadJson
timestamp=$(date +%Y%m%d-%H%M%S)
scp /home/ubuntu/SatSipComm/Files/downloadJson /home/pi/beiyou/downloadJson-$timestamp
