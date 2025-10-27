# TASK 14: Backend Refactor - Clean Architecture

**Status**: Not Started
**Estimated Time**: 8-10 hours
**Dependencies**: TASK 13 (Project restructure)
**Priority**: High

---

## OVERVIEW

Refactor the backend from a monolithic `claude_agent_server.py` into a clean architecture with separate routers, services, models, and core modules. Add JWT-based authentication system.

---

## OBJECTIVES

1. Implement clean architecture principles
2. Separate concerns: routers, services, models, core
3. Add JWT authentication and user management
4. Maintain all existing functionality
5. Improve testability and maintainability

---

## REQUIREMENTS

### Functional Requirements

1. **Folder Structure**:
   ```
   backend/
   ├── app/
   │   ├── main.py              # FastAPI app initialization
   │   ├── routers/             # API endpoints
   │   │   ├── __init__.py
   │   │   ├── auth.py         # Authentication routes
   │   │   ├── query.py        # Query routes
   │   │   ├── training.py     # Training data routes
   │   │   └── health.py       # Health check
   │   ├── services/            # Business logic
   │   │   ├── __init__.py
   │   │   ├── auth_service.py
   │   │   ├── query_service.py
   │   │   └── training_service.py
   │   ├── models/              # Pydantic models
   │   │   ├── __init__.py
   │   │   ├── user.py
   │   │   ├── query.py
   │   │   └── training.py
   │   ├── core/                # Core configs
   │   │   ├── __init__.py
   │   │   ├── config.py       # Settings
   │   │   ├── security.py     # JWT, passwords
   │   │   └── dependencies.py # DI
   │   ├── db/                  # Database
   │   │   ├── __init__.py
   │   │   ├── base.py
   │   │   └── session.py
   │   └── middleware/          # Custom middleware
   │       ├── __init__.py
   │       └── error_handler.py
   ├── src/                     # Keep existing Vanna code
   │   ├── detomo_vanna.py
   │   └── cache.py
   ├── tests/
   │   ├── test_routers/
   │   ├── test_services/
   │   └── test_core/
   └── main.py                  # Entry point (imports app/main.py)
   ```

2. **Authentication**:
   - User registration and login
   - JWT token generation and validation
   - Password hashing (bcrypt)
   - Token refresh mechanism
   - Protected routes

3. **API Compatibility**:
   - All existing endpoints must work
   - Same request/response formats
   - Backward compatible

---

## IMPLEMENTATION STEPS

### Step 1: Core Configuration

**backend/app/core/config.py**:
```python
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # App
    APP_NAME: str = "Detomo SQL AI"
    VERSION: str = "3.0.0"
    API_V0_PREFIX: str = "/api/v0"

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Anthropic
    ANTHROPIC_API_KEY: str
    CLAUDE_MODEL: str = "claude-sonnet-4-5"
    CLAUDE_TEMPERATURE: float = 0.1
    CLAUDE_MAX_TOKENS: int = 2048

    # Database
    DATABASE_PATH: str = "data/chinook.db"
    VECTOR_DB_PATH: str = "./detomo_vectordb"

    # SQLite for users (optional, can use same chinook.db)
    USER_DB_PATH: str = "data/users.db"

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

**backend/app/core/security.py**:
```python
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from .config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
```

**backend/app/core/dependencies.py**:
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .security import decode_token
from ..services.auth_service import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v0/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_token(token)
    if payload is None:
        raise credentials_exception

    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    # Get user from database
    auth_service = AuthService()
    user = auth_service.get_user_by_id(int(user_id))
    if user is None:
        raise credentials_exception

    return user

async def get_current_active_user(current_user = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
```

### Step 2: Database Models

**backend/app/models/user.py**:
```python
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserLogin(BaseModel):
    username: str
    password: str

class User(UserBase):
    id: int
    is_active: bool = True
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None
```

**backend/app/models/query.py**:
```python
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

# Move existing models from claude_agent_server.py
class QueryRequest(BaseModel):
    question: str = Field(..., description="Natural language question")
    language: Optional[str] = Field(default="en", description="Language: 'en' or 'jp'")

class QueryResponse(BaseModel):
    id: str
    question: str
    sql: str
    results: List[Dict[str, Any]]
    columns: List[str]
    visualization: Optional[Dict[str, Any]] = None
    row_count: int

# ... (keep all other models from claude_agent_server.py)
```

### Step 3: Authentication Service

**backend/app/db/base.py**:
```python
import sqlite3
from pathlib import Path

class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize user database tables"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                username TEXT UNIQUE NOT NULL,
                hashed_password TEXT NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        conn.close()

    def get_connection(self):
        return sqlite3.connect(self.db_path)
```

