"""Application settings loaded from environment variables and the root .env."""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    database_url: str | None = None
    environment: str = "development"
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    upload_max_mb: int = 10

    @property
    def allowed_cors_origins(self) -> list[str]:
        """Parse the comma-separated browser origins allowed to call the API."""
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Load settings once per process; real secrets stay outside source control."""
    return Settings()
