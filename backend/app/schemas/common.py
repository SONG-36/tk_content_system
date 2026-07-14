"""Shared response schemas."""

from __future__ import annotations

from typing import Any
from typing import Optional

from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    code: str
    message: str
    field: Optional[str] = None
    required_action: Optional[str] = None
    request_id: str
    retryable: bool = False
    details: dict[str, Any] = Field(default_factory=dict)


class ErrorResponse(BaseModel):
    error: ErrorDetail


class HealthResponse(BaseModel):
    status: str
    service: str
    contract_version: str
    environment: str
    request_id: str
