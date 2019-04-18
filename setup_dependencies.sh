#!/bin/bash

echo "updating..."
sudo apt-get update

echo "upgrading..."
sudo apt-get upgrade -y

echo "installing dependencies"
sudo apt-get install vim build-essential cmake libopenblas-dev liblapack-dev python3-dev libatlas-base-dev libcblas-dev libhdf5-dev libhdf5-serial-dev libatlas-base-dev libjasper-dev libqtgui4 libqt4-test libasound-dev portaudio19-dev -y

pip3 install opencv-python
pip3 install sounddevice
pip3 install soundfile
pip3 install google-cloud
pip3 install google-cloud-speech

# increasing swap size
echo "Increasing swap size"
sudo ex /etc/dphys-swapfile << EOEX
    :%s/CONF_SWAPSIZE=100/CONF_SWAPSIZE=1024/g
    :x
EOEX
sudo /etc/init.d/dphys-swapfile stop
sudo /etc/init.d/dphys-swapfile start

echo "confirming new swap size"
free -m


echo "downloading dlib source"
git clone https://github.com/davisking/dlib.git
cd dlib
sudo python3 setup.py install

cd ~


# decreasing swap size
# don't leave swap large or your SD card will die quickly.

echo "Decreasing swap size"
sudo ex /etc/dphys-swapfile << EOEX
    :%s/CONF_SWAPSIZE=1024/CONF_SWAPSIZE=100/g
    :x
EOEX
sudo /etc/init.d/dphys-swapfile stop
sudo /etc/init.d/dphys-swapfile start

echo "confirming new swap size"
free -m



# echo "downloading instrumented classroom source"
# git clone https://github.com/jenni-niels/instrumented_classroom.git



