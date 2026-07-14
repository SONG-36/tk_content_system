"""FastAPI dependencies for auth and server-side owner mapping."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import sessionmaker

from app.config import Settings, get_settings
from app.db.session import create_db_engine
from app.services.assets import AssetService
from app.services.errors import AuthInvalidError, AuthRequiredError

bearer_scheme = HTTPBearer(auto_error=False)


@dataclass(frozen=True)
class OwnerContext:
    owner_id: str


def require_owner_context(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
    settings: Settings = Depends(get_settings),
) -> OwnerContext:
    """Authenticate a Bearer API key and map it to a server-side owner id."""

    if credentials is None:
        raise AuthRequiredError()
    if credentials.scheme.lower() != "bearer" or credentials.credentials != settings.api_key:
        raise AuthInvalidError()
    return OwnerContext(owner_id=settings.owner_id)


@lru_cache(maxsize=8)
def _session_factory_for_url(database_url: str):
    engine = create_db_engine(database_url)
    return sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def get_asset_service(settings: Settings = Depends(get_settings)) -> AssetService:
    return AssetService(
        settings=settings,
        session_factory=_session_factory_for_url(settings.database_url),
    )
