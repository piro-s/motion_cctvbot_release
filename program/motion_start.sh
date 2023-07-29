#!/bin/bash

echo "***** Start motion and cctvbot $(date +'%Y.%m.%d %H:%M:%S')." 1>>/home/_user_/motion/cctvbot.log
motion -b 1>>/home/_user_/motion/cctvbot.log 2>>/home/_user_/motion/cctvbot.log &
python3 -u /home/_user_/motion/cctvbot.py 1>>/home/_user_/motion/cctvbot.log 2>>/home/_user_/motion/cctvbot.log &