# backend/app/utils/calculations.py

import pandas as pd
from services.brokers.fyers import FyersService
from utils.symbol_utils import get_symbol

def get_option_chain_data(instrument_name: str, expiry_date: str, side: str) -> pd.DataFrame:
    fyers_service = FyersService()
    symbol = get_symbol(instrument_name)
    strike_count = 50  # Adjust as needed (maximum allowed is 50)

    # Fetch option chain data
    option_chain_data = fyers_service.get_option_chain(symbol, strike_count)

    # Process data
    rows = []
    for chain in option_chain_data:
        strike_price = chain['strikePrice']
        options_list = chain.get(side.upper(), [])
        for option in options_list:
            price = option.get('ask', 0) if side.upper() == 'CE' else option.get('bid', 0)
            rows.append({
                "instrument_name": instrument_name,
                "strike_price": strike_price,
                "side": side.upper(),
                "price": price,
                "symbol": option["symbol"],
                "expiry_date": option["expiryDate"],
                # Other fields can be added as needed
            })

    df = pd.DataFrame(rows)
    return df
