# Backend Master Design Draft v0.2

## 1. Document Status

```yaml
document_status:
  document_version: "v0.2"
  status: "DRAFT"
  supersedes_for_review: "backend/docs/BACKEND_MASTER_DESIGN_DRAFT_v0.1.md"
  overwrites_v0_1: false
  created_for_phase: "Phase 2A"
  repository_model: "monorepo"
  backend_target: "independently deployable FastAPI subproject"
  implementation_allowed_by_this_document: false
  approval_required: true
  contract_version: "PROPOSED:v1"
  truth_rule_version: "PROPOSED:truth-rules-v0.2"
  provider_mapping_version: "PROPOSED:mock-provider-map-v0.2"
```

This draft revises v0.1 without replacing or deleting it. It is a design
baseline candidate only. It does not authorize FastAPI implementation, external
provider integration, database migration, or Custom GPT Builder changes.

## 2. Source Authority Levels

### Runtime Authoritative

These files are authoritative for the existing Custom GPT runtime and must not
be parsed by backend runtime code:

- `custom_gpt_package/multi_category_gpt/00_INSTRUCTIONS/MAIN_INSTRUCTIONS.md`
- `custom_gpt_package/multi_category_gpt/01_KNOWLEDGE_UPLOAD/01-18_*.md`

Runtime authoritative means the current Custom GPT should follow these files.
It does not mean backend code may read them dynamically. Any backend rule must
be translated into versioned JSON contract fields, deterministic code, and
tests.

### Backend Scope Authoritative

These files define repository and backend boundaries for Phase 2A design:

- `AGENTS.md`
- `backend/AGENTS.md`
- `backend/docs/reference/VIDEO_GENERATION_BACKEND_HANDOFF.md`

`VIDEO_GENERATION_BACKEND_HANDOFF.md` is included as the expected Backend
Handoff authority location. Its current repository content is
`CONTENT_PENDING`; therefore the path is authoritative for scope placement, but
the placeholder content is not enough to approve implementation decisions.

### Design Reference

These files inform design but do not independently authorize runtime behavior:

- `README.md`
- `master_design.md`
- `backend/docs/00_SCOPE_AND_BOUNDARIES.md`
- `backend/docs/01_BACKEND_ARCHITECTURE.md`
- `backend/docs/02_API_CONTRACT_DRAFT.md`
- `backend/docs/03_EXISTING_SYSTEM_MAPPING.md`
- `backend/docs/04_PHASE_2A_IMPLEMENTATION_PLAN.md`
- `backend/docs/BACKEND_MASTER_DESIGN_DRAFT_v0.1.md`
- `categories/**`
- `core/**`
- `instructions/**`
- `knowledge/**`
- `workflows/**`

These files may contain historical, source, draft, or duplicated material. They
can guide mapping work, but Phase 2A backend behavior must be expressed in the
approved API contract and implementation tests.

### Third-party / Non-authoritative

These files are not authoritative for backend runtime design:

- `seedance_skills/**`
- `custom_gpt_package/multi_category_gpt/02_SOURCE_FILES/seedance_skills/**`
- `source/open_source/**`

Third-party Seedance source files remain reference material for prompt and
workflow authors. They must not be treated as backend requirements, provider API
schemas, or executable runtime policy.

## 3. Executive Summary

The backend is a deterministic execution boundary for video generation jobs. It
does not replace the Custom GPT's creative reasoning and it must not become a
thin Seedance proxy.

The Custom GPT owns creative analysis, content transfer, script generation,
shot planning, category reasoning, Seedance package drafting, and final
deliverable assembly. The backend owns structured validation, Product Truth
gates, asset references, idempotency, job and attempt state, provider adapter
routing, result normalization, and auditable error responses.

Phase 2A is mock-only. It should prove the contract, state machines,
idempotency, Product Truth gates, and result handling with deterministic tests
before any external service or real Seedance adapter is introduced.

## 4. Existing Runtime Interpretation

`MAIN_INSTRUCTIONS.md` establishes the top-level Custom GPT runtime behavior:
Product Truth and safety override visual ambition, proof-bearing shots require
real proof, AI output cannot fabricate core product proof, Seedance routing is
conditional on `selected_model=Seedance`, and Knowledge 10 review can run only
after actual AI media exists.