**backend/app/services/auth_service.py**:
```python
import sqlite3
from datetime import timedelta
from typing import Optional
from ..db.base import Database
from ..models.user import User, UserCreate
from ..core.security import verify_password, get_password_hash, create_access_token
from ..core.config import settings

class AuthService:
    def __init__(self):
        self.db = Database(settings.USER_DB_PATH)

    def create_user(self, user: UserCreate) -> User:
        conn = self.db.get_connection()
        cursor = conn.cursor()

        # Check if user exists
        cursor.execute("SELECT id FROM users WHERE email = ? OR username = ?",
                      (user.email, user.username))
        if cursor.fetchone():
            raise ValueError("User already exists")

        # Create user
        hashed_password = get_password_hash(user.password)
        cursor.execute("""
            INSERT INTO users (email, username, hashed_password)
            VALUES (?, ?, ?)
        """, (user.email, user.username, hashed_password))

        user_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return self.get_user_by_id(user_id)

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        user = self.get_user_by_username(username)
        if not user:
            return None

        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT hashed_password FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        conn.close()

        if not result or not verify_password(password, result[0]):
            return None

        return user

    def get_user_by_id(self, user_id: int) -> Optional[User]:
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
        conn = self.db.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        return User(**dict(row))
```

### Step 4: Query and Training Services

**backend/app/services/query_service.py**:
```python
from src.detomo_vanna import DetomoVanna
from src.cache import MemoryCache
from typing import Optional, List, Dict, Any
from concurrent.futures import ThreadPoolExecutor
import asyncio

class QueryService:
    def __init__(self):
        self.vn: Optional[DetomoVanna] = None
        self.cache = MemoryCache()
        self.executor = ThreadPoolExecutor(max_workers=4)

    def initialize_vanna(self):
        # ... (move from claude_agent_server.py)
        pass

    async def query(self, question: str, language: str = "en"):
        # ... (move logic from claude_agent_server.py)
        pass

    async def generate_sql(self, question: str):
        # ... (move from claude_agent_server.py)
        pass

    # ... (move all other query methods)
```

**backend/app/services/training_service.py**:
```python
class TrainingService:
    def __init__(self, vn: DetomoVanna):
        self.vn = vn

    def add_training(self, ddl=None, documentation=None, question=None, sql=None):
        # ... (move from claude_agent_server.py)
        pass

    def get_training_data(self):
        # ... (move from claude_agent_server.py)
        pass

    def remove_training_data(self, id: str):
        # ... (move from claude_agent_server.py)
        pass
```

### Step 5: Routers

**backend/app/routers/auth.py**:
```python
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from ..models.user import UserCreate, User, Token
from ..services.auth_service import AuthService
from ..core.security import create_access_token
from ..core.config import settings
from ..core.dependencies import get_current_active_user

router = APIRouter(prefix="/auth", tags=["authentication"])
auth_service = AuthService()

@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate):
    try:
        return auth_service.create_user(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
```

**backend/app/routers/query.py**:
```python
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..models.query import *
from ..services.query_service import QueryService
from ..core.dependencies import get_current_active_user

router = APIRouter(prefix="/query", tags=["query"])
query_service = QueryService()

@router.post("", response_model=QueryResponse)
async def query(
    request: QueryRequest,
    current_user = Depends(get_current_active_user)
):
    return await query_service.query(request.question, request.language)

@router.post("/generate_sql", response_model=GenerateSQLResponse)
async def generate_sql(
    request: GenerateSQLRequest,
    current_user = Depends(get_current_active_user)
):
    return await query_service.generate_sql(request.question)

# ... (add all other query endpoints)
```

**backend/app/routers/training.py**:
```python
# ... (similar to query.py, move training endpoints)
```

**backend/app/routers/health.py**:
```python
from fastapi import APIRouter
from ..models.health import HealthResponse

router = APIRouter(tags=["health"])

@router.get("/health", response_model=HealthResponse)
async def health():
    return {
        "status": "healthy",
        "service": "Detomo SQL AI",
        "version": "3.0.0"
    }
```

### Step 6: Main App

**backend/app/main.py**:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .core.config import settings
from .routers import auth, query, training, health

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix=settings.API_V0_PREFIX)
app.include_router(auth.router, prefix=settings.API_V0_PREFIX)
app.include_router(query.router, prefix=settings.API_V0_PREFIX)
app.include_router(training.router, prefix=settings.API_V0_PREFIX)

# Initialize Vanna on startup
@app.on_event("startup")
async def startup_event():
    from .services.query_service import query_service
    query_service.initialize_vanna()
```

**backend/main.py** (entry point):
```python
import uvicorn
from app.main import app

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
```

### Step 7: Update Requirements

**backend/requirements.txt** (add):
```
python-jose[cryptography]
passlib[bcrypt]
python-multipart
pydantic-settings
```

### Step 8: Update Tests

Create new test files matching the new structure:
- `tests/test_routers/test_auth.py`
- `tests/test_routers/test_query.py`
- `tests/test_services/test_auth_service.py`
- etc.

---

## TESTING CHECKLIST

- [ ] All existing endpoints work
- [ ] Authentication endpoints work (register, login)
- [ ] JWT tokens generated correctly
- [ ] Protected routes require authentication
- [ ] User database created
- [ ] Password hashing works
- [ ] All tests pass (≥80% coverage)
- [ ] No breaking changes

---

## SUCCESS CRITERIA

- ✅ Clean architecture with routers/services/models/core
- ✅ JWT authentication working
- ✅ User registration and login working
- ✅ All existing endpoints functional
- ✅ Tests passing (≥80% coverage)
- ✅ No breaking changes
- ✅ Code well-organized and maintainable

---

**Created**: 2025-10-27
**Last Updated**: 2025-10-27
