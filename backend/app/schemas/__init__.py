"""Pydantic schemas for the Phase 2A backend foundation."""

from app.schemas.assets import UploadUrlRequest, UploadUrlResponse
from app.schemas.common import ErrorDetail, ErrorResponse, HealthResponse
from app.schemas.facts import ClientDeclaredFact, SourceRef
from app.schemas.jobs import (
    AssetSummary,
    AttemptSummary,
    CancelJobRequest,
    CancelJobResponse,
    CreateVideoJobRequest,
    CreateVideoJobResponse,
    GetVideoJobResponse,
    HybridAiLayer,
    HybridLayers,
    HybridRealLayer,
    PreservationLocks,
    ReferenceAsset,
    ResultMediaSummary,
    RetryJobRequest,
    RetryJobResponse,
    StoredJobError,
)
from app.schemas.proofs import ProofNeed

__all__ = [
    "AssetSummary",
    "AttemptSummary",
    "CancelJobRequest",
    "CancelJobResponse",
    "ClientDeclaredFact",
    "CreateVideoJobRequest",
    "CreateVideoJobResponse",
    "ErrorDetail",
    "ErrorResponse",
    "GetVideoJobResponse",
    "HealthResponse",
    "HybridAiLayer",
    "HybridLayers",
    "HybridRealLayer",
    "PreservationLocks",
    "ProofNeed",
    "ReferenceAsset",
    "ResultMediaSummary",
    "RetryJobRequest",
    "RetryJobResponse",
    "SourceRef",
    "StoredJobError",
    "UploadUrlRequest",
    "UploadUrlResponse",
]