Knowledge 01-18 define the GPT reasoning system:

- Knowledge 01-07: viral analysis, category-specific content psychology,
  hooks, visual mechanisms, scripts, scoring, and professional shooting rules.
- Knowledge 08: shot production type routing.
- Knowledge 09: Seedance package drafting after a shot is approved for
  `AI_GENERATION` or `HYBRID` and `selected_model=Seedance`.
- Knowledge 10: post-generation AI media review.
- Knowledge 11-16: category and product routing.
- Knowledge 17: self-contained Seedance reference consolidation for runtime
  knowledge.
- Knowledge 18: final deliverable and output contract.

The backend must not execute this reasoning. It receives structured JSON output
from the Custom GPT and validates only the backend-owned invariants.

## 5. Backend Boundary

The backend must be an independently deployable FastAPI subproject under
`backend/`.

Backend runtime must not:

- Parse Markdown Knowledge, Skills, instructions, or workflows.
- Import prompt logic from the Custom GPT package.
- Treat `seedance_skills/**` or `source/open_source/**` as authoritative.
- Connect to real Seedance in Phase 2A.
- Trust `owner_id` from request body.
- Let public API callers select mock scenarios.

Backend runtime must:

- Accept only versioned JSON contracts.
- Keep `selected_model` separate from `execution_provider`.
- Keep `generation_status` separate from `ai_review_status`.
- Require `Idempotency-Key` for side-effecting or cost-bearing operations.
- Convert Product Truth, HYBRID, and AI proof rules into deterministic fields,
  validators, state transitions, and tests.

## 6. Responsibility Split

| Area | Custom GPT | Backend | Provider |
| --- | --- | --- | --- |
| Creative hook and script | Owns | Does not generate | Does not own |
| Category reasoning | Owns | Receives structured category/support fields | Does not own |
| Shot production plan | Owns proposal | Validates allowed execution boundary | Does not own |
| Product Truth rule text | Owns runtime reasoning | Owns deterministic translated rules | Does not own |
| Asset storage/reference | Provides asset ids or upload flow input | Owns asset records and references | May host result media later |
| Job state | Requests and polls | Owns public job state | Owns provider-native state only |
| Provider submission | Drafts package | Maps approved request to adapter | Executes |
| AI quality review | Knowledge 10 owns review logic | Stores/reports review status | Does not decide review pass |

## 7. Core Phase 2A Decisions

The following changes from v0.1 are adopted as v0.2 proposed baseline:

- Backend Handoff path is included in Backend Scope Authoritative sources.
- `seedance_skills/**` and `source/open_source/**` are non-authoritative.
- Public Job states are fixed to `QUEUED`, `PROCESSING`, `SUCCEEDED`,
  `FAILED`, `CANCELLED`.
- Public Job state `DRAFT` is removed.
- Attempt states own submission, cancellation, and unknown provider state.
- API candidate paths use `/v1/video-jobs`.
- Phase 2A persistence recommendation is fixed to SQLite + SQLAlchemy 2.x +
  Alembic.
- Phase 2A auth recommendation is single-tenant Bearer API key.
- Mock scenario control is internal/test-only.

Items marked `DECISION_REQUIRED` still require human approval before coding.

## 8. Domain Model Overview

| Model | Purpose | Phase 2A Status |
| --- | --- | --- |
| `Asset` | Backend-owned media/reference object. | PROPOSED |
| `JobAssetReference` | Per-job asset usage and proof role binding. | PROPOSED |
| `VideoJob` | Public user-visible generation job. | PROPOSED |
| `JobAttempt` | One provider execution attempt. | PROPOSED |
| `GenerationRequestSnapshot` | Immutable accepted request snapshot. | PROPOSED |
| `IdempotencyRecord` | Duplicate side-effect and cost protection. | PROPOSED |
| `Fact` | Atomic product, claim, or context fact. | PROPOSED |
| `FactProvenance` | Source and trust context for a fact. | PROPOSED |
| `VerificationRecord` | Evidence-backed verification event. | PROPOSED |
| `ProofElement` | Smallest proof obligation linked to fact/shot/job. | PROPOSED |
| `HybridLayerPolicy` | Real/AI layer split and rewrite locks. | PROPOSED |
| `ProviderSubmission` | Normalized adapter request. | PROPOSED |
| `ProviderResult` | Normalized provider output metadata. | PROPOSED |
| `ReviewResult` | Knowledge 10 or future reviewer result. | PROPOSED |
| `ErrorRecord` | Structured error/audit record. | PROPOSED |

## 9. Version Fields

Every accepted job snapshot should include:

```yaml
versioning:
  contract_version: "v1"
  truth_rule_version: "truth-rules-v0.2"
  provider_mapping_version: "mock-provider-map-v0.2"
```

`contract_version` governs request/response schema. `truth_rule_version` governs
deterministic Product Truth and proof validators. `provider_mapping_version`
governs adapter mapping from contract fields to provider submission fields.

Changing any of these may require new compatibility tests and should be
visible in job snapshots.

## 10. Fact Provenance / Verification Model

Facts must be separated from claims, plans, and evidence.

```yaml
fact:
  fact_id: "fact_..."
  fact_type: "sku | accessory | function | material | compatibility | safety | performance | category | user_resource | visual_identity | structure"
  subject: ""
  value: {}
  verification_status: "UNVERIFIED | USER_ASSERTED | PLANNED | VERIFIED | REJECTED | EXPIRED"
  provenance_ids: []
  verification_record_ids: []
```

```yaml
fact_provenance:
  provenance_id: "prov_..."
  fact_id: "fact_..."
  source_type: "USER_INPUT | PRODUCT_SPEC | UPLOADED_ASSET | CONTROLLED_TEST | REVIEW_RESULT | PROVIDER_RESULT | BACKEND_DERIVED"
  source_ref: ""
  captured_at: ""
  trust_level: "LOW | MEDIUM | HIGH"
  notes: ""
```

```yaml
verification_record:
  verification_id: "ver_..."
  fact_id: "fact_..."
  method: "ASSET_REVIEW | CONTROLLED_TEST | SPEC_MATCH | HUMAN_REVIEW | AUTOMATED_METADATA_CHECK"
  evidence_asset_ids: []
  reviewer: "backend | human | custom_gpt | test"
  result: "VERIFIED | REJECTED | INCONCLUSIVE"
  verified_at: ""
  expires_at: null
```

Rules:

- `real_shoot_plan` is a plan, not verified evidence.
- `user_claim` is user assertion, not verified evidence.
- A `Fact` can be usable as context while still unverified.
- Backend gates should block only when execution asks unverified or AI-owned
  material to carry proof.
- Compatibility, identity, and structure are not automatically blocked.
  They are blocked when AI/provider output is asked to invent, rewrite, or prove
  them without approved evidence or lock policy.

## 11. Product Truth And Proof Model

Proof must be modeled at proof-element level. `production_type`,
`presentation_layer`, proof owner, evidence source, and verification status are
separate fields.

```yaml
proof_element:
  proof_id: "proof_..."
  shot_id: "shot_..."
  linked_fact_ids: []
  proof_type: "identity | structure | accessory | function | result | human_efficacy | safety | sterilization | compatibility | before_after | suction | dirt_intake | transparent_bin | pet_hair | gap_access | attachment_performance | measurable_performance"
  production_type: "REAL_SHOOT | AI_GENERATION | HYBRID | STOCK_ASSET"
  presentation_layer: "REAL_CAPTURE | AI_VISUALIZATION | AI_ENVIRONMENT | STOCK_CONTEXT | TEXT_CLAIM"
  proof_owner: "REAL_CAPTURE | CONTROLLED_TEST | VERIFIED_FACT | HUMAN_REVIEW | NONE"
  evidence_source: "UPLOADED_ASSET | RESULT_MEDIA | CONTROLLED_TEST_RECORD | PRODUCT_SPEC | USER_CLAIM | REAL_SHOOT_PLAN | NONE"
  verification_status: "UNVERIFIED | USER_ASSERTED | PLANNED | VERIFIED | REJECTED | NEEDS_REVIEW"
  required_asset_reference_ids: []
  backend_gate_result: "ALLOW | WARN | BLOCK"
```

Interpretation:

