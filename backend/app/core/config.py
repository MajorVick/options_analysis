# backend/app/core/config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    UPSTOX_API_KEY: str
    UPSTOX_API_SECRET: str
    UPSTOX_ACCESS_TOKEN: str

    class Config:
        env_file = ".env"

settings = Settings()
