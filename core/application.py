# Fixed imports (complete)
from typing import Dict, List, Any, Optional, Callable
from .config import Config
from .security import SecurityConfig
from web.websockets import WebSocketManager
from web.request import Request
from web.response import Response
from core.routing import Router
from core.middleware import MiddlewareManager


class AbriPy:
    """AbriPy Framework - Modern, secure web framework"""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.routes: Dict[str, Dict[str, Callable]] = {}
        self.middleware_stack = MiddlewareManager()
        self.websocket_manager = WebSocketManager()
        self.security = SecurityConfig()
        self.before_request_handlers: List[Callable] = []
        self.after_request_handlers: List[Callable] = []
        self.router = Router()  # Initialize router
        
        # Initialize security
        if self.config.security.secret_key:
            self.secret_key = self.config.security.secret_key
        else:
            import secrets
            self.secret_key = secrets.token_urlsafe(32)
    
    def route(self, path: str, methods: List[str] = None):
        """Decorator for defining routes"""
        if methods is None:
            methods = ['GET']
            
        def decorator(func: Callable):
            for method in methods:
                self.router.add_route(method, path, func)
            return func
        return decorator
    
    def get(self, path: str):
        """GET route decorator"""
        return self.route(path, ['GET'])
    
    def post(self, path: str):
        """POST route decorator"""
        return self.route(path, ['POST'])
    
    def put(self, path: str):
        """PUT route decorator"""
        return self.route(path, ['PUT'])
    
    def delete(self, path: str):
        """DELETE route decorator"""
        return self.route(path, ['DELETE'])
    
    def websocket(self, path: str):
        """WebSocket route decorator"""
        def decorator(func: Callable):
            # WebSocket handling logic here
            return func
        return decorator
    
    def middleware(self, middleware_class):
        """Add middleware"""
        self.middleware_stack.add(middleware_class)
        return middleware_class
    
    def before_request(self, func: Callable):
        """Add before request handler"""
        self.before_request_handlers.append(func)
        return func
    
    def after_request(self, func: Callable):
        """Add after request handler"""
        self.after_request_handlers.append(func)
        return func
    
    async def __call__(self, scope, receive, send):
        """ASGI interface"""
        if scope['type'] == 'http':
            await self.handle_http(scope, receive, send)
        elif scope['type'] == 'websocket':
            await self.handle_websocket(scope, receive, send)

    async def handle_http(self, scope, receive, send):
        """Handle HTTP requests"""
        # Create request object with proper ASGI parameters
        request = Request(scope, receive)
        
        # Get the path and method
        path = scope["path"]
        method = scope["method"]
        
        try:
            # Find matching route
            handler = self.router.match(path, method)
            
            if handler is None:
                # 404 Not Found
                response = Response("Not Found", status_code=404)
            else:
                # Call the handler
                result = await handler(request)
                
                # Convert result to Response if it's not already
                if isinstance(result, dict):
                    response = Response.json(result)
                elif isinstance(result, str):
                    response = Response(result)
                elif not isinstance(result, Response):
                    response = Response(str(result))
                else:
                    response = result
                    
        except Exception as e:
            # 500 Internal Server Error
            response = Response(f"Internal Server Error: {str(e)}", status_code=500)
            print(f"Error handling request: {e}")  # Debug logging
        
        # Send the response
        await response(scope, receive, send)

    async def handle_websocket(self, scope, receive, send):
        """Handle WebSocket connections"""
        # Basic WebSocket handler - you can expand this
        await send({
            'type': 'websocket.accept'
        })
    
    def run(self, host: str = None, port: int = None, debug: bool = None):
        """Run the application"""
        import uvicorn
        import sys
        import os
        
        host = host or self.config.server.host
        port = port or self.config.server.port
        debug = debug if debug is not None else self.config.server.debug
        
        print(f"🚀 Starting AbriPy Framework on {host}:{port}")
        
        if debug:
            # For development with reload, we need to pass the import string
            # Get the module name from the main script
            main_module = sys.modules['__main__']
            module_name = getattr(main_module, '__file__', None)
            
            if module_name:
                # Get the module name without .py extension
                module_name = os.path.splitext(os.path.basename(module_name))[0]
                app_string = f"{module_name}:app"
                
                print(f"🔄 Running in development mode with auto-reload")
                uvicorn.run(
                    app_string,
                    host=host,
                    port=port,
                    reload=True
                )
            else:
                # Fallback: run without reload
                print("⚠️  Cannot determine module name, running without reload")
                uvicorn.run(
                    self,
                    host=host,
                    port=port
                )
        else:
            # Production mode: run directly with the app instance
            uvicorn.run(
                self,
                host=host,
                port=port
            )
