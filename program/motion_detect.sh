#!/bin/bash


camera_name=$1
image_filename=$2

echo "----- Motion event $(date +'%Y.%m.%d %H:%M:%S') on camera $camera_name" 1>>/home/_user_/motion/cctvbot.log
python3 /home/_user_/motion/event_change.py $image_filename 1>>/home/_user_/motion/cctvbot.log 2>>/home/_user_/motion/cctvbot.log