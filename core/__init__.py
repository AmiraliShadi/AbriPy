"""
AbriPy Framework - Core Package
"""

# Import main classes that should be available when importing the core package
from .application import AbriPy
from .config import Config, ServerConfig, SecurityConfig, DatabaseConfig
from .routing import Router

# Package metadata
__version__ = "1.0.0"
__author__ = "Amirali Shadi"

# Define what gets imported with "from core import *"
__all__ = [
    'AbriPy',
    'Config',
    'ServerConfig', 
    'SecurityConfig',
    'DatabaseConfig',
    'Router'
]
