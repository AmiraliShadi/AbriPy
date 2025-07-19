# templating/components.py
from typing import Dict, Any, Optional
from .engine import TemplateEngine

class Component:
    """Reusable template component"""
    
    def __init__(self, name: str, template: str):
        self.name = name
        self.template = template
        self.engine = TemplateEngine()
    
    def render(self, context: Dict[str, Any] = None) -> str:
        """Render component with context"""
        return self.engine._process_template(self.template, context or {})

class ComponentRegistry:
    """Registry for template components"""
    
    def __init__(self):
        self.components: Dict[str, Component] = {}
    
    def register(self, component: Component):
        """Register component"""
        self.components[component.name] = component
    
    def get(self, name: str) -> Optional[Component]:
        """Get component by name"""
        return self.components.get(name)
    
    def render(self, name: str, context: Dict[str, Any] = None) -> str:
        """Render component by name"""
        component = self.get(name)
        if not component:
            raise ValueError(f"Component '{name}' not found")
        
        return component.render(context)

# Global component registry
_component_registry = ComponentRegistry()

def register_component(name: str, template: str):
    """Register a new component"""
    component = Component(name, template)
    _component_registry.register(component)
    return component

def render_component(name: str, context: Dict[str, Any] = None) -> str:
    """Render registered component"""
    return _component_registry.render(name, context)

# Built-in components
register_component('alert', """
<div class="alert alert-{{ type or 'info' }}">
    {% if title %}<h4>{{ title }}</h4>{% endif %}
    <p>{{ message }}</p>
</div>
""")

register_component('card', """
<div class="card">
    {% if header %}<div class="card-header">{{ header }}</div>{% endif %}
    <div class="card-body">
        {{ content }}
    </div>
    {% if footer %}<div class="card-footer">{{ footer }}</div>{% endif %}
</div>
""")
