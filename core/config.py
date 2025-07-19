# core/config.py
import os
from typing import Any, Dict, Optional
from dataclasses import dataclass, field
import json

@dataclass
class DatabaseConfig:
    """Database configuration"""
    url: str = "sqlite://app.db"
    pool_size: int = 10
    max_overflow: int = 20
    echo: bool = False

@dataclass
class SecurityConfig:
    """Security configuration"""
    secret_key: str = ""
    csrf_enabled: bool = True
    rate_limit_enabled: bool = True
    secure_headers_enabled: bool = True
    session_timeout: int = 3600

@dataclass
class ServerConfig:
    """Server configuration"""
    host: str = "127.0.0.1"
    port: int = 8000
    workers: int = 1
    debug: bool = False
    auto_reload: bool = False

@dataclass
class LoggingConfig:
    """Logging configuration"""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file: Optional[str] = None

@dataclass
class Config:
    """Main application configuration"""
    app_name: str = "AbriPy App"
    environment: str = "development"
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    server: ServerConfig = field(default_factory=ServerConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    custom: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def from_env(cls) -> 'Config':
        """Load configuration from environment variables"""
        config = cls()
        
        # Server config
        config.server.host = os.getenv('HOST', config.server.host)
        config.server.port = int(os.getenv('PORT', config.server.port))
        config.server.debug = os.getenv('DEBUG', '').lower() == 'true'
        
        # Database config
        config.database.url = os.getenv('DATABASE_URL', config.database.url)
        
        # Security config
        config.security.secret_key = os.getenv('SECRET_KEY', config.security.secret_key)
        
        return config
    
    @classmethod
    def from_file(cls, file_path: str) -> 'Config':
        """Load configuration from JSON file"""
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        config = cls()
        
        # Update config with file data
        for key, value in data.items():
            if hasattr(config, key):
                if isinstance(getattr(config, key), (DatabaseConfig, SecurityConfig, ServerConfig, LoggingConfig)):
                    # Update nested config
                    nested_config = getattr(config, key)
                    for nested_key, nested_value in value.items():
                        if hasattr(nested_config, nested_key):
                            setattr(nested_config, nested_key, nested_value)
                else:
                    setattr(config, key, value)
        
        return config
