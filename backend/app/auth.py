from fastapi import HTTPException, Depends, status, Request, Path
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.security import SecurityScopes
import jwt
import os
from app.config import settings
from typing import Optional

# Custom HTTPBearer class that returns 401 instead of 403 for missing tokens
class CustomHTTPBearer(HTTPBearer):
    def __init__(self, *args, **kwargs):
        # Ensure auto_error is False so we can handle the error ourselves
        kwargs.setdefault("auto_error", False)
        super().__init__(*args, **kwargs)

    async def __call__(self, request):
        # Get the authorization header from the request
        authorization = request.headers.get("Authorization")
        scheme = None
        param = None

        if authorization:
            try:
                scheme, param = authorization.split(" ", 1)
                if scheme.lower() != "bearer":
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid authentication scheme",
                        headers={"WWW-Authenticate": "Bearer"},
                    )
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authorization header format",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        else:
            # No authorization header provided
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization header is missing",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Return the credentials
        return HTTPAuthorizationCredentials(scheme=scheme, credentials=param)

# Define security with custom class
security = CustomHTTPBearer()

def verify_token(token: str) -> Optional[dict]:
    """
    Verify the JWT token using the Better Auth shared secret
    """
    # Use BETTER_AUTH_SECRET from environment variables
    better_auth_secret = os.getenv("BETTER_AUTH_SECRET")
    if not better_auth_secret:
        # Fallback to SECRET_KEY if BETTER_AUTH_SECRET is not set
        better_auth_secret = settings.SECRET_KEY

    try:
        payload = jwt.decode(
            token,
            better_auth_secret,
            algorithms=[settings.ALGORITHM]
        )
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
    Get the current user from the JWT token
    Returns the user_id extracted from the token
    """
    # The custom security class already raises 401 if credentials are None
    token = credentials.credentials
    payload = verify_token(token)

    # Extract user_id from the token (assuming it's in 'user_id' or 'sub' field)
    user_id = payload.get("user_id") or payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_id

def get_current_user_optional(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Get the current user from the JWT token in development mode.
    If no token is provided or invalid, return a default user ID.
    In development, also allow mock-user-id without a token.
    """
    if settings.ENVIRONMENT == "development":
        try:
            token = credentials.credentials
            payload = verify_token(token)

            # Extract user_id from the token (assuming it's in 'user_id' or 'sub' field)
            user_id = payload.get("user_id") or payload.get("sub")

            if user_id is None:
                # If token validation fails in development, return a default user ID
                return "dev-user-id"

            return user_id
        except Exception:
            # If any error occurs (invalid token, etc.), return a default user ID in development
            return "dev-user-id"
    else:
        # In production, always require valid authentication
        token = credentials.credentials
        try:
            payload = verify_token(token)

            # Extract user_id from the token (assuming it's in 'user_id' or 'sub' field)
            user_id = payload.get("user_id") or payload.get("sub")

            if user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            return user_id
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

def get_current_user_dev_bypass(user_id: str = None) -> str:
    """
    Development-only function to bypass authentication and return the user_id directly.
    This allows mock-user-id to be used without a token in development.
    """
    if settings.ENVIRONMENT == "development":
        # If user_id is provided and is "mock-user-id", return it directly
        if user_id and user_id == "mock-user-id":
            return user_id
        # Otherwise return a default dev user ID
        return "dev-user-id"
    else:
        # In production, this function shouldn't be used
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Direct user ID bypass is only allowed in development",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_user_id_or_mock(user_id: str) -> str:
    """
    A dependency that returns the user_id if in development and it's mock-user-id,
    otherwise performs normal authentication.
    This is used for path parameters in development.
    """
    if settings.ENVIRONMENT == "development" and user_id == "mock-user-id":
        return user_id
    else:
        # In production or for other user IDs, require proper authentication
        # For this to work properly, we need to handle it differently
        # Since this function can't use Depends, we'll return the user_id as-is
        # The actual authentication will happen in the routes that require it
        return user_id

