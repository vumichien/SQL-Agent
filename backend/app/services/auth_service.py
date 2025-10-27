"""
Authentication service for user management.

Handles user registration, login, and authentication.
"""

import sqlite3
from datetime import timedelta
from typing import Optional
from ..db.base import get_db
from ..models.user import User, UserCreate
from ..core.security import verify_password, get_password_hash, create_access_token
from ..core.config import settings


class AuthService:
    """Service for user authentication and management."""

    def __init__(self):
        """Initialize authentication service."""
        self.db = get_db()

    def create_user(self, user: UserCreate) -> User:
        """
        Create a new user.

        Args:
            user (UserCreate): User registration data

        Returns:
            User: Created user

        Raises:
            ValueError: If user already exists

        Example:
            >>> auth_service = AuthService()
            >>> new_user = auth_service.create_user(
            ...     UserCreate(
            ...         email="john@example.com",
            ...         username="john",
            ...         password="password123"
            ...     )
            ... )
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            # Check if user exists
            cursor.execute(
                "SELECT id FROM users WHERE email = ? OR username = ?",
                (user.email, user.username)
            )
            if cursor.fetchone():
                raise ValueError("User with this email or username already exists")

            # Create user
            hashed_password = get_password_hash(user.password)
            cursor.execute(
                """
                INSERT INTO users (email, username, hashed_password)
                VALUES (?, ?, ?)
                """,
                (user.email, user.username, hashed_password)
            )

            user_id = cursor.lastrowid
            conn.commit()

            # Return created user
            return self.get_user_by_id(user_id)

        except ValueError:
            raise
        except Exception as e:
            conn.rollback()
            raise ValueError(f"Failed to create user: {str(e)}")
        finally:
            conn.close()

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """
        Authenticate a user by username and password.

        Args:
            username (str): Username
            password (str): Plain text password

        Returns:
            User or None: User if authenticated, None otherwise

        Example:
            >>> auth_service = AuthService()
            >>> user = auth_service.authenticate_user("john", "password123")
            >>> if user:
            ...     print(f"Welcome {user.username}!")
        """
        user = self.get_user_by_username(username)
        if not user:
            return None

        # Get hashed password
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT hashed_password FROM users WHERE username = ?",
            (username,)
        )
        result = cursor.fetchone()
        conn.close()

        if not result or not verify_password(password, result[0]):
            return None

        return user

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Get user by ID.

        Args:
            user_id (int): User ID

        Returns:
            User or None: User if found, None otherwise
        """
        conn = self.db.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        return User(**dict(row))

    def get_user_by_username(self, username: str) -> Optional[User]:
        """
        Get user by username.

        Args:
            username (str): Username

        Returns:
            User or None: User if found, None otherwise
        """
        conn = self.db.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        return User(**dict(row))

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email.

        Args:
            email (str): Email address

        Returns:
            User or None: User if found, None otherwise
        """
        conn = self.db.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        return User(**dict(row))

    def create_access_token_for_user(self, user: User) -> str:
        """
        Create access token for a user.

        Args:
            user (User): User to create token for

        Returns:
            str: JWT access token
        """
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id)},
            expires_delta=access_token_expires
        )
        return access_token

    def deactivate_user(self, user_id: int) -> bool:
        """
        Deactivate a user account.

        Args:
            user_id (int): User ID to deactivate

        Returns:
            bool: True if successful, False otherwise
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "UPDATE users SET is_active = 0 WHERE id = ?",
                (user_id,)
            )
            conn.commit()
            return cursor.rowcount > 0
        except Exception:
            conn.rollback()
            return False
        finally:
            conn.close()

    def activate_user(self, user_id: int) -> bool:
        """
        Activate a user account.

        Args:
            user_id (int): User ID to activate

        Returns:
            bool: True if successful, False otherwise
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "UPDATE users SET is_active = 1 WHERE id = ?",
                (user_id,)
            )
            conn.commit()
            return cursor.rowcount > 0
        except Exception:
            conn.rollback()
            return False
        finally:
            conn.close()
