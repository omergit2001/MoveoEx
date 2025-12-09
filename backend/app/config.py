import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = False  # Tokens don't expire (can be changed)
    
    # MongoDB configuration
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://localhost:27017/crypto_dashboard'
    
    # External API keys
    COINGECKO_API_KEY = os.environ.get('COINGECKO_API_KEY') or ''
    CRYPTOPANIC_API_KEY = os.environ.get('CRYPTOPANIC_API_KEY') or ''
    OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY') or ''
    
    # External API endpoints
    COINGECKO_BASE_URL = 'https://api.coingecko.com/api/v3'
    CRYPTOPANIC_BASE_URL = 'https://cryptopanic.com/api/v1'
    OPENROUTER_BASE_URL = 'https://openrouter.ai/api/v1'
    
    # AI Model configuration
    AI_MODEL = os.environ.get('AI_MODEL') or 'meta-llama/llama-3.2-3b-instruct:free'

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

