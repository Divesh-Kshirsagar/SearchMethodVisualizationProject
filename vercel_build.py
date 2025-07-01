#!/usr/bin/env python3
"""
Build script for Vercel deployment.
This script handles static file collection for Django on Vercel.
"""

import os
import subprocess
import sys

def main():
    print("Starting Vercel build process...")
    
    # Set the Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SearchMethods.settings')
    
    try:
        # Install requirements
        print("Installing requirements...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
        
        # Collect static files
        print("Collecting static files...")
        subprocess.run([sys.executable, 'manage.py', 'collectstatic', '--noinput'], check=True)
        
        print("Build completed successfully!")
        
    except subprocess.CalledProcessError as e:
        print(f"Build failed with error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error during build: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
