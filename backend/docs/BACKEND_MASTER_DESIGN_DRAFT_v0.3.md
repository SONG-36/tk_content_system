# Backend Master Design Draft v0.3

## 1. Document Status

```yaml
document_status:
  document_version: "v0.3"
  status: "DRAFT_FOR_PHASE_2A_CODING_REVIEW"
  supersedes_for_review: "backend/docs/BACKEND_MASTER_DESIGN_DRAFT_v0.2.md"
  overwrites_v0_2: false
  implementation_code_created: false
  approval_required_before_coding: true
  handoff_read: true
  handoff_path: "backend/docs/reference/VIDEO_GENERATION_BACKEND_HANDOFF.md"
  handoff_status: "REAL_HANDOFF_READ"
```

This document closes the v0.2 design gaps for Phase 2A planning. It does not
modify v0.1, v0.2, backend docs 00-04, Custom GPT frozen files, Knowledge
01-18, or third-party Skills.

## 2. Authoritative Sources

### Runtime Authoritative

- `custom_gpt_package/multi_category_gpt/00_INSTRUCTIONS/MAIN_INSTRUCTIONS.md`
- `custom_gpt_package/multi_category_gpt/01_KNOWLEDGE_UPLOAD/01-18_*.md`

These files define Custom GPT behavior. Backend runtime must not parse them.

### Backend Scope Authoritative

- `AGENTS.md`
- `backend/AGENTS.md`
- `backend/docs/reference/VIDEO_GENERATION_BACKEND_HANDOFF.md`

The handoff file is no longer `CONTENT_PENDING`. It defines the Phase 2A
backend target: FastAPI backend, mock first, six public endpoints, Truth Gate,
HYBRID Gate, idempotency, asset flow, status polling, cancel/retry, and no real
Seedance connection in Phase 2A.

### Design Reference

- `backend/docs/BACKEND_MASTER_DESIGN_DRAFT_v0.1.md`
- `backend/docs/BACKEND_MASTER_DESIGN_DRAFT_v0.2.md`
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

These remain reference material only. They are not backend API contracts,
provider schemas, or runtime policy sources.

## 3. v0.3 Scope

Phase 2A should produce a mock FastAPI backend with:

- Public HTTPS-compatible JSON API contract.
- Mock asset upload flow.
- Mock provider only.
- SQLite persistence with SQLAlchemy 2.x and Alembic.
- Bearer API key authentication.
- Structural Truth Gate and HYBRID Gate.
- Idempotency for side-effecting endpoints.
- Job state, Attempt state, and AI review status separation.
- OpenAPI Action schema for the public endpoints only.

Phase 2A must not:

- Connect to real Seedance.
- Claim semantic media truth verification.
- Put mock scenario controls into the public Action schema.
- Let the client control backend verification, trust, or mapping fields.
- Modify frozen Custom GPT files.

## 4. Layer Separation

### API Client Input

Client input is what Custom GPT Action may submit.

Allowed client-controlled concepts:

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
- `product_proof_owner`
- `hybrid_layers`
- `duration_seconds`
- `aspect_ratio`
- user-declared facts
- proof needs
- source references
- production plan

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

Domain objects express backend concepts independent of SQL tables:

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
- `IdempotencyDecision`

### Persistence Model

Persistence objects store backend state and audit trail:

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
- `provider_submissions`
- `provider_results`
- `review_results`
- `idempotency_records`
- `error_records`

The persistence model may differ from API field names. API compatibility should
be managed by `contract_version`, while database evolution is managed by
Alembic migrations.

## 5. Version Control Fields

Client submits:

```yaml
contract_version: "v1"
expected_truth_rule_version: "truth-rules-v0.3" # optional compatibility check only
```

Server controls:

```yaml
truth_rule_version: "truth-rules-v0.3"
provider_mapping_version: "mock-provider-map-v0.3"
```

Rules:

- Client must not submit `truth_rule_version`.
- Client must not submit `provider_mapping_version`.
- If `expected_truth_rule_version` is provided and mismatches the server
  version, return `VERSION_CONFLICT`.
- The accepted job snapshot stores the server-controlled versions.

## 6. Client Fact And Proof Input

Custom GPT is not a product Fact verifier. It may declare facts, proof needs,
source references, and production plan boundaries.

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
source_ref:
  source_ref_id: "src_..."
  source_type: "USER_INPUT | UPLOADED_ASSET | PRODUCT_LINK | PRODUCT_SPEC_TEXT | PRIOR_SCRIPT | MANUAL_NOTE"
  source_value: ""
  asset_id: null
```

```yaml
proof_need:
  proof_need_id: "pneed_..."
  shot_id: "shot_..."
  proof_type: "identity | structure | accessory | function | result | human_efficacy | safety | sterilization | compatibility | before_after | suction | dirt_intake | transparent_bin | pet_hair | gap_access | attachment_performance | measurable_performance"
  linked_client_fact_ids: []
  required_evidence_refs: []
  production_type: "REAL_SHOOT | AI_GENERATION | HYBRID | STOCK_ASSET"
```

The backend may derive `BackendFact` and `VerificationRecord` from client input,
asset metadata, and internal structural checks. Phase 2A does not claim it can
automatically verify media semantic truth.

## 7. Proof Model v0.3

The v0.2 `proof_owner` field is replaced by a more precise split:

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

Client may submit the desired `presentation_layer` as part of a production
plan, but the backend determines `proof_carrier`, `verification_method`,
`backend_verification_status`, and `backend_gate_result`.

## 8. AI Visualization Versus AI Proof

AI visualization means AI renders or enhances an already bounded visual layer.
AI proof means AI output is asked to prove a product fact, result, function, or
safety claim.

Allowed in Phase 2A structural gate:

- AI environment or atmosphere for non-proof Hook.
- AI visualization of a product reference when the job does not ask AI to prove
  identity, structure, accessory, function, or result.
- HYBRID when real layer carries proof and AI layer cannot rewrite proof facts.

Blocked:

- Pure AI carrying high-truth proof.
- AI suction proof.
- AI dirt-intake proof.
- AI cleaning Before/After.
- AI transparent-bin proof.
- AI beauty or grooming efficacy proof.
- AI sterilization or safety proof.
- AI proof of unverified accessory or structure.

Compatibility, identity, and structure are not automatically blocked. They are
blocked only when the request asks AI/provider output to invent, rewrite, or
prove them without acceptable real source refs and rewrite constraints.

## 9. Structural Truth Enforcement

Phase 2A Truth Enforcement is structural. It validates that the request contract
does not assign proof to forbidden layers and that required fields exist.

It can enforce:

- `truth_dependency=high` cannot use pure `AI_GENERATION`.
- HYBRID must include real layer, AI layer, real proof carrier, and
  `ai_must_not_rewrite`.
- Product proof carried by AI is blocked for prohibited proof types.
- Asset ids referenced by the request must exist, belong to the server-mapped
  owner, and be `READY`.
- `selected_model=Seedance` and `execution_provider=mock` are the only Phase 2A
  public Action combination.

It cannot claim:

- The uploaded video truly proves suction.
- The product structure in a frame is semantically correct.
- The result media is commercially truthful.
- Knowledge 10 review has passed.

Those require human review, controlled tests, or later semantic review systems.

## 10. Phase 2A Action Contract Limits

For the public Custom GPT Action schema:

```yaml
selected_model:
  allowed: ["Seedance"]
execution_provider:
  allowed: ["mock"]
```

`selected_model=Seedance` means the Custom GPT selected Seedance in the
production plan. `execution_provider=mock` means the backend uses a mock adapter
in Phase 2A. Real Seedance remains out of scope.

## 11. Asset Flow

Phase 2A Mock Asset Flow:

1. Client calls `POST /v1/assets/upload-url`.
2. Backend creates `Asset(status=PENDING_UPLOAD)`.
3. Backend returns `asset_id` and a mock upload URL.
4. Test harness or internal developer tool performs an internal-only mock PUT
   upload.
5. Upload success marks `Asset(status=READY)`.
6. Client creates a video job referencing `READY` asset ids.

The internal-only mock PUT endpoint is not public and must not appear in the
default Custom GPT Action schema.

No public asset complete endpoint is included in the default Phase 2A Action
schema. A future public completion endpoint is `DECISION_REQUIRED`.

Asset states:

- `PENDING_UPLOAD`
- `READY`
- `FAILED`
- `EXPIRED`
- `DELETED`

Upload URL expiry does not automatically equal Asset expiry.

## 12. Job State Transition Table

Public Job states:

- `QUEUED`
- `PROCESSING`
- `SUCCEEDED`
- `FAILED`
- `CANCELLED`

| From | Event | To | Allowed | Notes |
| --- | --- | --- | --- | --- |
| none | accepted create job | `QUEUED` | yes | Only after all pre-create gates pass. |
| none | gate blocked | none | yes | Return 422; no `VideoJob`. |
| `QUEUED` | worker starts attempt | `PROCESSING` | yes | First attempt should be `PREPARED` or `SUBMITTED`. |
| `QUEUED` | cancel accepted before submit | `CANCELLED` | yes | Attempt becomes `CANCELLED` if present. |
| `QUEUED` | provider/prep failure | `FAILED` | yes | No retry without retry endpoint. |
| `PROCESSING` | attempt succeeds | `SUCCEEDED` | yes | Does not imply AI review `PASS`. |
| `PROCESSING` | attempt fails terminally | `FAILED` | yes | Error stored. |
| `PROCESSING` | cancel completed | `CANCELLED` | yes | Provider cancel may be best effort in future. |
| `PROCESSING` | attempt unknown | `PROCESSING` | yes | Attempt holds `UNKNOWN_PROVIDER_STATE`. |
| `FAILED` | retry accepted | `QUEUED` | yes | Same job, new attempt, unchanged payload. |
| `CANCELLED` | retry accepted | `QUEUED` | conditional | Only if retry policy allows. |
| `SUCCEEDED` | retry | none | no | Regeneration with changes creates a new job. |
| `FAILED` | direct processing | none | no | Must go through retry. |
| `CANCELLED` | direct processing | none | no | Must go through retry if allowed. |

## 13. Attempt State Transition Table

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
| `UNKNOWN_PROVIDER_STATE` | reconcile success | `SUCCEEDED` | yes | Result recovered. |
| `UNKNOWN_PROVIDER_STATE` | reconcile failure | `FAILED` | yes | Error terminal. |
| `UNKNOWN_PROVIDER_STATE` | reconcile cancelled | `CANCELLED` | yes | Cancel confirmed. |
| terminal | resubmit same attempt | none | no | Retry creates a new attempt. |

## 14. Attempt To Job Aggregation

| Current Attempt State | Job Status | Notes |
| --- | --- | --- |
| `PREPARED` | `QUEUED` | No provider work yet. |
| `SUBMITTED` | `PROCESSING` | Provider submission has begun. |
| `PROCESSING` | `PROCESSING` | Normal in-flight state. |
| `SUCCEEDED` | `SUCCEEDED` | Generated media exists; review may still be `NOT_RUN`. |
| `FAILED` | `FAILED` | Unless retry creates a new current attempt. |
| `CANCEL_REQUESTED` | `PROCESSING` | Cancel is pending, not terminal. |
| `CANCELLED` | `CANCELLED` | Terminal unless retry allowed. |
| `UNKNOWN_PROVIDER_STATE` | `PROCESSING` | Do not mark job failed until reconciliation timeout/policy. |

If multiple attempts exist, Job status follows the current attempt. Historical
attempts remain immutable audit records.

## 15. Cancel, Retry, And Unknown Provider State

Cancel:

- Requires `Idempotency-Key`.
- Allowed for `QUEUED` and `PROCESSING`.
- If job is `SUCCEEDED`, return `JOB_CANCEL_NOT_ALLOWED`.
- If already `CANCELLED`, return current job state.
- If provider state is unknown, cancel may record `CANCEL_REQUESTED` and require
  reconciliation.

Retry:

- Requires `Idempotency-Key`.
- Creates a new Attempt under the same Job only when the accepted snapshot is
  unchanged.
- Does not allow client to change prompt, assets, proof needs, or provider
  mapping.
- Changed creative request creates a new Job, not retry.
- Successful jobs are not retryable by default.

Unknown provider state:

- Belongs to Attempt.
- Blocks blind duplicate submission.
- Job remains `PROCESSING` until reconciliation or policy timeout.
- Real provider reconciliation is future scope; mock provider should simulate
  this deterministically in tests.

## 16. AI Review Status

AI review status remains separate from generation status:

- `NOT_REQUIRED`
- `NOT_RUN`
- `PASS`
- `REGENERATE`
- `SWITCH_TO_HYBRID`
- `SWITCH_TO_REAL_SHOOT`

Generation `SUCCEEDED` means result media exists. It does not mean Knowledge 10
has passed. Phase 2A can expose review status but should not implement full
review submission unless separately approved.

## 17. End-to-End Business Flows

| # | Flow | Summary | Expected Outcome |
| --- | --- | --- | --- |
| 1 | Health check | Client calls `GET /health`. | 200 with service/version. |
| 2 | Request mock upload URL | Client requests asset upload URL with content metadata. | Asset `PENDING_UPLOAD`; URL returned. |
| 3 | Internal mock upload success | Internal mock PUT marks upload complete. | Asset `READY`. |
| 4 | Create no-asset non-proof job | AI non-proof plan, no proof asset needed. | Job `QUEUED`; attempt prepared. |
| 5 | Create HYBRID with ready proof asset | Real proof layer plus AI environment. | Job accepted. |
| 6 | Block high-truth pure AI | `truth_dependency=high` with `AI_GENERATION`. | Deterministic 422; no job. |
| 7 | Block AI suction proof | Proof need is suction and proof carrier would be AI. | Deterministic 422; no job. |
| 8 | Block missing HYBRID real layer | HYBRID lacks real layer or rewrite locks. | Deterministic 422; no job. |
| 9 | Duplicate create same payload | Same idempotency key and canonical payload. | Same cached response. |
| 10 | Duplicate create different payload | Same key, different payload. | `IDEMPOTENCY_CONFLICT`. |
| 11 | Poll queued/processing/succeeded | Client polls job status. | Current job, attempt, result/ref status. |
| 12 | Cancel queued job | Cancel before provider processing. | Job `CANCELLED`. |
| 13 | Cancel processing job | Cancel after provider started. | Attempt `CANCEL_REQUESTED`, then terminal. |
| 14 | Retry failed job | Same snapshot, new key. | New attempt; job returns to `QUEUED`. |
| 15 | Unknown provider state | Mock simulates submit timeout. | Attempt `UNKNOWN_PROVIDER_STATE`; no duplicate submit. |
| 16 | Result media returned | Mock succeeds. | `RESULT_MEDIA` Asset with secure URL metadata. |

## 18. Public API Contract Details

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
  upload_url: "mock://..."
  upload_url_expires_at: ""
```

HTTP status: `201`, `400`, `401`, `409`, `413`, `415`, `500`.

Errors: `AUTH_REQUIRED`, `AUTH_INVALID`, `SCHEMA_INVALID`,
`ASSET_TYPE_UNSUPPORTED`, `ASSET_TOO_LARGE`, `IDEMPOTENCY_CONFLICT`,
`INTERNAL_ERROR`.

Idempotency: required. Cache successful `201` response. Cache deterministic
schema/asset validation failures after auth. Do not cache auth failures or
unexpected `500`.

### POST /v1/video-jobs

Request schema concept:

```yaml
request:
  contract_version: "v1"
  expected_truth_rule_version: "truth-rules-v0.3" # optional
  selected_model: "Seedance"
  execution_provider: "mock"
  shot_number: ""
  production_type: "AI_GENERATION | HYBRID"
  generation_mode: "T2V | I2V | R2V | FLF2V | EDIT | EXTEND"
  prompt: ""
  negative_constraints: []
  preservation_constraints: []
  reference_assets: []
  truth_dependency: "low | medium | high"
  product_proof_owner: "real_shoot | none"
  hybrid_layers: null
  duration_seconds: 8
  aspect_ratio: "9:16"
  client_declared_facts: []
  source_refs: []
  proof_needs: []
```

Response schema concept:

```yaml
response:
  job_id: "job_..."
  generation_status: "QUEUED"
  ai_review_status: "NOT_RUN | NOT_REQUIRED"
  execution_provider: "mock"
  contract_version: "v1"
  truth_rule_version: "truth-rules-v0.3"
  provider_mapping_version: "mock-provider-map-v0.3"
```

HTTP status: `202`, `400`, `401`, `409`, `422`, `500`.

Errors: `AUTH_REQUIRED`, `AUTH_INVALID`, `SCHEMA_INVALID`,
`VERSION_CONFLICT`, `ASSET_NOT_READY`, `TRUTH_GATE_BLOCKED`,
`HYBRID_GATE_BLOCKED`, `AI_PROOF_NOT_ALLOWED`, `PROVIDER_UNSUPPORTED`,
`IDEMPOTENCY_CONFLICT`, `INTERNAL_ERROR`.

Idempotency: required. Cache successful `202`. Gate-blocked deterministic
`422` must be saved in `IdempotencyRecord`. Cache deterministic validation
failures after auth. Do not cache auth failures, transient provider errors, or
unexpected `500`.

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
  ai_review_status: "NOT_REQUIRED | NOT_RUN | PASS | REGENERATE | SWITCH_TO_HYBRID | SWITCH_TO_REAL_SHOOT"
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
  attempt_status: "CANCEL_REQUESTED | CANCELLED"
```

HTTP status: `200`, `202`, `400`, `401`, `404`, `409`, `500`.

Errors: `AUTH_REQUIRED`, `AUTH_INVALID`, `JOB_NOT_FOUND`,
`JOB_CANCEL_NOT_ALLOWED`, `JOB_INVALID_STATE`, `IDEMPOTENCY_CONFLICT`,
`INTERNAL_ERROR`.

Idempotency: required. Cache accepted cancel responses (`200` or `202`) and
deterministic not-allowed conflicts. Do not cache auth failures or `500`.

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
```

HTTP status: `202`, `400`, `401`, `404`, `409`, `500`.

Errors: `AUTH_REQUIRED`, `AUTH_INVALID`, `JOB_NOT_FOUND`,
`JOB_NOT_RETRYABLE`, `JOB_INVALID_STATE`, `IDEMPOTENCY_CONFLICT`,
`INTERNAL_ERROR`.

Idempotency: required. Cache accepted retry responses and deterministic
not-retryable conflicts. Do not cache auth failures or `500`.

## 19. Idempotency Policy

Phase 2A default TTL:

```yaml
idempotency:
  default_ttl_hours: 24
```

Cache in `IdempotencyRecord`:

- Successful `POST /v1/assets/upload-url`.
- Successful `POST /v1/video-jobs`.
- Deterministic 422 gate-block responses for `POST /v1/video-jobs`.
- Successful or accepted cancel responses.
- Successful or accepted retry responses.
- Deterministic post-auth validation failures that will repeat for the same
  payload.

Do not cache in `IdempotencyRecord`:

- `GET /health`.
- `GET /v1/video-jobs/{job_id}`.
- Auth failures.
- Rate-limit responses unless later explicitly approved.
- Unexpected `500`.
- Provider transient errors where retry may be safe.

Same key plus same canonical payload returns the saved response. Same key plus
different canonical payload returns `IDEMPOTENCY_CONFLICT`.

## 20. ProviderResult And Result Media

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
  secure_url: "mock://result/..."
  url_expires_at: ""
  checksum_sha256: ""
  content_type: "video/mp4"
  size_bytes: 0
