"""
AbriPy Framework Example Application
"""

from core.application import AbriPy, Config
from web.response import json_response, html_response
from templating.engine import render_template

# Create AbriPy app
app = AbriPy()

@app.get('/')
async def home(request):
    """Home page"""
    features = [
        "Async-first architecture",
        "Built-in security features",
        "Type-safe development", 
        "WebSocket support",
        "Database ORM included",
        "Hot reloading in development"
    ]
    
    context = {
        'title': 'AbriPy Framework',
        'features': features,
        'content': 'Welcome to the most exciting Python web framework!'
    }
    
    return html_response(render_template('home.html', context))

@app.get('/api/health')
async def health_check(request):
    """Health check endpoint"""
    return json_response({
        'status': 'healthy',
        'framework': 'AbriPy',
        'version': '0.1.0'
    })

@app.get('/users/{user_id}')
async def get_user(request, user_id: str):
    """Get user by ID"""
    return json_response({
        'user_id': user_id,
        'name': f'User {user_id}',
        'framework': 'AbriPy'
    })

@app.post('/api/data')
async def create_data(request):
    """Create new data"""
    data = await request.json()
    
    # Process data here
    response_data = {
        'message': 'Data created successfully',
        'received_data': data,
        'framework': 'AbriPy'
    }
    
    return json_response(response_data, status_code=201)

if __name__ == '__main__':
    print("🚀 Starting AbriPy Framework Example")
    app.run(debug=True)
