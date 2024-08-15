#!/bin/bash

echo "Checking for Python..."
if ! command -v python3 &> /dev/null
then
    echo "Python is not installed. Please install Python 3.11.6 or later."
    exit
fi

echo "Checking for pip..."
if ! command -v pip3 &> /dev/null
then
    echo "pip is not installed. Please install pip."
    exit
fi

echo "Installing dependencies..."
pip3 install -r requirements.txt

echo "Starting 2048 Game..."
python3 main.py
