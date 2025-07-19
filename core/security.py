# core/security.py
import hashlib
import hmac
import secrets
import time
from typing import Dict, Optional, Set
from dataclasses import dataclass, field
from collections import defaultdict
import asyncio

@dataclass
class SecurityConfig:
    """Security configuration"""
    csrf_enabled: bool = True
    rate_limit_enabled: bool = True
    secure_headers_enabled: bool = True
    xss_protection: bool = True
    content_security_policy: str = "default-src 'self'"
    rate_limit_requests: int = 100
    rate_limit_window: int = 3600  # 1 hour

class CSRFProtection:
    """CSRF Protection middleware"""
    
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
    
    def generate_token(self, session_id: str) -> str:
        """Generate CSRF token"""
        timestamp = str(int(time.time()))
        message = f"{session_id}:{timestamp}"
        signature = hmac.new(
            self.secret_key.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        return f"{timestamp}:{signature}"
    
    def validate_token(self, token: str, session_id: str) -> bool:
        """Validate CSRF token"""
        try:
            timestamp, signature = token.split(':', 1)
            
            # Check if token is not too old (24 hours)
            if int(time.time()) - int(timestamp) > 86400:
                return False
            
            message = f"{session_id}:{timestamp}"
            expected_signature = hmac.new(
                self.secret_key.encode(),
                message.encode(),
                hashlib.sha256
            ).hexdigest()
            
            return hmac.compare_digest(signature, expected_signature)
        except (ValueError, TypeError):
            return False

class RateLimiter:
    """Rate limiting middleware"""
    
    def __init__(self, requests_per_window: int = 100, window_seconds: int = 3600):
        self.requests_per_window = requests_per_window
        self.window_seconds = window_seconds
        self.clients: Dict[str, list] = defaultdict(list)
        self._cleanup_task = None
    
    def is_allowed(self, client_ip: str) -> bool:
        """Check if request is allowed"""
        now = time.time()
        
        # Clean old requests
        self.clients[client_ip] = [
            req_time for req_time in self.clients[client_ip]
            if now - req_time < self.window_seconds
        ]
        
        # Check rate limit
        if len(self.clients[client_ip]) >= self.requests_per_window:
            return False
        
        # Add current request
        self.clients[client_ip].append(now)
        return True
    
    async def cleanup_old_entries(self):
        """Periodic cleanup of old entries"""
        while True:
            await asyncio.sleep(300)  # Clean every 5 minutes
            now = time.time()
            
            for client_ip in list(self.clients.keys()):
                self.clients[client_ip] = [
                    req_time for req_time in self.clients[client_ip]
                    if now - req_time < self.window_seconds
                ]
                
                # Remove empty entries
                if not self.clients[client_ip]:
                    del self.clients[client_ip]

class SecurityHeaders:
    """Security headers middleware"""
    
    def __init__(self, config: SecurityConfig):
        self.config = config
    
    def get_headers(self) -> Dict[str, str]:
        """Get security headers"""
        headers = {}
        
        if self.config.xss_protection:
            headers['X-XSS-Protection'] = '1; mode=block'
            headers['X-Content-Type-Options'] = 'nosniff'
            headers['X-Frame-Options'] = 'DENY'
        
        if self.config.content_security_policy:
            headers['Content-Security-Policy'] = self.config.content_security_policy
        
        headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        
        return headers
