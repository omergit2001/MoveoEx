"""
Meme service for fetching crypto memes
"""
import json
import os
import random
from flask import current_app

def get_random_meme():
    """
    Get a random crypto meme from static JSON file
    
    Returns:
        Dictionary with meme data
    """
    try:
        # Get the path to the memes.json file
        # Assuming it's in the project root/data directory
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
        
        # Fallback memes if file doesn't exist
        return get_fallback_meme()
        
    except Exception as e:
        current_app.logger.error(f"Meme service error: {str(e)}")
        return get_fallback_meme()

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

