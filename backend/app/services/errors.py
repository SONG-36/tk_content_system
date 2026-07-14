"""Domain exceptions and error conversion."""

from __future__ import annotations

from typing import Any
from typing import Optional


class DomainError(Exception):
    """Base exception rendered through the contract error envelope."""

    status_code = 500
    code = "INTERNAL_ERROR"
    message = "Unexpected server error."
    field: Optional[str] = None
    required_action: Optional[str] = None
    retryable = False

    def __init__(
        self,
        message: Optional[str] = None,
        *,
        field: Optional[str] = None,
        required_action: Optional[str] = None,
        retryable: Optional[bool] = None,
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(message or self.message)
        self.message = message or self.message
        self.field = field if field is not None else self.field
        self.required_action = (
            required_action if required_action is not None else self.required_action
        )
        self.retryable = retryable if retryable is not None else self.retryable
        self.details = details or {}


class AuthRequiredError(DomainError):
    status_code = 401
    code = "AUTH_REQUIRED"
    message = "Bearer authentication is required."
    required_action = "Provide an Authorization: Bearer <api-key> header."


class AuthInvalidError(DomainError):
    status_code = 401
    code = "AUTH_INVALID"
    message = "Bearer authentication is invalid."
    required_action = "Provide a valid API key."


class IdempotencyKeyRequiredError(DomainError):
    status_code = 422
    code = "IDEMPOTENCY_KEY_REQUIRED"
    message = "A valid Idempotency-Key header is required."
    required_action = "Provide a non-empty Idempotency-Key header."
    retryable = False


class IdempotencyConflictError(DomainError):
    status_code = 409
    code = "IDEMPOTENCY_CONFLICT"
    message = "The Idempotency-Key was already used for a different request."
    required_action = "Use the original request payload or provide a new Idempotency-Key."
    retryable = False


class IdempotencyPendingError(DomainError):
    status_code = 409
    code = "IDEMPOTENCY_PENDING"
    message = "An identical request with this Idempotency-Key is still pending."
    required_action = "Retry the same request later with the same Idempotency-Key."
    retryable = True


class AssetTypeUnsupportedError(DomainError):
    status_code = 415
    code = "ASSET_TYPE_UNSUPPORTED"
    message = "The asset content type is not supported."
    field = "content_type"
    required_action = "Use image/png, image/jpeg, or video/mp4."


class SchemaInvalidError(DomainError):
    status_code = 422
    code = "SCHEMA_INVALID"
    message = "Request schema validation failed."
    required_action = "Fix the request to match the API contract."


class AssetTooLargeError(DomainError):
    status_code = 413
    code = "ASSET_TOO_LARGE"
    message = "The asset exceeds the configured maximum size."
    field = "size_bytes"
    required_action = "Upload a smaller asset."


class AssetInvalidStateError(DomainError):
    status_code = 409
    code = "ASSET_INVALID_STATE"
    message = "The asset is not in a valid state for this operation."
    required_action = "Create a new upload URL or use an asset that is pending upload."


class AssetInvalidForJobError(DomainError):
    status_code = 422
    code = "ASSET_INVALID_STATE"
    message = "A referenced asset cannot be used for video job creation."
    required_action = "Reference a READY, non-deleted Phase 2A supported asset."


class UploadTokenInvalidError(DomainError):
    status_code = 404
    code = "UPLOAD_TOKEN_INVALID"
    message = "The upload token is invalid."
    required_action = "Request a new upload URL."


class UploadTokenExpiredError(DomainError):
    status_code = 410
    code = "UPLOAD_TOKEN_EXPIRED"
    message = "The upload token has expired."
    required_action = "Request a new upload URL."


class UploadAlreadyCompletedError(DomainError):
    status_code = 409
    code = "UPLOAD_ALREADY_COMPLETED"
    message = "This upload token has already been used."
    required_action = "Use the uploaded asset or request a new upload URL."


class ChecksumMismatchError(DomainError):
    status_code = 422
    code = "CHECKSUM_MISMATCH"
    message = "The uploaded bytes do not match the declared checksum."
    field = "checksum_sha256"
    required_action = "Upload bytes matching the declared SHA-256 checksum."


class InternalServerError(DomainError):
    status_code = 500
    code = "INTERNAL_ERROR"
    message = "Unexpected server error."
    required_action = "Retry later or contact support if the issue persists."
    retryable = True


class VersionConflictError(DomainError):
    status_code = 409
    code = "VERSION_CONFLICT"
    message = "The requested truth rule version is not compatible."
    field = "expected_truth_rule_version"
    required_action = "Refresh the contract and retry with the current truth rule version."


class AssetNotFoundError(DomainError):
    status_code = 422
    code = "ASSET_NOT_FOUND"
    message = "A referenced asset was not found for this owner."
    required_action = "Upload the asset and reference an owner-visible asset_id."


class AssetNotReadyError(DomainError):
    status_code = 422
    code = "ASSET_NOT_READY"
    message = "A referenced asset is not READY."
    required_action = "Complete the mock upload before creating the video job."


class TruthGateBlockedError(DomainError):
    status_code = 422
    code = "TRUTH_GATE_BLOCKED"
    message = "The request failed structural Truth Gate validation."
    required_action = "Revise proof ownership, evidence, or production type."


class HybridGateBlockedError(DomainError):
    status_code = 422
    code = "HYBRID_GATE_BLOCKED"
    message = "The request failed structural HYBRID Gate validation."
    required_action = "Revise hybrid layers and real proof ownership."


class AIProofNotAllowedError(DomainError):
    status_code = 422
    code = "AI_PROOF_NOT_ALLOWED"
    message = "AI output cannot carry this product proof."
    required_action = "Use real proof evidence or switch the proof-carrying shot to real capture."


class ProviderUnsupportedError(DomainError):
    status_code = 422
    code = "PROVIDER_UNSUPPORTED"
    message = "The selected model and execution provider are not supported in Phase 2A."
    required_action = "Use selected_model=Seedance and execution_provider=mock."
