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
