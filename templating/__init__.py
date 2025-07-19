# templating/__init__.py
from .engine import TemplateEngine
from .components import Component, render_component

__all__ = [
    'TemplateEngine',
    'Component',
    'render_component'
]
