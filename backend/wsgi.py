"""
WSGI entry point for Gunicorn (alternative)
"""
import os
from app import create_app
from app.config import Config, ProductionConfig

# Use ProductionConfig if available, otherwise fall back to Config
config_class = ProductionConfig if os.environ.get('FLASK_ENV') == 'production' else Config
app = create_app(config_class)

