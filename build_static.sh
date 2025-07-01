#!/bin/bash

# This script is for Vercel static build
echo "Starting static file build process..."

# Copy static files directly (no need for pip/python as this runs in the static build environment)
mkdir -p staticfiles

# Copy all files from static directory to staticfiles
cp -r static/* staticfiles/

echo "Static files copied successfully!"
ls -la staticfiles

# Success
exit 0
