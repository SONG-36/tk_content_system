"""Persistence enums, UTC time helpers, and id generation."""

from __future__ import annotations

import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import Enum as SAEnum


class AssetKind(str, enum.Enum):
    INPUT_MEDIA = "INPUT_MEDIA"
    RESULT_MEDIA = "RESULT_MEDIA"
    REFERENCE = "REFERENCE"


class AssetStatus(str, enum.Enum):
    PENDING_UPLOAD = "PENDING_UPLOAD"
    READY = "READY"
    FAILED = "FAILED"
    EXPIRED = "EXPIRED"
    DELETED = "DELETED"


class GenerationStatus(str, enum.Enum):
    QUEUED = "QUEUED"
    PROCESSING = "PROCESSING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class AttemptStatus(str, enum.Enum):
    PREPARED = "PREPARED"
    SUBMITTED = "SUBMITTED"
    PROCESSING = "PROCESSING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    CANCEL_REQUESTED = "CANCEL_REQUESTED"
    CANCELLED = "CANCELLED"
    UNKNOWN_PROVIDER_STATE = "UNKNOWN_PROVIDER_STATE"


class AIReviewStatus(str, enum.Enum):
    NOT_RUN = "NOT_RUN"


class IdempotencyStatus(str, enum.Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"


class ProviderNormalizedStatus(str, enum.Enum):
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    UNKNOWN_PROVIDER_STATE = "UNKNOWN_PROVIDER_STATE"


def enum_column(enum_cls: type[enum.Enum], name: str) -> SAEnum:
    return SAEnum(
        enum_cls,
        name=name,
        native_enum=False,
        create_constraint=True,
        validate_strings=True,
        values_callable=lambda values: [item.value for item in values],
    )


def utc_now() -> datetime:
    """Return an aware UTC timestamp."""

    return datetime.now(timezone.utc)


def generate_prefixed_id(prefix: str) -> str:
    """Generate a stable prefixed id for service-layer use."""

    return f"{prefix}_{uuid.uuid4().hex}"
