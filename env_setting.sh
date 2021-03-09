#!/bin/bash 

# Python enviornment setup
apt install python3 python3-pip python3-venv
python3 -m venv backend/.venv
source backend/.venv/bin/activate && pip install -r backend/requirements.txt

# node.js & vue_cli setup
apt install npm
npm install -g vue-cli
cd frontend && npm install
cd ..
