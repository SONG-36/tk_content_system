"""Proof need schemas."""

from __future__ import annotations

from pydantic import field_validator

from app.schemas.base import APIModel, validate_prefixed_id
from app.schemas.enums import PresentationLayer, ProductionType, ProofType


class ProofNeed(APIModel):
    proof_need_id: str
    shot_id: str
    proof_type: ProofType
    linked_client_fact_ids: list[str] = []
    required_evidence_refs: list[str] = []
    production_type: ProductionType
    presentation_layer: PresentationLayer

    @field_validator("proof_need_id")
    @classmethod
    def validate_proof_need_id(cls, value: str) -> str:
        return validate_prefixed_id(value, "pneed_")
