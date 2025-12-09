"""
MongoDB document models and schemas
"""
from datetime import datetime
from bson import ObjectId

class User:
    """User model structure"""
    @staticmethod
    def create_user(email, password_hash, name):
        """Create a new user document"""
        return {
            'email': email,
            'password_hash': password_hash,
            'name': name,
            'preferences': None,  # Will be set during onboarding
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
    
    @staticmethod
    def update_preferences(user_id, preferences):
        """Update user preferences"""
        return {
            '$set': {
                'preferences': preferences,
                'updated_at': datetime.utcnow()
            }
        }

class Preferences:
    """User preferences structure"""
    @staticmethod
    def create_preferences(investor_type, interested_assets, content_types):
        """Create preferences document"""
        return {
            'investor_type': investor_type,
            'interested_assets': interested_assets,  # Array of strings
            'content_types': content_types,  # Array of strings
            'created_at': datetime.utcnow()
        }

class Feedback:
    """Feedback model structure"""
    @staticmethod
    def create_feedback(user_id, content_type, content_hash, vote):
        """Create a feedback document"""
        return {
            'user_id': ObjectId(user_id) if isinstance(user_id, str) else user_id,
            'content_type': content_type,  # 'news', 'insight', 'meme', 'price'
            'content_hash': content_hash,  # Unique identifier for the content
            'vote': vote,  # 1 for thumbs up, -1 for thumbs down
            'timestamp': datetime.utcnow()
        }

