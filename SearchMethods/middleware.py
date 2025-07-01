"""
Custom middleware for handling Vercel deployment issues
"""

import logging

logger = logging.getLogger(__name__)

class VercelHeaderFixMiddleware:
    """
    Middleware to handle common header issues on Vercel
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process the request before it reaches the view
        self.process_request(request)
        
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
        """Ensure response headers are properly formatted"""
        # Set standard security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        
        # Don't include CORS headers by default as they might cause issues
        # Only add them if you need cross-origin requests
        
        return response
