from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from app.config import settings
import os

# Create the async database engine
database_url = settings.DATABASE_URL

# For Vercel deployment, we'll use environment variables for the database
# In serverless environments, we typically use a hosted database like Neon or Supabase
# For now, we'll use an in-memory database for testing purposes
if os.getenv("VERCEL"):
    # Use a temporary file database for Vercel deployments
    database_url = "sqlite+aiosqlite:///tmp/todo_app.db"
    # Ensure the directory exists
    db_path = database_url.replace("sqlite+aiosqlite:///", "")
    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)

# Create the async engine with appropriate settings for SQLite
connect_args = {"check_same_thread": False} if database_url.startswith("sqlite") else {}
engine = create_async_engine(database_url, echo=False, connect_args=connect_args)

async def create_db_and_tables():
    """Create database tables"""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
    except Exception as e:
        print(f"Database initialization error: {e}")
        # In serverless environments, we might not be able to create tables
        # depending on the database setup

async def get_async_session():
    async with AsyncSession(engine) as session:
        yield session