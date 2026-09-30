"""SQLAlchemy engine and per-operation database sessions."""

from collections.abc import Generator
from functools import lru_cache

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings

SessionLocal = sessionmaker(autoflush=False, expire_on_commit=False)


@lru_cache
def get_engine() -> Engine:
    """Create the shared connection pool when database access is first needed."""
    database_url = get_settings().database_url
    if not database_url:
        raise RuntimeError(
            "DATABASE_URL is not configured. Set it in the project .env file "
            "or in the hosting environment."
        )

    return create_engine(database_url, pool_pre_ping=True)


def get_db() -> Generator[Session, None, None]:
    """Yield a short-lived ORM session and always close it after the request."""
    with SessionLocal(bind=get_engine()) as session:
        yield session


def check_database_connection() -> None:
    """Run a lightweight query to verify database connectivity."""
    with get_engine().connect() as connection:
        connection.execute(text("SELECT 1"))
