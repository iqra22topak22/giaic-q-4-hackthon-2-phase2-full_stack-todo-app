from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import timedelta
from app.user_auth.service import authenticate_user, create_user
from app.user_auth.schemas import UserRegister, UserLogin, Token
from app.database import get_async_session
from app.core.security import create_access_token
from app.config import settings
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=Token)
async def register(user_register: UserRegister, session: AsyncSession = Depends(get_async_session)):
    """Register a new user and return an access token."""
    try:
        db_user = await create_user(session, UserRegister(**user_register.dict()))
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(db_user.id)}, expires_delta=access_token_expires
        )
        
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during registration: {str(e)}"
        )


@router.post("/login", response_model=Token)
async def login(user_login: UserLogin, session: AsyncSession = Depends(get_async_session)):
    """Authenticate user and return an access token."""
    user = await authenticate_user(session, user_login.username, user_login.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}