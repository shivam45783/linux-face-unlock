#!/bin/bash

echo "Installing dependencies..."

sudo apt update
sudo apt install -y python3 python3-venv cmake build-essential libopencv-dev

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

echo "Setup complete."
echo "Next step: Register your face."