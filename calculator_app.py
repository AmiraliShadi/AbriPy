from core.application import AbriPy
from core.config import Config
from web.response import Response
import json
import math
from typing import Union

# Initialize AbriPy
app = AbriPy()

class Calculator:
    """Calculator logic class"""
    
    @staticmethod
    def evaluate_expression(expression: str) -> dict:
        """Safely evaluate mathematical expressions"""
        try:
            # Clean the expression
            expression = expression.replace(" ", "")
            
            # Security: Only allow safe characters
            allowed_chars = "0123456789+-*/.()sincostanlogsqrtpi"
            if not all(c.lower() in allowed_chars for c in expression):
                return {"error": "Invalid characters in expression"}
            
            # Replace common functions
            expression = expression.replace("sin", "math.sin")
            expression = expression.replace("cos", "math.cos") 
            expression = expression.replace("tan", "math.tan")
            expression = expression.replace("log", "math.log")
            expression = expression.replace("sqrt", "math.sqrt")
            expression = expression.replace("pi", "math.pi")
            
            # Evaluate safely
            result = eval(expression, {"__builtins__": {}, "math": math})
            
            return {
                "result": result,
                "expression": expression,
                "success": True
            }
            
        except ZeroDivisionError:
            return {"error": "Division by zero", "success": False}
        except ValueError as e:
            return {"error": f"Math error: {str(e)}", "success": False}
        except Exception as e:
            return {"error": f"Invalid expression: {str(e)}", "success": False}

