# Backend Master Design

## 1. Document Status

```yaml
document_status:
  status: "APPROVED_FOR_PHASE_2A"
  design_version: "1.0"
  implementation_allowed: true
  phase: "Phase 2A"
  backend_target: "independently deployable FastAPI backend"
  contract_version: "v1"
  truth_rule_version: "truth-rules-v0.4"
  provider_mapping_version: "mock-provider-map-v0.4"
```

This is the authoritative backend design for Phase 2A implementation. It is
self-contained and does not require reading previous design revisions.

## 2. Authority And Boundaries

Runtime authoritative Custom GPT files:

- `custom_gpt_package/multi_category_gpt/00_INSTRUCTIONS/MAIN_INSTRUCTIONS.md`
- `custom_gpt_package/multi_category_gpt/01_KNOWLEDGE_UPLOAD/01-18_*.md`

Backend scope authoritative files:

- `AGENTS.md`
- `backend/AGENTS.md`
- `backend/docs/BACKEND_MASTER_DESIGN.md`
- `backend/docs/reference/VIDEO_GENERATION_BACKEND_HANDOFF.md`

Third-party or non-authoritative backend sources:

- `seedance_skills/**`
- `custom_gpt_package/multi_category_gpt/02_SOURCE_FILES/seedance_skills/**`
- `source/open_source/**`

Backend runtime must not parse Custom GPT Markdown, Knowledge files, Skills, or
third-party prompt references. Rules needed by backend are translated into JSON
schemas, enums, validators, state machines, persistence, and tests.

## 3. Phase 2A Scope

Phase 2A implements:

- Python FastAPI backend under `backend/`.
- Six public Custom GPT Action-compatible JSON endpoints.
- Two internal mock HTTP routes excluded from Action OpenAPI.
- SQLite + SQLAlchemy 2.x + Alembic.
- Single-tenant Bearer API key auth.
- Structural Truth Gate and HYBRID Gate.
- Mock asset upload and result URL flow.
- Mock provider only.
- FastAPI BackgroundTasks mock runner.
- Idempotency for side-effect endpoints.
- Public Job state, Attempt state, and AI review status separation.
- Tests for schemas, gates, idempotency, state machines, mock runner, and API
  contract.

Phase 2A does not implement:

- Real Seedance, ByteDance, BytePlus, storage, queue, Redis, Celery, billing, or
  external service calls.
- Semantic media truth verification.
- Knowledge 10 review submission endpoint.
- Public mock scenario control.
- Open-ended external URL fetching.
- Multi-tenant auth.

## 4. Public And Internal Routes

Public Custom GPT Action routes:

- `GET /health`
- `POST /v1/assets/upload-url`
- `POST /v1/video-jobs`
- `GET /v1/video-jobs/{job_id}`
- `POST /v1/video-jobs/{job_id}/cancel`
- `POST /v1/video-jobs/{job_id}/retry`

Internal non-Action routes:

- `PUT /_internal/mock-uploads/{token}`
- `GET /_internal/mock-results/{token}`

Internal routes are for tests and local development only. They must not be
included in the Custom GPT Action OpenAPI schema.

## 5. Layer Separation

Client-controlled fields:

- `contract_version`
- optional `expected_truth_rule_version`
- `selected_model`
- `execution_provider`
- `shot_number`
- `production_type`
- `generation_mode`
- `prompt`
- `negative_constraints`
- `preservation_constraints`
- `reference_assets`
- `truth_dependency`
- `hybrid_layers`
- `duration_seconds`
- `aspect_ratio`
- `client_declared_facts`
- `source_refs`
- `proof_needs`

Client-disallowed fields:

- `verification_status`
- `trust_level`
- `backend_gate_result`
- `verification_record.result`
- `truth_rule_version`
- `provider_mapping_version`
- `owner_id`
- `generation_status`
- `ai_review_status`
- `attempt_status`
- `provider_job_id`
- `provider_result`
- mock scenario selector

Proof ownership is expressed only through `proof_needs`, `hybrid_layers`, and
`reference_assets`.

## 6. Persistence Profile

Required Phase 2A tables:

- `assets`
- `video_jobs`
- `job_attempts`
- `generation_request_snapshots`
- `job_asset_references`
- `provider_results`
- `idempotency_records`

Optional Phase 2A table:

- `error_records`

No Phase 2A tables:

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

## 7. Version Fields

Client submits:

```yaml
contract_version: "v1"
expected_truth_rule_version: "truth-rules-v0.4" # optional compatibility check
```

Server controls:

```yaml
truth_rule_version: "truth-rules-v0.4"
provider_mapping_version: "mock-provider-map-v0.4"
```

If the optional expected truth rule version mismatches the server version, the
backend returns HTTP 409 `VERSION_CONFLICT`.

## 8. Request Model

```yaml
create_video_job_request:
  contract_version: "v1"
  expected_truth_rule_version: "truth-rules-v0.4"
  selected_model: "Seedance"
  execution_provider: "mock"
  shot_number: "Shot 03"
  production_type: "AI_GENERATION | HYBRID"
  generation_mode: "T2V | I2V | R2V | FLF2V"
  prompt: ""
  negative_constraints: []
  preservation_constraints: []
  reference_assets:
    - asset_id: "asset_..."
      usage_role: "PRODUCT_IDENTITY | FIRST_FRAME | LAST_FRAME | MOTION_REFERENCE | CAMERA_REFERENCE | ENVIRONMENT_REFERENCE | PROOF_EVIDENCE | SOURCE_CLIP"
      shot_number: "Shot 03"
      linked_proof_need_ids: []
      required_for_truth_gate: false
      preservation_locks:
        lock_identity: false
        lock_structure: false
        lock_motion: false
        lock_environment: false
        lock_text: false
  truth_dependency: "low | medium | high"
  hybrid_layers:
    real_layer:
      required: true
      description: ""
      reference_asset_ids: []
      carries_proof_need_ids: []
    ai_layer:
      required: true
      description: ""
      allowed_roles: ["environment", "atmosphere", "transition", "non_proof_hook"]
      prohibited_roles: ["core_product_proof", "before_after", "measurable_performance"]
    ai_must_not_rewrite:
      - "product_shape"
      - "logo"
      - "controls"
      - "accessory_set"
      - "proof_result"
  duration_seconds: 8
  aspect_ratio: "9:16"
  client_declared_facts:
    - client_fact_id: "cfact_..."
      fact_type: "sku | accessory | structure | function | compatibility | performance | safety | category | visual_identity"
      subject: ""
      value: {}
      source_ref_ids: []
  source_refs:
    - source_ref_id: "src_..."
      source_type: "USER_INPUT | UPLOADED_ASSET | PRODUCT_LINK | PRODUCT_SPEC_TEXT | PRIOR_SCRIPT | MANUAL_NOTE"
      source_value: ""
      asset_id: null
  proof_needs:
    - proof_need_id: "pneed_..."
      shot_id: "Shot 03"
      proof_type: "identity | structure | accessory | function | result | human_efficacy | safety | sterilization | compatibility | before_after | suction | dirt_intake | transparent_bin | pet_hair | gap_access | attachment_performance | measurable_performance"
      linked_client_fact_ids: []
      required_evidence_refs: []
      production_type: "AI_GENERATION | HYBRID"
      presentation_layer: "REAL_CAPTURE | AI_VISUALIZATION | AI_ENVIRONMENT | STOCK_CONTEXT | TEXT_CLAIM"
```

`PRODUCT_LINK` source refs are untrusted opaque metadata in Phase 2A. Backend
must not crawl, fetch, preview, download, validate, or scrape external URLs.

## 9. Request Integrity Rules

Request-local uniqueness:

- Every `client_fact_id` must be unique.
- Every `source_ref_id` must be unique.
- Every `proof_need_id` must be unique.

Linked id rules:

- Every linked id must exist.
- `proof_needs[].linked_client_fact_ids[]` must reference existing
  `client_declared_facts[].client_fact_id`.
- `reference_assets[].linked_proof_need_ids[]` must reference existing
  `proof_needs[].proof_need_id`.
- `hybrid_layers.real_layer.carries_proof_need_ids[]` must reference existing
  proof needs.
- `hybrid_layers.real_layer.reference_asset_ids[]` must reference existing
  `reference_assets[].asset_id`.
- `required_evidence_refs` must use deterministic prefixes: `src_` references
  `source_refs`; `asset_` references assets.

Cross-field rules:

- `reference_assets[].shot_number` must match request `shot_number`.
- `proof_needs[].production_type` must match request `production_type`.
- `HYBRID` requests must include `hybrid_layers`.
- `AI_GENERATION` requests must not include `hybrid_layers`.

