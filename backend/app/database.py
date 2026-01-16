from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from app.config import settings
import os

# Create the async database engine
database_url = settings.DATABASE_URL

# For SQLite, we need to handle the path properly
if database_url.startswith("sqlite+aiosqlite:///"):
    # Ensure the directory exists for SQLite file
    db_path = database_url.replace("sqlite+aiosqlite:///", "")
    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)

# Create the async engine with appropriate settings for SQLite
connect_args = {"check_same_thread": False} if database_url.startswith("sqlite") else {}
engine = create_async_engine(database_url, echo=True, connect_args=connect_args)

async def create_db_and_tables():
    """Create database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_async_session():
    async with AsyncSession(engine) as session:
        yield session