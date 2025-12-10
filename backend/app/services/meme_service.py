"""
Meme service for fetching crypto memes from Reddit or static JSON
"""
import json
import os
import random
import requests
from flask import current_app

def get_random_meme():
    """
    Get a random crypto meme from Reddit API or static JSON file
    
    Returns:
        Dictionary with meme data
    """
    # Try Reddit API first
    try:
        meme = get_reddit_meme()
        if meme:
            return meme
    except Exception as e:
        current_app.logger.error(f"Reddit API error: {str(e)}")
    
    # Fallback to static JSON
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        memes_path = os.path.join(base_dir, 'data', 'memes.json')
        
        if os.path.exists(memes_path):
            with open(memes_path, 'r', encoding='utf-8') as f:
                memes = json.load(f)
            
            if memes and len(memes) > 0:
                meme = random.choice(memes)
                return {
                    'id': meme.get('id', 'meme-1'),
                    'url': meme.get('url', ''),
                    'title': meme.get('title', 'Crypto Meme'),
                    'source': meme.get('source', 'Reddit'),
                    'description': meme.get('description', '')
                }
    except Exception as e:
        current_app.logger.error(f"Static JSON error: {str(e)}")
    
    # Final fallback
    return get_fallback_meme()

def get_reddit_meme():
    """
    Fetch a random crypto meme from Reddit using public JSON API
    
    Returns:
        Dictionary with meme data or None if failed
    """
    # List of crypto meme subreddits
    subreddits = [
        'cryptomemes',
        'cryptocurrencymemes',
        'bitcoinmemes',
        'ethereum',
        'cryptocurrency'
    ]
    
    # Try each subreddit until we find one with image posts
    for subreddit in subreddits:
        try:
            # Reddit JSON API endpoint (no auth required for public data)
            url = f"https://www.reddit.com/r/{subreddit}/hot.json"
            headers = {
                'User-Agent': 'CryptoDashboard/1.0 (Educational Project)'
            }
            params = {
                'limit': 25
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                posts = data.get('data', {}).get('children', [])
                
                # Filter for image posts (jpg, png, gif, etc.)
                image_posts = []
                for post in posts:
                    post_data = post.get('data', {})
                    
                    # Skip stickied posts, NSFW, and galleries
                    if post_data.get('stickied') or post_data.get('over_18') or post_data.get('is_gallery'):
                        continue
                    
                    url_overridden_by_dest = post_data.get('url_overridden_by_dest', '')
                    url = post_data.get('url', '')
                    post_hint = post_data.get('post_hint', '')
                    
                    # Check if it's an image URL
                    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
                    image_url = url_overridden_by_dest or url
                    
                    # Check if it's an image: direct image URLs, i.redd.it, or post_hint indicates image
                    is_image = (
                        any(image_url.lower().endswith(ext) for ext in image_extensions) or
                        'i.redd.it' in image_url or
                        'preview.redd.it' in image_url or
                        post_hint == 'image'
                    )
                    
                    # Skip if it's a link to another site (not a direct image)
                    if is_image and not any(skip in image_url.lower() for skip in ['reddit.com/r/', 'reddit.com/user/']):
                        image_posts.append({
                            'id': post_data.get('id', ''),
                            'url': image_url,
                            'title': post_data.get('title', 'Crypto Meme'),
                            'source': f"r/{subreddit}",
                            'description': post_data.get('selftext', '')[:200] if post_data.get('selftext') else ''
                        })
                
                # Return a random image post if found
                if image_posts:
                    meme = random.choice(image_posts)
                    return {
                        'id': meme.get('id', 'reddit-meme'),
                        'url': meme.get('url', ''),
                        'title': meme.get('title', 'Crypto Meme'),
                        'source': meme.get('source', 'Reddit'),
                        'description': meme.get('description', '')
                    }
        except Exception as e:
            current_app.logger.error(f"Error fetching from r/{subreddit}: {str(e)}")
            continue
    
    return None

def get_fallback_meme():
    """Return a fallback meme if file is not available"""
    fallback_memes = [
        {
            'id': 'fallback-1',
            'url': 'https://i.redd.it/crypto-meme-1.jpg',
            'title': 'HODL Strong',
            'source': 'Reddit',
            'description': 'Classic HODL meme'
        },
        {
            'id': 'fallback-2',
            'url': 'https://i.redd.it/crypto-meme-2.jpg',
            'title': 'To The Moon',
            'source': 'Reddit',
            'description': 'Moon meme'
        },
        {
            'id': 'fallback-3',
            'url': 'https://i.redd.it/crypto-meme-3.jpg',
            'title': 'Diamond Hands',
            'source': 'Reddit',
            'description': 'Diamond hands meme'
        }
    ]
    return random.choice(fallback_memes)

