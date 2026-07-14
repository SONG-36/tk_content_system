"""Asset request and response schemas."""

from __future__ import annotations

from datetime import datetime

from pydantic import Field, field_validator

from app.schemas.base import APIModel, HttpUrl, validate_prefixed_id, validate_sha256
from app.schemas.enums import AssetStatus, UsageRole


class UploadUrlRequest(APIModel):
    contract_version: str = "v1"
    content_type: str
    size_bytes: int = Field(gt=0)
    checksum_sha256: str
    intended_usage_role: UsageRole

    @field_validator("contract_version")
    @classmethod
    def validate_contract_version(cls, value: str) -> str:
        if value != "v1":
            raise ValueError("must be v1")
        return value

    @field_validator("content_type")
    @classmethod
    def validate_content_type(cls, value: str) -> str:
        allowed = {"image/png", "image/jpeg", "video/mp4"}
        if value not in allowed:
            raise ValueError("unsupported content_type")
        return value

    @field_validator("checksum_sha256")
    @classmethod
    def validate_checksum(cls, value: str) -> str:
        return validate_sha256(value)


class UploadUrlResponse(APIModel):
    asset_id: str
    asset_status: AssetStatus = AssetStatus.PENDING_UPLOAD
    upload_url: HttpUrl
    upload_url_expires_at: datetime
    idempotent_replay: bool

    @field_validator("asset_id")
    @classmethod
    def validate_asset_id(cls, value: str) -> str:
        return validate_prefixed_id(value, "asset_")

    @field_validator("asset_status")
    @classmethod
    def validate_pending_status(cls, value: AssetStatus) -> AssetStatus:
        if value != AssetStatus.PENDING_UPLOAD:
            raise ValueError("must be PENDING_UPLOAD")
        return value


class InternalUploadResponse(APIModel):
    asset_id: str
    asset_status: AssetStatus = AssetStatus.READY
    content_type: str
    size_bytes: int
    checksum_sha256: str

    @field_validator("asset_id")
    @classmethod
    def validate_asset_id(cls, value: str) -> str:
        return validate_prefixed_id(value, "asset_")

    @field_validator("asset_status")
    @classmethod
    def validate_ready_status(cls, value: AssetStatus) -> AssetStatus:
        if value != AssetStatus.READY:
            raise ValueError("must be READY")
        return value

    @field_validator("checksum_sha256")
    @classmethod
    def validate_checksum(cls, value: str) -> str:
        return validate_sha256(value)
