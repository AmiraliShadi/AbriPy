from typing import Dict, Any, List, Optional
import json
import urllib.parse

class Request:
    """ASGI Request class"""
    
    def __init__(self, scope: Dict[str, Any], receive):
        self.scope = scope
        self.receive = receive
        self._body = None
        self._json = None
        self._form = None
        
    @property
    def method(self) -> str:
        """Get HTTP method"""
        return self.scope.get("method", "GET")
    
    @property
    def path(self) -> str:
        """Get request path"""
        return self.scope.get("path", "/")
    
    @property
    def query_string(self) -> bytes:
        """Get raw query string"""
        return self.scope.get("query_string", b"")
    
    @property
    def query_params(self) -> Dict[str, str]:
        """Get parsed query parameters"""
        if not self.query_string:
            return {}
        
        query_string = self.query_string.decode("utf-8")
        return dict(urllib.parse.parse_qsl(query_string))
    
    @property
    def headers(self) -> Dict[str, str]:
        """Get request headers as a dictionary"""
        headers = {}
        for raw_header in self.scope.get("headers", []):
            name = raw_header[0].decode("latin1").lower()
            value = raw_header[1].decode("latin1")
            headers[name] = value
        return headers
    
    @property
    def client_ip(self) -> str:
        """Get client IP address"""
        client = self.scope.get("client")
        if client:
            return client[0]
        return "127.0.0.1"
    
    @property
    def url(self) -> str:
        """Get full URL"""
        scheme = self.scope.get("scheme", "http")
        host = None
        port = None
        
        # Try to get host from headers first
        headers = self.headers
        if "host" in headers:
            host_header = headers["host"]
            if ":" in host_header:
                host, port_str = host_header.split(":", 1)
                try:
                    port = int(port_str)
                except ValueError:
                    port = None
            else:
                host = host_header
        
        # Fallback to server info
        if not host:
            server = self.scope.get("server")
            if server:
                host, port = server
        
        # Build URL
        url = f"{scheme}://{host or 'localhost'}"
        if port and ((scheme == "http" and port != 80) or (scheme == "https" and port != 443)):
            url += f":{port}"
        
        url += self.path
        if self.query_string:
            url += f"?{self.query_string.decode('utf-8')}"
        
        return url
    
    async def body(self) -> bytes:
        """Get raw request body"""
        if self._body is None:
            body_parts = []
            more_body = True
            
            while more_body:
                message = await self.receive()
                body_parts.append(message.get("body", b""))
                more_body = message.get("more_body", False)
            
            self._body = b"".join(body_parts)
        
        return self._body
    
    async def json(self) -> Any:
        """Parse request body as JSON"""
        if self._json is None:
            body = await self.body()
            if body:
                try:
                    self._json = json.loads(body.decode("utf-8"))
                except (json.JSONDecodeError, UnicodeDecodeError):
                    self._json = {}
            else:
                self._json = {}
        
        return self._json
    
    async def form(self) -> Dict[str, Any]:
        """Parse request body as form data"""
        if self._form is None:
            body = await self.body()
            if body:
                try:
                    body_str = body.decode("utf-8")
                    self._form = dict(urllib.parse.parse_qsl(body_str))
                except UnicodeDecodeError:
                    self._form = {}
            else:
                self._form = {}
        
        return self._form
    
    def get_header(self, name: str, default: str = None) -> Optional[str]:
        """Get a specific header value"""
        return self.headers.get(name.lower(), default)
    
    @property
    def content_type(self) -> Optional[str]:
        """Get content type header"""
        return self.get_header("content-type")
    
    @property
    def content_length(self) -> Optional[int]:
        """Get content length"""
        length_str = self.get_header("content-length")
        if length_str:
            try:
                return int(length_str)
            except ValueError:
                pass
        return None
    
    def __repr__(self) -> str:
        return f"<Request {self.method} {self.path}>"