- `production_type` describes how the shot is produced.
- `presentation_layer` describes what the viewer sees.
- `proof_owner` describes which layer is allowed to carry proof.
- `evidence_source` describes what supports the proof.
- `verification_status` describes whether evidence has actually been verified.

AI can visualize an already verified structure only when the contract marks it
as `presentation_layer=AI_VISUALIZATION`, links to verified facts/assets, and
does not make AI the `proof_owner`. AI output carrying proof is different and is
blocked for high-truth product proof.

Direct blocks:

- AI-owned suction, dirt intake, transparent bin, before/after, human efficacy,
  sterilization, safety proof, or measurable performance proof.
- HYBRID without a real proof owner for proof-bearing elements.
- Stock media used as product-specific proof.
- Any proof element whose only evidence is `USER_CLAIM` or `REAL_SHOOT_PLAN`
  and whose output would present the claim as verified.

Warnings:

- User-supplied but unverified facts used as context only.
- Identity/structure/compatibility references available but not verified.
- Skeleton category support.
- Result media exists but Knowledge 10 review is still `NOT_RUN`.

## 12. HYBRID And AI Proof Rules

HYBRID must separate layers:

```yaml
hybrid_layer_policy:
  real_layer:
    required: true
    owns: ["identity", "function", "result", "safety"]
    asset_reference_ids: []
  ai_layer:
    allowed_roles: ["environment", "atmosphere", "transition", "non_proof_hook"]
    prohibited_roles: ["core_product_proof", "before_after", "measurable_performance"]
  proof_layer_owner: "REAL_CAPTURE | CONTROLLED_TEST | VERIFIED_FACT"
  ai_must_not_rewrite:
    - "product_shape"
    - "accessory_set"
    - "debris_result"
    - "safety_behavior"
```

The backend should validate structural presence and illegal ownership. It
should not judge creative quality or write prompts.

## 13. Asset Model

`Asset` represents the media object itself, independent of a specific job usage.

```yaml
asset:
  asset_id: "asset_..."
  owner_id: "server_mapped_owner"
  asset_kind: "INPUT_MEDIA | RESULT_MEDIA | REFERENCE"
  content_type: "image/png | image/jpeg | video/mp4 | ..."
  size_bytes: 0
  checksum_sha256: ""
  status: "PENDING_UPLOAD | READY | FAILED | EXPIRED | DELETED"
  secure_url: ""
  url_expires_at: ""
  storage_uri: ""
  created_at: ""
  deleted_at: null
```

Allowed Asset states are only:

- `PENDING_UPLOAD`
- `READY`
- `FAILED`
- `EXPIRED`
- `DELETED`

Upload URL expiry is not the same as Asset expiry. An upload URL can expire
while the Asset remains `PENDING_UPLOAD`. A result access URL can expire while
the Asset remains `READY`; the backend may issue a new secure URL if policy
allows.

## 14. JobAssetReference Model

`JobAssetReference` separates the Asset body from its per-job usage role.

```yaml
job_asset_reference:
  job_asset_reference_id: "jar_..."
  job_id: "job_..."
  asset_id: "asset_..."
  usage_role: "PRODUCT_IDENTITY | FIRST_FRAME | LAST_FRAME | MOTION_REFERENCE | CAMERA_REFERENCE | ENVIRONMENT_REFERENCE | PROOF_EVIDENCE | SOURCE_CLIP | RESULT_MEDIA | REVIEW_TARGET"
  presentation_layer: "REAL_CAPTURE | AI_VISUALIZATION | AI_ENVIRONMENT | STOCK_CONTEXT | RESULT_OUTPUT"
  linked_proof_ids: []
  required_for_truth_gate: false
  lock_policy:
    lock_identity: false
    lock_structure: false
    lock_motion: false
    lock_environment: false
  created_at: ""
```

The same `Asset` may be product identity in one job and first-frame reference in
another. The usage role belongs to `JobAssetReference`, not the Asset.

## 15. Job Creation Gate

Truth and schema gates run before `VideoJob` creation.

If a gate blocks, the backend must not create a `VideoJob`. It returns a
structured HTTP 422 response:

```yaml
status_code: 422
error:
  code: "TRUTH_GATE_BLOCKED"
  message: "Generation request violates Product Truth rules."
  request_id: "req_..."
  field: "proof_elements[0]"
  required_action: "Switch proof-bearing shot to REAL_SHOOT or provide verified evidence."
  retryable: false
  details:
    blocked_reasons: []
    truth_rule_version: "truth-rules-v0.2"
```

