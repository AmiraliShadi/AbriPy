# auth/authentication.py
import hashlib
import secrets
import time
import jwt
from typing import Dict, Optional, Any
from dataclasses import dataclass

@dataclass
class User:
    """User data class"""
    id: int
    username: str
    email: str
    password_hash: str
    is_active: bool = True
    created_at: Optional[str] = None

class PasswordHasher:
    """Password hashing utility"""
    
    @staticmethod
    def hash_password(password: str, salt: Optional[str] = None) -> tuple:
        """Hash password with salt"""
        if salt is None:
            salt = secrets.token_hex(32)
        
        password_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        )
        
        return password_hash.hex(), salt
    
    @staticmethod
    def verify_password(password: str, password_hash: str, salt: str) -> bool:
        """Verify password against hash"""
        expected_hash, _ = PasswordHasher.hash_password(password, salt)
        return secrets.compare_digest(password_hash, expected_hash)

class JWTManager:
    """JWT token management"""
    
    def __init__(self, secret_key: str, algorithm: str = 'HS256'):
        self.secret_key = secret_key
        self.algorithm = algorithm
    
    def generate_token(self, user_data: Dict[str, Any], expires_in: int = 3600) -> str:
        """Generate JWT token"""
        payload = {
            'user_data': user_data,
            'exp': time.time() + expires_in,
            'iat': time.time()
        }
        
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def decode_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Decode and validate JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            
            # Check expiration
            if payload['exp'] < time.time():
                return None
            
            return payload['user_data']
        except jwt.InvalidTokenError:
            return None

class SessionManager:
    """Session management"""
    
    def __init__(self):
        self.sessions: Dict[str, Dict[str, Any]] = {}
    
    def create_session(self, user_data: Dict[str, Any]) -> str:
        """Create new session"""
        session_id = secrets.token_urlsafe(32)
        self.sessions[session_id] = {
            'user_data': user_data,
            'created_at': time.time(),
            'last_accessed': time.time()
        }
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session data"""
        if session_id not in self.sessions:
            return None
        
        session = self.sessions[session_id]
        
        # Check if session is expired (24 hours)
        if time.time() - session['created_at'] > 86400:
            del self.sessions[session_id]
            return None
        
        # Update last accessed
        session['last_accessed'] = time.time()
        return session['user_data']
    
    def delete_session(self, session_id: str):
        """Delete session"""
        if session_id in self.sessions:
            del self.sessions[session_id]

# auth/authorization.py
from functools import wraps
from typing import List, Callable, Any
from web.request import Request
from web.response import Response, json_response

def login_required(func: Callable) -> Callable:
    """Decorator to require authentication"""
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        # Check for session or token
        session_id = request.get_header('Authorization')
        if not session_id or not hasattr(request, 'user'):
            return json_response(
                {'error': 'Authentication required'}, 
                status_code=401
            )
        
        return await func(request, *args, **kwargs)
    return wrapper

def require_roles(required_roles: List[str]):
    """Decorator to require specific roles"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            if not hasattr(request, 'user'):
                return json_response(
                    {'error': 'Authentication required'}, 
                    status_code=401
                )
            
            user_roles = getattr(request.user, 'roles', [])
            
            if not any(role in user_roles for role in required_roles):
                return json_response(
                    {'error': 'Insufficient permissions'}, 
                    status_code=403
                )
            
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator
