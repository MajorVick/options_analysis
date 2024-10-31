# backend/app/routers/option_chain.py

from fastapi import APIRouter, HTTPException
from app.utils.calculations import get_option_chain_data

router = APIRouter()

@router.get("/option-chain")
def option_chain(instrument_name: str, expiry_date: str, side: str):
    print(f"Received request with instrument_name: {instrument_name}, expiry_date: {expiry_date}, side: {side}")
    try:
        data = get_option_chain_data(instrument_name, expiry_date, side)
        print(f"Data retrieved: {data}")
        # For testing purposes, you can assign dummy values for margin and premium
        data['margin_required'] = 0  # Dummy value
        data['premium_earned'] = 0   # Dummy value
        print(f"Modified data with dummy values: {data}")
        return data.to_dict(orient='records')
    except Exception as e:
        # Log the error
        print(f"Error in option_chain endpoint: {str(e)}")
        # Raise an HTTPException with status code 500
        raise HTTPException(status_code=500, detail=str(e))