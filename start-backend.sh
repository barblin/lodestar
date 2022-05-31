#!/bin/bash
# backenk start


cd lodestar-backend
source venv/bin/activate

export FLASK_APP=./app.py
flask run

deactivate
cd ..
bash
