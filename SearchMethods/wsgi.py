"""
WSGI config for SearchMethods project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SearchMethods.settings')

# Collect static files on first import (Vercel deployment)
import django
from django.core.management import execute_from_command_line
from django.conf import settings

# Initialize Django
django.setup()

# Check if we're on Vercel and static files haven't been collected
if os.environ.get('VERCEL') and not os.path.exists(settings.STATIC_ROOT):
    try:
        print("Collecting static files...")
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
        print("Static files collected successfully!")
    except Exception as e:
        print(f"Warning: Could not collect static files: {e}")

application = get_wsgi_application()

# This is for Vercel deployment
app = application