Failures return HTTP 422 `SCHEMA_INVALID`.

## 10. Generation Mode Cross-validation

Allowed modes:

- `T2V`
- `I2V`
- `R2V`
- `FLF2V`

| Mode | Required Reference Assets | Invalid Cases |
| --- | --- | --- |
| `T2V` | No required assets. | Optional assets may not carry AI-owned proof. |
| `I2V` | At least one `FIRST_FRAME` or `PRODUCT_IDENTITY`. | No usable first-frame or product reference. |
| `R2V` | At least one reference asset of any allowed usage role. | Empty `reference_assets`. |
| `FLF2V` | Exactly one `FIRST_FRAME` and exactly one `LAST_FRAME`. | Missing either role or duplicate first/last frame. |

## 11. Truth And HYBRID Gates

Phase 2A Truth Enforcement is structural. It validates that the request contract
does not assign proof to forbidden layers and that required fields exist. It
does not verify media semantics.

Schema, Truth Gate, and HYBRID Gate failures return HTTP 422. State conflicts
and idempotency conflicts return HTTP 409.

Truth Gate blocks:

- `truth_dependency=high` with pure `AI_GENERATION`.
- AI as proof carrier for prohibited proof types.
- Proof-bearing asset reference missing, not owned by caller, or not `READY`.
- Client attempts to submit server-controlled fields.
- `selected_model` or `execution_provider` outside Phase 2A allowed values.

HYBRID Gate blocks:

- Missing `real_layer`.
- Missing `ai_layer`.
- Missing `ai_must_not_rewrite`.
- No real asset/reference for proof-bearing proof needs.
- AI layer allowed to rewrite a field linked to proof.

AI visualization is allowed only when it does not carry proof. AI proof is
blocked for suction, dirt intake, before/after, transparent bin, human efficacy,
sterilization, safety, and unverified accessory or structure proof.

## 12. Asset Flow

Asset states:

- `PENDING_UPLOAD`
- `READY`
- `FAILED`
- `EXPIRED`
- `DELETED`

Mock upload flow:

1. Client calls `POST /v1/assets/upload-url`.
2. Backend creates `Asset(status=PENDING_UPLOAD)`.
3. Backend returns an HTTP/HTTPS mock upload URL.
4. Internal client calls `PUT /_internal/mock-uploads/{token}`.
5. Upload validates content type, size, and checksum.
6. Success marks Asset `READY`.

Mock upload URL and idempotency TTL are both 24 hours.

Upload token:

```yaml
upload_token:
  route: "PUT /_internal/mock-uploads/{token}"
  bound_to: ["asset_id", "owner_id"]
  ttl_hours: 24
  one_time_use: true
  validates: ["content_type", "size_bytes", "checksum_sha256"]
```

Result token:

```yaml
result_token:
  route: "GET /_internal/mock-results/{token}"
  bound_to: ["asset_id", "owner_id"]
  ttl_hours: 24
  one_time_use: false
  requires_asset_status: "READY"
```

Result URLs must use tokens and must not expose only `asset_id`.

## 13. Job And Attempt States

Public Job states:

- `QUEUED`
- `PROCESSING`
- `SUCCEEDED`
- `FAILED`
- `CANCELLED`

Attempt states:

- `PREPARED`
- `SUBMITTED`
- `PROCESSING`
- `SUCCEEDED`
- `FAILED`
- `CANCEL_REQUESTED`
- `CANCELLED`
- `UNKNOWN_PROVIDER_STATE`

Job transitions:

| From | Event | To |
| --- | --- | --- |
| none | accepted create job | `QUEUED` |
| none | schema/truth/hybrid gate blocked | none |
| `QUEUED` | worker starts attempt | `PROCESSING` |
| `QUEUED` | cancel before provider submit | `CANCELLED` |
| `QUEUED` | preparation failure | `FAILED` |
| `PROCESSING` | current attempt succeeds | `SUCCEEDED` |
| `PROCESSING` | current attempt fails terminally | `FAILED` |
| `PROCESSING` | cancel completed | `CANCELLED` |
| `PROCESSING` | current attempt unknown | `PROCESSING` |
| `FAILED` | retry accepted | `QUEUED` |
| `CANCELLED` | retry accepted if policy allows | `QUEUED` |

