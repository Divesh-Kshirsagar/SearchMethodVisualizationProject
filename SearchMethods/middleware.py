"""
Custom middleware for handling Vercel deployment issues
"""

import logging
import re
import os
import mimetypes

logger = logging.getLogger(__name__)

# Ensure proper MIME types are registered
mimetypes.add_type("text/css", ".css")
mimetypes.add_type("application/javascript", ".js")
mimetypes.add_type("text/html", ".html")

class VercelHeaderFixMiddleware:
    """
    Middleware to handle common header issues on Vercel
    and fix MIME type issues for static files
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # Common static file extensions
        self.extensions = {
            '.js': 'application/javascript',
            '.css': 'text/css',
            '.html': 'text/html',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.svg': 'image/svg+xml',
        }

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
        path = request.path_info.lower()
        
        # Check if this is a static file based on the path
        if '/static/' in path:
            # Get the file extension
            _, ext = os.path.splitext(path)
            
            # Set the correct MIME type based on extension
            if ext in self.extensions:
                response['Content-Type'] = self.extensions[ext]
                
                # For debugging
                response['X-Content-Type-Override'] = f"Set to {self.extensions[ext]} for {ext}"
            
            # Remove caching headers for static files during debugging
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
        
        return response
