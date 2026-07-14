# Backend Master Design Draft v0.1

## 1. Document Status

```yaml
document_status:
  document_version: "v0.1"
  status: "DRAFT"
  created_for_phase: "Phase 2A-0"
  repository_model: "monorepo"
  backend_target: "independently deployable FastAPI subproject"
  approval_required: true
```

### Source Documents

Read for this draft:

- `AGENTS.md`
- `backend/AGENTS.md`
- all third-party `source/open_source/**/AGENTS.md`
- `README.md`
- `master_design.md`
- `custom_gpt_package/multi_category_gpt/00_INSTRUCTIONS/MAIN_INSTRUCTIONS.md`
- `custom_gpt_package/multi_category_gpt/01_KNOWLEDGE_UPLOAD/01-18_*.md`
- `core/**`
- `categories/**`
- `workflows/**`
- `seedance_skills/**`
- `backend/docs/00_SCOPE_AND_BOUNDARIES.md`
- `backend/docs/01_BACKEND_ARCHITECTURE.md`
- `backend/docs/02_API_CONTRACT_DRAFT.md`
- `backend/docs/03_EXISTING_SYSTEM_MAPPING.md`
- `backend/docs/04_PHASE_2A_IMPLEMENTATION_PLAN.md`

Expected but missing:

- `backend/docs/reference/VIDEO_GENERATION_BACKEND_HANDOFF.md`

### Authoritative Documents

These are authoritative for the existing Custom GPT runtime:

- `custom_gpt_package/multi_category_gpt/00_INSTRUCTIONS/MAIN_INSTRUCTIONS.md`
- `custom_gpt_package/multi_category_gpt/01_KNOWLEDGE_UPLOAD/01-18_*.md`

These are authoritative source/reference documents for current repo structure:

- `README.md`
- `core/**`
- `categories/**`
- `workflows/**`
- `seedance_skills/**`

### Non-Authoritative Drafts

The following documents are DRAFT_REFERENCE only. They informed this design but
do not freeze backend architecture:

- `backend/docs/00_SCOPE_AND_BOUNDARIES.md`
- `backend/docs/01_BACKEND_ARCHITECTURE.md`
- `backend/docs/02_API_CONTRACT_DRAFT.md`
- `backend/docs/03_EXISTING_SYSTEM_MAPPING.md`
- `backend/docs/04_PHASE_2A_IMPLEMENTATION_PLAN.md`

### Unresolved Decisions

All choices marked `DECISION_REQUIRED` must be approved before Phase 2A coding.

## 2. Executive Summary

The backend solves execution, safety, state, idempotency, asset, provider, and
result-tracking problems that the Custom GPT should not solve inside prompt
logic.

The backend must not be a thin Seedance API proxy. A proxy would forward prompts
without enforcing Product Truth, HYBRID proof ownership, status separation,
asset ownership, idempotency, retry safety, or cost protection. This system needs
a domain backend: it receives the Custom GPT's structured plan, validates it,
decides whether execution is allowed, stores immutable request snapshots, routes
to a provider adapter, records attempts, and returns auditable state.

The final system should provide:

- Custom GPT creative planning and contract output.
- Backend deterministic guardrails and job execution.
- Provider abstraction with mock first and real Seedance later.
- Review integration that keeps generation completion separate from Knowledge
  10 quality review.

Phase relationship:

- Phase 2A-0: this master design draft.
- Phase 2A: API contract, schemas, validators, mock backend.
- Phase 2B: Custom GPT Action integration against mock backend.
- Phase 2C: real Seedance adapter design and implementation.
- Phase 2D: end-to-end generation, review, and operating feedback loop.

## 3. Existing System Interpretation

### MAIN_INSTRUCTIONS Role

`MAIN_INSTRUCTIONS.md` is the top-level runtime instruction for the Custom GPT.
It defines role, task routing, category routing, support levels, Product Truth,
production types, Seedance routing, AI review timing, scoring, and final
delivery behavior.

The backend must not parse this file at runtime. Its rules must be translated
into explicit API fields and deterministic validators.

### Knowledge 01-18 Role

Knowledge files define the GPT's reasoning system:

- 01: viral analysis.
- 02-04: automotive-specific psychology, hooks, visual mechanisms.
- 05: script writing.
- 06: commercial scoring.
- 07: professional shot language.
- 08: shot production planning and production type routing.
- 09: Seedance package drafting after routing.
- 10: AI material quality review after actual media exists.
- 11: category and main router bundle.
- 12: automotive category pack.
- 13: car vacuum product pack.
- 14-16: skeleton packs for home, steam, and beauty.
- 17: self-contained Seedance reference pack.
- 18: final delivery and output contract.

