#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p reports
mkdir -p templates
mkdir -p utils
mkdir -p extractor

# Set permissions
chmod +x setup.sh 