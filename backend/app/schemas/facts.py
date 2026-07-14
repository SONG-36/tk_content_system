"""Fact and source reference schemas."""

from __future__ import annotations

from typing import Any, Optional

from pydantic import field_validator, model_validator

from app.schemas.base import APIModel, validate_prefixed_id
from app.schemas.enums import SourceType


class ClientDeclaredFact(APIModel):
    client_fact_id: str
    fact_type: str
    subject: str
    value: dict[str, Any]
    source_ref_ids: list[str] = []

    @field_validator("client_fact_id")
    @classmethod
    def validate_client_fact_id(cls, value: str) -> str:
        return validate_prefixed_id(value, "cfact_")


class SourceRef(APIModel):
    source_ref_id: str
    source_type: SourceType
    source_value: str
    asset_id: Optional[str] = None

    @field_validator("source_ref_id")
    @classmethod
    def validate_source_ref_id(cls, value: str) -> str:
        return validate_prefixed_id(value, "src_")

    @field_validator("asset_id")
    @classmethod
    def validate_asset_id(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        return validate_prefixed_id(value, "asset_")

    @model_validator(mode="after")
    def validate_uploaded_asset_source(self) -> "SourceRef":
        if self.source_type == SourceType.UPLOADED_ASSET and self.asset_id is None:
            raise ValueError("asset_id is required when source_type=UPLOADED_ASSET")
        return self
