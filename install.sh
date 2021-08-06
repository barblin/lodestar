#!/bin/bash
# service setup

sudo apt update
sudo apt upgrade
sudo apt install curl
sudo apt-get install python3.7
sudo apt-get install docker-compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version

cd lodestar-backend
python3.7 -m venv venv
source venv/bin/activate
python3.7 -m pip install -r ./requirements.txt
sudo rm -r diptest
git clone https://github.com/alimuldal/diptest.git
cd diptest
python setup.py build_ext -i -f
python setup.py install
cd ..
cd ..

deactivate
bash