# Routes
@app.get("/")
async def calculator_home(request):
    """Serve the calculator interface"""
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AbriPy Calculator 🧮</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .calculator {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            padding: 30px;
            max-width: 400px;
            width: 100%;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .header h1 {
            color: #333;
            font-size: 2rem;
            margin-bottom: 10px;
        }
        
        .header p {
            color: #666;
            font-size: 0.9rem;
        }
        
        .display {
            background: #f8f9fa;
            border: 2px solid #e9ecef;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            min-height: 80px;
            display: flex;
            align-items: center;
            justify-content: flex-end;
            font-size: 1.5rem;
            font-weight: 500;
            color: #333;
            overflow: hidden;
            word-break: break-all;
        }
        
        .buttons {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
        }
        
        .btn {
            padding: 20px;
            border: none;
            border-radius: 10px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        .btn-number {
            background: #f8f9fa;
            color: #333;
            border: 2px solid #e9ecef;
        }
        
        .btn-number:hover {
            background: #e9ecef;
        }
        
        .btn-operator {
            background: #667eea;
            color: white;
        }
        
        .btn-operator:hover {
            background: #5a67d8;
        }
        
        .btn-equals {
            background: #48bb78;
            color: white;
            grid-column: span 2;
        }
        
        .btn-equals:hover {
            background: #38a169;
        }
        
        .btn-clear {
            background: #f56565;
            color: white;
        }
        
        .btn-clear:hover {
            background: #e53e3e;
        }
        
        .btn-function {
            background: #ed8936;
            color: white;
            font-size: 0.9rem;
        }
        
        .btn-function:hover {
            background: #dd7824;
        }
        
        .error {
            color: #e53e3e;
            font-size: 1rem;
        }
        
        .history {
            margin-top: 20px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 10px;
            max-height: 150px;
            overflow-y: auto;
        }
        
        .history h3 {
            margin-bottom: 10px;
            color: #333;
            font-size: 1rem;
        }
        
        .history-item {
            padding: 5px 0;
            border-bottom: 1px solid #e9ecef;
            font-size: 0.9rem;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="calculator">
        <div class="header">
            <h1>🧮 AbriPy Calculator</h1>
            <p>Built with AbriPy Framework v1.0.0</p>
        </div>
        
        <div class="display" id="display">0</div>
        
        <div class="buttons">
            <button class="btn btn-clear" onclick="clearDisplay()">C</button>
            <button class="btn btn-operator" onclick="appendToDisplay('/')">/</button>
            <button class="btn btn-operator" onclick="appendToDisplay('*')">×</button>
            <button class="btn btn-operator" onclick="deleteLastChar()">⌫</button>
            
            <button class="btn btn-number" onclick="appendToDisplay('7')">7</button>
            <button class="btn btn-number" onclick="appendToDisplay('8')">8</button>
            <button class="btn btn-number" onclick="appendToDisplay('9')">9</button>
            <button class="btn btn-operator" onclick="appendToDisplay('-')">-</button>
            
            <button class="btn btn-number" onclick="appendToDisplay('4')">4</button>
            <button class="btn btn-number" onclick="appendToDisplay('5')">5</button>
            <button class="btn btn-number" onclick="appendToDisplay('6')">6</button>
            <button class="btn btn-operator" onclick="appendToDisplay('+')">+</button>
            
            <button class="btn btn-number" onclick="appendToDisplay('1')">1</button>
            <button class="btn btn-number" onclick="appendToDisplay('2')">2</button>
            <button class="btn btn-number" onclick="appendToDisplay('3')">3</button>
            <button class="btn btn-function" onclick="appendToDisplay('sqrt(')" title="Square Root">√</button>
            
            <button class="btn btn-number" onclick="appendToDisplay('0')">0</button>
            <button class="btn btn-number" onclick="appendToDisplay('.')">.</button>
            <button class="btn btn-function" onclick="appendToDisplay('pi')" title="Pi">π</button>
            <button class="btn btn-equals" onclick="calculate()">=</button>
            
            <button class="btn btn-function" onclick="appendToDisplay('sin(')" title="Sine">sin</button>
            <button class="btn btn-function" onclick="appendToDisplay('cos(')" title="Cosine">cos</button>
            <button class="btn btn-function" onclick="appendToDisplay('tan(')" title="Tangent">tan</button>
            <button class="btn btn-function" onclick="appendToDisplay('log(')" title="Logarithm">log</button>
        </div>
        
        <div class="history" id="history" style="display: none;">
            <h3>📝 History</h3>
            <div id="history-items"></div>
        </div>
    </div>

    <script>
        let display = document.getElementById('display');
        let currentInput = '0';
        let history = [];
        
        function updateDisplay() {
            display.textContent = currentInput;
        }
        
        function appendToDisplay(value) {
            if (currentInput === '0' && value !== '.') {
                currentInput = value;
            } else {
                currentInput += value;
            }
            updateDisplay();
        }
        
        function clearDisplay() {
            currentInput = '0';
            updateDisplay();
        }
        
        function deleteLastChar() {
            if (currentInput.length > 1) {
                currentInput = currentInput.slice(0, -1);
            } else {
                currentInput = '0';
            }
            updateDisplay();
        }
        
        async function calculate() {
            try {
                const response = await fetch('/api/calculate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        expression: currentInput.replace('×', '*')
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    // Add to history
                    history.unshift(`${currentInput} = ${data.result}`);
                    if (history.length > 5) history.pop();
                    updateHistory();
                    
                    currentInput = data.result.toString();
                    display.classList.remove('error');
                } else {
                    display.classList.add('error');
                    currentInput = data.error;
                }
                
                updateDisplay();
                
            } catch (error) {
                display.classList.add('error');
                currentInput = 'Network Error';
                updateDisplay();
            }
        }
        
        function updateHistory() {
            const historyDiv = document.getElementById('history');
            const historyItems = document.getElementById('history-items');
            
            if (history.length > 0) {
                historyDiv.style.display = 'block';
                historyItems.innerHTML = history
                    .map(item => `<div class="history-item">${item}</div>`)
                    .join('');
            }
        }
        
        // Keyboard support
        document.addEventListener('keydown', function(event) {
            const key = event.key;
            
            if (key >= '0' && key <= '9') {
                appendToDisplay(key);
            } else if (key === '.') {
                appendToDisplay('.');
            } else if (key === '+') {
                appendToDisplay('+');
            } else if (key === '-') {
                appendToDisplay('-');
            } else if (key === '*') {
                appendToDisplay('*');
            } else if (key === '/') {
                event.preventDefault();
                appendToDisplay('/');
            } else if (key === 'Enter' || key === '=') {
                event.preventDefault();
                calculate();
            } else if (key === 'Escape' || key === 'c' || key === 'C') {
                clearDisplay();
            } else if (key === 'Backspace') {
                deleteLastChar();
            }
        });
    </script>
</body>
</html>
    """
    return Response.html(html_content)

@app.post("/api/calculate")
async def calculate_api(request):
    """API endpoint for calculations"""
    try:
        # Get JSON data from request
        body = await request.json()
        expression = body.get('expression', '')
        
        if not expression:
            return Response.json({
                "error": "No expression provided",
                "success": False
            }, status_code=400)
        
        # Calculate result
        result = Calculator.evaluate_expression(expression)
        
        return Response.json(result)
        
    except Exception as e:
        return Response.json({
            "error": f"Server error: {str(e)}",
            "success": False
        }, status_code=500)

@app.get("/api/help")
async def calculator_help(request):
    """API endpoint for calculator help"""
    return Response.json({
        "calculator": "AbriPy Web Calculator",
        "version": "1.0.0",
        "supported_operations": [
            "Basic: +, -, *, /",
            "Scientific: sin(), cos(), tan(), log(), sqrt()",
            "Constants: pi",
            "Parentheses: ()"
        ],
        "keyboard_shortcuts": {
            "numbers": "0-9",
            "operators": "+, -, *, /",
            "calculate": "Enter or =",
            "clear": "Escape or C",
            "delete": "Backspace"
        },
        "endpoints": {
            "/": "Calculator interface",
            "/api/calculate": "POST - Calculate expression",
            "/api/help": "GET - This help message"
        }
    })

if __name__ == "__main__":
    print("🧮 Starting AbriPy Calculator...")
    app.run(host="127.0.0.1", port=8000, debug=True)
