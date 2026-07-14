"""API contract enums for Phase 2A."""

from __future__ import annotations

import enum


class SelectedModel(str, enum.Enum):
    Seedance = "Seedance"


class ExecutionProvider(str, enum.Enum):
    mock = "mock"


class ProductionType(str, enum.Enum):
    AI_GENERATION = "AI_GENERATION"
    HYBRID = "HYBRID"


class GenerationMode(str, enum.Enum):
    T2V = "T2V"
    I2V = "I2V"
    R2V = "R2V"
    FLF2V = "FLF2V"


class TruthDependency(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"


class UsageRole(str, enum.Enum):
    PRODUCT_IDENTITY = "PRODUCT_IDENTITY"
    FIRST_FRAME = "FIRST_FRAME"
    LAST_FRAME = "LAST_FRAME"
    MOTION_REFERENCE = "MOTION_REFERENCE"
    CAMERA_REFERENCE = "CAMERA_REFERENCE"
    ENVIRONMENT_REFERENCE = "ENVIRONMENT_REFERENCE"
    PROOF_EVIDENCE = "PROOF_EVIDENCE"
    SOURCE_CLIP = "SOURCE_CLIP"


class SourceType(str, enum.Enum):
    USER_INPUT = "USER_INPUT"
    UPLOADED_ASSET = "UPLOADED_ASSET"
    PRODUCT_LINK = "PRODUCT_LINK"
    PRODUCT_SPEC_TEXT = "PRODUCT_SPEC_TEXT"
    PRIOR_SCRIPT = "PRIOR_SCRIPT"
    MANUAL_NOTE = "MANUAL_NOTE"


class PresentationLayer(str, enum.Enum):
    REAL_CAPTURE = "REAL_CAPTURE"
    AI_VISUALIZATION = "AI_VISUALIZATION"
    AI_ENVIRONMENT = "AI_ENVIRONMENT"
    STOCK_CONTEXT = "STOCK_CONTEXT"
    TEXT_CLAIM = "TEXT_CLAIM"


class ProofType(str, enum.Enum):
    identity = "identity"
    structure = "structure"
    accessory = "accessory"
    function = "function"
    result = "result"
    human_efficacy = "human_efficacy"
    safety = "safety"
    sterilization = "sterilization"
    compatibility = "compatibility"
    before_after = "before_after"
    suction = "suction"
    dirt_intake = "dirt_intake"
    transparent_bin = "transparent_bin"
    pet_hair = "pet_hair"
    gap_access = "gap_access"
    attachment_performance = "attachment_performance"
    measurable_performance = "measurable_performance"


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
