#!/bin/bash
# service setup

sudo apt update
sudo apt upgrade
sudo apt install curl
sudo apt install python3.7
sudo apt install python3-venv
sudo apt install python3.7-dev
sudo apt-get install docker-compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version

cd lodestar-backend
python3 -m venv venv
source venv/bin/activate
sudo python3.7 -m pip install -r ./requirements.txt
sudo rm -r diptest
git clone https://github.com/alimuldal/diptest.git
cd diptest
sudo python3.7 setup.py build_ext -i -f
sudo python3.7 setup.py install
cd ..
cd ..

deactivate
bash
