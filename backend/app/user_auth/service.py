from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException, status
from app.models.user import User, UserCreate
from app.core.security import get_password_hash, verify_password
from app.database import get_async_session
from typing import AsyncGenerator


async def get_user_by_username(session: AsyncSession, username: str):
    """Get a user by username."""
    statement = select(User).where(User.username == username)
    result = await session.exec(statement)
    return result.first()


async def get_user_by_email(session: AsyncSession, email: str):
    """Get a user by email."""
    statement = select(User).where(User.email == email)
    result = await session.exec(statement)
    return result.first()


async def authenticate_user(session: AsyncSession, username: str, password: str):
    """Authenticate a user by username and password."""
    user = await get_user_by_username(session, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


async def create_user(session: AsyncSession, user_create: UserCreate):
    """Create a new user."""
    # Check if user with username or email already exists
    existing_user = await get_user_by_username(session, user_create.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    existing_email = await get_user_by_email(session, user_create.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_create.password)
    db_user = User(
        username=user_create.username,
        email=user_create.email,
        hashed_password=hashed_password
    )
    
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    
    return db_user