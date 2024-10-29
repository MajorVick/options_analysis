# backend/app/utils/calculations.py
import pandas as pd
from services.brokers.upstox_service import UpstoxService

def get_option_chain_data(instrument_name: str, expiry_date: str, side: str) -> pd.DataFrame:
    upstox = UpstoxService()
    
    # Map instrument_name to instrument_key
    instrument_key = get_instrument_key(instrument_name)
    
    # Fetch option chain data
    option_chain_data = upstox.get_option_chain(instrument_key, expiry_date)
    
    # Process data
    rows = []
    for item in option_chain_data:
        strike_price = item["strike_price"]
        if side == "PE":
            option_data = item["put_options"]
            price = option_data["market_data"]["bid_price"]
        elif side == "CE":
            option_data = item["call_options"]
            price = option_data["market_data"]["ask_price"]
        else:
            continue  # Invalid side
        
        rows.append({
            "instrument_name": instrument_name,
            "strike_price": strike_price,
            "side": side,
            "price": price,
            "instrument_key": option_data["instrument_key"]
        })
    
    df = pd.DataFrame(rows)
    return df

def calculate_margin_and_premium(data: pd.DataFrame) -> pd.DataFrame:
    upstox = UpstoxService()
    margins = []
    premiums = []
    
    for _, row in data.iterrows():
        instrument_key = row["instrument_key"]
        # Assuming lot_size is constant; in real scenario, fetch lot size from API or config
        lot_size = 75  # Example lot size for NIFTY options
        transaction_type = "SELL"
        
        # Fetch margin requirement from API
        margin = upstox.get_margin_requirement(transaction_type, instrument_key, lot_size)
        premium_earned = row["price"] * lot_size
        
        margins.append(margin)
        premiums.append(premium_earned)
    
    data["margin_required"] = margins
    data["premium_earned"] = premiums
    return data
