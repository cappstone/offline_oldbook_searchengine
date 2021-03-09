#!/bin/bash

# python flask launch
source backend/.venv/bin/activate
python backend/api_server.py 7000 &

# vue cli launch
cd frontend
npm run serve