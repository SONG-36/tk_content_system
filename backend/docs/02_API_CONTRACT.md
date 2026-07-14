# API Contract

## Authority

`backend/docs/BACKEND_MASTER_DESIGN.md` is authoritative. This document mirrors
the approved Phase 2A API contract for implementation convenience. Any conflict
is resolved in favor of the Master Design.

## Public Action Endpoints

These six endpoints are the complete Phase 2A public Custom GPT Action surface:

- `GET /health`
- `POST /v1/assets/upload-url`
- `POST /v1/video-jobs`
- `GET /v1/video-jobs/{job_id}`
- `POST /v1/video-jobs/{job_id}/cancel`
- `POST /v1/video-jobs/{job_id}/retry`

## Internal Mock Routes

These routes are internal only and must not be included in the Custom GPT Action
OpenAPI schema:

- `PUT /_internal/mock-uploads/{token}`
- `GET /_internal/mock-results/{token}`

## Shared Versions And Enums

```yaml
contract_version: "v1"
truth_rule_version: "truth-rules-v0.4"
provider_mapping_version: "mock-provider-map-v0.4"
selected_model: "Seedance"
execution_provider: "mock"
generation_mode: "T2V | I2V | R2V | FLF2V"
production_type: "AI_GENERATION | HYBRID"
generation_status: "QUEUED | PROCESSING | SUCCEEDED | FAILED | CANCELLED"
attempt_status: "PREPARED | SUBMITTED | PROCESSING | SUCCEEDED | FAILED | CANCEL_REQUESTED | CANCELLED | UNKNOWN_PROVIDER_STATE"
ai_review_status: "NOT_RUN"
asset_status: "PENDING_UPLOAD | READY | FAILED | EXPIRED | DELETED"
```

## Authentication And Headers

Bearer Auth is required for every public endpoint except `GET /health`.

```http
Authorization: Bearer <api-key>
```

`Idempotency-Key` is required for every side-effect endpoint:

- `POST /v1/assets/upload-url`
- `POST /v1/video-jobs`
- `POST /v1/video-jobs/{job_id}/cancel`
- `POST /v1/video-jobs/{job_id}/retry`

```http
Idempotency-Key: <stable-client-key>
```

## Nested Objects

```yaml
reference_asset:
  asset_id: "asset_..."
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
```

```yaml
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
  ai_must_not_rewrite: []
```

```yaml
client_declared_fact:
  client_fact_id: "cfact_..."
  fact_type: "sku | accessory | structure | function | compatibility | performance | safety | category | visual_identity"
  subject: ""
  value: {}
  source_ref_ids: []
```

```yaml
source_ref:
  source_ref_id: "src_..."
  source_type: "USER_INPUT | UPLOADED_ASSET | PRODUCT_LINK | PRODUCT_SPEC_TEXT | PRIOR_SCRIPT | MANUAL_NOTE"
  source_value: ""
  asset_id: null
```

```yaml
proof_need:
  proof_need_id: "pneed_..."
  shot_id: "Shot 03"
  proof_type: "identity | structure | accessory | function | result | human_efficacy | safety | sterilization | compatibility | before_after | suction | dirt_intake | transparent_bin | pet_hair | gap_access | attachment_performance | measurable_performance"
  linked_client_fact_ids: []
  required_evidence_refs: []
  production_type: "AI_GENERATION | HYBRID"
  presentation_layer: "REAL_CAPTURE | AI_VISUALIZATION | AI_ENVIRONMENT | STOCK_CONTEXT | TEXT_CLAIM"
```

## Response Models

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

All interface errors use `error_response`.

## GET /health

Response 200:

```yaml
status: "ok"
service: "video-generation-backend"
contract_version: "v1"
```

Status codes: 200, 500.

Errors: `INTERNAL_ERROR`.

Error response: `error_response`.

Idempotency: not required.

## POST /v1/assets/upload-url

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

Status codes: 201, 401, 409, 413, 415, 422, 500.

Errors: `AUTH_REQUIRED`, `AUTH_INVALID`, `SCHEMA_INVALID`,
`ASSET_TYPE_UNSUPPORTED`, `ASSET_TOO_LARGE`, `IDEMPOTENCY_KEY_REQUIRED`,
`IDEMPOTENCY_CONFLICT`, `IDEMPOTENCY_PENDING`, `INTERNAL_ERROR`.

Error response: `error_response`.

