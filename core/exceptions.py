# core/exceptions.py
"""
AbriPy Framework Exceptions
"""

class AbriPyException(Exception):
    """Base AbriPy framework exception"""
    status_code = 500
    message = "Internal server error"

class RouteNotFound(AbriPyException):
    """Raised when a route is not found"""
    status_code = 404
    message = "Route not found"

class ValidationError(AbriPyException):
    """Raised when validation fails"""
    status_code = 400
    message = "Validation error"

class AuthenticationError(AbriPyException):
    """Raised when authentication fails"""
    status_code = 401
    message = "Authentication required"

class PermissionError(AbriPyException):
    """Raised when permission is denied"""
    status_code = 403
    message = "Permission denied"

class MethodNotAllowed(AbriPyException):
    """Raised when HTTP method is not allowed"""
    status_code = 405
    message = "Method not allowed"
