# backend/app/utils/calculations.py

import pandas as pd
from app.services.fyers import FyersService
from app.utils.symbol_utils import get_symbols

def get_option_chain_data(instrument_name: str, expiry_date: str, side: str) -> pd.DataFrame:
    print(f"Fetching option chain data for instrument: {instrument_name}, expiry: {expiry_date}, side: {side}")
    fyers_service = FyersService()
    print('Fyer_service instance created')
    symbol = get_symbols(instrument_name)
    print(f"Symbol resolved to: {symbol}")
    strike_count = 50  # Adjust as needed (maximum allowed is 50)

    try:
        # Fetch option chain data
        option_chain_data = fyers_service.get_option_chain(symbol, strike_count)
        print(f"Option chain data fetched successfully: {option_chain_data}")
    except Exception as e:
        # Handle exceptions from the FyersService
        print(f"Error fetching option chain data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    # Process data
    rows = []
    for chain in option_chain_data:
        strike_price = chain['strikePrice']
        options_list = chain.get(side.upper(), [])
        print(f"Processing strike price: {strike_price}, options list: {options_list}")
        for option in options_list:
            price = option.get('ask', 0) if side.upper() == 'CE' else option.get('bid', 0)
            print(f"Processing option: {option}, resolved price: {price}")
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
    print(f"Final DataFrame constructed: {df}")
    return df

def calculate_margin_and_premium(df: pd.DataFrame) -> pd.DataFrame:
    df['margin'] = 1000  # Dummy value for margin
    df['premium'] = 50   # Dummy value for premium
    return df
