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
if os.environ.get('VERCEL'):
    import django
    from django.core.management import execute_from_command_line
    from django.conf import settings
    
    # Initialize Django
    django.setup()
    
    # Check if we need to collect static files
    # Skip the collectstatic step since we're using @vercel/static directly
    print("Vercel deployment detected - static files are handled separately")

application = get_wsgi_application()

# This is for Vercel deployment
app = application
