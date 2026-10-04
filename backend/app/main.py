"""FastAPI application entry point for ResumeLens."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import get_settings
from app.core.database import check_database_connection
from app.api.routes import router as api_router

settings = get_settings()

app = FastAPI(
    title="ResumeLens API",
    description="Job-specific resume analysis API.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_cors_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

app.include_router(api_router)


@app.get("/", tags=["status"])
def root() -> dict[str, str]:
    """Provide a small welcome response and point to the API docs."""
    return {
        "name": "ResumeLens API",
        "message": "The backend is running.",
        "docs": "/docs",
    }


@app.get("/health", tags=["status"])
def health() -> dict[str, str]:
    """Report that the API process is responding."""
    return {"status": "ok"}


@app.get("/health/database", tags=["status"])
def database_health() -> dict[str, str]:
    """Check database connectivity without exposing credentials or internals."""
    try:
        check_database_connection()
    except (RuntimeError, SQLAlchemyError):
        raise HTTPException(
            status_code=503,
            detail="Database is not configured or is unavailable.",
        ) from None

    return {"status": "ok"}