### Custom GPT And Backend Boundary

Custom GPT owns creative reasoning, content transfer, scripts, shot contracts,
and generation package drafting. Backend owns deterministic enforcement, asset
and job operations, idempotency, provider dispatch, state transitions, error
model, and audit trail.

### Rules That Need Backend Translation

Backend translation candidates:

- Production type enum.
- Readiness status enum.
- Selected model enum.
- Execution provider enum.
- Truth dependency.
- Proof type, proof owner, proof evidence source.
- HYBRID real/AI/proof layer policy.
- Seedance route eligibility.
- AI review status timing.
- Claim evidence and blocking rules.
- Idempotency and cost-protection rules.

### Skills That Should Not Enter Backend

The backend must not import, parse, execute, or treat as runtime config:

- `seedance_skills/reference-workflow.md`
- `seedance_skills/seedance-prompt/SKILL.md`
- `seedance_skills/seedance-camera/SKILL.md`
- `seedance_skills/seedance-motion/SKILL.md`
- `custom_gpt_package/multi_category_gpt/02_SOURCE_FILES/seedance_skills/**`
- `source/open_source/**/SKILL.md`

Seedance skills are prompt/reference authoring material, not backend execution
logic.

### File Relationship

Formal runtime upload files live in `custom_gpt_package/multi_category_gpt/`.
Source files live in `knowledge/`, `instructions/`, `categories/`, `workflows/`,
and `seedance_skills/`. Audit copies live under
`custom_gpt_package/multi_category_gpt/02_SOURCE_FILES/`. Historical material
lives under `archive/` and must not be treated as current runtime truth.

## 4. Business Goals And Non-Goals

### Current Goal

Create a candidate backend master design that preserves the existing GPT system
while defining a clean backend execution boundary.

### Phase 2A Goal

Build only a mock backend with versioned JSON contracts, deterministic
validators, state machines, idempotency, and mock provider behavior.

### Long-Term Goal

Support paid provider execution safely, starting with Seedance, while preserving
Product Truth and ensuring that generation, review, costs, assets, retries, and
audit trails are controlled by backend code rather than prompt text.

### Explicit Non-Goals

- No real Seedance integration in Phase 2A.
- No provider billing.
- No external storage.
- No real database until approved.
- No runtime Markdown parsing.
- No Custom GPT creative logic inside backend.
- No automatic upgrade of skeleton categories into complete product support.

### Scope Control Rules

Any proposal that requires external services, real costs, database migration,
new provider fields, or GPT Builder changes is `DECISION_REQUIRED`.

## 5. Actors And Clients

| Actor | Can Do | Cannot Do |
| --- | --- | --- |
| User | Provide product facts, assets, approval, prompts, retry intent. | Bypass truth gates or force fake proof. |
| Custom GPT | Analyze, route, write scripts, produce shot contracts, draft Seedance package. | Execute generation, charge money, decide backend state by prose. |
| Custom GPT Action | Send versioned JSON to backend. | Assume binary attachment forwarding is available until verified. |
| Backend | Validate, persist, enforce gates, dispatch provider, expose job state. | Invent creative claims or parse Knowledge Markdown at runtime. |
| Mock Provider | Simulate provider execution deterministically in Phase 2A. | Represent real Seedance capability or cost. |
| Future Seedance Provider | Execute approved provider submissions. | Override backend truth gates or proof ownership. |
| Future Web UI | Manage assets, jobs, approvals, status views. | Replace Product Truth validation. |
| Post-generation reviewer | Submit or record Knowledge 10 review results. | Mark prompt-only plans as review `PASS`. |

## 6. End-To-End Business Flows

Each flow below is `PROPOSED`.

| Flow | Preconditions | Input | Validation Order | State Changes | Output | Errors | Idempotency | Cost |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1. No-asset mock job | GPT has AI/HYBRID non-proof plan; provider mock. | Create job without assets. | Auth, schema, idempotency, readiness, truth gate, provider gate. | Job `DRAFT/QUEUED`; Attempt `QUEUED`. | job id, status, warnings. | Missing proof asset if proof required; unsupported provider. | Required on create. Same key+payload returns same job. | No real cost in Phase 2A. |
| 2. Request upload URL | Client needs asset handle. | owner, role, content type, size, checksum. | Auth, schema, idempotency, size/type, owner scope. | Asset `PENDING_UPLOAD`. | upload URL or mock URL, asset id, expiry. | unsupported type, too large, unsafe URL. | Required. | No real cost; future storage cost possible. |
| 3. Complete upload | Asset bytes or mock completion exists. | asset id, checksum, metadata. | Auth, owner, checksum, content type, status. | Asset `READY` or `FAILED`. | ready asset. | checksum mismatch, expired, owner mismatch. | Recommended. | Possible storage cost later. |
| 4. Job with asset | READY asset exists. | create job referencing assets. | Auth, idempotency, asset owner/readiness, truth gate. | Job and Attempt created. | accepted job. | asset not ready, wrong role, expired. | Required. | Mock no cost. |
| 5. HYBRID job | real proof asset and AI layer plan exist. | hybrid policy with real/AI layers. | Auth, schema, asset gate, HYBRID gate, truth gate. | Job accepted only if proof owner is real. | job with proof ownership. | missing layer, AI owns proof, rewrite lock missing. | Required. | Mock no cost; real cost later. |
| 6. Product Truth block | Request delegates proof to AI. | proof elements requiring real evidence. | Truth gate before provider submission. | Job may be `REJECTED` or not created; `DECISION_REQUIRED`. | structured error. | truth gate violation. | Same key returns same rejection. | No cost; provider not called. |
| 7. Duplicate submit | Same client resends. | same key and canonical payload. | Idempotency before side effects. | No new job/attempt. | original response. | same key different payload -> conflict. | Required. | Prevents double charge. |
| 8. Query job | Job exists. | job id. | Auth, owner, existence. | none. | job, attempts, statuses. | not found, owner mismatch. | Not required. | No cost. |
| 9. Cancel job | Job cancelable. | job id, reason. | Auth, owner, idempotency, state gate. | Job/Attempt `CANCEL_REQUESTED` then `CANCELED` or terminal unchanged. | cancel result. | terminal state, provider unknown. | Required. | Future provider may charge if already submitted. |
| 10. Retry failed | Attempt failed or timed out. | job id, retry policy. | Auth, idempotency, job state, payload snapshot, cost confirmation. | New Attempt under same Job. | retry attempt id. | non-retryable, changed prompt, missing confirmation. | Required. | Possible cost later; mock no cost. |
| 11. Success before review | Generation succeeded, no Knowledge 10 review. | provider result. | Provider result mapping. | `generation_status=SUCCEEDED`; `ai_review_status=NOT_RUN`. | media result, review needed. | none. | Provider callback/query idempotent. | Real cost may already exist later. |
| 12. Real Seedance cost confirmation | Future real provider selected. | estimate, duration, model, user confirmation. | Auth, estimate, confirmation, idempotency, provider gate. | `COST_CONFIRMATION_REQUIRED` then submitted if approved. | confirmation record. | no confirmation, stale estimate. | Required before submit. | Yes. |
| 13. Provider timeout/unknown | Provider submit or poll uncertain. | provider submission id or timeout. | Provider id lookup before resubmit. | Attempt `UNKNOWN_PROVIDER_STATE`. | retry instructions. | duplicate risk, unknown result. | Required; never blind resubmit. | Prevent duplicate charge. |
| 14. Prompt changed and regenerate | User changes creative request. | changed prompt/package. | Compare canonical payload to prior snapshot. | New Job recommended; not retry. | new job id. | same idempotency key with different payload. | New key required. | Future cost possible. |

## 7. System Boundary

Custom GPT owns creative and planning output. Backend owns execution permission,
asset readiness, idempotency, state, provider abstraction, and audit. Provider
owns only provider-side execution and provider-native results. Knowledge 10 owns
AI material review after actual media exists. Future Web UI owns user-facing
job/asset management and human confirmations.

No layer may assume another layer's authority. In particular, provider success
does not imply review pass, and GPT prose does not override backend gates.

## 8. Domain Model

All models are candidate models.

