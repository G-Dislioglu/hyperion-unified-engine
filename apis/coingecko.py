"""
CoinGecko API client for Hyperion Unified Engine
Basic implementation with error handling
"""

import requests
import logging
from typing import Dict, Any, Optional, List

class CoinGeckoClient:
    BASE_URL = "https://api.coingecko.com/api/v3"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.session = requests.Session()
        if api_key:
            self.session.params = {"x_cg_pro_api_key": api_key}
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle API response and errors"""
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            logging.error(f"CoinGecko API HTTP error: {e}")
            try:
                error_data = response.json()
                logging.error(f"CoinGecko API error details: {error_data}")
            except:
                logging.error(f"CoinGecko API error status code: {response.status_code}")
            raise
        except requests.exceptions.RequestException as e:
            logging.error(f"CoinGecko API request error: {e}")
            raise
        except ValueError as e:
            logging.error(f"CoinGecko API JSON decode error: {e}")
            raise
    
    def get_coin_price(self, coin_ids: List[str], vs_currencies: List[str]) -> Dict[str, Any]:
        """Get current price for specified coins in specified currencies"""
        try:
            endpoint = f"{self.BASE_URL}/simple/price"
            params = {
                "ids": ",".join(coin_ids),
                "vs_currencies": ",".join(vs_currencies)
            }
            response = self.session.get(endpoint, params=params)
            return self._handle_response(response)
        except Exception as e:
            logging.error(f"Error getting coin prices: {e}")
            raise
    
    def get_coin_market_data(self, coin_id: str) -> Dict[str, Any]:
        """Get detailed market data for a specific coin"""
        try:
            endpoint = f"{self.BASE_URL}/coins/{coin_id}"
            params = {"localization": "false", "tickers": "false", "community_data": "false", "developer_data": "false"}
            response = self.session.get(endpoint, params=params)
            return self._handle_response(response)
        except Exception as e:
            logging.error(f"Error getting market data for {coin_id}: {e}")
            raise
