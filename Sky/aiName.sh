#!/bin/bash
tar cvf /home/ubuntu/ai_output.tar /home/ubuntu/output
timestamp=$(date +%Y%m%d-%H%M%S)
sudo chmod +x /home/ubuntu/ai_output.tar
scp /home/ubuntu/ai_output.tar /home/pi/beiyou/ai_output-$timestamp.tar
rm /home/ubuntu/ai_output.tar
