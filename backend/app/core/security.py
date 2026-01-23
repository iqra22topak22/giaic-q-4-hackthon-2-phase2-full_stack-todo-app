from datetime import datetime, timedelta
from typing import Optional
import jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config import settings

import hashlib
import secrets

# JWT security scheme
security = HTTPBearer(auto_error=False)

def get_password_hash(password: str) -> str:
    """Generate a hash for the given password using SHA-256 with salt."""
    # Generate a random salt
    salt = secrets.token_hex(16)
    # Combine password and salt
    pwd_salt = password + salt
    # Hash the combination
    hashed_pwd = hashlib.sha256(pwd_salt.encode()).hexdigest()
    # Return salt + hashed password (first 32 chars for salt, rest for hash)
    return salt + hashed_pwd

def verify_password(plain_password: str, salted_hashed_password: str) -> bool:
    """Verify a plain password against its salted hash."""
    if len(salted_hashed_password) < 32:  # Minimum length for salt
        return False

    # Extract salt (first 32 characters, which represents 16 bytes in hex)
    salt = salted_hashed_password[:32]
    stored_hash = salted_hashed_password[32:]

    # Hash the input password with the same salt
    pwd_salt = plain_password + salt
    hashed_input = hashlib.sha256(pwd_salt.encode()).hexdigest()

    # Compare the hashes
    return hashed_input == stored_hash

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)  # Default 30 minutes
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """Verify the JWT token and return the payload."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Get the current user from the JWT token.
    Returns the user_id extracted from the token.
    """
    token = credentials.credentials
    payload = verify_token(token)

    # Extract user_id from the token
    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_id