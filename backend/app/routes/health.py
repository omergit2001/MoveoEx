"""
Health check endpoint for monitoring and testing
"""
from flask import Blueprint, jsonify

health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'crypto-dashboard-backend',
        'message': 'API is running'
    }), 200

@health_bp.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    return jsonify({
        'message': 'Crypto Dashboard API',
        'version': '1.0.0',
        'endpoints': {
            'health': '/api/health',
            'auth': '/api/auth/login',
            'dashboard': '/api/dashboard'
        }
    }), 200