Attempt transitions:

| From | Event | To | Notes |
| --- | --- | --- | --- |
| none | create attempt | `PREPARED` | Request mapped, not submitted. |
| `PREPARED` | cancel before provider submit | `CANCELLED` | No provider call occurred. |
| `PREPARED` | submit to mock provider | `SUBMITTED` | Provider submission record created first. |
| `SUBMITTED` | provider accepted | `PROCESSING` | Async work begins. |
| `SUBMITTED` | provider rejects | `FAILED` | Provider error mapped. |
| `SUBMITTED` | timeout after uncertain submit | `UNKNOWN_PROVIDER_STATE` | No blind duplicate submit. |
| `PROCESSING` | provider success | `SUCCEEDED` | Result media asset created. |
| `PROCESSING` | provider failure | `FAILED` | Terminal attempt failure. |
| `PROCESSING` | cancel requested | `CANCEL_REQUESTED` | Job remains `PROCESSING`. |
| `CANCEL_REQUESTED` | provider confirms cancel | `CANCELLED` | Job becomes `CANCELLED`. |
| `CANCEL_REQUESTED` | provider already succeeded | `SUCCEEDED` | Cancel lost race. |
| `CANCEL_REQUESTED` | provider unknown | `UNKNOWN_PROVIDER_STATE` | Reconciliation needed. |
| `UNKNOWN_PROVIDER_STATE` | cancel requested | `UNKNOWN_PROVIDER_STATE` | Save cancellation intent. |
| `UNKNOWN_PROVIDER_STATE` | reconcile success | `SUCCEEDED` | Result recovered. |
| `UNKNOWN_PROVIDER_STATE` | reconcile failure | `FAILED` | Error terminal. |
| `UNKNOWN_PROVIDER_STATE` | reconcile cancelled | `CANCELLED` | Cancel confirmed. |

Attempt-to-Job aggregation:

| Attempt | Job |
| --- | --- |
| `PREPARED` | `QUEUED` |
| `SUBMITTED` | `PROCESSING` |
| `PROCESSING` | `PROCESSING` |
| `SUCCEEDED` | `SUCCEEDED` |
| `FAILED` | `FAILED` |
| `CANCEL_REQUESTED` | `PROCESSING` |
| `CANCELLED` | `CANCELLED` |
| `UNKNOWN_PROVIDER_STATE` | `PROCESSING` |

When cancellation is requested while the current attempt is
`UNKNOWN_PROVIDER_STATE`, the attempt remains `UNKNOWN_PROVIDER_STATE`,
`cancellation_intent=true` and `cancel_requested_at` are saved, Job remains
`PROCESSING`, and blind resubmission is forbidden.

## 14. BackgroundTasks Mock Runner

```yaml
mock_provider_runner:
  runner: "FastAPI BackgroundTasks"
  default_outcome: "success"
  test_outcome_control: "dependency_injection_only"
  supported_test_outcomes: ["success", "failed", "unknown", "cancel"]
  clock: "Fake Clock"
  public_scenario_field: false
  celery: false
  redis: false
  external_queue: false
```

Rules:

- All runner state transitions must be legal and persisted.
- API polling is not required to observe every short-lived intermediate state.
- State-machine unit tests verify transitions through Runner and Repository,
  not only through polling.
- Public API requests must not contain scenario or outcome fields.
- Tests choose failed, unknown, or cancel behavior through dependency
  injection.
- On startup, any non-terminal mock attempt left by a prior process is marked
  `FAILED` with failure reason `MOCK_RUNNER_INTERRUPTED`.
- `MOCK_RUNNER_INTERRUPTED` is a Job/Attempt failure reason. `GET /v1/video-jobs/{job_id}`
  still returns HTTP 200 with Job status `FAILED`; it is not a GET Job HTTP 500.

## 15. AI Review Status

Phase 2A create job always initializes:

```yaml
ai_review_status: "NOT_RUN"
```

Generation `SUCCEEDED` means result media exists. It does not mean Knowledge 10
has passed. Review submission is outside Phase 2A public Action schema.

## 16. Idempotency

Side-effect endpoints require `Idempotency-Key`:

- `POST /v1/assets/upload-url`
- `POST /v1/video-jobs`
- `POST /v1/video-jobs/{job_id}/cancel`
- `POST /v1/video-jobs/{job_id}/retry`