`IdempotencyRecord` may store the blocked response so repeated same-key,
same-payload requests return the same 422 response without creating a job.

## 16. VideoJob Model

`VideoJob` is the public generation unit created only after schema, auth,
idempotency, provider eligibility, and truth gates pass.

```yaml
video_job:
  job_id: "job_..."
  owner_id: "server_mapped_owner"
  contract_version: "v1"
  truth_rule_version: "truth-rules-v0.2"
  provider_mapping_version: "mock-provider-map-v0.2"
  selected_model: "Seedance | none | other"
  execution_provider: "mock"
  generation_status: "QUEUED | PROCESSING | SUCCEEDED | FAILED | CANCELLED"
  ai_review_status: "NOT_REQUIRED | NOT_RUN | PASS | REGENERATE | SWITCH_TO_HYBRID | SWITCH_TO_REAL_SHOOT"
  current_attempt_id: ""
  created_at: ""
  updated_at: ""
```

Public Job states are fixed to:

- `QUEUED`
- `PROCESSING`
- `SUCCEEDED`
- `FAILED`
- `CANCELLED`

`DRAFT` is not a public Job state. Pre-job draft, validation, and blocked
states belong to request validation and `IdempotencyRecord`, not `VideoJob`.

## 17. JobAttempt Model

Attempt owns provider submission state and uncertainty.

```yaml
job_attempt:
  attempt_id: "attempt_..."
  job_id: "job_..."
  attempt_no: 1
  execution_provider: "mock"
  provider_model: ""
  provider_job_id: ""
  attempt_status: "PREPARED | SUBMITTED | PROCESSING | SUCCEEDED | FAILED | CANCEL_REQUESTED | CANCELLED | UNKNOWN_PROVIDER_STATE"
  provider_submission_id: ""
  provider_result_id: ""
  error_code: ""
  created_at: ""
  submitted_at: null
  terminal_at: null
```

Attempt states are fixed to:

- `PREPARED`
- `SUBMITTED`
- `PROCESSING`
- `SUCCEEDED`
- `FAILED`
- `CANCEL_REQUESTED`
- `CANCELLED`
- `UNKNOWN_PROVIDER_STATE`

`UNKNOWN_PROVIDER_STATE` belongs to Attempt because the provider submission may
be ambiguous while the public Job can remain `PROCESSING` or eventually
`FAILED` after reconciliation.

## 18. Generation And Review Status Separation

`generation_status` and `ai_review_status` must never be collapsed.

Generation states describe backend/provider execution. Review states describe
Knowledge 10 or future reviewer judgment after actual AI media exists.

Rules:

- Provider success does not imply `ai_review_status=PASS`.
- Prompt, storyboard, or Seedance package cannot receive `PASS`.
- No-AI jobs use `ai_review_status=NOT_REQUIRED`.
- AI jobs start at `ai_review_status=NOT_RUN` after generated media exists.
- Review update APIs are `DECISION_REQUIRED` and not in the default Phase 2A
  Custom GPT Action schema.

## 19. Provider Abstraction

Field separation is mandatory:

- `selected_model`: creative/model intent from the Custom GPT plan.
- `execution_provider`: backend adapter used to execute the job.
- `provider_model`: provider-native model identifier.

Phase 2A supports only:

```yaml
execution_provider: "mock"
```

Mock scenario control must not appear in the public Custom GPT Action schema.
It may be controlled only by test injection or internal development
configuration.

## 20. ProviderResult As RESULT_MEDIA Asset

Provider output must normalize into a `ProviderResult` and at least one
`RESULT_MEDIA` Asset.

```yaml
provider_result:
  provider_result_id: "pr_..."
  attempt_id: "attempt_..."
  provider_job_id: ""
  normalized_status: "SUCCEEDED | FAILED | UNKNOWN_PROVIDER_STATE"
  result_asset_ids: []
  raw_payload_ref: ""
  received_at: ""
```

