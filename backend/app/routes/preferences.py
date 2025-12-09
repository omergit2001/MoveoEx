"""
User preferences routes for onboarding
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from app import mongo
from app.models import User, Preferences

preferences_bp = Blueprint('preferences', __name__)

@preferences_bp.route('/preferences', methods=['POST'])
@jwt_required()
def save_preferences():
    """Save user preferences from onboarding quiz"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        investor_type = data.get('investor_type')
        interested_assets = data.get('interested_assets', [])
        content_types = data.get('content_types', [])
        
        # Validate investor_type
        valid_investor_types = ['HODLer', 'Day Trader', 'NFT Collector', 'DeFi Enthusiast', 'General Investor']
        if investor_type and investor_type not in valid_investor_types:
            return jsonify({'error': f'Invalid investor_type. Must be one of: {", ".join(valid_investor_types)}'}), 400
        
        # Validate arrays
        if not isinstance(interested_assets, list):
            return jsonify({'error': 'interested_assets must be an array'}), 400
        
        if not isinstance(content_types, list):
            return jsonify({'error': 'content_types must be an array'}), 400
        
        # Validate content_types
        valid_content_types = ['Market News', 'Charts', 'Social', 'Fun']
        if content_types:
            invalid_types = [ct for ct in content_types if ct not in valid_content_types]
            if invalid_types:
                return jsonify({'error': f'Invalid content_types: {", ".join(invalid_types)}'}), 400
        
        # Create preferences document
        preferences = Preferences.create_preferences(
            investor_type=investor_type or 'General Investor',
            interested_assets=interested_assets,
            content_types=content_types if content_types else ['Market News']
        )
        
        # Update user document
        update_data = User.update_preferences(user_id, preferences)
        result = mongo.db.users.update_one(
            {'_id': ObjectId(user_id)},
            update_data
        )
        
        if result.modified_count == 0:
            return jsonify({'error': 'User not found or preferences not updated'}), 404
        
        return jsonify({
            'message': 'Preferences saved successfully',
            'preferences': preferences
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@preferences_bp.route('/preferences', methods=['GET'])
@jwt_required()
def get_preferences():
    """Get current user preferences"""
    try:
        user_id = get_jwt_identity()
        user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        preferences = user.get('preferences')
        
        if not preferences:
            return jsonify({
                'preferences': None,
                'message': 'No preferences set. Please complete onboarding.'
            }), 200
        
        return jsonify({
            'preferences': preferences
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