TTL and lease:

```yaml
idempotency:
  completed_ttl_hours: 24
  pending_lease_seconds: 60
```

Missing key returns HTTP 422 `IDEMPOTENCY_KEY_REQUIRED`.

Canonical request hash rules:

- Parse JSON body before hashing.
- Reject invalid JSON before idempotency completion.
- Use UTF-8.
- Recursively sort object keys lexicographically.
- Remove insignificant whitespace.
- Preserve array order.
- Preserve strings exactly after JSON decoding.
- Represent integers as JSON numbers.
- Reject non-finite numbers.
- Include HTTP method, route template, path parameters, server-mapped owner id,
  and request body.
- Exclude `Idempotency-Key` from the canonical body hash but include it in the
  idempotency lookup scope.

Unique constraint:

```yaml
unique_constraint:
  table: "idempotency_records"
  columns:
    - owner_id
    - http_method
    - route_template
    - path_params_hash
    - idempotency_key_hash
```

States:

- `PENDING`
- `COMPLETED`

Concurrent behavior:

- First request inserts `PENDING` in the transaction that starts side effects.
- Concurrent same-key request during active lease returns HTTP 409
  `IDEMPOTENCY_PENDING`.
- Same key with different canonical hash returns HTTP 409
  `IDEMPOTENCY_CONFLICT`.
- Expired `PENDING` with same canonical hash may be taken over after checking
  for already-created resources.
- If a related asset, job, cancel intent, or retry attempt already exists,
  complete the idempotency record from that resource rather than duplicating
  side effects.
- Successful or deterministic replay responses include
  `idempotent_replay=false` on first completion and `true` on replay.

Do not cache state-volatile errors:

- `IDEMPOTENCY_PENDING`
- `INTERNAL_ERROR`
- provider transient errors
- errors whose truth can change without payload changes

Cache deterministic post-auth validation responses, including create-job 422
schema/truth/hybrid failures.

## 17. Response Models And Error Envelope

```yaml
attempt_summary:
  attempt_id: "attempt_..."
  attempt_no: 1
  attempt_status: "PREPARED | SUBMITTED | PROCESSING | SUCCEEDED | FAILED | CANCEL_REQUESTED | CANCELLED | UNKNOWN_PROVIDER_STATE"
  execution_provider: "mock"
  provider_job_id: null
  cancellation_intent: false
  cancel_requested_at: null
  failure_reason: null
  created_at: ""
  updated_at: ""
```

```yaml
asset_summary:
  asset_id: "asset_..."
  asset_kind: "INPUT_MEDIA | RESULT_MEDIA"
  usage_role: "PRODUCT_IDENTITY | FIRST_FRAME | LAST_FRAME | MOTION_REFERENCE | CAMERA_REFERENCE | ENVIRONMENT_REFERENCE | PROOF_EVIDENCE | SOURCE_CLIP | RESULT_MEDIA"
  asset_status: "PENDING_UPLOAD | READY | FAILED | EXPIRED | DELETED"
  content_type: ""
  size_bytes: 0
  checksum_sha256: ""
```

```yaml
result_media_summary:
  asset_id: "asset_..."
  content_type: "video/mp4"
  size_bytes: 0
  checksum_sha256: ""
  secure_url: "https://backend.local/_internal/mock-results/{token}"
  url_expires_at: ""
```

```yaml
stored_job_error:
  code: ""
  message: ""
  field: ""
  retryable: false
  details: {}
  created_at: ""
```

```yaml
error_response:
  error:
    code: ""
    message: ""
    field: ""
    required_action: ""
    request_id: ""
    retryable: false
    details: {}
```

All non-2xx API errors return the unified `error_response` envelope.

## 18. Public API Contract

### GET /health

Response 200:

```yaml
status: "ok"
service: "video-generation-backend"
contract_version: "v1"
```

Errors: `INTERNAL_ERROR`.

Idempotency: none.

### POST /v1/assets/upload-url

Request:

```yaml
contract_version: "v1"
content_type: "image/png | image/jpeg | video/mp4"
size_bytes: 0
checksum_sha256: ""
intended_usage_role: "PRODUCT_IDENTITY | FIRST_FRAME | LAST_FRAME | MOTION_REFERENCE | CAMERA_REFERENCE | ENVIRONMENT_REFERENCE | PROOF_EVIDENCE | SOURCE_CLIP"
```

