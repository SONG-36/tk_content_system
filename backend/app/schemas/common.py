"""Shared response schemas."""

from __future__ import annotations

from typing import Any
from typing import Optional

from pydantic import Field

from app.schemas.base import APIModel


class ErrorDetail(APIModel):
    code: str
    message: str
    field: Optional[str] = None
    required_action: Optional[str] = None
    request_id: str
    retryable: bool = False
    details: dict[str, Any] = Field(default_factory=dict)


class ErrorResponse(APIModel):
    error: ErrorDetail


class HealthResponse(APIModel):
    status: str = "ok"
    service: str
    contract_version: str = "v1"
    environment: str
    request_id: str
