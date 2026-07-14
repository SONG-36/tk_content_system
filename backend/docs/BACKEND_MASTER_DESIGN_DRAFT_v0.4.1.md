# Backend Master Design Draft v0.4.1

## 1. Document Status

```yaml
document_status:
  document_version: "v0.4.1"
  status: "DRAFT"
  base_document: "backend/docs/BACKEND_MASTER_DESIGN_DRAFT_v0.4.md"
  overwrites_v0_4: false
  document_type: "Phase 2A Implementation Profile"
  implementation_code_created: false
  approval_required_before_coding: true
```

This document does not rewrite v0.4. It is an implementation profile that
narrows Phase 2A coding scope while preserving the v0.4 architecture, public API
surface, Product Truth boundaries, and Custom GPT runtime freeze.

If this document conflicts with v0.4, v0.4.1 wins only for Phase 2A
implementation details. Broader product, provider, and post-Phase 2A decisions
remain governed by v0.4 until superseded.

## 2. Phase 2A Minimal Persistence Profile

Phase 2A creates only these required tables:

- `assets`
- `video_jobs`
- `job_attempts`
- `generation_request_snapshots`
- `job_asset_references`
- `provider_results`
- `idempotency_records`

Optional table:

- `error_records`

Phase 2A does not create independent tables for:

- `client_declared_facts`
- `source_refs`
- `proof_needs`
- `truth_gate_decisions`
- `hybrid_gate_decisions`
- `backend_facts`
- `verification_records`
- `review_results`

Storage rule:

```yaml
phase_2a_storage:
  client_declared_facts: "generation_request_snapshots.request_json"
  source_refs: "generation_request_snapshots.request_json"
  proof_needs: "generation_request_snapshots.request_json"
  truth_gate_decisions: "generation_request_snapshots.gate_result_json"
  hybrid_gate_decisions: "generation_request_snapshots.gate_result_json"
  backend_facts: "not_created_in_phase_2a"
  verification_records: "not_created_in_phase_2a"
  review_results: "not_created_in_phase_2a"
```

Rationale:

- Phase 2A validates structure and state behavior, not full fact verification.
- Keeping facts and gate results in snapshot JSON reduces premature schema
  surface.
- Dedicated verification/review tables should wait until review submission and
  semantic verification are designed.

## 3. Generation Mode Cross-validation

Allowed Phase 2A modes remain:

- `T2V`
- `I2V`
- `R2V`
- `FLF2V`

Cross-validation:

| Mode | Required Reference Assets | Invalid Cases |
| --- | --- | --- |
| `T2V` | No required assets. | Asset roles may be present only as optional context; proof still cannot be AI-owned. |
| `I2V` | At least one `FIRST_FRAME` or `PRODUCT_IDENTITY`. | No usable first-frame/product reference. |
| `R2V` | At least one reference asset of any allowed usage role. | Empty `reference_assets`. |
| `FLF2V` | Exactly one `FIRST_FRAME` and exactly one `LAST_FRAME`. | Missing either role, duplicate first frame, duplicate last frame. |

Modes without complete Phase 2A schema and tests remain excluded.

## 4. Reference Integrity Rules

Validate before Truth Gate and HYBRID Gate:

- Every `reference_assets[].asset_id` must exist, belong to the server-mapped
  owner, and be `READY`.
- Every `reference_assets[].shot_number` must match the request-level
  `shot_number` unless the field is explicitly omitted by future schema.
- Every `reference_assets[].linked_proof_need_ids[]` must reference an existing
  `proof_needs[].proof_need_id`.
- Every `proof_needs[].linked_client_fact_ids[]` must reference an existing
  `client_declared_facts[].client_fact_id`.
- Every `proof_needs[].required_evidence_refs[]` must reference an existing
  `source_refs[].source_ref_id` or valid asset id according to the schema field
  where it appears.
- `proof_needs[].production_type` must match request-level `production_type`.
- `HYBRID` requests must include `hybrid_layers`.
- `AI_GENERATION` requests must not include `hybrid_layers`.
- Any `hybrid_layers.real_layer.carries_proof_need_ids[]` must reference
  existing proof needs.
- Any `hybrid_layers.real_layer.reference_asset_ids[]` must reference existing
  `reference_assets[].asset_id`.

