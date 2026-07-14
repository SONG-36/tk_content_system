"""FastAPI dependencies for auth and server-side owner mapping."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.config import Settings, get_settings
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
