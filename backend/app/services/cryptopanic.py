"""
CryptoPanic API service for fetching cryptocurrency news
"""
import requests
from flask import current_app

def get_crypto_news(limit=5):
    """
    Fetch latest cryptocurrency news from CryptoPanic
    
    Args:
        limit: Maximum number of news articles to return
    
    Returns:
        List of news articles
    """
    try:
        base_url = current_app.config['CRYPTOPANIC_BASE_URL']
        api_key = current_app.config.get('CRYPTOPANIC_API_KEY', '')
        
        # CryptoPanic API endpoint
        url = f"{base_url}/posts"
        params = {
            'auth_token': api_key if api_key else 'public',
            'public': 'true',
            'filter': 'hot',
            'currencies': 'BTC,ETH,BNB,ADA,SOL,XRP'
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            
            news_items = []
            for item in results[:limit]:
                news_items.append({
                    'id': item.get('id'),
                    'title': item.get('title', ''),
                    'url': item.get('url', ''),
                    'source': item.get('source', {}).get('title', 'CryptoPanic'),
                    'published_at': item.get('published_at', ''),
                    'votes': item.get('votes', {}).get('positive', 0),
                    'currencies': [c.get('code', '') for c in item.get('currencies', [])]
                })
            
            return news_items
        
        # Fallback: Return static news if API fails
        return get_fallback_news()
        
    except Exception as e:
        current_app.logger.error(f"CryptoPanic API error: {str(e)}")
        return get_fallback_news()

def get_fallback_news():
    """Return static fallback news if API fails"""
    return [
        {
            'id': 'fallback-1',
            'title': 'Bitcoin continues to show strong market performance',
            'url': 'https://cryptopanic.com',
            'source': 'CryptoPanic',
            'published_at': '2024-01-01T00:00:00Z',
            'votes': 0,
            'currencies': ['BTC']
        },
        {
            'id': 'fallback-2',
            'title': 'Ethereum network upgrades improve transaction efficiency',
            'url': 'https://cryptopanic.com',
            'source': 'CryptoPanic',
            'published_at': '2024-01-01T00:00:00Z',
            'votes': 0,
            'currencies': ['ETH']
        },
        {
            'id': 'fallback-3',
            'title': 'Crypto market shows mixed signals as adoption grows',
            'url': 'https://cryptopanic.com',
            'source': 'CryptoPanic',
            'published_at': '2024-01-01T00:00:00Z',
            'votes': 0,
            'currencies': ['BTC', 'ETH']
        }
    ]

