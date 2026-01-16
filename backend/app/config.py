from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./database.db"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-super-secret-key-change-this-in-production!")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DEBUG: bool = True
    ENVIRONMENT: str = os.getenv("ENV", "development")  # Use ENV environment variable, default to "development"


settings = Settings()