| Model | Purpose | Main Fields | Owner | Lifecycle | Relationships | Persistence | Open Questions |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Asset | Track uploaded or referenced media. | asset_id, owner_id, role, content_type, size, checksum, status, URLs, expires_at. | Backend. | requested, uploaded, ready, expired, deleted. | Used by jobs and proof elements. | Required if assets exist. | Binary upload support from GPT Action. |
| AssetRole | Explain asset purpose. | product_identity, first_frame, last_frame, motion_reference, environment, proof_evidence, audio_tempo. | Backend contract. | immutable per job snapshot. | Attached to Asset. | Stored with Asset/Job. | Role taxonomy approval. |
| VideoJob | User-visible generation unit. | job_id, owner_id, contract_version, selected_model, execution_provider, statuses. | Backend. | created to terminal. | Has attempts, snapshots, assets. | Required. | Whether successful jobs can retry. |
| JobAttempt | One provider submission try. | attempt_id, job_id, attempt_no, provider, status, provider_job_id. | Backend. | queued, submitted, running, terminal or unknown. | Belongs to VideoJob. | Required. | Retry limit. |
| GenerationRequestSnapshot | Immutable copy of accepted request. | payload_hash, prompt, seedance_package, policies, assets, created_at. | Backend. | created once per job/attempt. | Used by idempotency and audit. | Required. | Redaction depth. |
| IdempotencyRecord | Prevent duplicate side effects. | key, scope, owner_id, canonical_hash, response_ref, expires_at. | Backend. | pending, completed, conflict, expired. | Points to job/asset/cancel/retry. | Required for cost safety. | TTL and persistence choice. |
| ProofElement | Smallest proof requirement. | proof_id, proof_type, subject, required_owner, evidence_source, status. | GPT proposes; backend validates. | proposed, accepted, blocked, reviewed. | Many per shot/job. | Required in snapshot. | Granularity by shot or element. |
| TruthContext | Product facts and claim boundaries. | category, product_type, sku, verified_facts, unverified_facts, risks. | GPT proposes; backend validates. | snapshot per request. | Feeds proof validation. | Required in snapshot. | Fact source trust model. |
| HybridPolicy | Layer ownership contract. | real_layer, ai_layer, proof_layer_owner, ai_must_not_rewrite. | GPT proposes; backend validates. | required for HYBRID. | Connected to proof elements and assets. | Required for HYBRID. | Whether per-shot or per-proof. |
| ProviderSubmission | Normalized provider request. | submission_id, attempt_id, provider_model, mode, payload, submitted_at. | Backend. | prepared, submitted, accepted, rejected. | One per attempt. | Required for real provider. | Seedance field mapping unknown. |
| ProviderResult | Provider output. | result_id, provider_job_id, media_assets, status, error, raw_ref. | Backend/provider. | pending, received, normalized. | Updates attempt/job. | Required. | Raw payload retention. |
| ReviewResult | Knowledge 10 or reviewer outcome. | review_id, job_id, media_asset_id, ai_review_status, findings. | Reviewer/backend. | not_required, not_run, reviewed. | Belongs to job/media. | Required after real media. | Reviewer source. |
| ErrorRecord | Auditable error. | code, message, field, request_id, retryable, details. | Backend. | created on failure. | Linked to request/job/attempt. | Recommended. | Retention. |
| CostConfirmation | Human approval for potential cost. | confirmation_id, estimate, model, duration, approved_by, expires_at. | User/backend. | required, approved, declined, expired. | Required before real provider submit. | Required for real cost. | Confirmation UX. |

The existing API draft is not expressive enough for multiple proof elements,
multiple asset roles, multiple proof owners, or repeated attempts. The master
design therefore recommends proof-element and attempt-level modeling.

## 9. Product Truth And Proof Model

### Candidate Fields

```yaml
truth_context:
  truth_dependency: "low | medium | high"
  product_identity:
    sku_id: ""
    brand: ""
    visible_structure: []
    verified_accessories: []
    unverified_accessories: []
  facts:
    verified: []
    unverified: []
    blocked_claims: []
  safety:
    safety_level: "low | medium | high"
    material_constraints: []
    compatibility_constraints: []
```

```yaml
proof_element:
  proof_type: "identity | structure | accessory | function | result | human_efficacy | safety | sterilization | compatibility | before_after | transparent_bin | suction | dirt_intake"
  proof_subject: ""
  proof_owner: "REAL_SHOOT | AI_GENERATION | HYBRID_REAL_LAYER | STOCK_ASSET | NONE"
  evidence_source: "uploaded_asset | real_shoot_plan | verified_fact | controlled_test | user_claim | none"
  required_asset_roles: []
  status: "PROPOSED | ACCEPTED | BLOCKED | WARNING"
  backend_validation: []
```

Proof should be modeled at proof-element level, linked to shot and job. A single
shot may have several proof elements, such as product identity, accessory
verification, dirt intake, and transparent-bin result. This avoids one broad
`core_product_proof` boolean hiding mixed ownership.

### Production Type Rules

| Production Type | Allowed | Blocked |
| --- | --- | --- |
| `REAL_SHOOT` | All high-truth proof if real evidence exists. | Claims without evidence. |
| `AI_GENERATION` | Non-proof hook, atmosphere, environment, transition. | Core proof, identity rewrite, result proof, human efficacy. |
| `HYBRID` | Real proof layer plus AI environment/atmosphere. | Undefined real layer, AI-owned proof, missing rewrite locks. |
| `STOCK_ASSET` | Generic non-proof B-roll, transitions, atmosphere. | Core product proof. |

