# auth/authorization.py
from typing import List, Callable, Any
from functools import wraps

def login_required(func: Callable) -> Callable:
    """Decorator to require login for a route"""
    @wraps(func)
    async def wrapper(request, *args, **kwargs):
        if not hasattr(request, 'user') or not request.user:
            from web.response import json_response
            return json_response(
                {'error': 'Authentication required'}, 
                status_code=401
            )
        return await func(request, *args, **kwargs)
    return wrapper

def require_roles(roles: List[str]) -> Callable:
    """Decorator to require specific roles"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(request, *args, **kwargs):
            if not hasattr(request, 'user') or not request.user:
                from web.response import json_response
                return json_response(
                    {'error': 'Authentication required'}, 
                    status_code=401
                )
            
            user_roles = getattr(request.user, 'roles', [])
            if not any(role in user_roles for role in roles):
                from web.response import json_response
                return json_response(
                    {'error': 'Insufficient permissions'}, 
                    status_code=403
                )
            
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator
