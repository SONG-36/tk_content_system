# Backend Master Design Draft v0.4

## 1. Document Status

```yaml
document_status:
  document_version: "v0.4"
  status: "DRAFT"
  supersedes_for_review: "backend/docs/BACKEND_MASTER_DESIGN_DRAFT_v0.3.md"
  overwrites_v0_3: false
  implementation_code_created: false
  approval_required_before_coding: true
  handoff_read: true
  handoff_path: "backend/docs/reference/VIDEO_GENERATION_BACKEND_HANDOFF.md"
```

This document is a close-out revision of v0.3. It does not modify v0.1, v0.2,
v0.3, backend docs 00-04, frozen Custom GPT files, Knowledge 01-18, or Skills.
It remains a draft until final approval.

## 2. Authoritative Sources

### Runtime Authoritative

- `custom_gpt_package/multi_category_gpt/00_INSTRUCTIONS/MAIN_INSTRUCTIONS.md`
- `custom_gpt_package/multi_category_gpt/01_KNOWLEDGE_UPLOAD/01-18_*.md`

Runtime authoritative files define Custom GPT behavior. Backend runtime must not
parse them.

### Backend Scope Authoritative

- `AGENTS.md`
- `backend/AGENTS.md`
- `backend/docs/reference/VIDEO_GENERATION_BACKEND_HANDOFF.md`

The handoff file defines the Phase 2A target: FastAPI backend, mock first, six
public endpoints, Truth Gate, HYBRID Gate, idempotency, asset flow, status
polling, cancel/retry, and no real Seedance connection.

### Design Reference

- `backend/docs/BACKEND_MASTER_DESIGN_DRAFT_v0.1.md`
- `backend/docs/BACKEND_MASTER_DESIGN_DRAFT_v0.2.md`
- `backend/docs/BACKEND_MASTER_DESIGN_DRAFT_v0.3.md`
- `backend/docs/00_SCOPE_AND_BOUNDARIES.md`
- `backend/docs/01_BACKEND_ARCHITECTURE.md`
- `backend/docs/02_API_CONTRACT_DRAFT.md`
- `backend/docs/03_EXISTING_SYSTEM_MAPPING.md`
- `backend/docs/04_PHASE_2A_IMPLEMENTATION_PLAN.md`
- `README.md`
- `master_design.md`
- `categories/**`
- `core/**`
- `instructions/**`
- `knowledge/**`
- `workflows/**`

### Third-party / Non-authoritative

- `seedance_skills/**`
- `custom_gpt_package/multi_category_gpt/02_SOURCE_FILES/seedance_skills/**`
- `source/open_source/**`

These files are not backend API contracts, provider schemas, or runtime policy.

## 3. Phase 2A Scope

Phase 2A creates a mock FastAPI backend with:

- Six public Custom GPT Action endpoints.
- Two internal-only mock routes excluded from Action OpenAPI.
- SQLite + SQLAlchemy 2.x + Alembic.
- Single-tenant Bearer API key.
- Structural Truth Gate and HYBRID Gate.
- Mock asset upload flow.
- Mock provider only.
- Idempotency for upload URL, create job, cancel, and retry.
- Public Job state, Attempt state, and AI review status separation.

Phase 2A must not:

- Connect to real Seedance.
- Execute real provider cost-bearing work.
- Claim semantic media truth verification.
- Put mock scenario controls into public Action schema.
- Let clients control backend verification, trust, state, or mapping fields.
- Access external URLs from `SourceRef`.
- Modify frozen Custom GPT files.

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
- `GET /_internal/mock-results/{asset_id}`

Internal routes are for tests and local development only. They must not be
included in the Custom GPT Action OpenAPI schema.

## 5. Layer Separation

### API Client Input

Client-controlled concepts:

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

The client does not submit a separate proof-owner field. Proof ownership is
expressed through `proof_needs`, `hybrid_layers`, and `reference_assets`.

Disallowed client-controlled fields:

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

### Domain Model

- `Asset`
- `JobAssetReference`
- `VideoJob`
- `JobAttempt`
- `ClientDeclaredFact`
- `SourceRef`
- `ProofNeed`
- `BackendFact`
- `VerificationRecord`
- `TruthGateDecision`
- `HybridGateDecision`
- `ProviderSubmission`
- `ProviderResult`
- `ReviewResult`
- `IdempotencyRecord`
- `ErrorRecord`

### Persistence Model

- `assets`
- `job_asset_references`
- `video_jobs`
- `job_attempts`
- `generation_request_snapshots`
- `client_declared_facts`
- `source_refs`
- `proof_needs`
- `backend_facts`
- `verification_records`
- `truth_gate_decisions`
- `hybrid_gate_decisions`
- `provider_submissions`
- `provider_results`
- `review_results`
- `idempotency_records`
- `error_records`

API compatibility is governed by `contract_version`. Database evolution is
governed by Alembic migrations.

## 6. Version Control Fields

Client submits:

```yaml
contract_version: "v1"
expected_truth_rule_version: "truth-rules-v0.4" # optional compatibility check only
```

Server controls:

```yaml
truth_rule_version: "truth-rules-v0.4"
provider_mapping_version: "mock-provider-map-v0.4"
```

Rules:

- Client must not submit `truth_rule_version`.
- Client must not submit `provider_mapping_version`.
- `expected_truth_rule_version` is optional and can only request a compatibility
  check.
- A mismatch returns HTTP 409 `VERSION_CONFLICT`.
- Accepted job snapshots store server-controlled versions.

## 7. SourceRef Policy

`SourceRef` captures opaque metadata only in Phase 2A.

```yaml
source_ref:
  source_ref_id: "src_..."
  source_type: "USER_INPUT | UPLOADED_ASSET | PRODUCT_LINK | PRODUCT_SPEC_TEXT | PRIOR_SCRIPT | MANUAL_NOTE"
  source_value: ""
  asset_id: null
```

Rules:

- `PRODUCT_LINK` is not fetched by the backend in Phase 2A.
- External URLs are stored as untrusted opaque metadata.
- Backend must not crawl, download, scrape, preview, or validate external URL
  content in Phase 2A.
- URL-based trust or verification is future scope.

## 8. Client Fact And Proof Input

Custom GPT is not a product Fact verifier. It may declare facts, proof needs,
source refs, and production plan boundaries.

```yaml
client_declared_fact:
  client_fact_id: "cfact_..."
  fact_type: "sku | accessory | structure | function | compatibility | performance | safety | category | visual_identity"
  subject: ""
  value: {}
  source_ref_ids: []
  declared_by: "custom_gpt"
```

```yaml
proof_need:
  proof_need_id: "pneed_..."
  shot_id: "shot_..."
  proof_type: "identity | structure | accessory | function | result | human_efficacy | safety | sterilization | compatibility | before_after | suction | dirt_intake | transparent_bin | pet_hair | gap_access | attachment_performance | measurable_performance"
  linked_client_fact_ids: []
  required_evidence_refs: []
  production_type: "REAL_SHOOT | AI_GENERATION | HYBRID | STOCK_ASSET"
  presentation_layer: "REAL_CAPTURE | AI_VISUALIZATION | AI_ENVIRONMENT | STOCK_CONTEXT | TEXT_CLAIM"
```

The backend derives gate decisions from structure. It does not verify media
semantics in Phase 2A.

## 9. Proof Evaluation

```yaml
proof_need_evaluation:
  proof_need_id: "pneed_..."
  presentation_layer: "REAL_CAPTURE | AI_VISUALIZATION | AI_ENVIRONMENT | STOCK_CONTEXT | TEXT_CLAIM"
  proof_carrier: "REAL_CAPTURE | VERIFIED_BACKEND_FACT | CONTROLLED_TEST | NONE"
  verification_method: "NONE | STRUCTURAL_CONTRACT_CHECK | ASSET_METADATA_CHECK | HUMAN_REVIEW_REQUIRED | CONTROLLED_TEST_REQUIRED | FUTURE_SEMANTIC_REVIEW"
  evidence_refs:
    source_ref_ids: []
    asset_ids: []
    verification_record_ids: []
  backend_verification_status: "NOT_VERIFIED | STRUCTURALLY_ACCEPTED | NEEDS_HUMAN_REVIEW | VERIFIED_BY_APPROVED_RECORD | REJECTED"
  backend_gate_result: "ALLOW | WARN | BLOCK"
```

Client may submit production intent. Backend determines proof carrier,
verification method, backend verification status, and gate result.

## 10. AI Visualization Versus AI Proof

AI visualization means AI renders or enhances a bounded visual layer. AI proof
means AI output is asked to prove a product fact, result, function, or safety
claim.

Allowed structurally:

- AI environment or atmosphere for non-proof Hook.
- AI visualization of a reference when the request does not ask AI to prove the
  referenced fact.
- HYBRID when real layer carries proof and AI layer cannot rewrite proof facts.

Blocked structurally:

- Pure AI carrying high-truth proof.
- AI suction proof.
- AI dirt-intake proof.
- AI cleaning Before/After.
- AI transparent-bin proof.
- AI beauty or grooming efficacy proof.
- AI sterilization or safety proof.
- AI proof of unverified accessory or structure.

Compatibility, identity, and structure are blocked only when AI/provider output
is asked to invent, rewrite, or prove them without acceptable real source refs
and preservation locks.

## 11. Create Job Schema Concept

Phase 2A public Action limits:

```yaml
selected_model:
  allowed: ["Seedance"]
execution_provider:
  allowed: ["mock"]
generation_mode:
  allowed: ["T2V", "I2V", "R2V", "FLF2V"]
```

Modes without a complete Phase 2A contract are not included.

```yaml
create_video_job_request:
  contract_version: "v1"
  expected_truth_rule_version: "truth-rules-v0.4" # optional
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
      production_type: "REAL_SHOOT | AI_GENERATION | HYBRID | STOCK_ASSET"
      presentation_layer: "REAL_CAPTURE | AI_VISUALIZATION | AI_ENVIRONMENT | STOCK_CONTEXT | TEXT_CLAIM"
```

## 12. Structural Truth And HYBRID Gates

Phase 2A Truth Enforcement is structural. It validates that the request
contract does not assign proof to forbidden layers and that required fields
exist.

Schema, Truth Gate, and HYBRID Gate failures all return HTTP 422.

Status conflicts and idempotency conflicts return HTTP 409.

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
- No real asset/reference for proof-bearing `proof_needs`.
- AI layer allowed to rewrite a field linked to proof.

Phase 2A cannot claim uploaded media semantically proves suction, structure,
result, safety, or any other product truth.

## 13. Asset Flow

Phase 2A Mock Asset Flow:

1. Client calls `POST /v1/assets/upload-url`.
2. Backend creates `Asset(status=PENDING_UPLOAD)`.
3. Backend returns `asset_id` and an HTTP/HTTPS mock upload URL.
4. Test harness or internal developer tool performs
   `PUT /_internal/mock-uploads/{token}`.
5. Upload success marks `Asset(status=READY)`.
6. Client creates a video job referencing `READY` asset ids.

Internal result route:

- `GET /_internal/mock-results/{asset_id}`

This route returns mock result bytes or metadata for tests/local development and
does not enter the Custom GPT Action OpenAPI.

Upload URL TTL:

```yaml
mock_upload_url_ttl_hours: 24
upload_url_idempotency_ttl_hours: 24
```

Mock upload URL expiry does not automatically expire the Asset.

Asset states:

- `PENDING_UPLOAD`
- `READY`
- `FAILED`
- `EXPIRED`
- `DELETED`

## 14. Job State Transition Table

Public Job states:

- `QUEUED`
- `PROCESSING`
- `SUCCEEDED`
- `FAILED`
- `CANCELLED`

| From | Event | To | Allowed | Notes |
| --- | --- | --- | --- | --- |
| none | accepted create job | `QUEUED` | yes | Only after all pre-create gates pass. |
| none | schema/truth/hybrid gate blocked | none | yes | Return deterministic 422; no `VideoJob`. |
| `QUEUED` | worker starts attempt | `PROCESSING` | yes | Current attempt moves from `PREPARED` to submit path. |
| `QUEUED` | cancel accepted before provider submit | `CANCELLED` | yes | Attempt can move `PREPARED -> CANCELLED`. |
| `QUEUED` | preparation failure | `FAILED` | yes | Error stored. |
| `PROCESSING` | current attempt succeeds | `SUCCEEDED` | yes | Does not imply AI review `PASS`. |
| `PROCESSING` | current attempt fails terminally | `FAILED` | yes | Error stored. |
| `PROCESSING` | cancel completed | `CANCELLED` | yes | Provider cancel may be best effort later. |
| `PROCESSING` | current attempt unknown | `PROCESSING` | yes | Attempt holds `UNKNOWN_PROVIDER_STATE`. |
| `FAILED` | retry accepted | `QUEUED` | yes | Same job, new attempt, unchanged snapshot. |
| `CANCELLED` | retry accepted | `QUEUED` | conditional | Only if retry policy allows. |
| `SUCCEEDED` | retry | none | no | Regeneration with changes creates a new job. |
| `FAILED` | direct processing | none | no | Must go through retry endpoint. |
| `CANCELLED` | direct processing | none | no | Must go through retry if allowed. |

## 15. Attempt State Transition Table

Attempt states:

- `PREPARED`
- `SUBMITTED`
- `PROCESSING`
- `SUCCEEDED`
- `FAILED`
- `CANCEL_REQUESTED`
- `CANCELLED`
- `UNKNOWN_PROVIDER_STATE`

| From | Event | To | Allowed | Notes |
| --- | --- | --- | --- | --- |
| none | create attempt | `PREPARED` | yes | Request mapped but not submitted. |
| `PREPARED` | cancel before provider submit | `CANCELLED` | yes | No provider call occurred. |
| `PREPARED` | submit to mock provider | `SUBMITTED` | yes | Provider submission record created first. |
| `SUBMITTED` | provider accepted | `PROCESSING` | yes | Async work begins. |
| `SUBMITTED` | provider rejects | `FAILED` | yes | Store mapped provider error. |
| `SUBMITTED` | timeout after uncertain submit | `UNKNOWN_PROVIDER_STATE` | yes | No blind duplicate submit. |
| `PROCESSING` | provider success | `SUCCEEDED` | yes | Result media asset created. |
| `PROCESSING` | provider failure | `FAILED` | yes | Terminal attempt failure. |
| `PROCESSING` | cancel requested | `CANCEL_REQUESTED` | yes | Public job may remain `PROCESSING`. |
| `CANCEL_REQUESTED` | provider confirms cancel | `CANCELLED` | yes | Public job becomes `CANCELLED`. |
| `CANCEL_REQUESTED` | provider already succeeded | `SUCCEEDED` | yes | Cancel lost race; result retained. |
| `CANCEL_REQUESTED` | provider unknown | `UNKNOWN_PROVIDER_STATE` | yes | Requires reconciliation. |
| `UNKNOWN_PROVIDER_STATE` | cancel requested | `UNKNOWN_PROVIDER_STATE` | yes | Save `cancellation_intent=true` and `cancel_requested_at`; Job stays `PROCESSING`; no blind resubmit. |
| `UNKNOWN_PROVIDER_STATE` | reconcile success | `SUCCEEDED` | yes | Result recovered. |
| `UNKNOWN_PROVIDER_STATE` | reconcile failure | `FAILED` | yes | Error terminal. |
| `UNKNOWN_PROVIDER_STATE` | reconcile cancelled | `CANCELLED` | yes | Cancel confirmed. |
| terminal | resubmit same attempt | none | no | Retry creates a new attempt. |

## 16. Attempt To Job Aggregation

| Current Attempt State | Job Status | Notes |
| --- | --- | --- |
| `PREPARED` | `QUEUED` | No provider work yet. |
| `SUBMITTED` | `PROCESSING` | Provider submission has begun. |
| `PROCESSING` | `PROCESSING` | Normal in-flight state. |
| `SUCCEEDED` | `SUCCEEDED` | Generated media exists; review remains `NOT_RUN` in Phase 2A. |
| `FAILED` | `FAILED` | Unless retry creates a new current attempt. |
| `CANCEL_REQUESTED` | `PROCESSING` | Cancel pending. |
| `CANCELLED` | `CANCELLED` | Terminal unless retry allowed. |
| `UNKNOWN_PROVIDER_STATE` | `PROCESSING` | Do not fail job until reconciliation policy decides. |

## 17. Cancel, Retry, And Unknown Provider State

Cancel:

- Requires `Idempotency-Key`.
- Allowed for `QUEUED` and `PROCESSING`.
- `PREPARED -> CANCELLED` is allowed before provider submission.
- If attempt is `UNKNOWN_PROVIDER_STATE`, keep the attempt in
  `UNKNOWN_PROVIDER_STATE`, save `cancellation_intent=true` and
  `cancel_requested_at`, keep Job `PROCESSING`, and forbid blind resubmission.
- If job is `SUCCEEDED`, return HTTP 409 `JOB_CANCEL_NOT_ALLOWED`.
- If already `CANCELLED`, return current job state.

Retry:

- Requires `Idempotency-Key`.
- Creates a new Attempt under the same Job only when the accepted snapshot is
  unchanged.
- Does not allow client to change prompt, assets, proof needs, source refs, or
  provider mapping.
- Changed creative request creates a new Job, not retry.
- Successful jobs are not retryable by default.
- Jobs with current attempt `UNKNOWN_PROVIDER_STATE` are not retryable until
  reconciliation resolves or policy marks them terminal.

Unknown provider state:

- Belongs to Attempt.
- Blocks blind duplicate submission.
- Job remains `PROCESSING`.
- Cancellation intent can be recorded without changing Attempt state.
- Mock provider should simulate this deterministically in tests.

## 18. AI Review Status

Phase 2A Create Job always initializes:

```yaml
ai_review_status: "NOT_RUN"
```

Generation `SUCCEEDED` means result media exists. It does not mean Knowledge 10
has passed. Review submission is not part of the Phase 2A public Action schema.

## 19. End-to-End Business Flows

| # | Flow | Summary | Expected Outcome |
| --- | --- | --- | --- |
| 1 | Health check | Client calls `GET /health`. | 200 with service/version. |
| 2 | Request mock upload URL | Client requests asset upload URL with metadata. | Asset `PENDING_UPLOAD`; HTTP/HTTPS upload URL returned. |
| 3 | Internal mock upload success | Internal PUT marks upload complete. | Asset `READY`. |
| 4 | Create no-asset non-proof job | AI non-proof plan, no proof asset needed. | Job `QUEUED`; attempt `PREPARED`; review `NOT_RUN`. |
| 5 | Create HYBRID with ready proof asset | Real proof layer plus AI environment. | Job accepted. |
| 6 | Block high-truth pure AI | `truth_dependency=high` with `AI_GENERATION`. | Deterministic 422; no job. |
| 7 | Block AI suction proof | Proof need is suction and AI would carry proof. | Deterministic 422; no job. |
| 8 | Block missing HYBRID real layer | HYBRID lacks real layer or rewrite locks. | Deterministic 422; no job. |
| 9 | Duplicate create same payload | Same key and canonical request. | Same cached response with `idempotent_replay=true`. |
| 10 | Duplicate create different payload | Same key, different canonical request. | HTTP 409 `IDEMPOTENCY_CONFLICT`. |
| 11 | Poll queued/processing/succeeded | Client polls job status. | Current job, attempt, result/ref status. |
| 12 | Cancel prepared job | Cancel before provider submit. | Attempt `CANCELLED`; Job `CANCELLED`. |
| 13 | Cancel processing job | Cancel after provider started. | Attempt `CANCEL_REQUESTED`, then terminal. |
| 14 | Cancel unknown attempt | Cancel while attempt is unknown. | Attempt stays `UNKNOWN_PROVIDER_STATE`; intent recorded. |
| 15 | Retry failed job | Same snapshot, new key. | New attempt; Job returns to `QUEUED`. |
| 16 | Unknown provider state | Mock simulates submit timeout. | Attempt `UNKNOWN_PROVIDER_STATE`; no duplicate submit. |
| 17 | Result media returned | Mock succeeds. | `RESULT_MEDIA` Asset with HTTPS secure URL metadata. |

## 20. Public API Contract Details

### GET /health

Request schema concept:

```yaml
request: {}
```

Response schema concept:

```yaml
response:
  status: "ok"
  service: "video-generation-backend"
  contract_version: "v1"
```

HTTP status: `200`, `500`.

Errors: `INTERNAL_ERROR`.

Idempotency: no `Idempotency-Key`; not cached in `IdempotencyRecord`.

### POST /v1/assets/upload-url

Request schema concept:

```yaml
request:
  contract_version: "v1"
  content_type: "image/png | image/jpeg | video/mp4"
  size_bytes: 0
  checksum_sha256: ""
  intended_usage_role: "PRODUCT_IDENTITY | FIRST_FRAME | LAST_FRAME | MOTION_REFERENCE | CAMERA_REFERENCE | ENVIRONMENT_REFERENCE | PROOF_EVIDENCE | SOURCE_CLIP"
```

Response schema concept:

```yaml
response:
  asset_id: "asset_..."
  asset_status: "PENDING_UPLOAD"
  upload_url: "https://backend.local/_internal/mock-uploads/{token}"
  upload_url_expires_at: ""
  idempotent_replay: false
```

HTTP status: `201`, `401`, `409`, `413`, `415`, `422`, `500`.

Errors: `AUTH_REQUIRED`, `AUTH_INVALID`, `SCHEMA_INVALID`,
`ASSET_TYPE_UNSUPPORTED`, `ASSET_TOO_LARGE`, `IDEMPOTENCY_CONFLICT`,
`IDEMPOTENCY_PENDING`, `INTERNAL_ERROR`.

Idempotency: required. Successful or deterministic replay responses include
`idempotent_replay`.

### POST /v1/video-jobs

Request schema concept: see Section 11.

Response schema concept:

```yaml
response:
  job_id: "job_..."
  generation_status: "QUEUED"
  ai_review_status: "NOT_RUN"
  execution_provider: "mock"
  contract_version: "v1"
  truth_rule_version: "truth-rules-v0.4"
  provider_mapping_version: "mock-provider-map-v0.4"
  idempotent_replay: false
```

HTTP status: `202`, `401`, `409`, `422`, `500`.

Errors: `AUTH_REQUIRED`, `AUTH_INVALID`, `SCHEMA_INVALID`,
`VERSION_CONFLICT`, `ASSET_NOT_FOUND`, `ASSET_NOT_READY`,
`ASSET_INVALID_STATE`, `TRUTH_GATE_BLOCKED`, `HYBRID_GATE_BLOCKED`,
`AI_PROOF_NOT_ALLOWED`, `PROVIDER_UNSUPPORTED`, `IDEMPOTENCY_CONFLICT`,
`IDEMPOTENCY_PENDING`, `INTERNAL_ERROR`.

Idempotency: required. Gate-blocked deterministic 422 responses must be saved
in `IdempotencyRecord`. Successful or deterministic replay responses include
`idempotent_replay`.

### GET /v1/video-jobs/{job_id}

Request schema concept:

```yaml
request:
  job_id: "job_..."
```

Response schema concept:

```yaml
response:
  job_id: "job_..."
  generation_status: "QUEUED | PROCESSING | SUCCEEDED | FAILED | CANCELLED"
  ai_review_status: "NOT_RUN"
  current_attempt: {}
  assets: []
  result_media: []
  errors: []
```

HTTP status: `200`, `401`, `404`, `500`.

Errors: `AUTH_REQUIRED`, `AUTH_INVALID`, `JOB_NOT_FOUND`, `OWNER_MISMATCH`,
`INTERNAL_ERROR`.

Idempotency: not required. Not cached in `IdempotencyRecord`.

### POST /v1/video-jobs/{job_id}/cancel

Request schema concept:

```yaml
request:
  reason: ""
```

Response schema concept:

```yaml
response:
  job_id: "job_..."
  generation_status: "CANCELLED | PROCESSING"
  attempt_status: "CANCEL_REQUESTED | CANCELLED | UNKNOWN_PROVIDER_STATE"
  cancellation_intent: false
  cancel_requested_at: null
  idempotent_replay: false
```

HTTP status: `200`, `202`, `401`, `404`, `409`, `422`, `500`.

Errors: `AUTH_REQUIRED`, `AUTH_INVALID`, `SCHEMA_INVALID`, `JOB_NOT_FOUND`,
`JOB_CANCEL_NOT_ALLOWED`, `JOB_INVALID_STATE`, `IDEMPOTENCY_CONFLICT`,
`IDEMPOTENCY_PENDING`, `INTERNAL_ERROR`.

Idempotency: required. Successful or deterministic replay responses include
`idempotent_replay`.

### POST /v1/video-jobs/{job_id}/retry

Request schema concept:

```yaml
request:
  reason: ""
```

Response schema concept:

```yaml
response:
  job_id: "job_..."
  generation_status: "QUEUED"
  new_attempt_id: "attempt_..."
  idempotent_replay: false
```

HTTP status: `202`, `401`, `404`, `409`, `422`, `500`.

Errors: `AUTH_REQUIRED`, `AUTH_INVALID`, `SCHEMA_INVALID`, `JOB_NOT_FOUND`,
`JOB_NOT_RETRYABLE`, `JOB_INVALID_STATE`, `UNKNOWN_PROVIDER_STATE`,
`IDEMPOTENCY_CONFLICT`, `IDEMPOTENCY_PENDING`, `INTERNAL_ERROR`.

Idempotency: required. Successful or deterministic replay responses include
`idempotent_replay`.

## 21. Detailed Core Flow: Upload URL

Preconditions:

- Bearer API key is configured.
- Request includes `Idempotency-Key`.
- Content type and size are supported.

Validation order:

1. Authenticate and map `owner_id`.
2. Validate `Idempotency-Key` presence.
3. Validate schema.
4. Validate content type and size.
5. Create or inspect idempotency record in transaction.

DB writes:

- Insert `idempotency_records(status=PENDING)`.
- Insert `assets(status=PENDING_UPLOAD)`.
- Update idempotency record to `COMPLETED` with response snapshot.

State transitions:

- Asset: none -> `PENDING_UPLOAD`.

Idempotency:

- Same key and canonical request after completion returns cached 201 with
  `idempotent_replay=true`.
- Same key and different canonical request returns 409.
- Concurrent same-key same-payload request sees `PENDING` and returns 409
  `IDEMPOTENCY_PENDING` or waits only if explicitly implemented later.

Response:

- 201 with HTTP/HTTPS mock upload URL and `idempotent_replay=false`.

Errors:

- 401 auth.
- 409 idempotency conflict or pending.
- 413 too large.
- 415 unsupported type.
- 422 schema.
- 500 unexpected.

## 22. Detailed Core Flow: Create Job

Preconditions:

- Bearer API key valid.
- Request includes `Idempotency-Key`.
- `selected_model=Seedance`.
- `execution_provider=mock`.
- Referenced assets, if any, exist and are `READY`.

Validation order:

1. Authenticate and map `owner_id`.
2. Validate `Idempotency-Key` presence.
3. Canonicalize request with path and body.
4. Create or inspect idempotency record in transaction.
5. Validate schema and client-disallowed fields.
6. Validate version compatibility.
7. Validate asset ownership and readiness.
8. Run Truth Gate.
9. Run HYBRID Gate.
10. Create job and first attempt.

DB writes:

- Insert `idempotency_records(status=PENDING)`.
- Insert request snapshot.
- Insert client facts, source refs, proof needs, and job asset references.
- Insert `video_jobs(status=QUEUED, ai_review_status=NOT_RUN)`.
- Insert `job_attempts(status=PREPARED)`.
- Insert gate decisions.
- Update idempotency record to `COMPLETED` with response snapshot.

State transitions:

- Job: none -> `QUEUED`.
- Attempt: none -> `PREPARED`.
- AI review: none -> `NOT_RUN`.

Idempotency:

- Deterministic 422 schema/truth/hybrid gate responses are stored.
- Same key and canonical request replays stored response with
  `idempotent_replay=true`.
- Same key and different canonical request returns 409.
- `PENDING` same-key request returns 409 `IDEMPOTENCY_PENDING`.

Response:

- 202 with job id and `idempotent_replay=false`.

Errors:

- 401 auth.
- 409 idempotency/version/status conflict.
- 422 schema/truth/hybrid/provider/asset validation.
- 500 unexpected.

## 23. Detailed Core Flow: Cancel

Preconditions:

- Bearer API key valid.
- Request includes `Idempotency-Key`.
- Job exists and belongs to owner.

Validation order:

1. Authenticate and map `owner_id`.
2. Validate `Idempotency-Key` presence.
3. Validate path `job_id`.
4. Create or inspect idempotency record in transaction.
5. Load job and current attempt.
6. Validate cancel policy.
7. Apply state transition or cancellation intent.

DB writes:

- Insert `idempotency_records(status=PENDING)`.
- If attempt `PREPARED`, update attempt to `CANCELLED` and job to
  `CANCELLED`.
- If attempt `PROCESSING`, update attempt to `CANCEL_REQUESTED`.
- If attempt `UNKNOWN_PROVIDER_STATE`, keep attempt unchanged and set
  `cancellation_intent=true`, `cancel_requested_at`.
- Update idempotency record to `COMPLETED`.

State transitions:

- `PREPARED -> CANCELLED`; Job `QUEUED -> CANCELLED`.
- `PROCESSING -> CANCEL_REQUESTED`; Job remains `PROCESSING`.
- `UNKNOWN_PROVIDER_STATE -> UNKNOWN_PROVIDER_STATE`; Job remains
  `PROCESSING`.

Idempotency:

- Accepted cancel response is replayed with `idempotent_replay=true`.
- Same key and different request returns 409.
- `PENDING` same-key request returns 409 `IDEMPOTENCY_PENDING`.

Response:

- 200 for already terminal or immediately cancelled.
- 202 for accepted asynchronous cancel or unknown-state cancellation intent.

Errors:

- 401 auth.
- 404 job not found.
- 409 job cancel not allowed, invalid state, idempotency conflict.
- 422 schema.
- 500 unexpected.

## 24. Detailed Core Flow: Retry

Preconditions:

- Bearer API key valid.
- Request includes `Idempotency-Key`.
- Job exists and belongs to owner.
- Job is `FAILED` or retry-eligible `CANCELLED`.
- Current attempt is not `UNKNOWN_PROVIDER_STATE`.

Validation order:

1. Authenticate and map `owner_id`.
2. Validate `Idempotency-Key` presence.
3. Validate path `job_id`.
4. Create or inspect idempotency record in transaction.
5. Load accepted job snapshot.
6. Validate retry policy.
7. Create new attempt.

DB writes:

- Insert `idempotency_records(status=PENDING)`.
- Insert new `job_attempts(status=PREPARED)`.
- Update `video_jobs(status=QUEUED, current_attempt_id=...)`.
- Update idempotency record to `COMPLETED`.

State transitions:

- Job: `FAILED` or retry-eligible `CANCELLED` -> `QUEUED`.
- Attempt: none -> `PREPARED`.

Idempotency:

- Accepted retry response is replayed with `idempotent_replay=true`.
- Same key and different request returns 409.
- `PENDING` same-key request returns 409 `IDEMPOTENCY_PENDING`.

Response:

- 202 with new attempt id.

Errors:

- 401 auth.
- 404 job not found.
- 409 job not retryable, invalid state, unknown provider state, idempotency
  conflict.
- 422 schema.
- 500 unexpected.

## 25. Idempotency Policy

Phase 2A defaults:

```yaml
idempotency_ttl_hours: 24
mock_upload_url_ttl_hours: 24
```

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
- Include HTTP method.
- Include route template.
- Include path parameters, including `job_id`.
- Include server-mapped `owner_id`.
- Include request body.
- Exclude `Idempotency-Key` from canonical body hash but include it in the
  idempotency lookup scope.

Database uniqueness:

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

Record states:

- `PENDING`
- `COMPLETED`

Concurrent behavior:

- First request inserts `PENDING` inside the same transaction that starts side
  effects.
- Concurrent same-key request with same canonical hash returns 409
  `IDEMPOTENCY_PENDING` unless a later implementation explicitly waits.
- Same key with different canonical hash returns 409
  `IDEMPOTENCY_CONFLICT`.
- Successful or deterministic replay responses include
  `idempotent_replay=false` on first completion and `true` on replay.
- If a request fails with unexpected 500 before completion, do not mark
  `COMPLETED`; leave safe recovery behavior to implementation policy.

Cache in `IdempotencyRecord`:

- Successful `POST /v1/assets/upload-url`.
- Successful `POST /v1/video-jobs`.
- Deterministic 422 schema/truth/hybrid gate responses for create job.
- Successful or accepted cancel responses.
- Successful or accepted retry responses.
- Deterministic post-auth validation failures.

Do not cache:

- `GET /health`.
- `GET /v1/video-jobs/{job_id}`.
- Auth failures.
- Unexpected 500 responses.
- Provider transient errors where retry may be safe.

## 26. ProviderResult And Result Media

Mock success creates:

```yaml
provider_result:
  provider_result_id: "pr_..."
  attempt_id: "attempt_..."
  normalized_status: "SUCCEEDED"
  result_asset_ids: []
```

Each result video is stored as:

```yaml
asset:
  asset_kind: "RESULT_MEDIA"
  status: "READY"
  secure_url: "https://backend.local/_internal/mock-results/{asset_id}"
  url_expires_at: ""
  checksum_sha256: ""
  content_type: "video/mp4"
  size_bytes: 0
```

Secure URL expiry does not expire the Asset.

## 27. Error Registry

| Code | HTTP | Meaning | Used By |
| --- | --- | --- | --- |
| `AUTH_REQUIRED` | 401 | Missing auth. | upload, create, get, cancel, retry |
| `AUTH_INVALID` | 401 | Invalid Bearer API key. | upload, create, get, cancel, retry |
| `OWNER_MISMATCH` | 404 | Resource not visible to owner. | get |
| `SCHEMA_INVALID` | 422 | Request shape or enum invalid. | upload, create, cancel, retry |
| `VERSION_CONFLICT` | 409 | Expected truth rule version mismatch. | create |
| `ASSET_NOT_FOUND` | 422 | Referenced asset does not exist for owner. | create |
| `ASSET_NOT_READY` | 422 | Referenced asset is not `READY`. | create |
| `ASSET_INVALID_STATE` | 422 | Asset state cannot be used for operation. | create |
| `ASSET_TYPE_UNSUPPORTED` | 415 | Unsupported upload content type. | upload |
| `ASSET_TOO_LARGE` | 413 | Upload size exceeds limit. | upload |
| `TRUTH_GATE_BLOCKED` | 422 | Structural Truth Gate blocked request. | create |
| `HYBRID_GATE_BLOCKED` | 422 | HYBRID layer policy invalid. | create |
| `AI_PROOF_NOT_ALLOWED` | 422 | AI assigned prohibited proof role. | create |
| `PROVIDER_UNSUPPORTED` | 422 | Provider/model combination unsupported. | create |
| `IDEMPOTENCY_CONFLICT` | 409 | Same key, different canonical request. | upload, create, cancel, retry |
| `IDEMPOTENCY_PENDING` | 409 | Same key request still pending. | upload, create, cancel, retry |
| `JOB_NOT_FOUND` | 404 | Job not found for owner. | get, cancel, retry |
| `JOB_INVALID_STATE` | 409 | Operation invalid for current state. | cancel, retry |
| `JOB_CANCEL_NOT_ALLOWED` | 409 | Job cannot be cancelled. | cancel |
| `JOB_NOT_RETRYABLE` | 409 | Job cannot be retried. | retry |
| `UNKNOWN_PROVIDER_STATE` | 409 | Retry blocked by unresolved provider ambiguity. | retry |
| `INTERNAL_ERROR` | 500 | Unexpected server error. | all |

Schema, Truth Gate, and HYBRID Gate use 422. State conflicts and idempotency
conflicts use 409.

## 28. Authentication And Persistence

Authentication:

```yaml
auth:
  mode: "single_tenant_bearer_api_key"
  owner_id_source: "server_side_mapping"
  trust_body_owner_id: false
```

Persistence:

```yaml
persistence:
  runtime: "SQLite + SQLAlchemy 2.x + Alembic"
  in_memory: "unit_tests_only"
```

All assets, jobs, attempts, results, and idempotency records are scoped to the
server-mapped owner.

## 29. Decision Log

| ID | Decision | Status | Phase 2A Result |
| --- | --- | --- | --- |
| D-001 | API base path | APPROVED_FOR_PHASE_2A | Use `/v1/video-jobs`. |
| D-002 | Persistence | APPROVED_FOR_PHASE_2A | SQLite + SQLAlchemy 2.x + Alembic. |
| D-003 | Cancelled spelling | APPROVED_FOR_PHASE_2A | Use `CANCELLED`. |
| D-004 | Processing state name | APPROVED_FOR_PHASE_2A | Use `PROCESSING`. |
| D-005 | GPT Action attachment handling | DECISION_REQUIRED | Binary attachment behavior remains unknown; mock upload URL flow approved. |
| D-006 | Owner identity source | APPROVED_FOR_PHASE_2A | Server-side Bearer API key mapping. |
| D-007 | Cost confirmation timing | DECISION_REQUIRED | Required before real Seedance, not Phase 2A blocker. |
| D-008 | Review result source | DECISION_REQUIRED | Review submission not in Phase 2A default Action schema. |
| D-009 | Retry semantics | APPROVED_FOR_PHASE_2A | Same job, new attempt, unchanged snapshot. |
| D-010 | Real Seedance fields | DECISION_REQUIRED | Defer to Phase 2C. |
| D-011 | Backend Handoff authority | APPROVED_FOR_PHASE_2A | Real handoff read. |
| D-012 | Authority levels | APPROVED_FOR_PHASE_2A | Runtime, Backend Scope, Design Reference, Third-party. |
| D-013 | Proof model split | APPROVED_FOR_PHASE_2A | Use presentation/proof/evidence/status split. |
| D-014 | Fact provenance model | APPROVED_FOR_PHASE_2A | Client declares facts; backend controls verification. |
| D-015 | JobAssetReference | APPROVED_FOR_PHASE_2A | Separate asset body from job usage. |
| D-016 | Asset states | APPROVED_FOR_PHASE_2A | Five-state Asset model. |
| D-017 | Gate block behavior | APPROVED_FOR_PHASE_2A | No job; deterministic 422 cached. |
| D-018 | Public/attempt state split | APPROVED_FOR_PHASE_2A | Public Job five states; Attempt owns provider ambiguity. |
| D-019 | Mock scenario control | APPROVED_FOR_PHASE_2A | Internal/test only. |
| D-020 | ProviderResult result media | APPROVED_FOR_PHASE_2A | Result media stored as `RESULT_MEDIA` Asset. |
| D-021 | Client-controlled backend fields | APPROVED_FOR_PHASE_2A | Disallow verification/trust/gate/version internals. |
| D-022 | Idempotency TTL | APPROVED_FOR_PHASE_2A | 24 hours default. |
| D-023 | Phase 2A Action provider/model | APPROVED_FOR_PHASE_2A | `selected_model=Seedance`, `execution_provider=mock`. |
| D-024 | Structural Truth Enforcement scope | APPROVED_FOR_PHASE_2A | No semantic media truth claims in Phase 2A. |
| D-025 | Default Action Schema excludes public asset complete endpoint | APPROVED_FOR_PHASE_2A | No public complete endpoint in default Action OpenAPI. |
| D-026 | Six public interfaces are complete Phase 2A Action surface | APPROVED_FOR_PHASE_2A | Only six public routes enter Action schema. |
| D-027 | Internal mock routes | APPROVED_FOR_PHASE_2A | `/_internal/mock-uploads/*` and `/_internal/mock-results/*` excluded from Action schema. |
| D-028 | Generation modes | APPROVED_FOR_PHASE_2A | Only `T2V`, `I2V`, `R2V`, `FLF2V`. |

## 30. Remaining Open Questions

- Can Custom GPT Actions directly upload binary attachments, or should Phase 2A
  rely only on upload URLs?
- What is the final retention policy for prompts, asset metadata, result URLs,
  and provider raw payloads?
- Who submits Knowledge 10 review results in Phase 2B/2D?
- What exact real Seedance API fields, status names, callbacks, cancellation,
  result URL behavior, and cost model apply in Phase 2C?
- Should cost confirmation become a separate endpoint before real provider
  submit?

## 31. Coding Blockers Before Phase 2A

The only remaining start-coding blocker is final human approval of v0.4 as the
Phase 2A implementation baseline.

Not blockers for Phase 2A mock coding:

- Direct binary attachment support.
- Real Seedance API details.
- Real cost confirmation endpoint.
- Knowledge 10 review submission endpoint.
- Production object storage.
- Multi-tenant auth.

## 32. Approval Checklist

Before starting code, approve:

- v0.4 as the Phase 2A baseline.
- Six public endpoints only.
- No public asset complete endpoint in default Action schema.
- Mock asset upload flow with internal-only HTTP/HTTPS routes.
- SQLite + SQLAlchemy 2.x + Alembic.
- Bearer API key single-tenant auth.
- `selected_model=Seedance` and `execution_provider=mock` in public Action.
- Structural Truth Enforcement only.
- 24-hour idempotency TTL and 24-hour mock upload URL TTL.
- `idempotent_replay` response field for idempotent operations.
- No public mock scenario selector.
- No modification to frozen Custom GPT files.