### Direct Blocks

Block when AI owns suction, dirt intake, transparent bin, Before/After, human
efficacy, sterilization, compatibility, product structure, accessories, safety,
or measurable performance proof.

### Warnings

Warn when facts are user-supplied but not verified, when category support is
`PARTIAL`, when product pack is missing, when asset roles are weak, or when
future review is required.

### Field Source

GPT provides proposed fields. Backend validates structure and deterministic gate
rules. Backend must not rely on prompt keyword scanning as the core validator.

## 10. Asset Design

Candidate asset fields:

- `asset_id`
- `owner_id`
- `role`
- `content_type`
- `size_bytes`
- `checksum_sha256`
- `status`
- `upload_url`
- `external_url`
- `mock_storage_uri`
- `reference_assets`
- `expires_at`
- `metadata`

Candidate roles:

- `PRODUCT_IDENTITY`
- `FIRST_FRAME`
- `LAST_FRAME`
- `MOTION_REFERENCE`
- `CAMERA_REFERENCE`
- `ENVIRONMENT_REFERENCE`
- `PROOF_EVIDENCE`
- `AUDIO_TEMPO`
- `SOURCE_CLIP`
- `RESULT_MEDIA`

Asset states should distinguish requested URL, upload pending, uploaded, ready,
failed, expired, and deleted. Ownership isolation is mandatory: an owner may not
reference another owner's asset id.

`DECISION_REQUIRED`: Custom GPT Action binary attachment handling is unverified.
Do not assume the Action can forward chat attachments directly. Phase 2A can use
mock asset ids and mock upload URLs.

## 11. Job And Attempt Model

`PROPOSED`: separate Job from Attempt.

Job represents user intent and stable request snapshot. Attempt represents one
provider execution. Retry creates a new attempt under the same job only when the
prompt and proof policy are unchanged. If prompt, proof ownership, assets, or
Seedance package materially changes, create a new job.

Retry safety:

- Same failed job, same canonical payload, new idempotency key -> new attempt.
- Same idempotency key and same payload -> same retry response.
- Same idempotency key and different payload -> `IDEMPOTENCY_CONFLICT`.
- Successful jobs are not retryable by default; regenerate with changes creates
  a new job.
- Canceled jobs are retryable only if no provider cost was incurred or if a new
  cost confirmation is recorded.

`provider_job_id` belongs to Attempt, not Job. Prompt and request snapshot must
be saved per Job and per Attempt if provider mapping changes.

## 12. State Machines

### Asset State Machine

States:

- `UPLOAD_URL_REQUESTED`
- `PENDING_UPLOAD`
- `UPLOADED`
- `READY`
- `FAILED`
- `EXPIRED`
- `DELETED`

Legal transitions:

- requested -> pending -> uploaded -> ready
- pending -> expired
- uploaded -> failed
- ready -> expired
- ready -> deleted

Illegal transitions:

- failed -> ready without re-upload
- expired -> ready without new upload URL
- deleted -> any active state

Errors: `ASSET_INVALID_STATE`, `ASSET_EXPIRED`, `ASSET_OWNER_MISMATCH`.

### Video Job State Machine

`PROPOSED` states:

- `DRAFT`
- `QUEUED`
- `PROCESSING`
- `SUCCEEDED`
- `FAILED`
- `CANCEL_REQUESTED`
- `CANCELED`
- `UNKNOWN_PROVIDER_STATE`

Legal transitions:

- draft -> queued -> processing -> succeeded
- draft/queued/processing -> failed
- queued/processing -> cancel_requested -> canceled
- processing -> unknown_provider_state
- failed -> queued only through retry attempt

Illegal transitions:

- succeeded -> processing
- canceled -> processing without new retry decision
- unknown_provider_state -> new provider submit without reconciliation

Errors: `JOB_INVALID_STATE`, `JOB_NOT_RETRYABLE`, `JOB_CANCEL_NOT_ALLOWED`.

Naming decisions:

- `PROCESSING` is recommended over `RUNNING` for API clarity, but
  `DECISION_REQUIRED`.
- `CANCELED` is recommended for American English consistency, but
  `DECISION_REQUIRED`.
- `DRAFT` is useful before provider submission, but `DECISION_REQUIRED`.
- `SUBMITTED` may be an Attempt state rather than Job state.
- `UNKNOWN_PROVIDER_STATE` is recommended for timeout/callback ambiguity.

### Attempt State Machine

States:

