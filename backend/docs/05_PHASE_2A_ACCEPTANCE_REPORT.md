# Phase 2A Acceptance Report

```yaml
phase_2a_status: PASS
phase_2b_allowed: true
acceptance_date: "2026-07-14"
master_design_version: "1.0"
api_contract_version: "v1"
truth_rule_version: "truth-rules-v0.4"
provider_mapping_version: "mock-provider-map-v0.4"
```

## Scope Accepted

Phase 2A implements the approved local mock backend boundary from
`backend/docs/BACKEND_MASTER_DESIGN.md`.

Public Action endpoints:

- `GET /health`
- `POST /v1/assets/upload-url`
- `POST /v1/video-jobs`
- `GET /v1/video-jobs/{job_id}`
- `POST /v1/video-jobs/{job_id}/cancel`
- `POST /v1/video-jobs/{job_id}/retry`

Internal mock routes excluded from Action OpenAPI:

- `PUT /_internal/mock-uploads/{token}`
- `GET /_internal/mock-results/{token}`

Database tables:

- `assets`
- `video_jobs`
- `job_attempts`
- `generation_request_snapshots`
- `job_asset_references`
- `provider_results`
- `idempotency_records`

## Runtime Behavior

Truth and HYBRID enforcement is structural only. The backend blocks unsupported
AI proof ownership, high-truth pure AI generation, missing real HYBRID proof
carriers, unsupported AI proof roles, and missing rewrite locks. It does not
perform semantic media truth verification.

Idempotency is implemented for upload URL, create job, cancel, and retry. Same
key plus same canonical request replays the stored response. Same key plus
different canonical request returns `IDEMPOTENCY_CONFLICT`. Completed records
use a 24-hour TTL and pending leases use 60 seconds. State errors without side
effects abandon pending records.

Mock Provider and Runner behavior:

- Mock provider only; no real Seedance, ByteDance, or BytePlus calls.
- `FastAPI BackgroundTasks` executes mock generation locally.
- Successful attempts create one `RESULT_MEDIA` asset and one ProviderResult.
- Failed attempts store deterministic error codes.
- Startup recovery marks non-terminal mock attempts `FAILED` with
  `MOCK_RUNNER_INTERRUPTED`.

Cancel and Retry behavior:

- QUEUED/PREPARED cancel completes immediately.
- PROCESSING cancel records `CANCEL_REQUESTED` and the cancel worker can finalize
  `CANCELLED`.
- UNKNOWN provider state only records cancellation intent.
- FAILED and CANCELLED jobs can retry by creating a new attempt and reusing the
  original request snapshot and asset references.
- SUCCEEDED, PROCESSING, and UNKNOWN jobs are not retryable.

Result Token behavior:

- Result URLs use stateless HMAC-SHA256 signed tokens.
- Tokens bind `purpose`, `asset_id`, `owner_id`, and expiry.
- Token secret is separate from Bearer API key.
- Tokens are not stored in plaintext in the database.
- Internal result downloads require a valid token and READY `RESULT_MEDIA`.

## Verification Results

Test commands executed:

- `python3 -m pytest backend -q`
- `python3 -m compileall backend/app`
- `python3 backend/tools/export_action_openapi.py`
- `python3 -m alembic -c alembic.ini upgrade head`
- `python3 -m alembic -c alembic.ini downgrade base`
- `python3 -m alembic -c alembic.ini upgrade head`
- `git diff --check`

Test result:

```text
196 collected
196 passed
0 failed
0 skipped
0 warnings reported
```

OpenAPI validation:

- Export path: `backend/openapi/custom_gpt_action.openapi.yaml`
- OpenAPI version: `3.1.0`
- Six public paths only.
- Stable operation IDs:
  `healthCheck`, `createAssetUploadUrl`, `createVideoJob`, `getVideoJob`,
  `cancelVideoJob`, `retryVideoJob`.
- BearerAuth is declared for all protected public endpoints.
- `Idempotency-Key` is required only on side-effect endpoints.
- Internal routes are excluded.
- Consecutive exports are byte-for-byte identical.
- The artifact does not contain API keys, result token secret, token hashes,
  storage paths, local absolute paths, database URLs, scenario/outcome controls,
  or mock fixture bytes.

Alembic validation:

- Upgrade to head succeeded.
- Downgrade to base succeeded.
- Re-upgrade to head succeeded.
- Runtime app code does not use `Base.metadata.create_all()` for schema
  management.
- SQLAlchemy metadata remains aligned with the seven approved Phase 2A tables.

Frozen file check:

- `custom_gpt_package/**`: no diff from this task.
- `knowledge/**`: no diff from this task.
- `seedance_skills/**`: no diff from this task.
- `backend/docs/BACKEND_MASTER_DESIGN.md`: no diff from this task.
- `backend/docs/02_API_CONTRACT.md`: no diff from this task.
- `backend/docs/04_PHASE_2A_IMPLEMENTATION_PLAN.md`: no diff from this task.
- `backend/alembic/versions/**`: no diff from this task.

## Known Limits

- BackgroundTasks is not a durable queue.
- Service restart marks non-terminal mock attempts `FAILED` with
  `MOCK_RUNNER_INTERRUPTED`.
- Mock file storage is for local tests and development only.
- The backend does not perform media semantic truth verification.
- Knowledge 10 Review is not implemented.
- Real Seedance is not connected.
- Result Token is a Phase 2A local capability credential.
- Authentication is single-tenant Bearer API Key.
- Custom GPT direct binary attachment input is not supported.
- Provider callback and UNKNOWN provider reconciliation are not implemented.

## Excluded From Phase 2A

- Real Seedance, ByteDance, BytePlus, payment, external storage, Redis, Celery,
  external queues, and billing integrations.
- Provider callbacks.
- UNKNOWN provider reconciliation.
- Knowledge 10 Review.
- PRODUCT_LINK fetching.
- Public mock scenario/outcome controls.
- Multi-tenant authentication.

## Final Decision

All blocking checks passed.

Phase 2A is accepted as a local mock backend implementation and may proceed to
Phase 2B planning or implementation under a new approved scope.
