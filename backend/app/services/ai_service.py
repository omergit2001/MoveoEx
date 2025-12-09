"""
OpenRouter AI service for generating daily crypto insights
"""
import requests
from flask import current_app

def generate_ai_insight(user_preferences=None):
    """
    Generate a daily crypto insight using OpenRouter AI
    
    Args:
        user_preferences: User's preferences dict with investor_type, interested_assets, etc.
    
    Returns:
        Dictionary with insight text and metadata
    """
    try:
        base_url = current_app.config['OPENROUTER_BASE_URL']
        api_key = current_app.config.get('OPENROUTER_API_KEY', '')
        model = current_app.config.get('AI_MODEL', 'meta-llama/llama-3.2-3b-instruct:free')
        
        if not api_key:
            # Return a default insight if no API key
            return get_default_insight(user_preferences)
        
        # Build prompt based on user preferences
        investor_type = user_preferences.get('investor_type', 'General Investor') if user_preferences else 'General Investor'
        assets = user_preferences.get('interested_assets', []) if user_preferences else []
        assets_str = ', '.join(assets) if assets else 'various cryptocurrencies'
        
        prompt = f"""You are a crypto market analyst. Provide a brief, insightful daily market analysis (2-3 sentences) for a {investor_type} interested in {assets_str}. 
        
Keep it concise, informative, and relevant to today's market conditions. Focus on actionable insights or interesting trends."""

        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'HTTP-Referer': 'https://crypto-dashboard.app',
            'X-Title': 'Crypto Dashboard'
        }
        
        payload = {
            'model': model,
            'messages': [
                {
                    'role': 'system',
                    'content': 'You are a helpful crypto market analyst providing daily insights.'
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            'max_tokens': 150,
            'temperature': 0.7
        }
        
        response = requests.post(
            f"{base_url}/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            insight_text = data['choices'][0]['message']['content'].strip()
            
            return {
                'text': insight_text,
                'model': model,
                'generated': True
            }
        else:
            current_app.logger.error(f"OpenRouter API error: {response.status_code} - {response.text}")
            return get_default_insight(user_preferences)
            
    except Exception as e:
        current_app.logger.error(f"AI service error: {str(e)}")
        return get_default_insight(user_preferences)

def get_default_insight(user_preferences=None):
    """Return a default insight if AI service is unavailable"""
    investor_type = user_preferences.get('investor_type', 'Investor') if user_preferences else 'Investor'
    assets = user_preferences.get('interested_assets', ['cryptocurrencies']) if user_preferences else ['cryptocurrencies']
    assets_str = ', '.join(assets[:3]) if assets else 'cryptocurrencies'
    
    insights = [
        f"As a {investor_type}, keep an eye on {assets_str}. Market volatility presents both opportunities and risks. Consider your risk tolerance and investment horizon when making decisions.",
        f"Today's crypto market shows continued interest in {assets_str}. For {investor_type.lower()}s, maintaining a diversified portfolio and staying informed about market trends remains key.",
        f"The {assets_str} markets are showing interesting patterns. {investor_type}s should monitor key support and resistance levels while keeping long-term fundamentals in mind."
    ]
    
    import random
    return {
        'text': random.choice(insights),
        'model': 'default',
        'generated': False
    }

