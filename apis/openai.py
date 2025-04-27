"""
OpenAI API client for Hyperion Unified Engine
Basic implementation with error handling
"""

import requests
import logging
import json
from typing import Dict, Any, Optional, List, Union

class OpenAIClient:
    BASE_URL = "https://api.openai.com/v1"
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle API response and errors"""
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            logging.error(f"OpenAI API HTTP error: {e}")
            try:
                error_data = response.json()
                logging.error(f"OpenAI API error details: {error_data}")
            except:
                logging.error(f"OpenAI API error status code: {response.status_code}")
            raise
        except requests.exceptions.RequestException as e:
            logging.error(f"OpenAI API request error: {e}")
            raise
        except ValueError as e:
            logging.error(f"OpenAI API JSON decode error: {e}")
            raise
    
    def create_completion(self, 
                         model: str = "gpt-3.5-turbo", 
                         messages: List[Dict[str, str]] = None,
                         max_tokens: int = 100,
                         temperature: float = 0.7) -> Dict[str, Any]:
        """Create a chat completion"""
        try:
            if messages is None:
                messages = [{"role": "user", "content": "Hello!"}]
                
            endpoint = f"{self.BASE_URL}/chat/completions"
            payload = {
                "model": model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature
            }
            
            response = self.session.post(endpoint, data=json.dumps(payload))
            return self._handle_response(response)
        except Exception as e:
            logging.error(f"Error creating completion: {e}")
            raise
    
    def list_models(self) -> Dict[str, Any]:
        """List available models"""
        try:
            endpoint = f"{self.BASE_URL}/models"
            response = self.session.get(endpoint)
            return self._handle_response(response)
        except Exception as e:
            logging.error(f"Error listing models: {e}")
            raise
