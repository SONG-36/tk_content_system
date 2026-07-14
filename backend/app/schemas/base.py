"""Shared Pydantic helpers for API contract schemas."""

from __future__ import annotations

import re
from datetime import datetime
from typing import Any

from pydantic import AnyHttpUrl, BaseModel, ConfigDict, field_validator


SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")


class APIModel(BaseModel):
    """Base model for public API schemas."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )


def validate_prefixed_id(value: str, prefix: str) -> str:
    if not value.startswith(prefix):
        raise ValueError(f"must start with {prefix}")
    return value


def validate_sha256(value: str) -> str:
    if not SHA256_RE.fullmatch(value):
        raise ValueError("must be a 64-character hexadecimal SHA-256")
    return value


class TimestampedModel(APIModel):
    created_at: datetime


class UrlModel(APIModel):
    @field_validator("*", mode="before")
    @classmethod
    def _keep_values(cls, value: Any) -> Any:
        return value


HttpUrl = AnyHttpUrl
