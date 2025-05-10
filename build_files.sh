#!/bin/bash

echo "BUILD START"

# Install dependencies
python3.9 -m pip install -r requirements.txt

# Run migrations
python3.9 manage.py migrate --noinput

# Collect static files
python3.9 manage.py collectstatic --noinput --clear

# Move static files to expected output directory
mkdir -p staticfiles_build
cp -r static/* staticfiles_build/

echo "BUILD END"
