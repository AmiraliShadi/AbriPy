"""
Middleware management for AbriPy Framework
"""

from typing import List, Callable, Any

class MiddlewareManager:
    """Manages middleware stack for the framework"""
    
    def __init__(self):
        self.middleware_stack: List[Callable] = []
    
    def add(self, middleware: Callable):
        """Add middleware to the stack"""
        self.middleware_stack.append(middleware)
    
    def remove(self, middleware: Callable):
        """Remove middleware from the stack"""
        if middleware in self.middleware_stack:
            self.middleware_stack.remove(middleware)
    
    async def process_request(self, request, handler):
        """Process request through middleware stack"""
        # Simple implementation - can be expanded later
        return await handler(request)
    
    def clear(self):
        """Clear all middleware"""
        self.middleware_stack.clear()
