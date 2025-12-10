import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo
from app.config import Config

mongo = PyMongo()
jwt = JWTManager()

def create_app(config_class=Config):
    """Application factory pattern for Flask"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    # CORS: Allow all origins in development, restrict in production
    allowed_origins = os.environ.get('CORS_ORIGINS', '*').split(',')
    if allowed_origins == ['*']:
        CORS(app, resources={r"/api/*": {"origins": "*"}})
    else:
        CORS(app, resources={r"/api/*": {"origins": allowed_origins}})
    mongo.init_app(app)
    jwt.init_app(app)
    
    # Register blueprints
    from app.routes.health import health_bp
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.preferences import preferences_bp
    from app.routes.feedback import feedback_bp
    
    app.register_blueprint(health_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/api')
    app.register_blueprint(preferences_bp, url_prefix='/api/user')
    app.register_blueprint(feedback_bp, url_prefix='/api')
    
    return app

