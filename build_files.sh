#!/bin/bash

echo "BUILD START"

# Install dependencies
python3.11.2 -m pip install -r requirements.txt

# Collect static files
python3.11.2 manage.py collectstatic --noinput --clear

# Move static files to expected output directory
mkdir -p staticfiles_build
cp -r static/* staticfiles_build/

echo "BUILD END"
