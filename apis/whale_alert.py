"""
Whale Alert API client for Hyperion Unified Engine
Basic implementation with error handling
"""

import requests
import logging
from typing import Dict, Any, Optional

class WhaleAlertClient:
    BASE_URL = "https://api.whale-alert.io/v1"
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({"X-WA-API-KEY": api_key})
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle API response and errors"""
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            logging.error(f"Whale Alert API HTTP error: {e}")
            try:
                error_data = response.json()
                logging.error(f"Whale Alert API error details: {error_data}")
            except:
                logging.error(f"Whale Alert API error status code: {response.status_code}")
            raise
        except requests.exceptions.RequestException as e:
            logging.error(f"Whale Alert API request error: {e}")
            raise
        except ValueError as e:
            logging.error(f"Whale Alert API JSON decode error: {e}")
            raise
    
    def get_transactions(self, min_value: int = 500000, start: Optional[int] = None, end: Optional[int] = None) -> Dict[str, Any]:
        """Get large cryptocurrency transactions"""
        try:
            endpoint = f"{self.BASE_URL}/transactions"
            params = {"min_value": min_value}
            
            if start:
                params["start"] = start
            if end:
                params["end"] = end
                
            response = self.session.get(endpoint, params=params)
            return self._handle_response(response)
        except Exception as e:
            logging.error(f"Error getting whale transactions: {e}")
            raise
    
    def get_status(self) -> Dict[str, Any]:
        """Get API status and limits"""
        try:
            endpoint = f"{self.BASE_URL}/status"
            response = self.session.get(endpoint)
            return self._handle_response(response)
        except Exception as e:
            logging.error(f"Error getting API status: {e}")
            raise
