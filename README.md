# Tracker 
Simple python script that keeps an eye on the files and executes requested shell commands if any of the tracked files got modified. Simplified version of **fswatch** (https://github.com/emcrisostomo/fswatch)

## Installation
1.  `git clone git@gitlab.nat.bt.com:611788519/file-tracker.git`
2.  `cd file-tracker`
3.  `cp config.ini.example config.ini`
4.  Add directories, where you will place files, which need to be tracked
5.  Change update interval as required - default 5 seconds, ie every 5 seconds script checks if tracked files have been modified
6.  Add shell commands, that should be executed when any of the files has been changed

## How to run
1.  To run script execute `python tracker.py -s config.ini`
2.  To run script in background execute `nohup python tracker.py -s config.ini &`
