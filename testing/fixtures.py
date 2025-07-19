# testing/fixtures.py
from typing import Dict, Any
from core.application import AbriPy, Config

def create_test_app() -> AbriPy:
    """Create a test application instance"""
    config = Config()
    config.testing = True
    config.database.url = "sqlite:///:memory:"
    
    app = AbriPy(config=config)
    
    # Add test routes
    @app.get('/test')
    async def test_route(request):
        from web.response import json_response
        return json_response({'message': 'test'})
    
    return app

def create_test_user(username: str = "testuser", email: str = "test@example.com") -> Dict[str, Any]:
    """Create a test user"""
    return {
        'id': 1,
        'username': username,
        'email': email,
        'created_at': '2025-07-19T20:00:00Z'
    }