Integrity failures are schema/contract failures and return HTTP 422
`SCHEMA_INVALID` with field-level details.

## 5. Mock Provider Runner

Phase 2A mock provider execution uses:

```yaml
mock_provider_runner:
  runner: "FastAPI BackgroundTasks"
  default_outcome: "success"
  test_outcome_control: "dependency_injection_only"
  supported_test_outcomes:
    - "success"
    - "failed"
    - "unknown"
    - "cancel"
  clock: "Fake Clock"
  public_scenario_field: false
  celery: false
  redis: false
  external_queue: false
```

Rules:

- Public API requests must not contain scenario or outcome fields.
- Tests can inject failed, unknown, or cancel behavior through application
  dependency overrides.
- BackgroundTasks is sufficient for Phase 2A local/mock execution.
- Do not introduce Celery, Redis, a durable queue, or a provider worker service
  in Phase 2A.
- On service startup, any non-terminal mock attempt left by a prior process is
  marked `FAILED` with error code `MOCK_RUNNER_INTERRUPTED`, unless it is
  already terminal.

Non-terminal mock attempts:

- `PREPARED`
- `SUBMITTED`
- `PROCESSING`
- `CANCEL_REQUESTED`
- `UNKNOWN_PROVIDER_STATE`

Terminal mock attempts:

- `SUCCEEDED`
- `FAILED`
- `CANCELLED`

## 6. Idempotency Implementation Profile

TTL and lease:

```yaml
idempotency:
  completed_ttl_hours: 24
  pending_lease_seconds: 60
```

Required header:

- All side-effect endpoints require `Idempotency-Key`.
- Missing key returns HTTP 422 `IDEMPOTENCY_KEY_REQUIRED`.

Record states:

- `PENDING`
- `COMPLETED`

Completed replay:

- Same scope, same key, same canonical request, completed within 24 hours:
  return stored response with `idempotent_replay=true`.

Pending lease:

- First request creates `PENDING` with `lease_expires_at=now+60s`.
- Concurrent same-key request during active lease returns HTTP 409
  `IDEMPOTENCY_PENDING`.
- Same key with different canonical hash returns HTTP 409
  `IDEMPOTENCY_CONFLICT`.

Expired PENDING takeover:

- If `PENDING.lease_expires_at < now`, a new request with the same key and same
  canonical hash may take over the idempotency record inside a transaction.
- Takeover updates the lease and continues the operation only after checking for
  already-created resources linked to the old pending record.
- If a resource already exists and has a deterministic response, complete the
  idempotency record from that resource instead of creating a duplicate.
- If partial resources exist but cannot be safely completed, return HTTP 409
  `IDEMPOTENCY_PENDING` or a deterministic recovery error; do not duplicate
  provider submission.

Resource recovery rules:

- Upload URL: if an `Asset(PENDING_UPLOAD)` already exists for the pending
  record, reuse it and complete the response if the upload token remains valid.
- Create Job: if a `VideoJob` already exists for the pending record, reuse it
  and complete the response; do not create a second job.
- Cancel: if cancellation state or intent was already written, replay the
  resulting state.
- Retry: if a new attempt was already created, replay that attempt id.

Do not cache state-volatile errors:

- `IDEMPOTENCY_PENDING`
- `INTERNAL_ERROR`
- provider transient errors
- errors whose truth can change without payload changes, such as temporarily
  unavailable database state

Continue caching deterministic post-auth validation responses, including create
job 422 schema/truth/hybrid failures.

## 7. Mock Upload And Result URL Profile

Mock upload URLs and result URLs must be HTTP/HTTPS URLs using one-time or
signed tokens.

Upload token:

```yaml
upload_token:
  route: "PUT /_internal/mock-uploads/{token}"
  bound_to:
    - "asset_id"
    - "owner_id"
  ttl_hours: 24
  one_time_use: true
  validates:
    - "content_type"
    - "size_bytes"
    - "checksum_sha256"
```

Result token:

```yaml
result_token:
  route: "GET /_internal/mock-results/{token}"
  bound_to:
    - "asset_id"
    - "owner_id"
  ttl_hours: 24
  one_time_use: false
  requires_asset_status: "READY"
```