Response 201:

```yaml
asset_id: "asset_..."
asset_status: "PENDING_UPLOAD"
upload_url: "https://backend.local/_internal/mock-uploads/{token}"
upload_url_expires_at: ""
idempotent_replay: false
```

Statuses: 201, 401, 409, 413, 415, 422, 500.

### POST /v1/video-jobs

Request: see Section 8.

Response 202:

```yaml
job_id: "job_..."
generation_status: "QUEUED"
ai_review_status: "NOT_RUN"
execution_provider: "mock"
contract_version: "v1"
truth_rule_version: "truth-rules-v0.4"
provider_mapping_version: "mock-provider-map-v0.4"
idempotent_replay: false
```

Statuses: 202, 401, 409, 422, 500.

### GET /v1/video-jobs/{job_id}

Response 200:

```yaml
job_id: "job_..."
generation_status: "QUEUED | PROCESSING | SUCCEEDED | FAILED | CANCELLED"
ai_review_status: "NOT_RUN"
current_attempt: "attempt_summary"
assets: ["asset_summary"]
result_media: ["result_media_summary"]
errors: ["stored_job_error"]
```

Statuses: 200, 401, 404, 500.

If the job failed because a previous mock runner was interrupted, this endpoint
still returns 200 with `generation_status=FAILED`.

### POST /v1/video-jobs/{job_id}/cancel

Response 200 or 202:

```yaml
job_id: "job_..."
generation_status: "CANCELLED | PROCESSING"
attempt_status: "CANCEL_REQUESTED | CANCELLED | UNKNOWN_PROVIDER_STATE"
cancellation_intent: false
cancel_requested_at: null
idempotent_replay: false
```

Statuses: 200, 202, 401, 404, 409, 422, 500.

### POST /v1/video-jobs/{job_id}/retry

Response 202:

```yaml
job_id: "job_..."
generation_status: "QUEUED"
new_attempt_id: "attempt_..."
idempotent_replay: false
```

Statuses: 202, 401, 404, 409, 422, 500.

## 18. Internal Route Contract

### PUT /_internal/mock-uploads/{token}

Purpose: local/test upload completion. Validates token, owner/asset binding,
expiry, content type, size, and checksum. Success marks Asset `READY`.

Errors:

- `UPLOAD_TOKEN_INVALID`
- `UPLOAD_TOKEN_EXPIRED`
- `UPLOAD_ALREADY_COMPLETED`
- `CHECKSUM_MISMATCH`
- `ASSET_INVALID_STATE`

### GET /_internal/mock-results/{token}

Purpose: local/test mock result retrieval. Validates token, owner/asset binding,
expiry, and result readiness.

Errors:

- `RESULT_TOKEN_INVALID`
- `RESULT_URL_EXPIRED`
- `RESULT_NOT_READY`

These routes are not public Action endpoints.

## 19. Core Operation Sequences

Upload URL:

1. Authenticate and map owner.
2. Require idempotency key.
3. Validate schema, content type, size.
4. Insert/inspect idempotency record.
5. Create Asset `PENDING_UPLOAD`.
6. Store response and complete idempotency record.
7. Return 201.

Create Job:

1. Authenticate and map owner.
2. Require idempotency key.
3. Canonicalize path/body.
4. Insert/inspect idempotency record.
5. Validate schema, versions, request-local ids, references, assets, modes.
6. Run Truth Gate and HYBRID Gate.
7. Insert snapshot, job, attempt, asset references.
8. Store response and complete idempotency record.
9. Return 202.

Cancel:

1. Authenticate and map owner.
2. Require idempotency key.
3. Load job and current attempt.
4. Apply cancel policy.
5. Persist legal transition or cancellation intent.
6. Store response and complete idempotency record.
7. Return 200 or 202.

Retry:

1. Authenticate and map owner.
2. Require idempotency key.
3. Load job, current attempt, and accepted snapshot.
4. Reject unresolved unknown provider state.
5. Create new Attempt `PREPARED`.
6. Move Job to `QUEUED`.
7. Store response and complete idempotency record.
8. Return 202.

## 20. Error Registry

