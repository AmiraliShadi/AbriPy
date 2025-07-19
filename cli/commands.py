# cli/commands.py
import click
import os
from pathlib import Path

@click.group()
def cli():
    """AbriPy Framework CLI"""
    pass

@cli.command()
@click.option('--host', default='127.0.0.1', help='Host to bind to')
@click.option('--port', default=8000, help='Port to bind to')
@click.option('--reload', is_flag=True, help='Enable auto-reload')
def runserver(host, port, reload):
    """Start the AbriPy development server"""
    import uvicorn
    
    click.echo(f"🚀 Starting AbriPy Framework on {host}:{port}")
    
    uvicorn.run(
        "app:app",
        host=host,
        port=port,
        reload=reload
    )

@cli.command()
@click.argument('project_name')
def startproject(project_name):
    """Create a new AbriPy project"""
    project_dir = Path(project_name)
    
    if project_dir.exists():
        click.echo(f"❌ Directory '{project_name}' already exists")
        return
    
    # Create project structure
    project_dir.mkdir()
    
    # Create subdirectories
    (project_dir / "templates").mkdir()
    (project_dir / "static").mkdir()
    (project_dir / "models").mkdir()
    (project_dir / "views").mkdir()
    
    # Create main app file
    app_content = f'''"""
{project_name} - AbriPy Framework Application
"""

from abripy import AbriPy, json_response, html_response
from abripy.templating import render_template

app = AbriPy()

@app.get('/')
async def home(request):
    """Home page"""
    context = {{
        'title': '{project_name.title()}',
        'message': 'Welcome to your AbriPy application!'
    }}
    return html_response(render_template('home.html', context))

@app.get('/api/health')
async def health_check(request):
    """Health check endpoint"""
    return json_response({{'status': 'healthy', 'framework': 'AbriPy'}})

if __name__ == '__main__':
    app.run(debug=True)
'''
    
    with open(project_dir / "app.py", "w") as f:
        f.write(app_content)
    
    # Create basic template
    template_content = '''<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .header { color: #e74c3c; }
    </style>
</head>
<body>
    <h1 class="header">{{ title }}</h1>
    <p>{{ message }}</p>
    <p>🚀 Powered by <strong>AbriPy Framework</strong></p>
</body>
</html>
'''
    
    with open(project_dir / "templates" / "home.html", "w") as f:
        f.write(template_content)
    
    # Create requirements.txt
    requirements = '''abripy>=0.1.0
uvicorn[standard]>=0.24.0
'''
    
    with open(project_dir / "requirements.txt", "w") as f:
        f.write(requirements)
    
    click.echo(f"✅ Created AbriPy project: {project_name}")
    click.echo(f"📁 cd {project_name}")
    click.echo(f"🚀 python app.py")

if __name__ == '__main__':
    cli()
