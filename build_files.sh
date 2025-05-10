# build_files.sh
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Create the directory referenced in vercel.json
mkdir -p staticfiles_build
cp -r staticfiles/* staticfiles_build/

# Make the script executable
chmod +x build_files.sh