```yaml
result_media_asset:
  asset_kind: "RESULT_MEDIA"
  status: "READY"
  secure_url: "https://..."
  url_expires_at: ""
  checksum_sha256: ""
  content_type: "video/mp4"
  size_bytes: 0
```

Secure URL expiry does not automatically expire the Asset. If the secure URL
expires, the Asset can remain `READY` and receive a refreshed access URL when
authorized.

## 21. Idempotency And Cost Protection

All operations that may mutate state, create assets, trigger generation, retry,
cancel provider work, or create future cost must require `Idempotency-Key`.

Scope:

- server-mapped `owner_id`
- HTTP method and endpoint
- idempotency key
- canonical payload hash
- contract version

Behavior:

- Same key plus same canonical payload returns the original response.
- Same key plus different canonical payload returns `IDEMPOTENCY_CONFLICT`.
- Gate-blocked 422 responses may be stored.
- A pending idempotency record must not trigger duplicate provider calls.
- Idempotency must be persisted in SQLite in Phase 2A, not only memory.

## 22. Persistence Decision

Phase 2A persistence recommendation is fixed:

```yaml
persistence:
  phase_2a: "SQLite + SQLAlchemy 2.x + Alembic"
  in_memory_usage: "unit_tests_only"
  postgres: "future_phase_decision_required"
```

Rationale:

- Idempotency must survive service restart in realistic local tests.
- Alembic forces schema discipline before external providers.
- SQLAlchemy 2.x keeps a later PostgreSQL migration feasible.
- In-memory state is acceptable only for isolated unit tests.

## 23. Authentication And Ownership

Phase 2A auth model:

```yaml
auth:
  mode: "single_tenant_bearer_api_key"
  owner_id_source: "server_side_api_key_mapping"
  request_body_owner_id_trusted: false
```

Rules:

- Custom GPT Action authenticates with Bearer API key.
- `owner_id` comes from server-side mapping.
- If request body includes `owner_id`, backend ignores it or rejects it.
- Assets, jobs, idempotency records, and results are owner-scoped.
- Logs must redact secrets, signed URLs, provider raw payloads, and sensitive
  prompt fields where practical.

Multi-tenant auth, OAuth, users, roles, and billing identity are
`DECISION_REQUIRED` for later phases.

## 24. API Surface Candidate

Default Phase 2A Action candidate paths:

| Operation | Method | Path | Auth | Idempotency | Default Action Schema |
| --- | --- | --- | --- | --- | --- |
| health | GET | `/health` | none or optional | no | yes |
| upload URL | POST | `/v1/assets/upload-url` | Bearer | required | yes |
| create job | POST | `/v1/video-jobs` | Bearer | required | yes |
| get job | GET | `/v1/video-jobs/{job_id}` | Bearer | no | yes |
| cancel job | POST | `/v1/video-jobs/{job_id}/cancel` | Bearer | required | yes |
| retry job | POST | `/v1/video-jobs/{job_id}/retry` | Bearer | required | yes |

Asset completion endpoint remains `DECISION_REQUIRED`:

```yaml
pending_endpoint:
  method: "POST"
  path: "/v1/assets/{asset_id}/complete"
  status: "DECISION_REQUIRED"
  default_custom_gpt_action_schema: false
```

The upload completion model depends on how Custom GPT Actions handle file
attachments and whether the backend uses direct upload, mock upload, or future
object storage.

## 25. Request Contract Draft

Create job request concept:

```yaml
create_video_job_request:
  contract_version: "v1"
  truth_rule_version: "truth-rules-v0.2"
  provider_mapping_version: "mock-provider-map-v0.2"
  selected_model: "Seedance | other"
  execution_provider: "mock"
  task_type: "APPROVED_SHOT_TO_GENERATION_PACKAGE"
  category:
    primary_category: ""
    product_pack: ""
    support_level: ""
  generation_plan:
    production_type: "AI_GENERATION | HYBRID"
    seedance_package: {}
    prompt: ""
  facts: []
  proof_elements: []
  assets: []
  job_asset_references: []
  hybrid_layer_policy: null
```

Backend validation order:

1. Auth and owner mapping.
2. Idempotency lookup.
3. Schema and enum validation.
4. Version compatibility.
5. Asset ownership/readiness validation.
6. Fact provenance and proof validation.
7. HYBRID layer validation.
8. Provider eligibility.
9. Create `VideoJob`, snapshot, first `JobAttempt`.

