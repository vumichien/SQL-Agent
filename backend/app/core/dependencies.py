"""
Dependency injection utilities for FastAPI.

Provides dependencies for authentication and authorization.
"""

from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .security import decode_token


# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v0/auth/login",
    auto_error=False  # Make authentication optional for some routes
)


async def get_current_user(token: Optional[str] = Depends(oauth2_scheme)):
    """
    Get the current authenticated user from JWT token.

    Args:
        token (str): JWT token from Authorization header

    Returns:
        User: The authenticated user

    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not token:
        raise credentials_exception

    payload = decode_token(token)
    if payload is None:
        raise credentials_exception

    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    # Import here to avoid circular dependency
    from ..services.auth_service import AuthService

    auth_service = AuthService()
    user = auth_service.get_user_by_id(int(user_id))

    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(current_user = Depends(get_current_user)):
    """
    Get the current active user (checks if user is not disabled).

    Args:
        current_user: User from get_current_user dependency

    Returns:
        User: The active user

    Raises:
        HTTPException: If user is inactive
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )

    return current_user


async def get_optional_user(token: Optional[str] = Depends(oauth2_scheme)):
    """
    Get the current user if authenticated, otherwise return None.

    Useful for routes that work both with and without authentication.

    Args:
        token (str, optional): JWT token from Authorization header

    Returns:
        User or None: The authenticated user, or None if not authenticated
    """
    if not token:
        return None

    payload = decode_token(token)
    if payload is None:
        return None

    user_id: str = payload.get("sub")
    if user_id is None:
        return None

    # Import here to avoid circular dependency
    from ..services.auth_service import AuthService

    auth_service = AuthService()
    user = auth_service.get_user_by_id(int(user_id))

    return user
