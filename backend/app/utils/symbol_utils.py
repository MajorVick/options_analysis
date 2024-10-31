# backend/app/utils/symbol_utils.py

import requests
import json

def get_symbols(instrument_name):
    print(f"Getting symbols for instrument: {instrument_name}")
    symbol_mappings = fetch_symbol_mappings()
    # Filter symbols where 'underSym' matches the instrument_name
    matching_symbols = []
    for symbol, details in symbol_mappings.items():
        under_sym = details.get('underSym', '').upper()
        if under_sym == instrument_name.upper():
            matching_symbols.append({'symbol': symbol, 'details': details})
    if not matching_symbols:
        raise ValueError(f"No symbols found for instrument: {instrument_name}")
    print(f"Found {len(matching_symbols)} symbols for instrument: {instrument_name}")
    return matching_symbols

def fetch_symbol_mappings():
    print("Fetching symbol mappings from URL...")
    url = "https://public.fyers.in/sym_details/NSE_FO_sym_master.json"
    response = requests.get(url)
    if response.status_code == 200:
        print(f"Successfully fetched symbols from {url}")
        data = response.json()
        return data
    else:
        print(f"Failed to fetch symbols from {url}")
        raise Exception(f"Failed to fetch symbols from {url}")