If any gate blocks before step 9, no `VideoJob` is created.

## 26. Error Model

Unified error structure:

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

Key error codes:

- `AUTH_REQUIRED`
- `AUTH_INVALID`
- `OWNER_MISMATCH`
- `SCHEMA_INVALID`
- `VERSION_UNSUPPORTED`
- `TRUTH_GATE_BLOCKED`
- `HYBRID_GATE_BLOCKED`
- `AI_PROOF_NOT_ALLOWED`
- `UNVERIFIED_PROOF_EVIDENCE`
- `ASSET_NOT_FOUND`
- `ASSET_NOT_READY`
- `ASSET_INVALID_STATE`
- `IDEMPOTENCY_CONFLICT`
- `IDEMPOTENCY_PENDING`
- `PROVIDER_UNSUPPORTED`
- `JOB_NOT_FOUND`
- `JOB_INVALID_STATE`
- `JOB_NOT_RETRYABLE`
- `JOB_CANCEL_NOT_ALLOWED`
- `UNKNOWN_PROVIDER_STATE`

## 27. Testing Strategy

Phase 2A tests should cover:

- Contract version validation.
- Truth rule version validation.
- Provider mapping version validation.
- `selected_model` versus `execution_provider` separation.
- Gate block returns 422 and creates no `VideoJob`.
- Gate-blocked idempotency returns same 422 for same key and payload.
- `USER_CLAIM` alone cannot verify proof.
- `REAL_SHOOT_PLAN` alone cannot verify proof.
- AI visualization of verified structure allowed only as presentation, not
  proof owner.
- Compatibility/identity/structure context does not auto-block unless AI is
  asked to prove or rewrite it.
- Job states exclude `DRAFT`.
- Attempt states include `UNKNOWN_PROVIDER_STATE`.
- Result media is represented as `RESULT_MEDIA` Asset.
- Mock scenario cannot be supplied through public API schema.
- SQLite idempotency survives restart in integration tests.
- In-memory persistence is used only in unit tests.

## 28. Deployment Shape

Phase 2A is local/mock backend only:

- FastAPI subproject under `backend/` in a monorepo.
- SQLite database file for local development.
- Alembic migrations.
- Bearer API key configured through environment.
- Mock provider only.
- No real Seedance, storage, queue, Redis, billing, or external provider calls.

Any hosted HTTPS deployment, object storage, callback receiver, or real provider
adapter is `DECISION_REQUIRED`.

## 29. Decision Log

| ID | Decision | Status | v0.2 Recommendation | Notes |
| --- | --- | --- | --- | --- |
| D-001 | API base path | PROPOSED | `/v1/video-jobs` | Revises v0.1 `/v1/video-generation-jobs`. |
| D-002 | Phase 2A persistence | PROPOSED | SQLite + SQLAlchemy 2.x + Alembic | In-memory only for unit tests. |
| D-003 | Cancelled spelling | PROPOSED | `CANCELLED` | British spelling fixed for API enum. |
| D-004 | Processing state name | PROPOSED | `PROCESSING` | Public Job and Attempt use same word. |
| D-005 | GPT Action attachment handling | DECISION_REQUIRED | Upload URL first; asset complete endpoint pending | Actual attachment behavior unverified. |
| D-006 | Owner identity source | PROPOSED | Server-side API key mapping | Body `owner_id` is not trusted. |
| D-007 | Cost confirmation timing | DECISION_REQUIRED | Before real provider submit | Not needed for mock-only Phase 2A. |
| D-008 | Review result source | DECISION_REQUIRED | Future mixed reviewer model | Review endpoint not default Phase 2A Action. |
| D-009 | Retry semantics | PROPOSED | Same job, new attempt when payload unchanged | Changed creative payload creates new job. |
| D-010 | Real Seedance fields | DECISION_REQUIRED | Defer | No real provider integration in Phase 2A. |
| D-011 | Backend Handoff authority | DECISION_REQUIRED | Handoff path included; content pending | Placeholder is not approved requirements. |
| D-012 | Authority levels | PROPOSED | Runtime, Backend Scope, Design Reference, Third-party | `seedance_skills` and `source/open_source` non-authoritative. |
| D-013 | Proof model split | PROPOSED | Split production, layer, owner, evidence, verification | Prevents AI presentation from becoming AI proof. |
| D-014 | Fact provenance model | PROPOSED | Add Fact, FactProvenance, VerificationRecord | `USER_CLAIM` and `REAL_SHOOT_PLAN` are not verified. |
| D-015 | JobAssetReference | PROPOSED | Separate Asset body from job usage role | Supports reused assets and per-job proof roles. |
| D-016 | Asset states | PROPOSED | `PENDING_UPLOAD`, `READY`, `FAILED`, `EXPIRED`, `DELETED` | URL expiry is separate from Asset expiry. |
| D-017 | Gate block behavior | PROPOSED | No job on blocked gate; structured 422 | Idempotency may store blocked response. |
| D-018 | Public/attempt state split | PROPOSED | Public Job five states; Attempt owns submit/cancel/unknown | Removes public `DRAFT`. |
| D-019 | Mock scenario control | PROPOSED | Test injection or internal dev config only | Must not enter Custom GPT Action schema. |
| D-020 | ProviderResult result media | PROPOSED | Normalize outputs as `RESULT_MEDIA` Assets | Include secure URL, expiry, checksum, type, size. |

