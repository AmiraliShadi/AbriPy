# templating/engine.py
import re
from typing import Dict, Any, Optional
from pathlib import Path

class TemplateEngine:
    """Simple template engine"""
    
    def __init__(self, template_dir: str = "templates"):
        self.template_dir = Path(template_dir)
        self.template_cache: Dict[str, str] = {}
        self.globals: Dict[str, Any] = {}
    
    def add_global(self, name: str, value: Any):
        """Add global template variable"""
        self.globals[name] = value
    
    def render(self, template_name: str, context: Dict[str, Any] = None) -> str:
        """Render template with context"""
        context = context or {}
        
        # Merge globals with context
        full_context = {**self.globals, **context}
        
        # Load template
        template_content = self._load_template(template_name)
        
        # Process template
        return self._process_template(template_content, full_context)
    
    def _load_template(self, template_name: str) -> str:
        """Load template from file"""
        if template_name in self.template_cache:
            return self.template_cache[template_name]
        
        template_path = self.template_dir / template_name
        
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_name}")
        
        with open(template_path, 'r') as f:
            content = f.read()
        
        self.template_cache[template_name] = content
        return content
    
    def _process_template(self, template: str, context: Dict[str, Any]) -> str:
        """Process template with context variables"""
        
        # Variable substitution: {{ variable }}
        def replace_variable(match):
            var_name = match.group(1).strip()
            return str(context.get(var_name, ''))
        
        template = re.sub(r'\{\{\s*([^}]+)\s*\}\}', replace_variable, template)
        
        # If statements: {% if condition %}...{% endif %}
        def replace_if(match):
            condition = match.group(1).strip()
            content = match.group(2)
            
            # Simple condition evaluation
            if condition in context and context[condition]:
                return content
            return ''
        
        template = re.sub(r'\{%\s*if\s+([^%]+)\s*%\}(.*?)\{%\s*endif\s*%\}', 
                         replace_if, template, flags=re.DOTALL)
        
        # For loops: {% for item in items %}...{% endfor %}
        def replace_for(match):
            loop_var = match.group(1).strip()
            collection_name = match.group(2).strip()
            content = match.group(3)
            
            if collection_name not in context:
                return ''
            
            result = []
            for item in context[collection_name]:
                # Create temporary context with loop variable
                loop_context = {**context, loop_var: item}
                processed_content = self._process_template(content, loop_context)
                result.append(processed_content)
            
            return ''.join(result)
        
        template = re.sub(r'\{%\s*for\s+(\w+)\s+in\s+(\w+)\s*%\}(.*?)\{%\s*endfor\s*%\}',
                         replace_for, template, flags=re.DOTALL)
        
        return template

# Template response helper
from web.response import Response

def render_template(template_name: str, context: Dict[str, Any] = None, 
                   template_engine: Optional[TemplateEngine] = None) -> Response:
    """Render template and return as response"""
    if template_engine is None:
        template_engine = TemplateEngine()
    
    html = template_engine.render(template_name, context)
    return Response(html, content_type="text/html")
