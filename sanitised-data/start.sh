#!/bin/bash
# Install requirements
pip install -r /sanitised-data/requirements.txt

# Run the sanitised data generator script
python3 /sanitised-data/sanitised_data.py
