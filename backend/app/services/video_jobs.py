"""Create video job service for Phase 2A."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from app.config import Settings
from app.db.types import AssetStatus
from app.gates import GateEvaluation, GateResult, evaluate_hybrid_gate, evaluate_truth_gate
from app.idempotency import IdempotencyDisposition, IdempotencyService
from app.idempotency.canonical import canonicalize_request
from app.idempotency.repository import IdempotencyRepository, SessionFactory
from app.idempotency.types import Clock, UtcClock, ensure_utc
from app.repositories.assets import AssetRepository, AssetSnapshot
from app.repositories.job_asset_references import JobAssetReferenceRepository
from app.repositories.job_attempts import JobAttemptRepository
from app.repositories.request_snapshots import GenerationRequestSnapshotRepository
from app.repositories.video_jobs import VideoJobRepository
from app.schemas.common import ErrorDetail, ErrorResponse
from app.schemas.enums import ExecutionProvider, SelectedModel
from app.schemas.jobs import CreateVideoJobRequest, CreateVideoJobResponse
from app.services.errors import (
    AIProofNotAllowedError,
    AssetInvalidForJobError,
    AssetNotFoundError,
    AssetNotReadyError,
    DomainError,
    HybridGateBlockedError,
    InternalServerError,
    ProviderUnsupportedError,
    TruthGateBlockedError,
    VersionConflictError,
)
from app.services.job_recovery import VideoJobRecoveryResolver

TRUTH_RULE_VERSION = "truth-rules-v0.4"
PROVIDER_MAPPING_VERSION = "mock-provider-map-v0.4"
ALLOWED_ASSET_CONTENT_TYPES = {"image/png", "image/jpeg", "video/mp4"}


@dataclass(frozen=True)
class ServiceResponse:
    status_code: int
    payload: dict[str, Any]
    dispatch_required: bool = False
    job_id: Optional[str] = None


class VideoJobService:
    """Coordinates idempotency, gates, and transactional job creation."""

    def __init__(
        self,
        *,
        settings: Settings,
        session_factory: SessionFactory,
        clock: Optional[Clock] = None,
        idempotency_service: Optional[IdempotencyService] = None,
        idempotency_repository: Optional[IdempotencyRepository] = None,
        asset_repository: Optional[AssetRepository] = None,
        video_jobs: Optional[VideoJobRepository] = None,
        attempts: Optional[JobAttemptRepository] = None,
        snapshots: Optional[GenerationRequestSnapshotRepository] = None,
        job_asset_references: Optional[JobAssetReferenceRepository] = None,
    ) -> None:
        self._settings = settings
        self._session_factory = session_factory
        self._clock = clock or UtcClock()
        self._idempotency_repository = idempotency_repository or IdempotencyRepository(
            session_factory
        )
        self._assets = asset_repository or AssetRepository(session_factory)
        self._video_jobs = video_jobs or VideoJobRepository(session_factory)
        self._attempts = attempts or JobAttemptRepository(session_factory)
        self._snapshots = snapshots or GenerationRequestSnapshotRepository(
            session_factory
        )
        self._job_asset_references = (
            job_asset_references or JobAssetReferenceRepository(session_factory)
        )
        self._idempotency = idempotency_service or IdempotencyService(
            repository=self._idempotency_repository,
            clock=self._clock,
            completed_ttl_hours=settings.idempotency_completed_ttl_hours,
            pending_lease_seconds=settings.idempotency_pending_lease_seconds,
            recovery_resolver=VideoJobRecoveryResolver(
                video_jobs=self._video_jobs,
                attempts=self._attempts,
                snapshots=self._snapshots,
            ),
        )

    def create_video_job(
        self,
        *,
        owner_id: str,
        request: CreateVideoJobRequest,
        idempotency_key: Optional[str],
        request_id: str,
    ) -> ServiceResponse:
        request_json = request.model_dump(mode="json")
        acquired = self._idempotency.acquire(
            owner_id=owner_id,
            http_method="POST",
            route_template="/v1/video-jobs",
            path_params={},
            request_body=request_json,
            idempotency_key=idempotency_key,
        )
        if acquired.disposition == IdempotencyDisposition.REPLAY:
            return ServiceResponse(
                status_code=acquired.response_status_code or 200,
                payload=acquired.response_json or {},
                dispatch_required=False,
                job_id=acquired.resource_id,
            )

        try:
            self._validate_versions_and_provider(request)
            assets_by_id = self._validate_reference_assets(owner_id, request)
            gate_evaluation = self._evaluate_gates(request, assets_by_id)
        except DomainError as error:
            return self._complete_error(
                record_id=acquired.record_id,
                error=error,
                request_id=request_id,
            )

        canonical = canonicalize_request(
            owner_id=owner_id,
            http_method="POST",
            route_template="/v1/video-jobs",
            path_params={},
            request_body=request_json,
        )
        now = ensure_utc(self._clock.now())
        try:
            with self._session_factory() as session:
                job = self._video_jobs.create_queued_job(
                    session,
                    owner_id=owner_id,
                    contract_version=request.contract_version,
                    truth_rule_version=TRUTH_RULE_VERSION,
                    provider_mapping_version=PROVIDER_MAPPING_VERSION,
                    selected_model=request.selected_model.value,
                    execution_provider=request.execution_provider.value,
                    now=now,
                )
                self._snapshots.create_snapshot(
                    session,
                    job_id=job.job_id,
                    canonical_request_hash=canonical.canonical_request_hash,
                    request_json=request_json,
                    gate_result_json=gate_evaluation.to_json(),
                    now=now,
                )
                attempt = self._attempts.create_prepared_attempt(
                    session,
                    job_id=job.job_id,
                    attempt_no=1,
                    execution_provider=request.execution_provider.value,
                    provider_model=request.selected_model.value,
                    now=now,
                )
                job = self._video_jobs.update_current_attempt_id(
                    session,
                    job_id=job.job_id,
                    attempt_id=attempt.attempt_id,
                    now=now,
                )
                self._job_asset_references.create_many(
                    session,
                    job_id=job.job_id,
                    references=request.reference_assets,
                    now=now,
                )
                self._idempotency_repository.bind_resource_in_session(
                    session,
                    record_id=acquired.record_id,
                    resource_type="video_job",
                    resource_id=job.job_id,
                    now=now,
                )
                session.commit()
        except Exception as exc:
            raise InternalServerError("Failed to create video job transaction.") from exc

        response = CreateVideoJobResponse(
            job_id=job.job_id,
            truth_rule_version=TRUTH_RULE_VERSION,
            provider_mapping_version=PROVIDER_MAPPING_VERSION,
            idempotent_replay=False,
        )
        payload = response.model_dump(mode="json")
        self._idempotency.complete(
            record_id=acquired.record_id,
            response_status_code=202,
            response_json=payload,
            resource_type="video_job",
            resource_id=job.job_id,
        )
        return ServiceResponse(
            status_code=202,
            payload=payload,
            dispatch_required=True,
            job_id=job.job_id,
        )

    def _validate_versions_and_provider(self, request: CreateVideoJobRequest) -> None:
        if (
            request.expected_truth_rule_version is not None
            and request.expected_truth_rule_version != TRUTH_RULE_VERSION
        ):
            raise VersionConflictError()
        if (
            request.selected_model != SelectedModel.Seedance
            or request.execution_provider != ExecutionProvider.mock
        ):
            raise ProviderUnsupportedError()

    def _validate_reference_assets(
        self, owner_id: str, request: CreateVideoJobRequest
    ) -> dict[str, AssetSnapshot]:
        assets_by_id: dict[str, AssetSnapshot] = {}
        for index, reference in enumerate(request.reference_assets):
            asset = self._assets.get_by_id_and_owner(
                asset_id=reference.asset_id,
                owner_id=owner_id,
            )
            if asset is None:
                raise AssetNotFoundError(field=f"reference_assets.{index}.asset_id")
            if asset.status == AssetStatus.PENDING_UPLOAD:
                raise AssetNotReadyError(field=f"reference_assets.{index}.asset_id")
            if (
                asset.status != AssetStatus.READY
                or asset.deleted_at is not None
                or asset.content_type not in ALLOWED_ASSET_CONTENT_TYPES
            ):
                raise AssetInvalidForJobError(field=f"reference_assets.{index}.asset_id")
            assets_by_id[asset.asset_id] = asset
        return assets_by_id

    def _evaluate_gates(
        self,
        request: CreateVideoJobRequest,
        assets_by_id: dict[str, AssetSnapshot],
    ) -> GateEvaluation:
        now = ensure_utc(self._clock.now())
        truth = evaluate_truth_gate(request, assets_by_id)
        if truth.result == GateResult.BLOCK:
            decision = truth.decisions[0]
            if decision.code == "AI_PROOF_NOT_ALLOWED":
                raise AIProofNotAllowedError(
                    message=decision.message,
                    field=decision.field,
                    required_action=decision.required_action,
                    details=decision.details,
                )
            raise TruthGateBlockedError(
                message=decision.message,
                field=decision.field,
                required_action=decision.required_action,
                details=decision.details,
            )
        hybrid = evaluate_hybrid_gate(request, assets_by_id)
        if hybrid.result == GateResult.BLOCK:
            decision = hybrid.decisions[0]
            raise HybridGateBlockedError(
                message=decision.message,
                field=decision.field,
                required_action=decision.required_action,
                details=decision.details,
            )
        return GateEvaluation(
            truth_gate=truth,
            hybrid_gate=hybrid,
            allowed=True,
            evaluated_at=now,
            truth_rule_version=TRUTH_RULE_VERSION,
        )

    def _complete_error(
        self,
        *,
        record_id: str,
        error: DomainError,
        request_id: str,
    ) -> ServiceResponse:
        payload = ErrorResponse(
            error=ErrorDetail(
                code=error.code,
                message=error.message,
                field=error.field,
                required_action=error.required_action,
                request_id=request_id,
                retryable=error.retryable,
                details=error.details,
            )
        ).model_dump(mode="json")
        self._idempotency.complete(
            record_id=record_id,
            response_status_code=error.status_code,
            response_json=payload,
        )
        return ServiceResponse(status_code=error.status_code, payload=payload)
