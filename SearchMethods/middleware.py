"""
Custom middleware for handling Vercel deployment issues
"""

import logging
import re
import os
from django.http import HttpResponse

logger = logging.getLogger(__name__)

class VercelHeaderFixMiddleware:
    """
    Middleware to handle common header issues on Vercel
    and fix MIME type issues for static files
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # Compile regex for static file extensions
        self.js_re = re.compile(r'\.js$')
        self.css_re = re.compile(r'\.css$')
        self.html_re = re.compile(r'\.html$')

    def __call__(self, request):
        # Process the request before it reaches the view
        self.process_request(request)
        
        # Get response
        response = self.get_response(request)
        
        # Process the response before it's sent
        return self.process_response(request, response)
    
    def process_request(self, request):
        """Clean up any problematic headers"""
        # Check for problematic headers in request.META
        problematic_headers = []
        
        for header_name, value in request.META.items():
            if header_name.startswith('HTTP_'):
                try:
                    # Test encoding to UTF-8 to catch any problematic characters
                    if isinstance(value, str):
                        value.encode('utf-8')
                except UnicodeEncodeError:
                    problematic_headers.append(header_name)
        
        # Remove problematic headers
        for header in problematic_headers:
            if header in request.META:
                logger.warning(f"Removing problematic header: {header}")
                del request.META[header]
    
    def process_response(self, request, response):
        """Ensure response headers are properly formatted and fix MIME types for static files"""
        # Set standard security headers
        response['X-Content-Type-Options'] = 'nosniff'
        
        # Fix MIME types for static files
        if os.getenv('VERCEL') and 'Content-Type' in response:
            path = request.path_info
            
            # Fix JavaScript files
            if self.js_re.search(path):
                response['Content-Type'] = 'application/javascript'
                
            # Fix CSS files
            elif self.css_re.search(path):
                response['Content-Type'] = 'text/css'
                
            # Fix HTML files
            elif self.html_re.search(path):
                response['Content-Type'] = 'text/html; charset=utf-8'
        
        return response
