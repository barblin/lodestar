#!/bin/bash
# frontend start

cd lodestar-ui
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.0/install.sh | bash
source ~/.profile
export NVM_DIR="/home/johannes/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
nvm install 16.14.2
nvm use 16.14.2
yarn
yarn dev

cd ..
bash
