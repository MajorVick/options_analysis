# backend/app/routers/option_chain.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from utils.calculations import get_option_chain_data, calculate_margin_and_premium
from models.option_chain import OptionChainData
from services.brokers.upstox_service import UpstoxService

router = APIRouter()

@router.get("/option-chain", response_model=List[OptionChainData])
def option_chain(instrument_name: str, expiry_date: str, side: str):
    try:
        data = get_option_chain_data(instrument_name, expiry_date, side)
        result = calculate_margin_and_premium(data)
        return result.to_dict(orient='records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
