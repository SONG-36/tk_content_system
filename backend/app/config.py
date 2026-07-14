"""Application configuration for the Phase 2A backend foundation."""

from __future__ import annotations

import os
from functools import lru_cache

from pydantic import BaseModel, ConfigDict, Field


class Settings(BaseModel):
    """Runtime settings loaded from environment variables."""

    model_config = ConfigDict(frozen=True)

    app_name: str = Field(default="TikTok Shop Product Video Backend")
    environment: str = Field(default="development")
    api_key: str = Field(default="dev-api-key")
    owner_id: str = Field(default="owner_dev")
    database_url: str = Field(default="sqlite:///./backend.db")
    public_base_url: str = Field(default="http://localhost:8000")


def load_settings() -> Settings:
    """Load settings from environment variables with local-safe defaults."""

    return Settings(
        app_name=os.getenv("BACKEND_APP_NAME", Settings.model_fields["app_name"].default),
        environment=os.getenv(
            "BACKEND_ENVIRONMENT", Settings.model_fields["environment"].default
        ),
        api_key=os.getenv("BACKEND_API_KEY", Settings.model_fields["api_key"].default),
        owner_id=os.getenv("BACKEND_OWNER_ID", Settings.model_fields["owner_id"].default),
        database_url=os.getenv(
            "BACKEND_DATABASE_URL", Settings.model_fields["database_url"].default
        ),
        public_base_url=os.getenv(
            "BACKEND_PUBLIC_BASE_URL",
            Settings.model_fields["public_base_url"].default,
        ),
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached settings for app runtime."""

    return load_settings()


def reset_settings_cache() -> None:
    """Clear cached settings for tests that override environment variables."""

    get_settings.cache_clear()
