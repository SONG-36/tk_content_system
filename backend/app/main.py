"""FastAPI application entrypoint for the Phase 2A backend foundation."""

from __future__ import annotations

from typing import Optional

from fastapi import Depends, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.health import router as health_router
from app.config import Settings, get_settings
from app.dependencies import OwnerContext, require_owner_context
from app.middleware.request_id import request_id_middleware
from app.schemas.assets import UploadUrlRequest
from app.schemas.common import ErrorDetail, ErrorResponse
from app.schemas.jobs import CreateVideoJobRequest
from app.services.errors import DomainError


def _request_id(request: Request) -> str:
    return getattr(request.state, "request_id", "")


def _error_response(request: Request, error: DomainError) -> JSONResponse:
    payload = ErrorResponse(
        error=ErrorDetail(
            code=error.code,
            message=error.message,
            field=error.field,
            required_action=error.required_action,
            request_id=_request_id(request),
            retryable=error.retryable,
            details=error.details,
        )
    )
    return JSONResponse(
        status_code=error.status_code,
        content=payload.model_dump(),
    )


def _validation_field(location: tuple[object, ...]) -> str:
    parts = [str(item) for item in location if item not in {"body", "query", "path"}]
    return ".".join(parts)


def create_app(
    *,
    settings_override: Optional[Settings] = None,
    include_test_routes: bool = False,
) -> FastAPI:
    """Create the FastAPI app with foundation middleware and handlers."""

    settings = settings_override or get_settings()
    app = FastAPI(title=settings.app_name)

    if settings_override is not None:
        app.dependency_overrides[get_settings] = lambda: settings_override

    app.middleware("http")(request_id_middleware)

    @app.exception_handler(DomainError)
    async def handle_domain_error(request: Request, exc: DomainError) -> JSONResponse:
        return _error_response(request, exc)

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        errors = [
            {
                "field": _validation_field(tuple(error.get("loc", ()))),
                "message": error.get("msg", "Invalid request."),
                "type": error.get("type", "validation_error"),
            }
            for error in exc.errors()
        ]
        first_field = errors[0]["field"] if errors else None
        payload = ErrorResponse(
            error=ErrorDetail(
                code="SCHEMA_INVALID",
                message="Request schema validation failed.",
                field=first_field,
                required_action="Fix the request body to match the API contract.",
                request_id=_request_id(request),
                retryable=False,
                details={"errors": errors},
            )
        )
        return JSONResponse(status_code=422, content=payload.model_dump())

    app.include_router(health_router)

    if include_test_routes:

        @app.get("/_test/protected")
        async def protected_test_route(
            owner: OwnerContext = Depends(require_owner_context),
        ) -> dict[str, str]:
            return {"owner_id": owner.owner_id}

        @app.post("/_test/upload-url-schema")
        async def upload_url_schema_test(payload: UploadUrlRequest) -> dict[str, str]:
            return {"contract_version": payload.contract_version}

        @app.post("/_test/video-job-schema")
        async def video_job_schema_test(payload: CreateVideoJobRequest) -> dict[str, str]:
            return {"shot_number": payload.shot_number}

    return app


app = create_app()
