# main.py - Test your AbriPy Framework
import asyncio
import uvicorn
from core.application import AbriPy
from core.config import Config

# Create your AbriPy app
app = AbriPy()

# Add some test routes
@app.route('/', methods=['GET'])
async def home(request):
    return {"message": "Welcome to AbriPy Framework! 🚀" "version 1.0.0"}

@app.route('/hello/<name>', methods=['GET'])
async def hello(request):
    name = request.path_params.get('name', 'World')
    return {"message": f"Hello, {name}!", "framework": "AbriPy"}

@app.route('/api/status', methods=['GET'])
async def status(request):
    return {
        "status": "running",
        "framework": "AbriPy",
        "endpoints": ["/", "/hello/<name>", "/api/status"]
    }

# Run the server
if __name__ == "__main__":
    print("🚀 Startin AbriPy Framework...")
    print("📍 Serve running at: http://127.0.0.1:8000")
    print("� Test endpoints:")
    print("   • http://127.0.0.1:8000/")
    print("   • http://127.0.0.1:8000/hello/YourName")
    print("   • http://127.0.0.1:8000/api/status")
    
    # Start with uvicorn
    uvicorn.run(
        "main:app", 
        host="127.0.0.1", 
        port=8000, 
        reload=True,
        log_level="info"
    )
