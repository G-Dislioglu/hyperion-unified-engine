"""
Binance API client for Hyperion Unified Engine
Basic implementation with error handling
"""

import requests
import logging
from typing import Dict, Any, Optional

class BinanceClient:
    BASE_URL = "https://api.binance.com"
    
    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None):
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        if api_key:
            self.session.headers.update({"X-MBX-APIKEY": api_key})
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle API response and errors"""
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            logging.error(f"Binance API HTTP error: {e}")
            try:
                error_data = response.json()
                logging.error(f"Binance API error details: {error_data}")
            except:
                logging.error(f"Binance API error status code: {response.status_code}")
            raise
        except requests.exceptions.RequestException as e:
            logging.error(f"Binance API request error: {e}")
            raise
        except ValueError as e:
            logging.error(f"Binance API JSON decode error: {e}")
            raise
    
    def get_ticker_price(self, symbol: str) -> Dict[str, Any]:
        """Get current price for a symbol"""
        try:
            endpoint = f"{self.BASE_URL}/api/v3/ticker/price"
            params = {"symbol": symbol}
            response = self.session.get(endpoint, params=params)
            return self._handle_response(response)
        except Exception as e:
            logging.error(f"Error getting ticker price for {symbol}: {e}")
            raise
    
    def get_exchange_info(self) -> Dict[str, Any]:
        """Get exchange information"""
        try:
            endpoint = f"{self.BASE_URL}/api/v3/exchangeInfo"
            response = self.session.get(endpoint)
            return self._handle_response(response)
        except Exception as e:
            logging.error(f"Error getting exchange info: {e}")
            raise
