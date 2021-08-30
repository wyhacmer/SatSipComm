#!/bin/bash
nohup python3 telemeter.py > log/telemeter.log 2>&1 &
nohup python3 handler.py > log/handler.log 2>&1 &
sudo systemctl start edgecore &
cat ser_run_num.txt | awk '{print $1+1 > "ser_run_num.txt"}'
