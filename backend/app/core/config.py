from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    FYERS_CLIENT_ID: str
    FYERS_CLIENT_ID_HASH: str
    FYERS_ACCESS_TOKEN: str
    FYERS_REFRESH_TOKEN: str
    FYERS_PIN: str
    api_host: str
    api_port: int
    environment: str
    FYERS_TOKEN_EXPIRES_AT: int  # Added this line

    class Config:
        env_file = ".env"

settings = Settings()

# Debugging: Print loaded settings
print("Loaded Settings:")
print(f"FYERS_CLIENT_ID: {settings.FYERS_CLIENT_ID}")
print(f"FYERS_CLIENT_ID_HASH: {settings.FYERS_CLIENT_ID_HASH}")
print(f"FYERS_REFRESH_TOKEN: {settings.FYERS_REFRESH_TOKEN}")
print(f"FYERS_PIN: {settings.FYERS_PIN}")
print(f"api_host: {settings.api_host}")
print(f"api_port: {settings.api_port}")
print(f"environment: {settings.environment}")
print(f"fyers_token_expires_at: {settings.FYERS_TOKEN_EXPIRES_AT}")  # Optional