- `PREPARED`
- `QUEUED`
- `SUBMITTED`
- `PROCESSING`
- `SUCCEEDED`
- `FAILED`
- `CANCEL_REQUESTED`
- `CANCELED`
- `TIMEOUT`
- `UNKNOWN_PROVIDER_STATE`

Provider submission changes attempt state, not review state.

### AI Review State Machine

States:

- `NOT_REQUIRED`
- `NOT_RUN`
- `PASS`
- `REGENERATE`
- `SWITCH_TO_HYBRID`
- `SWITCH_TO_REAL_SHOOT`

Legal transitions:

- `NOT_RUN` -> reviewed terminal states only after actual media exists.
- `NOT_REQUIRED` remains terminal for no-AI jobs.
- `PASS` requires reviewed generated media.

Illegal transitions:

- prompt/storyboard/package -> `PASS`
- generation success -> automatic `PASS`

Errors: `AI_REVIEW_MEDIA_REQUIRED`, `AI_REVIEW_INVALID_STATE`.

## 13. Idempotency And Cost Protection

`PROPOSED`: `Idempotency-Key` belongs in HTTP header. Body may include
`client_request_id`, but it is not the idempotency key.

Scope:

- owner id
- endpoint
- idempotency key
- canonical payload hash

Behavior:

- Same key + same canonical payload returns original result.
- Same key + different canonical payload returns `IDEMPOTENCY_CONFLICT`.
- Key must survive service restart once persistence is approved.
- Pending idempotency records must not trigger duplicate provider calls.

Endpoint requirements:

- create job: required
- retry job: required
- cancel job: required
- upload URL: required
- get job: not required
- health: not required

Provider timeout protection:

- Store provider submission before or atomically with submit.
- If timeout occurs after submit uncertainty, mark
  `UNKNOWN_PROVIDER_STATE`.
- Reconcile by provider job id or provider query before any second submit.

Future cost confirmation:

- Required before real Seedance submission.
- Must show duration, provider model, estimated cost, asset count, and
  non-refundable risk.
- Confirmation itself should be idempotent and expire.

## 14. Provider Abstraction

Field separation:

- `selected_model`: GPT/user intent, for example `Seedance`.
- `execution_provider`: backend adapter, for example `mock`.
- `provider_model`: provider-specific model identifier, unknown for real
  Seedance until official integration details are approved.
- `provider_job_id`: provider-side job id, stored on Attempt.
- `generation_mode`: T2V, I2V, V2V, R2V, FLF2V, edit, extend, or provider
  equivalent.

Provider abstraction must include capabilities:

- input asset roles
- supported modes
- duration support
- cancellation support
- retry behavior
- timeout behavior
- cost-estimate availability
- result URL TTL

Phase 2A Mock Provider should simulate:

- `QUEUED`
- `PROCESSING`
- `SUCCEEDED`
- `FAILED`
- `CANCELED`
- timeout
- `UNKNOWN_PROVIDER_STATE`

Use deterministic test clock and explicit mock scenario flags. Do not connect to
real Seedance or assume real Seedance request fields.

## 15. Persistence Decision

| Option | Speed | Restart Safety | Idempotency Reliability | History | Concurrency | Tests | Phase 2C Migration | Deployment |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| In-memory | Fastest | Poor | Poor after restart | Poor | Limited | Easy | Medium rewrite | Simple |
| SQLite | Fast | Good for local | Better | Good | Limited | Easy | Medium | Simple |
| PostgreSQL | Slower | Strong | Strong | Strong | Strong | Standard | Lowest later | More complex |

`RECOMMENDATION_PROPOSED`: use SQLite for Phase 2A if idempotency is tested
across restart; otherwise in-memory only for earliest contract tests. Use
PostgreSQL in later phases when real provider costs or multi-user deployment
begin.

`DECISION_REQUIRED`: choose Phase 2A persistence before coding.

## 16. Authentication And Security

Candidate security model:

- Custom GPT Action authenticates with Bearer API key.
- `owner_id` must come from authenticated client mapping, not trusted request
  body alone.
- All assets and jobs are scoped by owner.
- Upload URLs and result URLs expire.
- External URLs are untrusted and must be fetched only by approved backend
  logic in later phases.
- Logs must redact prompts, asset URLs, provider raw payloads, secrets, and
  user identifiers where practical.
- Every request gets `request_id`.
- Rate limits apply by owner and endpoint.
- Audit trail records actor, request id, job id, attempt id, state transition,
  idempotency key hash, and provider submission metadata.

`DECISION_REQUIRED`: exact Custom GPT Action auth mode and owner mapping.

## 17. API Surface Proposal

`PROPOSED`, not final OpenAPI.

