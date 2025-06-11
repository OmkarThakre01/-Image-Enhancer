#!/bin/bash

# Install Python 3.9
curl -O https://www.python.org/ftp/python/3.9.7/Python-3.9.7.tgz
tar -xzf Python-3.9.7.tgz
cd Python-3.9.7
./configure --enable-optimizations
make -j $(nproc)
sudo make altinstall

# Create and activate virtual environment
python3.9 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt 