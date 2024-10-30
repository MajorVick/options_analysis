# backend/app/utils/symbol_utils.py

import requests
import json
import os
import time

SYMBOL_CACHE_FILE = "symbol_cache.json"
SYMBOL_CACHE_EXPIRY = 24 * 3600  # Cache expiry in seconds (e.g., refresh every 24 hours)

def get_symbol(instrument_name):
    symbol_mappings = load_symbol_mappings()
    symbol = symbol_mappings.get(instrument_name.upper())
    if not symbol:
        raise ValueError(f"Symbol not found for instrument: {instrument_name}")
    return symbol

def load_symbol_mappings():
    # Check if cache exists and is valid
    if os.path.exists(SYMBOL_CACHE_FILE):
        cache_age = time.time() - os.path.getmtime(SYMBOL_CACHE_FILE)
        if cache_age < SYMBOL_CACHE_EXPIRY:
            # Load from cache
            with open(SYMBOL_CACHE_FILE, 'r') as f:
                return json.load(f)
    
    # Fetch and build the symbol mappings
    symbol_mappings = fetch_symbol_mappings()
    # Save to cache
    with open(SYMBOL_CACHE_FILE, 'w') as f:
        json.dump(symbol_mappings, f)
    return symbol_mappings

def fetch_symbol_mappings():
    # URLs for symbol master JSON files
    symbol_master_urls = [
        "https://public.fyers.in/sym_details/NSE_FO_sym_master.json",  # NSE Equity Derivatives
        "https://public.fyers.in/sym_details/NSE_CM_sym_master.json",  # NSE Capital Market
    ]
    symbol_mappings = {}
    for url in symbol_master_urls:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for item in data:
                symbol = item.get('symbol')
                description = item.get('name', '').upper()
                # Map the instrument name to the symbol
                if description:
                    symbol_mappings[description] = symbol
        else:
            print(f"Failed to fetch symbols from {url}")
    return symbol_mappings
