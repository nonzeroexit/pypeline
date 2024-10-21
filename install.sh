#!/bin/bash

if [ -L "/usr/local/bin/pypeline" ]; then
    sudo rm "/usr/local/bin/pypeline"
fi

if [ -d "/usr/local/bin/pypeline_files" ]; then
    sudo rm -r "/usr/local/bin/pypeline_files"
fi

if [ "$1" == "local" ];then
    sudo cp -r src /usr/local/bin/pypeline_files
else
    wget http://github.com/nonzeroexit/pypeline/archive/master.zip -O /tmp/pypeline.zip
    unzip -o /tmp/pypeline.zip -d /tmp
    sudo cp -r /tmp/pypeline-main/src /usr/local/bin/pypeline_files
fi
cd /usr/local/bin
sudo ln -s /usr/local/bin/pypeline_files/pypeline.py pypeline
sudo chmod a+rx pypeline
bash
