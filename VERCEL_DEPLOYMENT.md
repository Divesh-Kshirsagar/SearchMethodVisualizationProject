# Deploying to Vercel

This guide provides step-by-step instructions for deploying the Search Method Showcase Django application to Vercel.

## Prerequisites

- A Vercel account (sign up at [vercel.com](https://vercel.com))
- Git installed on your computer
- The project code pushed to a GitHub repository

## Configuration Files

The following files have been set up for Vercel deployment:

### 1. `vercel.json`

This file tells Vercel how to build and deploy your application:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "SearchMethods/wsgi.py",
      "use": "@vercel/python",
      "config": { "maxLambdaSize": "15mb", "runtime": "python3.10" }
    },
    {
      "src": "build_static.sh",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "staticfiles"
      }
    }
  ],
  "routes": [
    {
      "src": "/static/(.*)",
      "dest": "/staticfiles/$1"
    },
    {
      "src": "/(.*)",
      "dest": "SearchMethods/wsgi.py"
    }
  ],
  "env": {
    "DJANGO_SETTINGS_MODULE": "SearchMethods.settings"
  }
}
```

### 2. `build_static.sh`

A script to collect static files during deployment:

```bash
#!/bin/bash

# Install Python dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput
```

### 3. Modified `wsgi.py`

Updated to work with Vercel:

```python
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SearchMethods.settings')

application = get_wsgi_application()

# This is for Vercel deployment
app = application
```

### 4. `runtime.txt`

Specifies the Python version:

```
python-3.10.0
```

## Deployment Steps

### 1. Push Changes to GitHub

Ensure all code changes are committed and pushed to your GitHub repository:

```bash
git add .
git commit -m "Configure for Vercel deployment"
git push
```

### 2. Connect to Vercel

1. Log in to your Vercel account
2. Click "Add New..." → "Project"
3. Import your GitHub repository
4. Configure the project:
   - **Framework Preset**: Select "Other"
   - **Root Directory**: Leave as default (top level of your repo)
   - **Build Command**: Leave blank (handled by vercel.json)
   - **Output Directory**: Leave blank (handled by vercel.json)

### 3. Add Environment Variables

Add the following environment variables in the Vercel project settings:

- `DJANGO_SECRET_KEY`: Your Django secret key (the one in your .env file)
- `DEBUG`: Set to "False" for production

### 4. Deploy

Click "Deploy" and wait for the build to complete.

## Post-Deployment

### 1. Add Your Domain

In the Vercel project dashboard:

1. Go to "Settings" → "Domains"
2. Add your custom domain (if needed)

### 2. Check Logs

If there are issues, check the deployment logs in the Vercel dashboard.

### 3. Update ALLOWED_HOSTS

Make sure to update your Django `settings.py` to include your Vercel domain in `ALLOWED_HOSTS`:

```python
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'your-project.vercel.app']
```

## Local Development with Vercel

To test your Vercel configuration locally:

1. Install the Vercel CLI:
```bash
npm install -g vercel
```

2. Run the development server:
```bash
vercel dev
```

## Troubleshooting

### Static Files Not Loading

If static files aren't loading:

1. Check that `DEBUG` is set to `False` in production
2. Verify that `STATIC_URL` and `STATIC_ROOT` are correctly configured
3. Make sure the static files route in `vercel.json` matches your configuration

### Database Issues

Vercel uses serverless functions, which means:

1. The SQLite database is read-only
2. For a persistent database, use a service like PostgreSQL with a connection string

### Deployment Errors

If you encounter deployment errors:

1. Check the build logs in the Vercel dashboard
2. Verify that all dependencies are in `requirements.txt`
3. Make sure your Python version matches the one specified in `runtime.txt`