```

Secure URL expiry does not expire the Asset.

## 21. Authentication And Ownership

Phase 2A uses single-tenant Bearer API key.

```yaml
auth:
  mode: "single_tenant_bearer_api_key"
  owner_id_source: "server_side_mapping"
  trust_body_owner_id: false
```

All assets, jobs, attempts, results, and idempotency records are scoped to the
server-mapped owner.

## 22. Persistence

Phase 2A persistence is:

```yaml
persistence:
  runtime: "SQLite + SQLAlchemy 2.x + Alembic"
  in_memory: "unit_tests_only"
```

In-memory state is not acceptable for API integration tests that validate
idempotency or state recovery behavior.

## 23. Error Model

```yaml
error:
  code: ""
  message: ""
  field: ""
  required_action: ""
  request_id: ""
  retryable: false
  details: {}
```

Core errors:

- `AUTH_REQUIRED`
- `AUTH_INVALID`
- `OWNER_MISMATCH`
- `SCHEMA_INVALID`
- `VERSION_CONFLICT`
- `ASSET_NOT_FOUND`
- `ASSET_NOT_READY`
- `ASSET_INVALID_STATE`
- `TRUTH_GATE_BLOCKED`
- `HYBRID_GATE_BLOCKED`
- `AI_PROOF_NOT_ALLOWED`
- `PROVIDER_UNSUPPORTED`
- `IDEMPOTENCY_CONFLICT`
- `JOB_NOT_FOUND`
- `JOB_INVALID_STATE`
- `JOB_CANCEL_NOT_ALLOWED`
- `JOB_NOT_RETRYABLE`
- `UNKNOWN_PROVIDER_STATE`
- `INTERNAL_ERROR`

## 24. Decision Log

| ID | Decision | Status | Phase 2A Result |
| --- | --- | --- | --- |
| D-001 | API base path | APPROVED_FOR_PHASE_2A | Use `/v1/video-jobs`. |
| D-002 | Persistence | APPROVED_FOR_PHASE_2A | SQLite + SQLAlchemy 2.x + Alembic. |
| D-003 | Cancelled spelling | APPROVED_FOR_PHASE_2A | Use `CANCELLED`. |
| D-004 | Processing state name | APPROVED_FOR_PHASE_2A | Use `PROCESSING`. |
| D-005 | GPT Action attachment handling | DECISION_REQUIRED | Public complete endpoint excluded; mock upload flow approved. |
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
| D-025 | Public asset complete endpoint | DECISION_REQUIRED | Not in default Action schema. |

## 25. Remaining Open Questions

- Can Custom GPT Actions directly upload binary attachments, or should Phase 2A
  rely only on mock upload URLs?
- Should a public asset complete endpoint exist after Phase 2A mock testing?
- What is the final retention policy for prompts, asset metadata, result URLs,
  and provider raw payloads?
- Who submits Knowledge 10 review results in Phase 2B/2D?
- What exact real Seedance API fields, status names, callbacks, cancellation,
  result URL behavior, and cost model apply in Phase 2C?
- Should cost confirmation become a separate endpoint before real provider
  submit?

## 26. Coding Blockers Before Phase 2A

The following are true blockers before coding:

- Confirm v0.3 is the approved Phase 2A implementation baseline.
- Confirm that excluding a public asset complete endpoint from the default
  Action schema is acceptable.
- Confirm the six public endpoints are the complete Phase 2A Action surface.

The following are not blockers for Phase 2A mock coding:

- Real Seedance API details.
- Real cost confirmation endpoint.
- Knowledge 10 review submission endpoint.
- Production object storage.
- Multi-tenant auth.

## 27. Approval Checklist

Before starting code, approve:

- v0.3 as the Phase 2A baseline.
- Six public endpoints only.
- Mock asset upload flow with internal-only mock PUT.
- SQLite + SQLAlchemy 2.x + Alembic.
- Bearer API key single-tenant auth.
- `selected_model=Seedance` and `execution_provider=mock` in public Action.
- Structural Truth Enforcement only.
- 24-hour idempotency TTL.
- No public mock scenario selector.
- No modification to frozen Custom GPT files.
