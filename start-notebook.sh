#!/bin/bash
# service setup

cd lodestar-backend

source venv/bin/activate

jupyter notebook

deactivate
cd ..
bash
