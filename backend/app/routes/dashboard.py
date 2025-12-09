"""
Dashboard route that orchestrates all external API calls
"""
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from app import mongo
from app.services.coingecko import get_coin_prices
from app.services.cryptopanic import get_crypto_news
from app.services.ai_service import generate_ai_insight
from app.services.meme_service import get_random_meme
from app.utils import generate_content_hash

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard():
    """Get dashboard data with all sections"""
    try:
        user_id = get_jwt_identity()
        
        # Get user preferences
        user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        preferences = user.get('preferences', {})
        interested_assets = preferences.get('interested_assets', []) if preferences else []
        content_types = preferences.get('content_types', ['Market News']) if preferences else ['Market News']
        
        # Fetch data from all services
        dashboard_data = {
            'news': [],
            'prices': [],
            'ai_insight': {},
            'meme': {}
        }
        
        # 1. Market News (if user wants Market News)
        if 'Market News' in content_types or not content_types:
            news_items = get_crypto_news(limit=5)
            for item in news_items:
                item['content_hash'] = generate_content_hash({
                    'type': 'news',
                    'id': item.get('id'),
                    'title': item.get('title')
                })
            dashboard_data['news'] = news_items
        
        # 2. Coin Prices
        prices = get_coin_prices(interested_assets=interested_assets, limit=10)
        for coin in prices:
            coin['content_hash'] = generate_content_hash({
                'type': 'price',
                'id': coin.get('id'),
                'name': coin.get('name')
            })
        dashboard_data['prices'] = prices
        
        # 3. AI Insight (if user wants Market News or Charts)
        if 'Market News' in content_types or 'Charts' in content_types or not content_types:
            insight = generate_ai_insight(preferences)
            insight['content_hash'] = generate_content_hash({
                'type': 'insight',
                'text': insight.get('text', ''),
                'date': str(user.get('updated_at', ''))
            })
            dashboard_data['ai_insight'] = insight
        
        # 4. Fun Meme (if user wants Fun content)
        if 'Fun' in content_types or not content_types:
            meme = get_random_meme()
            meme['content_hash'] = generate_content_hash({
                'type': 'meme',
                'id': meme.get('id'),
                'url': meme.get('url')
            })
            dashboard_data['meme'] = meme
        
        return jsonify({
            'dashboard': dashboard_data,
            'user_preferences': {
                'investor_type': preferences.get('investor_type') if preferences else None,
                'interested_assets': interested_assets,
                'content_types': content_types
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

