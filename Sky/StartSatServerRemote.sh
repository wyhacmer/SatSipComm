#!/bin/bash
nohup python3 TeleThread.py > log/telemeter.log 2>&1 &
nohup python3 handler.py > log/handler.log 2>&1 &
