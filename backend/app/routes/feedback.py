"""
Feedback routes for thumbs up/down voting
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from app import mongo
from app.models import Feedback

feedback_bp = Blueprint('feedback', __name__)

@feedback_bp.route('/feedback', methods=['POST'])
@jwt_required()
def submit_feedback():
    """Submit feedback (thumbs up/down) for content"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        content_type = data.get('content_type')
        content_hash = data.get('content_hash')
        vote = data.get('vote')
        
        if not content_type or not content_hash or vote is None:
            return jsonify({'error': 'Missing required fields: content_type, content_hash, vote'}), 400
        
        # Validate content_type
        valid_content_types = ['news', 'insight', 'meme', 'price']
        if content_type not in valid_content_types:
            return jsonify({'error': f'Invalid content_type. Must be one of: {", ".join(valid_content_types)}'}), 400
        
        # Validate vote
        if vote not in [1, -1]:
            return jsonify({'error': 'Vote must be 1 (thumbs up) or -1 (thumbs down)'}), 400
        
        # Check if user already voted on this content
        existing_feedback = mongo.db.feedback.find_one({
            'user_id': ObjectId(user_id),
            'content_type': content_type,
            'content_hash': content_hash
        })
        
        if existing_feedback:
            # Update existing feedback
            mongo.db.feedback.update_one(
                {
                    'user_id': ObjectId(user_id),
                    'content_type': content_type,
                    'content_hash': content_hash
                },
                {
                    '$set': {
                        'vote': vote,
                        'timestamp': Feedback.create_feedback(user_id, content_type, content_hash, vote)['timestamp']
                    }
                }
            )
            return jsonify({
                'message': 'Feedback updated successfully',
                'feedback': {
                    'content_type': content_type,
                    'content_hash': content_hash,
                    'vote': vote
                }
            }), 200
        
        # Create new feedback
        feedback_doc = Feedback.create_feedback(user_id, content_type, content_hash, vote)
        mongo.db.feedback.insert_one(feedback_doc)
        
        return jsonify({
            'message': 'Feedback submitted successfully',
            'feedback': {
                'content_type': content_type,
                'content_hash': content_hash,
                'vote': vote
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@feedback_bp.route('/feedback', methods=['GET'])
@jwt_required()
def get_user_feedback():
    """Get all feedback submitted by the current user"""
    try:
        user_id = get_jwt_identity()
        
        feedback_list = list(mongo.db.feedback.find(
            {'user_id': ObjectId(user_id)},
            {'_id': 0, 'user_id': 0}
        ).sort('timestamp', -1))
        
        # Convert ObjectId to string for JSON serialization
        for fb in feedback_list:
            if 'timestamp' in fb:
                fb['timestamp'] = fb['timestamp'].isoformat()
        
        return jsonify({
            'feedback': feedback_list,
            'count': len(feedback_list)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