| Code | HTTP | Meaning |
| --- | --- | --- |
| `AUTH_REQUIRED` | 401 | Missing auth. |
| `AUTH_INVALID` | 401 | Invalid Bearer API key. |
| `OWNER_MISMATCH` | 404 | Resource not visible to owner. |
| `SCHEMA_INVALID` | 422 | Request shape, enum, or integrity invalid. |
| `VERSION_CONFLICT` | 409 | Expected truth rule version mismatch. |
| `ASSET_NOT_FOUND` | 422 | Referenced asset does not exist for owner. |
| `ASSET_NOT_READY` | 422 | Referenced asset is not `READY`. |
| `ASSET_INVALID_STATE` | 422 | Asset state cannot be used for operation. |
| `ASSET_TYPE_UNSUPPORTED` | 415 | Unsupported upload content type. |
| `ASSET_TOO_LARGE` | 413 | Upload size exceeds limit. |
| `TRUTH_GATE_BLOCKED` | 422 | Structural Truth Gate blocked request. |
| `HYBRID_GATE_BLOCKED` | 422 | HYBRID layer policy invalid. |
| `AI_PROOF_NOT_ALLOWED` | 422 | AI assigned prohibited proof role. |
| `PROVIDER_UNSUPPORTED` | 422 | Provider/model combination unsupported. |
| `IDEMPOTENCY_KEY_REQUIRED` | 422 | Missing idempotency key. |
| `IDEMPOTENCY_CONFLICT` | 409 | Same key, different canonical request. |
| `IDEMPOTENCY_PENDING` | 409 | Same key request still pending. |
| `JOB_NOT_FOUND` | 404 | Job not found for owner. |
| `JOB_INVALID_STATE` | 409 | Operation invalid for current state. |
| `JOB_CANCEL_NOT_ALLOWED` | 409 | Job cannot be cancelled. |
| `JOB_NOT_RETRYABLE` | 409 | Job cannot be retried. |
| `UNKNOWN_PROVIDER_STATE` | 409 | Retry blocked by unresolved provider ambiguity. |
| `UPLOAD_TOKEN_INVALID` | 404 | Upload token invalid. |
| `UPLOAD_TOKEN_EXPIRED` | 410 | Upload token expired. |
| `UPLOAD_ALREADY_COMPLETED` | 409 | Upload already completed. |
| `CHECKSUM_MISMATCH` | 422 | Uploaded bytes do not match checksum. |
| `RESULT_TOKEN_INVALID` | 404 | Result token invalid. |
| `RESULT_URL_EXPIRED` | 410 | Result URL token expired. |
| `RESULT_NOT_READY` | 409 | Result Asset is not ready. |
| `MOCK_RUNNER_INTERRUPTED` | n/a | Stored Job/Attempt failure reason, not GET Job HTTP 500. |
| `INTERNAL_ERROR` | 500 | Unexpected server error. |

## 21. Decisions Approved For Phase 2A

- API base path: `/v1/video-jobs`.
- Persistence: SQLite + SQLAlchemy 2.x + Alembic.
- Public Job states: `QUEUED`, `PROCESSING`, `SUCCEEDED`, `FAILED`,
  `CANCELLED`.
- Attempt states: `PREPARED`, `SUBMITTED`, `PROCESSING`, `SUCCEEDED`,
  `FAILED`, `CANCEL_REQUESTED`, `CANCELLED`, `UNKNOWN_PROVIDER_STATE`.
- Single-tenant Bearer API key and server-side owner mapping.
- No public asset complete endpoint in default Action schema.
- Six public interfaces are the complete Phase 2A Action surface.
- Internal mock routes are excluded from Action schema.
- Only `selected_model=Seedance` and `execution_provider=mock`.
- Only generation modes `T2V`, `I2V`, `R2V`, `FLF2V`.
- Minimal persistence tables listed in Section 6.
- Snapshot JSON storage for client facts, source refs, proof needs, and gate
  results.
- FastAPI BackgroundTasks mock runner with dependency-injected test outcomes.
- Idempotency completed TTL 24 hours and pending lease 60 seconds.
- Tokenized HTTP/HTTPS mock upload and result URLs.

## 22. Remaining Future Decisions

Not blockers for Phase 2A:

- Direct Custom GPT binary attachment support.
- Real Seedance API fields, callbacks, cancellation, and cost model.
- Real cost confirmation endpoint.
- Knowledge 10 review submission endpoint.
- Production object storage.
- Multi-tenant auth.
- Dedicated tables for facts, verification, and review.
