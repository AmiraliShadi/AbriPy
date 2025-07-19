# testing/client.py
import asyncio
import json
from typing import Dict, Any, Optional
from web.request import Request
from web.response import Response

class TestClient:
    """Test client for AbriPy applications"""
    
    def __init__(self, app):
        self.app = app
    
    async def get(self, path: str, headers: Dict[str, str] = None) -> Response:
        """Make GET request"""
        return await self._request('GET', path, headers=headers)
    
    async def post(self, path: str, data: Any = None, json_data: Dict = None, 
                   headers: Dict[str, str] = None) -> Response:
        """Make POST request"""
        return await self._request('POST', path, data=data, json_data=json_data, headers=headers)
    
    async def put(self, path: str, data: Any = None, json_data: Dict = None,
                  headers: Dict[str, str] = None) -> Response:
        """Make PUT request"""
        return await self._request('PUT', path, data=data, json_data=json_data, headers=headers)
    
    async def delete(self, path: str, headers: Dict[str, str] = None) -> Response:
        """Make DELETE request"""
        return await self._request('DELETE', path, headers=headers)
    
    async def _request(self, method: str, path: str, data: Any = None, 
                      json_data: Dict = None, headers: Dict[str, str] = None) -> Response:
        """Make HTTP request"""
        headers = headers or {}
        
        # Prepare body
        body = b''
        if json_data:
            body = json.dumps(json_data).encode()
            headers['Content-Type'] = 'application/json'
        elif data:
            if isinstance(data, str):
                body = data.encode()
            elif isinstance(data, bytes):
                body = data
        
        # Create request
        request = Request(
            method=method,
            path=path,
            headers=headers,
            query_params={},
            body=body,
            client_ip='127.0.0.1'
        )
        
        # Process request through app
        # This is a simplified version - in reality you'd need to go through the full ASGI flow
        return await self._process_request(request)
    
    async def _process_request(self, request: Request) -> Response:
        """Process request through application"""
        # Find matching route
        for route_path, methods in self.app.routes.items():
            if request.method in methods:
                handler = methods[request.method]
                
                # Simple path matching (would need proper routing in real implementation)
                if route_path == request.path:
                    if asyncio.iscoroutinefunction(handler):
                        result = await handler(request)
                    else:
                        result = handler(request)
                    
                    if isinstance(result, Response):
                        return result
                    elif isinstance(result, dict):
                        return Response(json.dumps(result), content_type='application/json')
                    else:
                        return Response(str(result))
        
        return Response("Not Found", status_code=404)
