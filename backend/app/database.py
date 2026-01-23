from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from app.config import settings
import os

# Create the async database engine
database_url = settings.DATABASE_URL

# Update PostgreSQL URLs to use async drivers if available
if database_url.startswith("postgresql://") or database_url.startswith("postgres://"):
    try:
        # Try to use asyncpg driver and remove unsupported parameters
        import asyncpg  # Check if asyncpg is available
        # Replace both postgres:// and postgresql:// with postgresql+asyncpg://
        database_url = database_url.replace("postgres://", "postgresql+asyncpg://", 1)
        database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)

        # For Neon databases, we should handle sslmode and channel_binding parameters differently
        # asyncpg doesn't accept these parameters in the connection string, so we need to remove them
        # but we'll store them separately if needed for connection configuration

        # Remove channel_binding parameter which is not supported by asyncpg
        if "channel_binding=" in database_url:
            import re
            database_url = re.sub(r'&channel_binding=[^&]*', '', database_url)
            # Clean up any double ampersands that might result
            database_url = database_url.replace("&&", "&")
        # Remove sslmode parameter which is not supported by asyncpg
        if "sslmode=" in database_url:
            import re
            database_url = re.sub(r'&?sslmode=[^&]*', '', database_url)
            # Clean up any double ampersands that might result
            database_url = database_url.replace("&&", "&")
            # Ensure the URL still has the correct format after removal
            if "?&" in database_url:
                database_url = database_url.replace("?&", "?")

        # For Neon, we may need to handle other parameters differently
        if "neon.tech" in database_url:
            if "options=" in database_url:
                # Handle options parameter specially for Neon
                pass  # Keep options as is for Neon
    except ImportError:
        # If asyncpg is not available, try psycopg2-binary as fallback
        try:
            import psycopg2  # Check if psycopg2 is available
            # Replace with psycopg2 driver
            database_url = database_url.replace("postgres://", "postgresql+psycopg2://", 1)
            database_url = database_url.replace("postgresql://", "postgresql+psycopg2://", 1)
            print("Using psycopg2 driver - this is not an async driver but will work for now")
        except ImportError:
            # If neither is available, keep the original URL
            print("Warning: Neither asyncpg nor psycopg2-binary is available.")
            pass
elif "sqlite" not in database_url:
    # If it's not PostgreSQL and not SQLite, default to SQLite for development
    print("Database URL is not PostgreSQL or SQLite, defaulting to SQLite for development")
    database_url = "sqlite+aiosqlite:///./todo_app.db"

# For Vercel deployments with PostgreSQL, we don't need special handling
# For local SQLite, ensure the directory exists
if database_url.startswith("sqlite+aiosqlite:///"):
    # Ensure the directory exists for SQLite file
    db_path = database_url.replace("sqlite+aiosqlite:///", "")
    # For Vercel, we'll skip creating directories since file system is ephemeral
    if settings.ENVIRONMENT not in ["production", "local_with_db"]:
        os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)

# Create the async engine with appropriate settings
# For SQLite we need check_same_thread=False, for PostgreSQL we don't
connect_args = {"check_same_thread": False} if "sqlite" in database_url else {}

# Additional engine kwargs for PostgreSQL in production
engine_kwargs = {}
if "postgresql" in database_url.lower():
    engine_kwargs.update({
        "pool_size": 5,
        "max_overflow": 10,
        "pool_pre_ping": True,
        "pool_recycle": 300
    })
elif "sqlite" in database_url.lower():
    # For SQLite, use memory database in production to avoid file system issues
    if settings.ENVIRONMENT == "production":
        database_url = "sqlite+aiosqlite:///:memory:"
        connect_args = {"check_same_thread": False}

engine = create_async_engine(
    database_url,
    echo=(settings.ENVIRONMENT in ["development", "local_with_db"]),  # Echo in development and local_with_db
    connect_args=connect_args,
    **engine_kwargs
)

async def create_db_and_tables():
    """Create database tables"""
    # For Vercel deployments with external DB, we can create tables
    # For SQLite on Vercel, table creation will happen but data won't persist
    if "sqlite" in settings.DATABASE_URL and settings.ENVIRONMENT == "production":
        # Create tables in memory database for Vercel
        print("Creating tables in memory database for Vercel deployment")

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_async_session():
    async with AsyncSession(engine) as session:
        yield session