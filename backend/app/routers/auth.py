"""
Authentication router for user registration and login.
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from ..models.user import UserCreate, User, Token
from ..services.auth_service import AuthService
from ..core.dependencies import get_current_active_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["authentication"])
auth_service = AuthService()


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate):
    """
    Register a new user.

    Args:
        user (UserCreate): User registration data

    Returns:
        User: Created user

    Raises:
        HTTPException: If user already exists

    Example:
        POST /api/v0/auth/register
        {
            "email": "john@example.com",
            "username": "john",
            "password": "password123"
        }

        Response:
        {
            "id": 1,
            "email": "john@example.com",
            "username": "john",
            "is_active": true,
            "created_at": "2025-10-27T12:00:00"
        }
    """
    try:
        new_user = auth_service.create_user(user)
        logger.info(f"User registered: {new_user.username}")
        return new_user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login with username and password.

    Args:
        form_data (OAuth2PasswordRequestForm): Login credentials

    Returns:
        Token: JWT access token

    Raises:
        HTTPException: If credentials are invalid

    Example:
        POST /api/v0/auth/login
        Form data:
            username=john
            password=password123

        Response:
        {
            "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
            "token_type": "bearer"
        }
    """
    user = auth_service.authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = auth_service.create_access_token_for_user(user)
    logger.info(f"User logged in: {user.username}")

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
    Get current authenticated user.

    Args:
        current_user (User): Current user from JWT token

    Returns:
        User: Current user data

    Example:
        GET /api/v0/auth/me
        Authorization: Bearer <token>

        Response:
        {
            "id": 1,
            "email": "john@example.com",
            "username": "john",
            "is_active": true,
            "created_at": "2025-10-27T12:00:00"
        }
    """
    return current_user
