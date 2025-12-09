"""
CoinGecko API service for fetching cryptocurrency prices
"""
import requests
from flask import current_app

def get_coin_prices(interested_assets=None, limit=10):
    """
    Fetch cryptocurrency prices from CoinGecko
    
    Args:
        interested_assets: List of coin IDs user is interested in (e.g., ['bitcoin', 'ethereum'])
        limit: Maximum number of coins to return
    
    Returns:
        List of coin data with prices
    """
    try:
        base_url = current_app.config['COINGECKO_BASE_URL']
        
        # If user has specific assets, fetch those
        if interested_assets and len(interested_assets) > 0:
            # Map common names to CoinGecko IDs
            coin_id_map = {
                'bitcoin': 'bitcoin',
                'btc': 'bitcoin',
                'ethereum': 'ethereum',
                'eth': 'ethereum',
                'binancecoin': 'binancecoin',
                'bnb': 'binancecoin',
                'cardano': 'cardano',
                'ada': 'cardano',
                'solana': 'solana',
                'sol': 'solana',
                'ripple': 'ripple',
                'xrp': 'ripple',
                'polkadot': 'polkadot',
                'dot': 'polkadot',
                'dogecoin': 'dogecoin',
                'doge': 'dogecoin',
                'chainlink': 'chainlink',
                'link': 'chainlink',
                'litecoin': 'litecoin',
                'ltc': 'litecoin'
            }
            
            # Convert user input to CoinGecko IDs
            coin_ids = []
            for asset in interested_assets:
                asset_lower = asset.lower().strip()
                if asset_lower in coin_id_map:
                    coin_ids.append(coin_id_map[asset_lower])
                elif asset_lower not in coin_ids:
                    coin_ids.append(asset_lower)
            
            if coin_ids:
                # Fetch specific coins
                ids_param = ','.join(coin_ids[:limit])
                url = f"{base_url}/simple/price"
                params = {
                    'ids': ids_param,
                    'vs_currencies': 'usd',
                    'include_24hr_change': 'true',
                    'include_market_cap': 'true'
                }
                
                response = requests.get(url, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    coins = []
                    for coin_id, price_data in data.items():
                        coins.append({
                            'id': coin_id,
                            'name': coin_id.capitalize(),
                            'price_usd': price_data.get('usd', 0),
                            'price_change_24h': price_data.get('usd_24h_change', 0),
                            'market_cap': price_data.get('usd_market_cap', 0)
                        })
                    return coins
        
        # Fallback: Get top coins by market cap
        url = f"{base_url}/coins/markets"
        params = {
            'vs_currency': 'usd',
            'order': 'market_cap_desc',
            'per_page': limit,
            'page': 1,
            'sparkline': False
        }
        
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            coins = []
            for coin in data:
                coins.append({
                    'id': coin['id'],
                    'name': coin['name'],
                    'symbol': coin['symbol'].upper(),
                    'price_usd': coin['current_price'],
                    'price_change_24h': coin.get('price_change_percentage_24h', 0),
                    'market_cap': coin.get('market_cap', 0),
                    'image': coin.get('image', '')
                })
            return coins
        
        # If API fails, return empty list
        return []
        
    except Exception as e:
        current_app.logger.error(f"CoinGecko API error: {str(e)}")
        return []

