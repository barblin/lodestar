#!/bin/bash
# service setup

cd lodestar-backend

source venv/bin/activate
pip install -r requirements.txt

jupyter notebook

deactivate
cd ..
bash
