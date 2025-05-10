#!/bin/bash
# Exit on error
set -o errexit

# Use the Python executable that Vercel provides
echo "Python version:"
python3 --version

# Install dependencies using the full path to pip
echo "Installing dependencies..."
python3 -m pip install -r requirements.txt

# Collect static files
echo "Collecting static files..."
python3 manage.py collectstatic --noinput

# Create the directory referenced in vercel.json
echo "Creating staticfiles_build directory..."
mkdir -p staticfiles_build
cp -r staticfiles/* staticfiles_build/

echo "Build completed successfully!"