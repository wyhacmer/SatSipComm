#!/bin/bash
tar cvf /home/ubuntu/chinamobile_upf/upf_output.tar /home/ubuntu/chinamobile_upf/testResult
timestamp=$(date +%Y%m%d-%H%M%S)
sudo chmod +x /home/ubuntu/chinamobile_upf/upf_output.tar
scp /home/ubuntu/chinamobile_upf/upf_output.tar /home/pi/beiyou/upf_output-$timestamp.tar
rm /home/ubuntu/chinamobile_upf/upf_output.tar
