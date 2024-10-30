# backend/app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    FYERS_CLIENT_ID: str
    FYERS_CLIENT_ID_HASH: str
    FYERS_REFRESH_TOKEN: str
    FYERS_PIN: str
    FYERS_ACCESS_TOKEN: str = ""
    FYERS_TOKEN_EXPIRES_AT: int = 0
    
    # Add these fields
    api_host: str
    api_port: str
    environment: str

    class Config:
        env_file = ".env"


settings = Settings()