## 30. Open Questions

- What approved content should replace the current
  `VIDEO_GENERATION_BACKEND_HANDOFF.md` placeholder?
- Can Custom GPT Actions upload binary attachments directly, or must all media
  use upload URLs?
- Should `/v1/assets/{asset_id}/complete` exist in Phase 2A, and if yes, who
  calls it?
- What TTL should apply to upload URLs, result URLs, idempotency records, and
  result assets?
- Should health be `/health` only, or should `/v1/health` also exist as an
  alias?
- What exact fields from Knowledge 18 should be mandatory in the first Action
  schema?
- Who will submit Knowledge 10 review results after actual media exists?
- What is the retention policy for prompts, provider raw payload refs, secure
  URLs, and generated result metadata?
- What is the final naming and governance process for `truth_rule_version`?
- What is the final naming and governance process for
  `provider_mapping_version`?
- When real Seedance begins, what official API fields, status names, callback
  semantics, result URL behavior, and cancellation semantics apply?

## 31. Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Handoff placeholder is mistaken for approved requirements. | Premature implementation. | Keep `CONTENT_PENDING` and require D-011 approval. |
| Third-party Seedance docs are treated as backend API truth. | False provider assumptions. | Mark `seedance_skills/**` and `source/open_source/**` non-authoritative. |
| AI visualization is confused with AI proof. | Product Truth violation. | Split presentation layer from proof owner. |
| `USER_CLAIM` or `REAL_SHOOT_PLAN` treated as verified. | Fake proof. | Fact provenance and verification status required. |
| Gate block creates a job anyway. | Polling and audit confusion. | 422 before job creation; store only idempotency response. |
| Upload URL expiry is treated as Asset expiry. | Lost assets or bad retries. | Separate URL expiry fields from Asset status. |
| Mock scenario leaks into public Action schema. | Users can force fake success/failure. | Internal config or test injection only. |
| Owner id trusted from body. | Cross-owner asset/job leak. | Server-side API key mapping only. |
| SQLite used beyond its approved phase. | Concurrency and ops risk. | Mark PostgreSQL/multi-user deployment as later decision. |
| Provider success auto-sets review pass. | Quality/safety review bypass. | Keep generation and AI review statuses separate. |

## 32. Approval Checklist

Before Phase 2A implementation, approve or resolve:

- D-011 Backend Handoff content.
- D-001 API base path `/v1/video-jobs`.
- D-002 SQLite + SQLAlchemy 2.x + Alembic.
- D-003 `CANCELLED` enum spelling.
- D-005 attachment/upload/asset completion behavior.
- D-006 single-tenant Bearer API key and server-side owner mapping.
- D-013 proof model split.
- D-014 fact provenance and verification model.
- D-015 `JobAssetReference` model.
- D-017 no-job-on-gate-block behavior.
- D-019 mock scenario control boundary.
- Contract/version field names and initial values.
- Logging and redaction policy.
- Whether v0.2 becomes the approved baseline for Phase 2A coding.
