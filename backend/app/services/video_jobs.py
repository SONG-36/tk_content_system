"""Create video job service for Phase 2A."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from sqlalchemy.exc import IntegrityError

from app.config import Settings
from app.db.types import (
    AIReviewStatus,
    AssetKind,
    AssetStatus,
    AttemptStatus,
    GenerationStatus,
)
from app.gates import GateEvaluation, GateResult, evaluate_hybrid_gate, evaluate_truth_gate
from app.idempotency import IdempotencyDisposition, IdempotencyService
from app.idempotency.canonical import canonicalize_request
from app.idempotency.repository import IdempotencyRepository, SessionFactory
from app.idempotency.types import Clock, UtcClock, ensure_utc
from app.models.job_attempt import JobAttempt
from app.models.video_job import VideoJob
from app.repositories.assets import AssetRepository, AssetSnapshot
from app.repositories.job_asset_references import JobAssetReferenceRepository
from app.repositories.job_attempts import JobAttemptRepository
from app.repositories.provider_results import ProviderResultRepository
from app.repositories.request_snapshots import GenerationRequestSnapshotRepository
from app.repositories.video_jobs import VideoJobRepository
from app.schemas.common import ErrorDetail, ErrorResponse
from app.schemas.enums import ExecutionProvider, SelectedModel
from app.schemas.jobs import (
    AssetSummary,
    AttemptSummary,
    CancelJobRequest,
    CancelJobResponse,
    CreateVideoJobRequest,
    CreateVideoJobResponse,
    GetVideoJobResponse,
    ResultMediaSummary,
    RetryJobRequest,
    RetryJobResponse,
    StoredJobError,
)
from app.services.errors import (
    AIProofNotAllowedError,
    AssetInvalidForJobError,
    AssetNotFoundError,
    AssetNotReadyError,
    DomainError,
    HybridGateBlockedError,
    InternalServerError,
    JobCancelNotAllowedError,
    JobInvalidStateError,
    JobNotFoundError,
    JobNotRetryableError,
    ProviderUnsupportedError,
    TruthGateBlockedError,
    UnknownProviderStateError,
    VersionConflictError,
)
from app.services.job_recovery import (
    CancelJobRecoveryResolver,
    RetryJobRecoveryResolver,
    VideoJobRecoveryResolver,
)
from app.services.result_tokens import ResultTokenService
from app.state_machines.attempts import assert_attempt_transition
from app.state_machines.jobs import assert_job_transition

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
        provider_results: Optional[ProviderResultRepository] = None,
        snapshots: Optional[GenerationRequestSnapshotRepository] = None,
        job_asset_references: Optional[JobAssetReferenceRepository] = None,
        result_tokens: Optional[ResultTokenService] = None,
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
        self._provider_results = provider_results or ProviderResultRepository(
            session_factory
        )
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
        self._result_tokens = result_tokens or ResultTokenService(
            settings=settings,
            clock=self._clock,
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

    def get_video_job(self, *, owner_id: str, job_id: str) -> GetVideoJobResponse:
        job = self._video_jobs.get_by_id_and_owner(job_id=job_id, owner_id=owner_id)
        if job is None:
            raise JobNotFoundError()
        return self._build_get_response(job_id=job.job_id, owner_id=owner_id)

    def cancel_video_job(
        self,
        *,
        owner_id: str,
        job_id: str,
        request: CancelJobRequest,
        idempotency_key: Optional[str],
    ) -> ServiceResponse:
        idempotency = self._cancel_idempotency()
        request_json = request.model_dump(mode="json")
        acquired = idempotency.acquire(
            owner_id=owner_id,
            http_method="POST",
            route_template="/v1/video-jobs/{job_id}/cancel",
            path_params={"job_id": job_id},
            request_body=request_json,
            idempotency_key=idempotency_key,
        )
        if acquired.disposition == IdempotencyDisposition.REPLAY:
            return ServiceResponse(
                status_code=acquired.response_status_code or 200,
                payload=acquired.response_json or {},
                dispatch_required=False,
                job_id=job_id,
            )

        try:
            outcome = self._apply_cancel(
                owner_id=owner_id,
                job_id=job_id,
                record_id=acquired.record_id,
            )
        except DomainError:
            idempotency.abandon(acquired.record_id)
            raise

        idempotency.complete(
            record_id=acquired.record_id,
            response_status_code=outcome.status_code,
            response_json=outcome.payload,
            resource_type="video_job",
            resource_id=job_id,
        )
        return outcome

    def retry_video_job(
        self,
        *,
        owner_id: str,
        job_id: str,
        request: RetryJobRequest,
        idempotency_key: Optional[str],
    ) -> ServiceResponse:
        idempotency = self._retry_idempotency()
        request_json = request.model_dump(mode="json")
        acquired = idempotency.acquire(
            owner_id=owner_id,
            http_method="POST",
            route_template="/v1/video-jobs/{job_id}/retry",
            path_params={"job_id": job_id},
            request_body=request_json,
            idempotency_key=idempotency_key,
        )
        if acquired.disposition == IdempotencyDisposition.REPLAY:
            dispatch = self._retry_replay_should_dispatch(
                job_id=job_id,
                attempt_id=acquired.resource_id,
            )
            return ServiceResponse(
                status_code=acquired.response_status_code or 202,
                payload=acquired.response_json or {},
                dispatch_required=dispatch,
                job_id=job_id,
            )

        try:
            outcome = self._apply_retry(
                owner_id=owner_id,
                job_id=job_id,
                record_id=acquired.record_id,
            )
        except DomainError:
            idempotency.abandon(acquired.record_id)
            raise

        idempotency.complete(
            record_id=acquired.record_id,
            response_status_code=outcome.status_code,
            response_json=outcome.payload,
            resource_type="job_attempt",
            resource_id=outcome.payload["new_attempt_id"],
        )
        return outcome

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

    def _build_get_response(self, *, job_id: str, owner_id: str) -> GetVideoJobResponse:
        job = self._video_jobs.get_by_id_and_owner(job_id=job_id, owner_id=owner_id)
        if job is None:
            raise JobNotFoundError()
        current_attempt = None
        if job.current_attempt_id is not None:
            attempt = self._attempts.get_current_for_job(
                job_id=job.job_id,
                current_attempt_id=job.current_attempt_id,
            )
            if attempt is not None:
                current_attempt = _attempt_summary(attempt)

        references = self._job_asset_references.list_for_job(job.job_id)
        assets_by_id = {
            asset.asset_id: asset
            for asset in self._assets.list_by_ids_and_owner(
                asset_ids=[reference.asset_id for reference in references],
                owner_id=owner_id,
            )
        }
        assets = []
        for reference in references:
            asset = assets_by_id.get(reference.asset_id)
            if asset is None or asset.asset_kind == AssetKind.RESULT_MEDIA:
                continue
            assets.append(
                AssetSummary(
                    asset_id=asset.asset_id,
                    asset_kind=asset.asset_kind,
                    asset_status=asset.status,
                    content_type=asset.content_type,
                    size_bytes=asset.size_bytes,
                    checksum_sha256=asset.checksum_sha256,
                    usage_role=reference.usage_role,
                )
            )

        result_media = []
        if (
            job.current_attempt_id is not None
            and job.generation_status == GenerationStatus.SUCCEEDED
        ):
            provider_result = self._provider_results.get_by_attempt_id(
                job.current_attempt_id
            )
            if provider_result is not None:
                for asset_id in provider_result.result_asset_ids_json:
                    asset = self._assets.get_result_asset_by_id_and_owner(
                        asset_id=asset_id,
                        owner_id=owner_id,
                    )
                    if asset is None or asset.status != AssetStatus.READY:
                        continue
                    token, expires_at = self._result_tokens.issue(
                        asset_id=asset.asset_id,
                        owner_id=owner_id,
                    )
                    result_media.append(
                        ResultMediaSummary(
                            asset_id=asset.asset_id,
                            content_type=asset.content_type,
                            size_bytes=asset.size_bytes,
                            checksum_sha256=asset.checksum_sha256,
                            result_url=(
                                f"{self._settings.public_base_url}"
                                f"/_internal/mock-results/{token}"
                            ),
                            result_url_expires_at=expires_at,
                        )
                    )

        errors = [
            StoredJobError(
                code=attempt.error_code,
                message=_stored_error_message(attempt.error_code),
                attempt_id=attempt.attempt_id,
                created_at=attempt.terminal_at or attempt.updated_at,
            )
            for attempt in self._attempts.list_for_job(job.job_id)
            if attempt.error_code is not None
        ]

        return GetVideoJobResponse(
            job_id=job.job_id,
            generation_status=job.generation_status,
            ai_review_status=AIReviewStatus.NOT_RUN,
            current_attempt=current_attempt,
            assets=assets,
            result_media=result_media,
            errors=errors,
        )

    def _apply_cancel(
        self, *, owner_id: str, job_id: str, record_id: str
    ) -> ServiceResponse:
        now = ensure_utc(self._clock.now())
        with self._session_factory() as session:
            job = session.get(VideoJob, job_id)
            if job is None or job.owner_id != owner_id or job.current_attempt_id is None:
                raise JobNotFoundError()
            attempt = session.get(JobAttempt, job.current_attempt_id)
            if attempt is None:
                raise JobInvalidStateError()

            if (
                job.generation_status == GenerationStatus.QUEUED
                and attempt.attempt_status == AttemptStatus.PREPARED
            ):
                assert_attempt_transition(AttemptStatus.PREPARED, AttemptStatus.CANCELLED)
                assert_job_transition(GenerationStatus.QUEUED, GenerationStatus.CANCELLED)
                attempt_ok = self._attempts.transition_attempt(
                    session,
                    attempt_id=attempt.attempt_id,
                    expected_status=AttemptStatus.PREPARED,
                    target_status=AttemptStatus.CANCELLED,
                    cancellation_intent=True,
                    cancel_requested_at=now,
                    terminal_at=now,
                    now=now,
                )
                job_ok = self._video_jobs.transition_job(
                    session,
                    job_id=job.job_id,
                    expected_status=GenerationStatus.QUEUED,
                    target_status=GenerationStatus.CANCELLED,
                    now=now,
                )
                if not attempt_ok or not job_ok:
                    session.rollback()
                    raise JobInvalidStateError()
                self._idempotency_repository.bind_resource_in_session(
                    session,
                    record_id=record_id,
                    resource_type="video_job",
                    resource_id=job.job_id,
                    now=now,
                )
                session.commit()
                return _cancel_response(job.job_id, GenerationStatus.CANCELLED, AttemptStatus.CANCELLED, True, now, 200)

            if job.generation_status == GenerationStatus.PROCESSING:
                if attempt.attempt_status == AttemptStatus.SUBMITTED:
                    assert_attempt_transition(AttemptStatus.SUBMITTED, AttemptStatus.PROCESSING)
                    if not self._attempts.transition_attempt(
                        session,
                        attempt_id=attempt.attempt_id,
                        expected_status=AttemptStatus.SUBMITTED,
                        target_status=AttemptStatus.PROCESSING,
                        now=now,
                    ):
                        session.rollback()
                        raise JobInvalidStateError()
                    attempt = session.get(JobAttempt, attempt.attempt_id)
                if attempt.attempt_status == AttemptStatus.PROCESSING:
                    assert_attempt_transition(AttemptStatus.PROCESSING, AttemptStatus.CANCEL_REQUESTED)
                    if not self._attempts.transition_attempt(
                        session,
                        attempt_id=attempt.attempt_id,
                        expected_status=AttemptStatus.PROCESSING,
                        target_status=AttemptStatus.CANCEL_REQUESTED,
                        cancellation_intent=True,
                        cancel_requested_at=now,
                        now=now,
                    ):
                        session.rollback()
                        raise JobInvalidStateError()
                    self._idempotency_repository.bind_resource_in_session(
                        session,
                        record_id=record_id,
                        resource_type="video_job",
                        resource_id=job.job_id,
                        now=now,
                    )
                    session.commit()
                    return _cancel_response(job.job_id, GenerationStatus.PROCESSING, AttemptStatus.CANCEL_REQUESTED, True, now, 202, dispatch=True)
                if attempt.attempt_status == AttemptStatus.CANCEL_REQUESTED:
                    self._idempotency_repository.bind_resource_in_session(
                        session,
                        record_id=record_id,
                        resource_type="video_job",
                        resource_id=job.job_id,
                        now=now,
                    )
                    session.commit()
                    return _cancel_response(job.job_id, GenerationStatus.PROCESSING, AttemptStatus.CANCEL_REQUESTED, True, attempt.cancel_requested_at, 202, dispatch=True)
                if attempt.attempt_status == AttemptStatus.UNKNOWN_PROVIDER_STATE:
                    cancel_requested_at = attempt.cancel_requested_at or now
                    self._attempts.set_cancellation_intent(
                        session,
                        attempt_id=attempt.attempt_id,
                        now=cancel_requested_at,
                    )
                    self._idempotency_repository.bind_resource_in_session(
                        session,
                        record_id=record_id,
                        resource_type="video_job",
                        resource_id=job.job_id,
                        now=now,
                    )
                    session.commit()
                    return _cancel_response(job.job_id, GenerationStatus.PROCESSING, AttemptStatus.UNKNOWN_PROVIDER_STATE, True, cancel_requested_at, 202)

            if (
                job.generation_status == GenerationStatus.CANCELLED
                and attempt.attempt_status == AttemptStatus.CANCELLED
            ):
                self._idempotency_repository.bind_resource_in_session(
                    session,
                    record_id=record_id,
                    resource_type="video_job",
                    resource_id=job.job_id,
                    now=now,
                )
                session.commit()
                return _cancel_response(job.job_id, GenerationStatus.CANCELLED, AttemptStatus.CANCELLED, True, attempt.cancel_requested_at, 200)

            if job.generation_status in {GenerationStatus.SUCCEEDED, GenerationStatus.FAILED}:
                raise JobCancelNotAllowedError()
            raise JobInvalidStateError()

    def _apply_retry(
        self, *, owner_id: str, job_id: str, record_id: str
    ) -> ServiceResponse:
        now = ensure_utc(self._clock.now())
        try:
            with self._session_factory() as session:
                job = session.get(VideoJob, job_id)
                if job is None or job.owner_id != owner_id or job.current_attempt_id is None:
                    raise JobNotFoundError()
                current_attempt = session.get(JobAttempt, job.current_attempt_id)
                if current_attempt is None:
                    raise JobInvalidStateError()
                if current_attempt.attempt_status == AttemptStatus.UNKNOWN_PROVIDER_STATE:
                    raise UnknownProviderStateError()
                if not (
                    (
                        job.generation_status == GenerationStatus.FAILED
                        and current_attempt.attempt_status == AttemptStatus.FAILED
                    )
                    or (
                        job.generation_status == GenerationStatus.CANCELLED
                        and current_attempt.attempt_status == AttemptStatus.CANCELLED
                    )
                ):
                    raise JobNotRetryableError()
                attempt_no = self._attempts.next_attempt_no(session, job.job_id)
                new_attempt = self._attempts.create_prepared_attempt(
                    session,
                    job_id=job.job_id,
                    attempt_no=attempt_no,
                    execution_provider=job.execution_provider,
                    provider_model=job.selected_model,
                    now=now,
                )
                assert_job_transition(job.generation_status, GenerationStatus.QUEUED)
                if not self._video_jobs.transition_job_and_current_attempt(
                    session,
                    job_id=job.job_id,
                    expected_status=job.generation_status,
                    expected_current_attempt_id=current_attempt.attempt_id,
                    target_status=GenerationStatus.QUEUED,
                    target_current_attempt_id=new_attempt.attempt_id,
                    now=now,
                ):
                    session.rollback()
                    raise JobNotRetryableError()
                self._idempotency_repository.bind_resource_in_session(
                    session,
                    record_id=record_id,
                    resource_type="job_attempt",
                    resource_id=new_attempt.attempt_id,
                    now=now,
                )
                session.commit()
        except IntegrityError as exc:
            raise JobNotRetryableError() from exc

        response = RetryJobResponse(
            job_id=job_id,
            new_attempt_id=new_attempt.attempt_id,
            idempotent_replay=False,
        )
        return ServiceResponse(
            status_code=202,
            payload=response.model_dump(mode="json"),
            dispatch_required=True,
            job_id=job_id,
        )

    def _cancel_idempotency(self) -> IdempotencyService:
        return IdempotencyService(
            repository=self._idempotency_repository,
            clock=self._clock,
            completed_ttl_hours=self._settings.idempotency_completed_ttl_hours,
            pending_lease_seconds=self._settings.idempotency_pending_lease_seconds,
            recovery_resolver=CancelJobRecoveryResolver(
                video_jobs=self._video_jobs,
                attempts=self._attempts,
            ),
        )

    def _retry_idempotency(self) -> IdempotencyService:
        return IdempotencyService(
            repository=self._idempotency_repository,
            clock=self._clock,
            completed_ttl_hours=self._settings.idempotency_completed_ttl_hours,
            pending_lease_seconds=self._settings.idempotency_pending_lease_seconds,
            recovery_resolver=RetryJobRecoveryResolver(
                video_jobs=self._video_jobs,
                attempts=self._attempts,
            ),
        )

    def _retry_replay_should_dispatch(
        self, *, job_id: str, attempt_id: Optional[str]
    ) -> bool:
        if attempt_id is None:
            return False
        job = self._video_jobs.get_by_id(job_id)
        attempt = self._attempts.get_by_id(attempt_id)
        return (
            job is not None
            and attempt is not None
            and job.current_attempt_id == attempt_id
            and job.generation_status == GenerationStatus.QUEUED
            and attempt.attempt_status == AttemptStatus.PREPARED
        )

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


def _attempt_summary(attempt) -> AttemptSummary:
    return AttemptSummary(
        attempt_id=attempt.attempt_id,
        attempt_no=attempt.attempt_no,
        attempt_status=attempt.attempt_status,
        execution_provider=attempt.execution_provider,
        provider_job_id=attempt.provider_job_id,
        cancellation_intent=attempt.cancellation_intent,
        cancel_requested_at=attempt.cancel_requested_at,
        error_code=attempt.error_code,
        created_at=attempt.created_at,
        submitted_at=attempt.submitted_at,
        terminal_at=attempt.terminal_at,
        updated_at=attempt.updated_at,
    )


def _cancel_response(
    job_id: str,
    generation_status: GenerationStatus,
    attempt_status: AttemptStatus,
    cancellation_intent: bool,
    cancel_requested_at,
    status_code: int,
    *,
    dispatch: bool = False,
) -> ServiceResponse:
    response = CancelJobResponse(
        job_id=job_id,
        generation_status=generation_status,
        attempt_status=attempt_status,
        cancellation_intent=cancellation_intent,
        cancel_requested_at=cancel_requested_at,
        idempotent_replay=False,
    )
    return ServiceResponse(
        status_code=status_code,
        payload=response.model_dump(mode="json"),
        dispatch_required=dispatch,
        job_id=job_id,
    )


def _stored_error_message(error_code: Optional[str]) -> str:
    messages = {
        "MOCK_PROVIDER_FAILED": "The mock provider reported a failed generation.",
        "MOCK_RESULT_STORAGE_FAILED": "The mock result could not be stored.",
        "MOCK_RUNNER_INTERNAL_ERROR": "The mock runner failed unexpectedly.",
        "MOCK_RUNNER_INTERRUPTED": "The mock runner was interrupted during startup recovery.",
        "MOCK_RESULT_INVALID": "The mock provider returned an invalid result payload.",
    }
    if error_code is None:
        return ""
    return messages.get(error_code, "The job attempt failed.")
