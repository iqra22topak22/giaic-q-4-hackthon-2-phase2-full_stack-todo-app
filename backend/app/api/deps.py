from fastapi import Depends
from app.database import get_async_session
from app.auth import get_current_user_optional
from sqlmodel.ext.asyncio.session import AsyncSession

async def get_db_session():
    async for session in get_async_session():
        yield session

# Dependency that provides the current user ID
# In development, this allows unauthenticated access with a default user ID
CurrentUser = Depends(get_current_user_optional)