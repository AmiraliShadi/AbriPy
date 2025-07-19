import re
from typing import Dict, Any, Callable, Optional, List, Tuple

class Router:
    """Simple router for AbriPy framework"""
    
    def __init__(self):
        self.routes: List[Tuple[str, str, Callable]] = []  # (method, pattern, handler)
        self.static_routes: Dict[str, Dict[str, Callable]] = {}  # {path: {method: handler}}
    
    def add_route(self, method: str, path: str, handler: Callable):
        """Add a route to the router"""
        method = method.upper()
        
        # Check if it's a static route (no parameters)
        if '{' not in path and '<' not in path:
            if path not in self.static_routes:
                self.static_routes[path] = {}
            self.static_routes[path][method] = handler
        else:
            # Dynamic route with parameters
            pattern = self._path_to_pattern(path)
            self.routes.append((method, pattern, handler))
    
    def match(self, path: str, method: str) -> Optional[Callable]:
        """Find a matching route handler"""
        method = method.upper()
        
        # First check static routes (faster)
        if path in self.static_routes:
            return self.static_routes[path].get(method)
        
        # Check dynamic routes
        for route_method, pattern, handler in self.routes:
            if route_method == method:
                match = re.match(pattern, path)
                if match:
                    return handler
        
        return None
    
    def _path_to_pattern(self, path: str) -> str:
        """Convert a path pattern to a regex pattern"""
        # Convert {param} or <param> to regex groups
        pattern = path
        pattern = re.sub(r'\{([^}]+)\}', r'(?P<\1>[^/]+)', pattern)
        pattern = re.sub(r'<([^>]+)>', r'(?P<\1>[^/]+)', pattern)
        pattern = f"^{pattern}$"
        return pattern
