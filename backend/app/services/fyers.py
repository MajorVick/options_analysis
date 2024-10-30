# backend/app/services/brokers/fyers_service.py

from fyers_apiv3 import fyersModel
import requests
import time
import json
from app.core.config import settings

class FyersService:
    BASE_URL = "https://api.fyers.in"
    
    def __init__(self):
        self.client_id = settings.FYERS_CLIENT_ID     # e.g., "ABCD12345"
        self.client_id_hash = settings.FYERS_CLIENT_ID_HASH  # Hash of client_id received from Fyers
        self.refresh_token = settings.FYERS_REFRESH_TOKEN    # Your refresh token
        self.pin = settings.FYERS_PIN                         # Your 4-digit pin
        
        self.access_token = settings.FYERS_ACCESS_TOKEN       # Will be updated dynamically
        self.token_expires_at = settings.FYERS_TOKEN_EXPIRES_AT  # Unix timestamp
        
        self.fyers = None
        self.authenticate()
    
    def authenticate(self):
        current_time = time.time()
        if not self.access_token or current_time >= self.token_expires_at:
            # Access token is missing or expired; refresh it
            self.refresh_access_token()
        else:
            # Access token is valid; initialize the FyersModel
            self.fyers = fyersModel.FyersModel(client_id=self.client_id, token=self.access_token, is_async=False)

    def refresh_access_token(self):
        url = 'https://api-t2.fyers.in/api/v2/validate-refresh-token'
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            'grant_type': 'refresh_token',
            'appIdHash': self.client_id_hash,
            'refresh_token': self.refresh_token,
            'pin': self.pin  # Your 4-digit pin
        }
        response = requests.post(url, headers=headers, json=data)
        response_data = response.json()
        
        if response.code == 200 and response_data.get("access_token"):
            self.access_token = response_data["access_token"]
            expires_in = response_data.get("expires_in", 86400)  # Default to 24 hours if not provided
            self.token_expires_at = time.time() + expires_in - 60  # Refresh 1 minute before expiry
            
            # Save the new access token and expiry time
            self.save_tokens()
            
            # Initialize FyersModel with the new access token
            self.fyers = fyersModel.FyersModel(client_id=self.client_id, token=self.access_token, is_async=False)
        else:
            raise Exception(f"Failed to refresh access token: {response_data.get('message', 'Unknown error')}")

    def save_tokens(self):
        # Update settings
        settings.FYERS_ACCESS_TOKEN = self.access_token
        settings.FYERS_TOKEN_EXPIRES_AT = self.token_expires_at

        # Save to .env or a secure storage
        self.update_env_file({
            "FYERS_ACCESS_TOKEN": self.access_token,
            "FYERS_TOKEN_EXPIRES_AT": str(int(self.token_expires_at))
        })

    def update_env_file(self, new_vars):
        # Read the existing .env file
        env_vars = {}
        if os.path.exists('.env'):
            with open('.env', 'r') as f:
                for line in f:
                    if line.strip() and '=' in line:
                        key, value = line.strip().split('=', 1)
                        env_vars[key] = value

        # Update with new variables
        env_vars.update(new_vars)

        # Write back to .env file
        with open('.env', 'w') as f:
            for key, value in env_vars.items():
                f.write(f"{key}={value}\n")

    def get_option_chain(self, symbol: str, strike_count: int = 50):
        data = {
            "symbol": symbol,
            "strike_count": strike_count,
            "timestamp": ""
        }
        response = self.fyers.option_chain(data)
        if response["s"] == "ok":
            return response["d"]  # The 'd' key contains the data
        else:
            raise Exception(f"Failed to get option chain data: {response.get('message', 'Unknown error')}")

    def get_margin_requirement(self, symbol: str, quantity: int):
        # Fyers may provide an API endpoint for margin calculations
        # Implement the API call here, if available
        pass  # To be implemented as per Fyers API documentation
