"""Video job request and response schemas."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import Field, field_validator, model_validator

from app.schemas.base import APIModel, HttpUrl, validate_prefixed_id
from app.schemas.enums import (
    AIReviewStatus,
    AssetKind,
    AssetStatus,
    AttemptStatus,
    ExecutionProvider,
    GenerationMode,
    GenerationStatus,
    ProductionType,
    SelectedModel,
    TruthDependency,
    UsageRole,
)
from app.schemas.facts import ClientDeclaredFact, SourceRef
from app.schemas.proofs import ProofNeed


class PreservationLocks(APIModel):
    lock_identity: bool = False
    lock_structure: bool = False
    lock_motion: bool = False
    lock_environment: bool = False
    lock_text: bool = False


class ReferenceAsset(APIModel):
    asset_id: str
    usage_role: UsageRole
    shot_number: str
    linked_proof_need_ids: list[str] = []
    required_for_truth_gate: bool = False
    preservation_locks: PreservationLocks = Field(default_factory=PreservationLocks)

    @field_validator("asset_id")
    @classmethod
    def validate_asset_id(cls, value: str) -> str:
        return validate_prefixed_id(value, "asset_")


class HybridRealLayer(APIModel):
    required: bool
    description: str
    reference_asset_ids: list[str] = []
    carries_proof_need_ids: list[str] = []

    @field_validator("reference_asset_ids")
    @classmethod
    def validate_reference_asset_ids(cls, values: list[str]) -> list[str]:
        for value in values:
            validate_prefixed_id(value, "asset_")
        return values


class HybridAiLayer(APIModel):
    required: bool
    description: str
    allowed_roles: list[str] = []
    prohibited_roles: list[str] = []


class HybridLayers(APIModel):
    real_layer: HybridRealLayer
    ai_layer: HybridAiLayer
    ai_must_not_rewrite: list[str]

    @model_validator(mode="after")
    def validate_required_layers(self) -> "HybridLayers":
        if self.real_layer.required is not True:
            raise ValueError("real_layer.required must be true")
        if self.ai_layer.required is not True:
            raise ValueError("ai_layer.required must be true")
        if not self.ai_must_not_rewrite:
            raise ValueError("ai_must_not_rewrite must not be empty")
        return self


class CreateVideoJobRequest(APIModel):
    contract_version: str = "v1"
    expected_truth_rule_version: Optional[str] = None
    selected_model: SelectedModel = SelectedModel.Seedance
    execution_provider: ExecutionProvider = ExecutionProvider.mock
    shot_number: str
    production_type: ProductionType
    generation_mode: GenerationMode
    prompt: str
    negative_constraints: list[str] = []
    preservation_constraints: list[str] = []
    reference_assets: list[ReferenceAsset] = []
    truth_dependency: TruthDependency
    hybrid_layers: Optional[HybridLayers] = None
    duration_seconds: int = Field(gt=0)
    aspect_ratio: str = "9:16"
    client_declared_facts: list[ClientDeclaredFact] = []
    source_refs: list[SourceRef] = []
    proof_needs: list[ProofNeed] = []

    @field_validator("contract_version")
    @classmethod
    def validate_contract_version(cls, value: str) -> str:
        if value != "v1":
            raise ValueError("must be v1")
        return value

    @field_validator("aspect_ratio")
    @classmethod
    def validate_aspect_ratio(cls, value: str) -> str:
        if value != "9:16":
            raise ValueError("must be 9:16")
        return value

    @model_validator(mode="after")
    def validate_cross_fields(self) -> "CreateVideoJobRequest":
        self._validate_unique_ids()
        self._validate_references()
        self._validate_shots_and_production_type()
        self._validate_generation_mode()
        self._validate_hybrid_structure()
        return self

    def _validate_unique_ids(self) -> None:
        _ensure_unique([item.client_fact_id for item in self.client_declared_facts], "client_fact_id")
        _ensure_unique([item.source_ref_id for item in self.source_refs], "source_ref_id")
        _ensure_unique([item.proof_need_id for item in self.proof_needs], "proof_need_id")
        asset_keys = [
            (item.asset_id, item.usage_role.value, item.shot_number)
            for item in self.reference_assets
        ]
        _ensure_unique(asset_keys, "asset_id + usage_role + shot_number")

    def _validate_references(self) -> None:
        source_ids = {item.source_ref_id for item in self.source_refs}
        fact_ids = {item.client_fact_id for item in self.client_declared_facts}
        proof_ids = {item.proof_need_id for item in self.proof_needs}
        asset_ids = {item.asset_id for item in self.reference_assets}

        for fact in self.client_declared_facts:
            for source_ref_id in fact.source_ref_ids:
                if source_ref_id not in source_ids:
                    raise ValueError(f"source_ref_ids references unknown id: {source_ref_id}")

        for proof in self.proof_needs:
            for fact_id in proof.linked_client_fact_ids:
                if fact_id not in fact_ids:
                    raise ValueError(f"linked_client_fact_ids references unknown id: {fact_id}")
            for evidence_ref in proof.required_evidence_refs:
                if evidence_ref.startswith("src_"):
                    if evidence_ref not in source_ids:
                        raise ValueError(f"required_evidence_refs references unknown id: {evidence_ref}")
                elif evidence_ref.startswith("asset_"):
                    if evidence_ref not in asset_ids:
                        raise ValueError(f"required_evidence_refs references unknown id: {evidence_ref}")
                else:
                    raise ValueError("required_evidence_refs must start with src_ or asset_")

        for asset in self.reference_assets:
            for proof_id in asset.linked_proof_need_ids:
                if proof_id not in proof_ids:
                    raise ValueError(f"linked_proof_need_ids references unknown id: {proof_id}")

        if self.hybrid_layers is not None:
            for proof_id in self.hybrid_layers.real_layer.carries_proof_need_ids:
                if proof_id not in proof_ids:
                    raise ValueError(f"carries_proof_need_ids references unknown id: {proof_id}")
            for asset_id in self.hybrid_layers.real_layer.reference_asset_ids:
                if asset_id not in asset_ids:
                    raise ValueError(f"reference_asset_ids references unknown id: {asset_id}")

    def _validate_shots_and_production_type(self) -> None:
        for asset in self.reference_assets:
            if asset.shot_number != self.shot_number:
                raise ValueError("reference_assets.shot_number must match shot_number")
        for proof in self.proof_needs:
            if proof.shot_id != self.shot_number:
                raise ValueError("proof_needs.shot_id must match shot_number")
            if proof.production_type != self.production_type:
                raise ValueError("proof_needs.production_type must match production_type")

    def _validate_generation_mode(self) -> None:
        roles = [item.usage_role for item in self.reference_assets]
        if self.generation_mode == GenerationMode.I2V and not (
            UsageRole.FIRST_FRAME in roles or UsageRole.PRODUCT_IDENTITY in roles
        ):
            raise ValueError("I2V requires FIRST_FRAME or PRODUCT_IDENTITY")
        if self.generation_mode == GenerationMode.R2V and not self.reference_assets:
            raise ValueError("R2V requires at least one ReferenceAsset")
        if self.generation_mode == GenerationMode.FLF2V:
            first_count = roles.count(UsageRole.FIRST_FRAME)
            last_count = roles.count(UsageRole.LAST_FRAME)
            if first_count != 1:
                raise ValueError("FLF2V requires exactly one FIRST_FRAME")
            if last_count != 1:
                raise ValueError("FLF2V requires exactly one LAST_FRAME")

    def _validate_hybrid_structure(self) -> None:
        if self.production_type == ProductionType.HYBRID and self.hybrid_layers is None:
            raise ValueError("HYBRID requires hybrid_layers")
        if self.production_type == ProductionType.AI_GENERATION and self.hybrid_layers is not None:
            raise ValueError("AI_GENERATION must not include hybrid_layers")


class CreateVideoJobResponse(APIModel):
    job_id: str
    generation_status: GenerationStatus = GenerationStatus.QUEUED
    ai_review_status: AIReviewStatus = AIReviewStatus.NOT_RUN
    execution_provider: ExecutionProvider = ExecutionProvider.mock
    contract_version: str = "v1"
    truth_rule_version: str
    provider_mapping_version: str
    idempotent_replay: bool

    @field_validator("job_id")
    @classmethod
    def validate_job_id(cls, value: str) -> str:
        return validate_prefixed_id(value, "job_")


class AttemptSummary(APIModel):
    attempt_id: str
    attempt_no: int
    attempt_status: AttemptStatus
    execution_provider: ExecutionProvider
    provider_job_id: Optional[str] = None
    cancellation_intent: bool
    cancel_requested_at: Optional[datetime] = None
    error_code: Optional[str] = None
    created_at: datetime
    submitted_at: Optional[datetime] = None
    terminal_at: Optional[datetime] = None
    updated_at: datetime

    @field_validator("attempt_id")
    @classmethod
    def validate_attempt_id(cls, value: str) -> str:
        return validate_prefixed_id(value, "attempt_")


class AssetSummary(APIModel):
    asset_id: str
    asset_kind: AssetKind
    asset_status: AssetStatus
    content_type: str
    size_bytes: int
    checksum_sha256: str
    usage_role: Optional[UsageRole] = None

    @field_validator("asset_id")
    @classmethod
    def validate_asset_id(cls, value: str) -> str:
        return validate_prefixed_id(value, "asset_")


class ResultMediaSummary(APIModel):
    asset_id: str
    content_type: str
    size_bytes: int
    result_url: HttpUrl
    result_url_expires_at: datetime
    checksum_sha256: str

    @field_validator("asset_id")
    @classmethod
    def validate_asset_id(cls, value: str) -> str:
        return validate_prefixed_id(value, "asset_")


class StoredJobError(APIModel):
    code: str
    message: str
    attempt_id: Optional[str] = None
    created_at: datetime

    @field_validator("attempt_id")
    @classmethod
    def validate_attempt_id(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        return validate_prefixed_id(value, "attempt_")


class GetVideoJobResponse(APIModel):
    job_id: str
    generation_status: GenerationStatus
    ai_review_status: AIReviewStatus = AIReviewStatus.NOT_RUN
    current_attempt: Optional[AttemptSummary] = None
    assets: list[AssetSummary] = []
    result_media: list[ResultMediaSummary] = []
    errors: list[StoredJobError] = []

    @field_validator("job_id")
    @classmethod
    def validate_job_id(cls, value: str) -> str:
        return validate_prefixed_id(value, "job_")


class CancelJobRequest(APIModel):
    reason: str


class CancelJobResponse(APIModel):
    job_id: str
    generation_status: GenerationStatus
    attempt_status: AttemptStatus
    cancellation_intent: bool
    cancel_requested_at: Optional[datetime] = None
    idempotent_replay: bool

    @field_validator("job_id")
    @classmethod
    def validate_job_id(cls, value: str) -> str:
        return validate_prefixed_id(value, "job_")

    @field_validator("generation_status")
    @classmethod
    def validate_generation_status(cls, value: GenerationStatus) -> GenerationStatus:
        if value not in {GenerationStatus.CANCELLED, GenerationStatus.PROCESSING}:
            raise ValueError("must be CANCELLED or PROCESSING")
        return value

    @field_validator("attempt_status")
    @classmethod
    def validate_attempt_status(cls, value: AttemptStatus) -> AttemptStatus:
        allowed = {
            AttemptStatus.CANCEL_REQUESTED,
            AttemptStatus.CANCELLED,
            AttemptStatus.UNKNOWN_PROVIDER_STATE,
        }
        if value not in allowed:
            raise ValueError("invalid cancel attempt_status")
        return value


class RetryJobRequest(APIModel):
    reason: str


class RetryJobResponse(APIModel):
    job_id: str
    generation_status: GenerationStatus = GenerationStatus.QUEUED
    new_attempt_id: str
    idempotent_replay: bool

    @field_validator("job_id")
    @classmethod
    def validate_job_id(cls, value: str) -> str:
        return validate_prefixed_id(value, "job_")

    @field_validator("new_attempt_id")
    @classmethod
    def validate_attempt_id(cls, value: str) -> str:
        return validate_prefixed_id(value, "attempt_")


def _ensure_unique(values: list[object], label: str) -> None:
    if len(values) != len(set(values)):
        raise ValueError(f"{label} must be unique")
