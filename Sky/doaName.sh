#!/bin/bash
tar cvf /home/ubuntu/DOA/doa_output.tar /home/ubuntu/DOA/output
timestamp=$(date +%Y%m%d-%H%M%S)
sudo chmod +x /home/ubuntu/DOA/doa_output.tar
scp /home/ubuntu/DOA/doa_output.tar /home/pi/beiyou/doa_output-$timestamp.tar
rm /home/ubuntu/DOA/doa_output.tar
