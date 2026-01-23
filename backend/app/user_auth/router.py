from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import timedelta
from app.user_auth.service import authenticate_user, create_user, get_user_by_id
from app.user_auth.schemas import UserRegister, UserLogin, Token, UserPublic
from app.database import get_async_session
from app.core.security import create_access_token
from app.config import settings
from app.models.user import User, UserCreate

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=Token)
async def register(user_register: UserRegister, session: AsyncSession = Depends(get_async_session)):
    """Register a new user and return an access token."""
    try:
        # Convert UserRegister to UserCreate to match service function signature
        user_create_data = UserCreate(
            username=user_register.username,
            email=user_register.email,
            password=user_register.password
        )
        db_user = await create_user(session, user_create_data)

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


@router.get("/users/{user_id}", response_model=UserPublic)
async def get_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    """Get user information by user ID."""
    user = await get_user_by_id(session, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


@router.post("/test-register", response_model=Token)
async def test_register(user_register: UserRegister, session: AsyncSession = Depends(get_async_session)):
    """Test registration endpoint without calling create_user."""
    print(f"DEBUG: Test endpoint - Username: {user_register.username}, Email: {user_register.email}, Password length: {len(user_register.password)}")

    # Just return a dummy token without creating a user
    from datetime import timedelta
    from app.core.security import create_access_token
    from app.config import settings

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": "dummy_user_id"}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/simple-test", response_model=dict)
async def simple_test(user_register: UserRegister):
    """Simple test endpoint to see if the issue is with UserRegister."""
    print(f"DEBUG: Simple test - Username: {user_register.username}, Password length: {len(user_register.password)}")
    return {"message": "Received", "username": user_register.username, "password_length": len(user_register.password)}