#!/bin/bash

isrootrunning=$(whoami)
if [ "$isrootrunning" != "root" ]; then
    echo -e "Please run as root or with sudo\n "
    exit 0
fi

# update OS
sudo apt-get update -y
sudo apt-get upgrade -y

# install required packages
sudo apt-get install python3-pip software-properties-common build-essential cmake libgtk-3-dev libboost-all-dev -y

# remove firefox esr (no hook support)
sudo apt-get remove firefox-esr -y

# install firefox (old, libc error)
# sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 9BDB3D89CE49EC21
# sudo add-apt-repository ppa:mozillateam/firefox-next -y
# sudo apt-get update -y
# sudo apt-get install firefox -y

# install firefox (new, static with no updates)
sudo wget https://download-installer.cdn.mozilla.net/pub/firefox/releases/81.0b5/linux-x86_64/en-US/firefox-81.0b5.tar.bz2 -P /opt/
sudo tar xfj /opt/firefox* -C /opt/
sudo ln -s /opt/firefox/firefox /usr/local/bin/firefox

# install geckodriver
sudo wget https://github.com/mozilla/geckodriver/releases/download/v0.27.0/geckodriver-v0.27.0-linux64.tar.gz
sudo tar xvzf geckodriver-v0.27.0-linux64.tar.gz
sudo mv geckodriver /usr/bin/geckodriver

# Install social mapper and python requirements
sudo chmod -R 777 ../../social_mapper
sudo python3 -m pip install --no-cache-dir -r requirements.txt

currentdir=$(pwd)
echo ""
echo "Please enter your account credentials in $currentdir/social_mapper/social_mapper.py"
echo "Run as your normal user, not as root"

