#!/bin/sh
# launcher.sh
# starts pigpiod and starts the clock
pigpiod
# go to folder of script
cd /home/pi/Workspace/ringclock
#start clock
python ringclock_management.py