Idempotency: required. Completed TTL 24 hours. Pending lease 60 seconds.

## POST /v1/video-jobs

Request:

```yaml
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
reference_assets: []
truth_dependency: "low | medium | high"
hybrid_layers: null
duration_seconds: 8
aspect_ratio: "9:16"
client_declared_facts: []
source_refs: []
proof_needs: []
```

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

Status codes: 202, 401, 409, 422, 500.

Errors: `AUTH_REQUIRED`, `AUTH_INVALID`, `SCHEMA_INVALID`,
`VERSION_CONFLICT`, `ASSET_NOT_FOUND`, `ASSET_NOT_READY`,
`ASSET_INVALID_STATE`, `TRUTH_GATE_BLOCKED`, `HYBRID_GATE_BLOCKED`,
`AI_PROOF_NOT_ALLOWED`, `PROVIDER_UNSUPPORTED`,
`IDEMPOTENCY_KEY_REQUIRED`, `IDEMPOTENCY_CONFLICT`,
`IDEMPOTENCY_PENDING`, `INTERNAL_ERROR`.

Error response: `error_response`.

Idempotency: required. Deterministic 422 gate responses are cached.

## GET /v1/video-jobs/{job_id}

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

Status codes: 200, 401, 404, 500.

Errors: `AUTH_REQUIRED`, `AUTH_INVALID`, `JOB_NOT_FOUND`, `OWNER_MISMATCH`,
`INTERNAL_ERROR`.

Error response: `error_response`.

Idempotency: not required.

`MOCK_RUNNER_INTERRUPTED` is returned as a stored failure reason on a failed
job/attempt, not as HTTP 500 for this endpoint.

## POST /v1/video-jobs/{job_id}/cancel

Request:

```yaml
reason: ""
```

Response 200 or 202:

```yaml
job_id: "job_..."
generation_status: "CANCELLED | PROCESSING"
attempt_status: "CANCEL_REQUESTED | CANCELLED | UNKNOWN_PROVIDER_STATE"
cancellation_intent: false
cancel_requested_at: null
idempotent_replay: false
```

Status codes: 200, 202, 401, 404, 409, 422, 500.

Errors: `AUTH_REQUIRED`, `AUTH_INVALID`, `SCHEMA_INVALID`, `JOB_NOT_FOUND`,
`JOB_CANCEL_NOT_ALLOWED`, `JOB_INVALID_STATE`, `IDEMPOTENCY_KEY_REQUIRED`,
`IDEMPOTENCY_CONFLICT`, `IDEMPOTENCY_PENDING`, `INTERNAL_ERROR`.

Error response: `error_response`.

Idempotency: required.

## POST /v1/video-jobs/{job_id}/retry

Request:

```yaml
reason: ""
```

Response 202:

```yaml
job_id: "job_..."
generation_status: "QUEUED"
new_attempt_id: "attempt_..."
idempotent_replay: false
```

Status codes: 202, 401, 404, 409, 422, 500.

Errors: `AUTH_REQUIRED`, `AUTH_INVALID`, `SCHEMA_INVALID`, `JOB_NOT_FOUND`,
`JOB_NOT_RETRYABLE`, `JOB_INVALID_STATE`, `UNKNOWN_PROVIDER_STATE`,
`IDEMPOTENCY_KEY_REQUIRED`, `IDEMPOTENCY_CONFLICT`,
`IDEMPOTENCY_PENDING`, `INTERNAL_ERROR`.

Error response: `error_response`.

Idempotency: required.

## Internal Mock Route Errors

- `UPLOAD_TOKEN_INVALID`
- `UPLOAD_TOKEN_EXPIRED`
- `UPLOAD_ALREADY_COMPLETED`
- `CHECKSUM_MISMATCH`
- `RESULT_TOKEN_INVALID`
- `RESULT_URL_EXPIRED`
- `RESULT_NOT_READY`

## Idempotency Rules

- `Idempotency-Key` is required for upload URL, create job, cancel, and retry.
- Completed idempotency records expire after 24 hours.
- Pending leases expire after 60 seconds.
- Same key plus same canonical request returns stored response with
  `idempotent_replay=true`.
- Same key plus different canonical request returns 409
  `IDEMPOTENCY_CONFLICT`.
- Active pending same-key request returns 409 `IDEMPOTENCY_PENDING`.
- Canonical request includes method, route template, path parameters,
  server-mapped owner id, and normalized JSON body.
