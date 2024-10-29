# backend/app/services/brokers/upstox_service.py
import requests
import os
from core.config import settings

class UpstoxService:
    BASE_URL = "https://api.upstox.com/v2"

    def __init__(self):
        self.access_token = settings.UPSTOX_ACCESS_TOKEN
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/json"
        }

    def get_option_chain(self, instrument_key: str, expiry_date: str):
        endpoint = f"{self.BASE_URL}/option/chain"
        params = {
            "instrument_key": instrument_key,
            "expiry_date": expiry_date
        }
        response = requests.get(endpoint, headers=self.headers, params=params)
        if response.status_code == 200:
            return response.json()["data"]
        else:
            response.raise_for_status()

    def get_margin_requirement(self, transaction_type: str, instrument_key: str, lot_size: int):
        endpoint = f"{self.BASE_URL}/charges/margin"
        payload = {
            "transaction_type": transaction_type,
            "exchange": "NSE_FO",
            "instrument_key": instrument_key,
            "quantity": lot_size
        }
        response = requests.post(endpoint, headers=self.headers, json=payload)
        if response.status_code == 200:
            return response.json()["data"]["margin"]
        else:
            response.raise_for_status()
