# core/server.py - Update imports
from typing import Dict, Callable, Any
# Change from relative to absolute imports:
from web.response import Response, json_response, html_response
from web.request import Request
from core.routing import Router
from core.application import AbriPy
import asyncio


class ASGIApp:
    """ASGI Application wrapper"""
    
    def __init__(self, framework: AbriPy):  # Now no quotes needed
        self.framework = framework
        self.router = Router()
        
        # ... rest of your code stays the same

        
        # Register all routes
        for path, methods in framework.routes.items():
            for method, handler in methods.items():
                self.router.add_route(path, method, handler)
    
    # ... rest of your code stays the same

    
    # ... rest of your existing code stays the same


    
    async def __call__(self, scope: Dict, receive: Callable, send: Callable):
        """ASGI application callable"""
        if scope['type'] == 'http':
            await self.handle_http(scope, receive, send)
        elif scope['type'] == 'websocket':
            await self.handle_websocket(scope, receive, send)
    
    async def handle_http(self, scope: Dict, receive: Callable, send: Callable):
        """Handle HTTP requests"""
        # Parse request
        request = await self._build_request(scope, receive)
        
        try:
            # Route matching
            match_result = self.router.match(request.path, request.method)
            
            if match_result is None:
                response = Response("Not Found", status_code=404)
            else:
                handler, params = match_result
                
                # Call handler (support both sync and async)
                if asyncio.iscoroutinefunction(handler):
                    result = await handler(request, **params)
                else:
                    result = handler(request, **params)
                
                # Convert result to Response if needed
                if isinstance(result, Response):
                    response = result
                elif isinstance(result, dict):
                    response = json_response(result)
                elif isinstance(result, str):
                    response = html_response(result)
                else:
                    response = Response(str(result))
        
        except Exception as e:
            if self.framework.config.debug:
                response = Response(f"Error: {str(e)}", status_code=500)
            else:
                response = Response("Internal Server Error", status_code=500)
        
        # Send response
        await self._send_response(response, send)
    
    async def _build_request(self, scope: Dict, receive: Callable) -> Request:
        """Build Request object from ASGI scope"""
        # Get body
        body = b''
        while True:
            message = await receive()
            if message['type'] == 'web.request':
                body += message.get('body', b'')
                if not message.get('more_body', False):
                    break
        
        # Parse headers
        headers = {}
        for name, value in scope.get('headers', []):
            headers[name.decode().lower()] = value.decode()
        
        # Parse query string
        query_params = {}
        if scope.get('query_string'):
            # Simple query string parsing
            query_string = scope['query_string'].decode()
            for param in query_string.split('&'):
                if '=' in param:
                    key, value = param.split('=', 1)
                    query_params[key] = value
        
        return Request(
            method=scope['method'],
            path=scope['path'],
            headers=headers,
            query_params=query_params,
            body=body,
            client_ip=scope.get('client', [''])[0]
        )
    
    async def _send_response(self, response: Response, send: Callable):
        """Send response via ASGI"""
        await send({
            'type': 'web.response.start',
            'status': response.status_code,
            'headers': [
                [b'content-type', response.content_type.encode()],
                *[[k.encode(), v.encode()] for k, v in response.headers.items()]
            ]
        })
        
        await send({
            'type': 'web.response.body',
            'body': response.body
        })
