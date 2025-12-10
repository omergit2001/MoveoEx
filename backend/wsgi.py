"""
WSGI entry point for Gunicorn
This file is used by Gunicorn to start the Flask application
"""
import os
import sys

# Ensure we can import from the app package
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from app import create_app
from app.config import Config, ProductionConfig

# Use ProductionConfig if available, otherwise fall back to Config
config_class = ProductionConfig if os.environ.get('FLASK_ENV') == 'production' else Config

# Create the Flask application instance
app = create_app(config_class)

# This is what Gunicorn will import
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

