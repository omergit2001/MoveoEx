"""
Dashboard route that orchestrates all external API calls
"""
from flask import Blueprint, jsonify, current_app
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
        
        # Fetch data only for selected content types
        dashboard_data = {
            'news': [],
            'prices': [],
            'ai_insight': {},
            'meme': {}
        }
        
        # 1. Market News - Only if "Market News" is selected
        if 'Market News' in content_types:
            try:
                news_items = get_crypto_news(limit=5)
                for item in news_items:
                    item['content_hash'] = generate_content_hash({
                        'type': 'news',
                        'id': item.get('id'),
                        'title': item.get('title')
                    })
                dashboard_data['news'] = news_items
            except Exception as e:
                current_app.logger.error(f"Error fetching news: {e}")
                dashboard_data['news'] = []
        
        # 2. Coin Prices (Charts) - Only if "Charts" is selected
        if 'Charts' in content_types:
        try:
            prices = get_coin_prices(interested_assets=interested_assets, limit=10)
            current_app.logger.info(f"Coin prices fetched: {len(prices) if prices else 0} coins")
            
            # Ensure we always have prices (fallback should provide at least some)
            if not prices or len(prices) == 0:
                current_app.logger.warning("Coin prices returned empty list, using fallback")
                from app.services.coingecko import get_fallback_coins
                prices = get_fallback_coins()
            
            # Add content hash to each coin
            for coin in prices:
                coin['content_hash'] = generate_content_hash({
                    'type': 'price',
                    'id': coin.get('id'),
                    'name': coin.get('name')
                })
            
            dashboard_data['prices'] = prices
            current_app.logger.info(f"Final prices count: {len(dashboard_data['prices'])}")
        except Exception as e:
            current_app.logger.error(f"Error fetching prices: {e}", exc_info=True)
            # Use fallback coins even on exception
            try:
                from app.services.coingecko import get_fallback_coins
                fallback_prices = get_fallback_coins()
                for coin in fallback_prices:
                    coin['content_hash'] = generate_content_hash({
                        'type': 'price',
                        'id': coin.get('id'),
                        'name': coin.get('name')
                    })
                dashboard_data['prices'] = fallback_prices
            except:
                dashboard_data['prices'] = []
        
        # 3. AI Insight (Social) - Only if "Social" is selected
        if 'Social' in content_types:
            try:
                insight = generate_ai_insight(preferences)
                insight['content_hash'] = generate_content_hash({
                    'type': 'insight',
                    'text': insight.get('text', ''),
                    'date': str(user.get('updated_at', ''))
                })
                dashboard_data['ai_insight'] = insight
            except Exception as e:
                current_app.logger.error(f"Error generating AI insight: {e}")
                dashboard_data['ai_insight'] = {}
        
        # 4. Fun Meme - Only if "Fun" is selected
        if 'Fun' in content_types:
            try:
                meme = get_random_meme()
                meme['content_hash'] = generate_content_hash({
                    'type': 'meme',
                    'id': meme.get('id'),
                    'url': meme.get('url')
                })
                dashboard_data['meme'] = meme
            except Exception as e:
                current_app.logger.error(f"Error fetching meme: {e}")
                dashboard_data['meme'] = {}
        
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

