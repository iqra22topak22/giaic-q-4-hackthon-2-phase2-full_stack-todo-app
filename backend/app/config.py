import os

# Settings class for configuration
class Settings:
    # Use DATABASE_URL from environment variable
    # For Vercel deployments, this should be set to a PostgreSQL database URL
    # For local development, it can fallback to SQLite
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./todo_app.db")

    # Environment setting - defaults to 'production' for deployed environments
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

    # Additional settings can be added here
    SECRET_KEY = os.getenv("SECRET_KEY", "your-default-secret-key-change-in-production")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

settings = Settings()