def get_authenticated_user_id_from_path():
    """
    A dependency that returns the authenticated user ID based on the path parameter and credentials.
    In development, if the path user_id is "mock-user-id", authentication is bypassed.
    In production, proper authentication is required.
    """
    async def dependency(request: Request, user_id: str = Path(...)):
        if settings.ENVIRONMENT.lower() == "development" and user_id == "mock-user-id":
            # In development, allow mock-user-id without authentication
            return user_id
        else:
            # For other user IDs, check for credentials
            authorization = request.headers.get("Authorization")

            if authorization:
                try:
                    scheme, param = authorization.split(" ", 1)
                    if scheme.lower() != "bearer":
                        raise HTTPException(
                            status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid authentication scheme",
                            headers={"WWW-Authenticate": "Bearer"},
                        )
                except ValueError:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid authorization header format",
                            headers={"WWW-Authenticate": "Bearer"},
                        )

                credentials = HTTPAuthorizationCredentials(scheme=scheme, credentials=param)

                if settings.ENVIRONMENT.lower() == "development":
                    # In development, with credentials provided, validate them
                    try:
                        token = credentials.credentials
                        if token:
                            payload = verify_token(token)
                            extracted_user_id = payload.get("user_id") or payload.get("sub")
                            return extracted_user_id or user_id
                    except Exception:
                        # If token validation fails, return the path user ID
                        return user_id
                else:
                    # In production, require proper authentication
                    try:
                        token = credentials.credentials
                        payload = verify_token(token)
                        extracted_user_id = payload.get("user_id") or payload.get("sub")

                        if extracted_user_id is None:
                            raise HTTPException(
                                status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Could not validate credentials",
                                headers={"WWW-Authenticate": "Bearer"},
                            )

                        # Check if the token user_id matches the path user_id
                        if extracted_user_id != user_id:
                            raise HTTPException(
                                status_code=status.HTTP_403_FORBIDDEN,
                                detail="Access denied: User ID mismatch",
                                headers={"WWW-Authenticate": "Bearer"},
                            )

                        return extracted_user_id
                    except HTTPException:
                        # Re-raise HTTP exceptions (like 401)
                        raise
                    except Exception as e:
                        raise HTTPException(
                            status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid authentication credentials",
                            headers={"WWW-Authenticate": "Bearer"},
                        )
            else:
                # No authorization header provided
                if settings.ENVIRONMENT.lower() == "development":
                    # In development, return the path user ID if no auth header is provided
                    return user_id
                else:
                    # In production, require authentication
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Authorization header is missing",
                        headers={"WWW-Authenticate": "Bearer"},
                    )

    return Depends(dependency)


def get_authenticated_user_id(path_user_id: str):
    """
    A dependency that returns the authenticated user ID based on the path parameter and credentials.
    In development, if the path_user_id is "mock-user-id", authentication is bypassed.
    In production, proper authentication is required.
    """
    async def dependency(request):
        if settings.ENVIRONMENT.lower() == "development" and path_user_id == "mock-user-id":
            # In development, allow mock-user-id without authentication
            return path_user_id
        else:
            # For other user IDs, check for credentials
            authorization = request.headers.get("Authorization")

            if authorization:
                try:
                    scheme, param = authorization.split(" ", 1)
                    if scheme.lower() != "bearer":
                        raise HTTPException(
                            status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid authentication scheme",
                            headers={"WWW-Authenticate": "Bearer"},
                        )
                except ValueError:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid authorization header format",
                            headers={"WWW-Authenticate": "Bearer"},
                        )

                credentials = HTTPAuthorizationCredentials(scheme=scheme, credentials=param)

                if settings.ENVIRONMENT.lower() == "development":
                    # In development, with credentials provided, validate them
                    try:
                        token = credentials.credentials
                        if token:
                            payload = verify_token(token)
                            user_id = payload.get("user_id") or payload.get("sub")
                            return user_id or path_user_id
                    except Exception:
                        # If token validation fails, return the path user ID
                        return path_user_id
                else:
                    # In production, require proper authentication
                    try:
                        token = credentials.credentials
                        payload = verify_token(token)
                        user_id = payload.get("user_id") or payload.get("sub")

                        if user_id is None:
                            raise HTTPException(
                                status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Could not validate credentials",
                                headers={"WWW-Authenticate": "Bearer"},
                            )

                        # Check if the token user_id matches the path user_id
                        if user_id != path_user_id:
                            raise HTTPException(
                                status_code=status.HTTP_403_FORBIDDEN,
                                detail="Access denied: User ID mismatch",
                                headers={"WWW-Authenticate": "Bearer"},
                            )

                        return user_id
                    except HTTPException:
                        # Re-raise HTTP exceptions (like 401)
                        raise
                    except Exception as e:
                        raise HTTPException(
                            status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid authentication credentials",
                            headers={"WWW-Authenticate": "Bearer"},
                        )
            else:
                # No authorization header provided
                if settings.ENVIRONMENT.lower() == "development":
                    # In development, return the path user ID if no auth header is provided
                    return path_user_id
                else:
                    # In production, require authentication
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Authorization header is missing",
                        headers={"WWW-Authenticate": "Bearer"},
                    )

    return Depends(dependency)