Path comparison:

- `/v1/video-jobs`: concise and stable if future jobs may include several
  generation types.
- `/v1/video-generation-jobs`: explicit and matches current domain language.

Recommendation: `/v1/video-generation-jobs` for Phase 2A clarity. Mark as
`DECISION_REQUIRED` before implementation.

| Operation | Method | Path | Auth | Idempotency | Request Concept | Response Concept | Error Codes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| health | GET | `/v1/health` | none or optional | no | none | status, version | `INTERNAL_ERROR` |
| upload URL | POST | `/v1/assets/upload-url` | Bearer | required | owner, role, type, size, checksum | asset id, upload URL, expiry | `ASSET_TYPE_UNSUPPORTED`, `IDEMPOTENCY_CONFLICT` |
| asset completion | POST | `/v1/assets/{asset_id}/complete` | Bearer | recommended | checksum, metadata | asset ready | `ASSET_INVALID_STATE`, `ASSET_OWNER_MISMATCH` |
| create job | POST | `/v1/video-generation-jobs` | Bearer | required | contract snapshot, assets, proof, provider | job accepted/rejected | `TRUTH_GATE_BLOCKED`, `HYBRID_GATE_BLOCKED`, `PROVIDER_UNSUPPORTED` |
| get job | GET | `/v1/video-generation-jobs/{job_id}` | Bearer | no | job id | job, attempts, assets, review | `JOB_NOT_FOUND` |
| cancel job | POST | `/v1/video-generation-jobs/{job_id}/cancel` | Bearer | required | reason | cancel state | `JOB_CANCEL_NOT_ALLOWED` |
| retry job | POST | `/v1/video-generation-jobs/{job_id}/retry` | Bearer | required | retry reason, cost confirmation if needed | new attempt | `JOB_NOT_RETRYABLE`, `COST_CONFIRMATION_REQUIRED` |

## 18. Error Model

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

Error categories:

- authentication: `AUTH_REQUIRED`, `AUTH_INVALID`, `OWNER_MISMATCH`
- schema validation: `SCHEMA_INVALID`, `FIELD_REQUIRED`
- truth gate: `TRUTH_GATE_BLOCKED`, `UNVERIFIED_CLAIM`
- hybrid gate: `HYBRID_LAYER_MISSING`, `AI_PROOF_NOT_ALLOWED`
- asset: `ASSET_NOT_FOUND`, `ASSET_NOT_READY`, `ASSET_EXPIRED`
- idempotency: `IDEMPOTENCY_CONFLICT`, `IDEMPOTENCY_PENDING`
- job state: `JOB_INVALID_STATE`, `JOB_NOT_RETRYABLE`
- provider: `PROVIDER_UNSUPPORTED`, `PROVIDER_TIMEOUT`,
  `UNKNOWN_PROVIDER_STATE`
- rate limit: `RATE_LIMITED`
- internal: `INTERNAL_ERROR`

## 19. Observability And Audit

Future backend must support:

- structured logs
- `request_id`
- `job_id`
- `attempt_id`
- `provider_job_id`
- state transition logs
- latency
- provider error mapping
- cost estimate and confirmation logs
- user confirmation audit
- redaction of prompts, URLs, secrets, and personal data

## 20. Testing Strategy

Test categories:

- unit tests for validators and canonical payload hash
- API contract tests
- state-machine tests
- idempotency tests
- Product Truth gate tests
- HYBRID gate tests
- repository tests for frozen file protection
- mock provider tests
- OpenAPI tests once schema exists
- end-to-end mock tests

Initial truth tests:

- AI suction proof blocked.
- HYBRID without real proof layer blocked.
- `selected_model=other` cannot execute Seedance package.
- generation success leaves review `NOT_RUN`.
- same key plus same payload returns same response.
- same key plus different payload conflicts.

## 21. Deployment Shape

Phase 2A design only:

- local development inside `backend/`
- Docker later for deployment parity
- public HTTPS required before Custom GPT Action can call non-local backend
- environment configuration for auth secrets and provider mode
- storage/database migration path from mock/local to real service

No external service is connected by this document.

## 22. Phase Plan

| Phase | Goal | Acceptance |
| --- | --- | --- |
| 2A-0 Master Design | Candidate design only. | Draft complete, decisions listed, no code. |
| 2A API Contract + Mock Backend | Schemas, validators, mock provider. | Tests pass; mock E2E works; no real provider. |
| 2B Custom GPT Action + Mock Integration | GPT Action calls mock backend. | GPT can create/query mock jobs; attachments behavior verified. |
| 2C Real Seedance Adapter | Add real provider behind adapter. | Cost confirmation, idempotency, timeout reconciliation pass. |
| 2D End-to-End And Review Integration | Generate, review, retry, audit. | Review states, result delivery, and safety gates verified end to end. |

