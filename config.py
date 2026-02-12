import os

from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    Uses pydantic for validation and type checking.
    """

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    DATABASE_URL: str

    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080",
    ]

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings():
    """
    Cache settings to avoid reading .env file multiple times.
    Returns the same Settings instance on subsequent calls.
    """
    return Settings()

settings = get_settings()