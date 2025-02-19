#!/bin/bash
# Install requirements
chmod +r /sanitised-data/requirements.txt
pip install -r /sanitised-data/requirements.txt

# Run the sanitised data generator script
python3 /sanitised-data/sanitised_data.py
