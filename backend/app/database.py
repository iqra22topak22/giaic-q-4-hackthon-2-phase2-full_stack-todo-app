from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from app.config import settings
import os

# Create the async database engine
database_url = settings.DATABASE_URL

# For Vercel deployments with PostgreSQL, we don't need special handling
# For local SQLite, ensure the directory exists
if database_url.startswith("sqlite+aiosqlite:///"):
    # Ensure the directory exists for SQLite file
    db_path = database_url.replace("sqlite+aiosqlite:///", "")
    # For Vercel, we'll skip creating directories since file system is ephemeral
    if settings.ENVIRONMENT != "production":
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
    echo=(settings.ENVIRONMENT == "development"),  # Only echo in development
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