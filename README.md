# 🌟 AbriP Framework

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI Compatible](https://img.shields.io/badge/ASGI-compatible-green.svg)](https://asgi.readthedocs.io/)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**AbriPy** is a modern, lightning-fast Python web framework built for developers who want the power of Flask with the performance of FastAPI. Create beautiful web applications with minimal code while maintaining enterprise-level security and scalability.

## ✨ Features

🚀 **Lightnin Fast** - Built on ASGI for async performance  
🛡️ **Security First**  Built-in CSRF, XSS, and security headers  
🔌 **WeSocket Ready** - Real-time applications made simple  
🎨 *Developer Friendly** - Intuitive decorators and clean syntax  
⚡ **Hot Reload** - Development server with automatic reloading  
🔧 **Middleware Support* - Extensible request/response processing  
📊 *Type Hints** - Full TypeScript-like type safety  

## 🚀 Quick Start

## Installation

```bash
pip install abripy
# Or for development
git clone https://github.com/AmiraliShadi/AbriPy.git
cd abripy
pip install -e .

### Your First App

python
from core import AbriPy

app = AbriPy()

@app.get('/')
async def hello():
return "Hello, AbriPy! 🚀"

app.post('/api/data')
async def handle_data(request):
data = await request.json()
return {"message": f"Received: {data}"}

if __name__ == "__main__":
app.run(debug=True)

**Run it:**
bash
python app.py

Visit `http://localhost:8000` and see your app in action! 🎉

##🏗️ Architecture


AriPy Framework
├── 🏛️ Core
│   ├── Applicatio Engine
│   ├── Router & URL Matching
│   ├── Middleware Pipeline
│   └── Configuration System
├── 🌐 Web Layer
│   ├── Reques/Response Objects
│   ├── WebSocket Manager
│   └── Static File Serving
└── � Security
├── CSRF Protection
├── Security Headers
└── Input Validation

## 💡 Wh AbriPy?

| Feature | Flask | FastAPI | **AbriPy** |
|---------|-------|---------|-----------|
| **Async Support** | ❌ | ✅ | ✅ |
| **Type Hints** | ❌ | ✅ | ✅ |
| **Built-in Security** | ❌ | ❌ | ✅ |
| **WebSocket** | Plugin | ✅ | ✅ |
| **Learning Curve** | Easy | Medium | **Easy** |
| **Performance** | Good | Excellent | **Excellent** |

## 🎯Perfect For

- 🚀 *Startups** building MVPs quickly
- 🏢 **Enterprises** neding secure, scalable APIs
- 🎓 **Students** learning modern web development
-  **Researchers** creating data visualization dashboards
- 🎮 **Rea-time apps** with WebSocket requirements

## 📚 Learn More

- 🎯 [API Reference](docs/apa.html)
- 💡 [Examples] (calculator_app.py)

## 🤝 Community

- 💬 [Discd Server](https://t.me/Amiralisahdii)
- 📧 Mailing List](mailto:ashadi8448@gmail.com)

## 📄 License

MIT License - see LICENSE](LICENSE) for details.

---

**Made with ❤️ by Amirali Shadi, for developers**

*"AbriPy - Where simplicity meets power"*


## 📚 **COMPREHENSIV DOCUMENTATION** (`docs/README.md`)

```