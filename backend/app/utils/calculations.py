# backend/app/utils/calculations.py

import pandas as pd
from app.services.fyers import FyersService
from app.utils.symbol_utils import get_symbol_name

def get_highest_option_prices(option_chain_df, instrument_name, side: str):
    """
    Get highest option prices for either PE bid or CE ask based on side parameter.
    Args:
        option_chain_df: DataFrame containing option chain data
        instrument_name: Name of the instrument
        side: 'PE' for put options or 'CE' for call options
    """
    result = []
    
    for strike in option_chain_df['strike_price'].unique():
        # Filter options by strike price and option type
        strike_df = option_chain_df[
            (option_chain_df['strike_price'] == strike) & 
            (option_chain_df['option_type'] == side)
        ]
        
        if not strike_df.empty:
            if side == 'PE':
                price = strike_df['bid'].max()
            else:  # CE
                price = strike_df['ask'].max()
                
            # Only append if price is not 0
            if price > 0:
                result.append([instrument_name, strike, side, price])
    
    # Convert result list to DataFrame
    result_df = pd.DataFrame(result, columns=['instrument_name', 'strike_price', 'side', 'bid/ask'])
    return result_df

def get_option_chain_data(instrument_name: str, expiry_date: str, side: str) -> pd.DataFrame:
    print(f"Fetching option chain data for instrument: {instrument_name}, expiry: {expiry_date}, side: {side}")
    fyers_service = FyersService()
    print('Fyer_service instance created')
    symbol = get_symbol_name(instrument_name, expiry_date, side)
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
    
    # Get the highest option prices for the given option chain
    result_df = get_highest_option_prices(option_chain_data, instrument_name, side)
    print(f"Resulting DataFrame: {result_df}")
    return result_df

def calculate_margin_and_premium(df: pd.DataFrame) -> pd.DataFrame:
    df['margin'] = 1000  # Dummy value for margin
    df['premium'] = 50   # Dummy value for premium
    return df
