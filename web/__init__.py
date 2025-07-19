"""Web components for AbriPy Framework"""

from .request import Request
from .response import Response  # ✅ Only import Response class
from .websockets import WebSocketManager

# Create convenience functions that match the old interface
def json_response(data, status_code=200, headers=None):
    """Convenience function for creating JSON responses"""
    return Response.json(data, status_code, headers)

def html_response(content, status_code=200, headers=None):
    """Convenience function for creating HTML responses"""  
    return Response.html(content, status_code, headers)

# Export everything
__all__ = [
    'Request',
    'Response', 
    'WebSocketManager',
    'json_response',
    'html_response'
]
