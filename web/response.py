import json
from typing import Any, Dict, Optional, Union

class Response:
    """HTTP Response class"""
    
    def __init__(
        self, 
        content: Union[str, bytes, dict] = "", 
        status_code: int = 200, 
        headers: Optional[Dict[str, str]] = None,
        media_type: Optional[str] = None
    ):
        self.content = content
        self.status_code = status_code
        self.headers = headers or {}
        self.media_type = media_type
        
        # Set content type if not provided
        if media_type and "content-type" not in self.headers:
            self.headers["content-type"] = media_type
    
    async def __call__(self, scope, receive, send):
        """ASGI interface for sending response"""
        # Prepare the body
        if isinstance(self.content, dict):
            body = json.dumps(self.content).encode("utf-8")
            if "content-type" not in self.headers:
                self.headers["content-type"] = "application/json"
        elif isinstance(self.content, str):
            body = self.content.encode("utf-8")
            if "content-type" not in self.headers:
                self.headers["content-type"] = "text/plain; charset=utf-8"
        else:
            body = self.content if isinstance(self.content, bytes) else str(self.content).encode("utf-8")
        
        # Send response start
        await send({
            "type": "http.response.start",
            "status": self.status_code,
            "headers": [
                [name.encode(), value.encode()] 
                for name, value in self.headers.items()
            ]
        })
        
        # Send response body
        await send({
            "type": "http.response.body",
            "body": body
        })
    
    @classmethod
    def json(cls, data: Any, status_code: int = 200, headers: Optional[Dict[str, str]] = None):
        """Create a JSON response"""
        return cls(
            content=data,
            status_code=status_code,
            headers=headers,
            media_type="application/json"
        )
    
    @classmethod
    def html(cls, content: str, status_code: int = 200, headers: Optional[Dict[str, str]] = None):
        """Create an HTML response"""
        return cls(
            content=content,
            status_code=status_code,
            headers=headers,
            media_type="text/html; charset=utf-8"
        )
    
    @classmethod
    def text(cls, content: str, status_code: int = 200, headers: Optional[Dict[str, str]] = None):
        """Create a text response"""
        return cls(
            content=content,
            status_code=status_code,
            headers=headers,
            media_type="text/plain; charset=utf-8"
        )
    
    @classmethod
    def redirect(cls, url: str, status_code: int = 302, headers: Optional[Dict[str, str]] = None):
        """Create a redirect response"""
        redirect_headers = {"location": url}
        if headers:
            redirect_headers.update(headers)
        
        return cls(
            content="",
            status_code=status_code,
            headers=redirect_headers
        )
