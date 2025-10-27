"""
Entry point for Detomo SQL AI backend.

Run with:
    python main.py

Or with uvicorn directly:
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
"""

import uvicorn
from app.main import app

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        port=8000,
        reload=True,
        log_level="info"
    )