Rules:

- Upload token is bound to both Asset and owner.
- Result URL uses a token and must not expose only `asset_id`.
- Upload validates declared content type, size, and checksum before marking an
  Asset `READY`.
- Checksum mismatch marks upload failed or returns deterministic upload error;
  implementation must not mark the Asset `READY`.
- Expired upload token does not automatically expire the Asset.
- Expired result token does not automatically expire the Asset.

Public Action schema still exposes only `POST /v1/assets/upload-url`; internal
upload/result routes are excluded.

## 8. Internal Route Error Codes

Add these internal route errors to the v0.4 registry:

| Code | HTTP | Meaning | Used By |
| --- | --- | --- | --- |
| `UPLOAD_TOKEN_INVALID` | 404 | Upload token does not exist or does not match owner/asset. | internal mock upload |
| `UPLOAD_TOKEN_EXPIRED` | 410 | Upload token expired. | internal mock upload |
| `UPLOAD_ALREADY_COMPLETED` | 409 | Upload token or Asset was already completed. | internal mock upload |
| `CHECKSUM_MISMATCH` | 422 | Uploaded bytes do not match declared checksum. | internal mock upload |
| `RESULT_TOKEN_INVALID` | 404 | Result token does not exist or does not match owner/asset. | internal mock result |
| `RESULT_URL_EXPIRED` | 410 | Result token expired. | internal mock result |
| `RESULT_NOT_READY` | 409 | Result Asset is not ready. | internal mock result |
| `IDEMPOTENCY_KEY_REQUIRED` | 422 | Required `Idempotency-Key` header is missing. | upload, create, cancel, retry |
| `MOCK_RUNNER_INTERRUPTED` | 500 | Non-terminal mock attempt was left by a previous process. | startup recovery, get job |

These codes supplement v0.4 Section 27. Internal route errors do not enter the
public Custom GPT Action schema unless their route becomes public in a later
phase.

## 9. Decision Log Addendum

Add D-029 through D-033 to the v0.4 Decision Log:

| ID | Decision | Status | Phase 2A Result |
| --- | --- | --- | --- |
| D-029 | Minimal persistence tables | APPROVED_FOR_PHASE_2A | Use only assets, video_jobs, job_attempts, generation_request_snapshots, job_asset_references, provider_results, idempotency_records; error_records optional. |
| D-030 | Snapshot JSON for client facts/proofs/gates | APPROVED_FOR_PHASE_2A | Store client facts, source refs, proof needs, and gate result JSON in request snapshot; no separate tables. |
| D-031 | Mock Provider Runner | APPROVED_FOR_PHASE_2A | FastAPI BackgroundTasks, default success, test dependency injection, Fake Clock, no Celery/Redis/queue. |
| D-032 | Idempotency lease profile | APPROVED_FOR_PHASE_2A | Completed TTL 24h, pending lease 60s, takeover with resource recovery. |
| D-033 | Tokenized mock upload/result URLs | APPROVED_FOR_PHASE_2A | HTTP/HTTPS token URLs bound to Asset and owner; 24h expiry; validate type, size, checksum. |

## 10. Updated Coding Blocker

The only remaining start-coding blocker remains final human approval of the
v0.4/v0.4.1 baseline and the future final filename.

Not blockers for Phase 2A mock coding:

- Direct binary attachment support.
- Independent fact/proof/review tables.
- Celery, Redis, or durable queue.
- Real Seedance API details.
- Real cost confirmation endpoint.
- Knowledge 10 review submission endpoint.
- Production object storage.
- Multi-tenant auth.

## 11. Approval Checklist Addendum

Before starting code, approve:

- v0.4.1 as the Phase 2A implementation profile.
- Minimal persistence table list.
- Snapshot JSON storage for facts, source refs, proof needs, and gate decisions.
- No Phase 2A tables for backend facts, verification records, or review
  results.
- Generation mode cross-validation matrix.
- Reference integrity rules.
- FastAPI BackgroundTasks mock runner with dependency-injected test outcomes.
- Completed idempotency TTL 24h and pending lease 60s.
- Tokenized HTTP/HTTPS mock upload and result URLs.
- Internal route errors listed in this addendum.
- Final document naming after approval.
