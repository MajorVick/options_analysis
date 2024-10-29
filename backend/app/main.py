# backend/app/main.py
from fastapi import FastAPI
from routers import option_chain
from core.config import settings

app = FastAPI(
    title="Options Trading Analysis API",
    version="1.0.0",
    description="API for fetching option chain data and calculating margins and premiums."
)

# Include routers
app.include_router(option_chain.router, prefix="/api/v1")

# You can add middleware or exception handlers here if needed