## 23. Decision Log

| ID | Decision | Status | Options | Recommendation | Evidence | Consequence | Approval Needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D-001 | API base path | DECISION_REQUIRED | `/v1/video-jobs`, `/v1/video-generation-jobs` | `/v1/video-generation-jobs` | Domain clarity | Longer path | yes |
| D-002 | Phase 2A persistence | DECISION_REQUIRED | in-memory, SQLite, PostgreSQL | SQLite or in-memory first | Idempotency needs restart safety | Affects tests and setup | yes |
| D-003 | Canceled spelling | DECISION_REQUIRED | `CANCELED`, `CANCELLED` | `CANCELED` | American English in repo docs | API compatibility once frozen | yes |
| D-004 | Processing state name | DECISION_REQUIRED | `PROCESSING`, `RUNNING` | `PROCESSING` | User-facing clarity | State enum freeze risk | yes |
| D-005 | GPT Action attachment handling | OPEN | direct binary, upload URL, external URL | upload URL contract | Not verified | Affects asset flow | yes |
| D-006 | Owner identity source | DECISION_REQUIRED | API key mapping, body owner, future OAuth | API key mapping | Body owner is unsafe | Security model | yes |
| D-007 | Cost confirmation timing | DECISION_REQUIRED | before job, before attempt, before provider submit | before provider submit | Prevents accidental charge | More UX steps | yes |
| D-008 | Review result source | OPEN | GPT, human reviewer, backend tool, mixed | mixed later | Knowledge 10 requires actual media | Affects review API | yes |
| D-009 | Retry semantics | DECISION_REQUIRED | same job new attempt, new job always | same job if payload unchanged | Attempt model supports history | Complexity | yes |
| D-010 | Real Seedance fields | OPEN | unknown | defer | No official API contract in repo | Prevents fake integration | yes |

## 24. Open Questions

- Where is `backend/docs/reference/VIDEO_GENERATION_BACKEND_HANDOFF.md`, or was it never created?
- Can Custom GPT Action forward chat attachments as binary files?
- Should Phase 2A create real upload URL endpoints or mock-only asset handles?
- What owner identity will Custom GPT Action provide?
- Should Phase 2A use SQLite to test restart-safe idempotency?
- What is the desired retention policy for prompts and provider raw payloads?
- Who performs Knowledge 10 review after real media exists?
- Should cost confirmation be separate endpoint or part of retry/create?
- How many retries are allowed per job?
- What is the expected duration/model choice UX before real Seedance submit?
- Will a future Web UI share the same API contract?
- What exact Seedance API fields and status names exist?

## 25. Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| GPT attachments cannot upload directly. | Asset flow blocked. | Use upload URL or mock asset handles; verify in Phase 2B. |
| Duplicate API calls create duplicate charges. | Cost loss. | Header idempotency and provider reconciliation. |
| Provider timeout after submission. | Unknown charge/result. | `UNKNOWN_PROVIDER_STATE`, no blind resubmit. |
| State drift between job, attempt, provider, review. | Wrong UX and unsafe retry. | Separate state machines and audit logs. |
| Product Truth declared incorrectly by client. | Fake proof execution. | Backend deterministic proof validators. |
| Markdown and code rules drift. | Backend allows stale behavior. | Explicit versioned rule tests and release process. |
| External media URL untrusted. | Security/privacy risk. | Do not fetch arbitrary URLs until approved. |
| Long tasks exceed HTTP timeouts. | Client confusion. | Async job model and polling. |
| Owner isolation missing. | Cross-user asset leak. | Owner-scoped auth and queries. |
| Prompt and asset privacy leak. | Sensitive content exposure. | Redaction and retention policy. |
| API contract freezes too early. | Rework. | Keep v0.1 DRAFT and require approval checklist. |

## 26. Recommended Approval Checklist

Before Phase 2A coding, human approval is required for:

- API base path.
- Phase 2A persistence choice.
- State enum names.
- Idempotency key TTL and storage.
- Owner/auth model.
- Asset upload strategy.
- Whether Custom GPT Action can send binary attachments.
- ProofElement schema and granularity.
- HYBRID policy schema.
- Cost confirmation flow.
- Mock provider scenario controls.
- Retry and cancel semantics.
- Prompt and URL logging/redaction rules.
- Whether any backend endpoint should exist before schemas and validators pass
  tests.
- Whether this document can become the approved backend design baseline.
