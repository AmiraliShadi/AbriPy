# app.py
from core.application import AbriPy
from core.config import Config
from web.response import Response

# Create AbriPy application
app = AbriPy()

@app.get('/')
async def hello(request):  # Add request parameter
    return "Hello, AbriPy! 🚀"

@app.get('/api/status')
async def status(request):  # Add request parameter
    return {"status": "healthy", "framework": "AbriPy"}

@app.post('/api/echo')
async def echo(request):  # This one already has it
    data = await request.json()
    return {"echo": data}

if __name__ == "__main__":
    print("start...")
    app.run(host="127.0.0.1", port=8000, debug=True)
