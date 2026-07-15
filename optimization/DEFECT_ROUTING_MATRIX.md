# Defect Routing Matrix

Rule: `Smallest Responsible Layer Wins`.

| defect_type | first_responsible_layer | source_files_to_check | generated_files_affected | protected_files | required_targeted_tests | builder_retest_required | owner_approval_required |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TASK_ROUTER | Task Router | `instructions/TikTok_Shop_Product_Video_Director_Main_Instructions.md`, `knowledge/18_Deliverable_and_Output_Contract.md` | `custom_gpt_package/multi_category_gpt/00_INSTRUCTIONS/MAIN_INSTRUCTIONS.md`, `custom_gpt_package/multi_category_gpt/01_KNOWLEDGE_UPLOAD/18_Deliverable_and_Output_Contract.md` | MAIN_INSTRUCTIONS, Knowledge 18 | `tools/validate_main_instructions.py`, `tools/validate_knowledge_18.py` | true | true |
| CATEGORY_ROUTER | Category Router | `workflows/Category_Router.md`, `workflows/TikTok_Shop_Product_Video_Main_Router.md` | `custom_gpt_package/multi_category_gpt/01_KNOWLEDGE_UPLOAD/11_Category_and_Main_Router.md` | Knowledge 11 | `tests/test_category_router.md`, `tests/test_incomplete_category_fallback.md` | true | true |
| SUPPORT_LEVEL | Category/Product support rules | `categories/**/README.md`, `categories/**/*skeleton*.md`, `workflows/Category_Router.md` | Knowledge 11, Knowledge 14-16 | Knowledge 11-16 | `tests/test_incomplete_category_fallback.md`, `tests/test_cross_category_guardrails.md` | true | true |
| PRODUCT_PACK | Product Pack | `categories/automotive_cleaning/products/car_vacuum/**` | Knowledge 13 | Knowledge 13 | `tests/test_car_vacuum_product_pack.md` | true | true |
| HOOK | Hook logic | `knowledge/01_TikTok_Viral_Analysis_Framework.md`, `knowledge/03_Cleaning_Video_Hook_Database.md`, product hook library | Knowledge 01, Knowledge 03, Knowledge 13 | Knowledge 01, 03, 13 | Builder smoke cases BST-01, BST-05 | true | false |
| SCRIPT | Script writing | `knowledge/05_TikTok_Shop_Script_Writing_Rules.md`, product script templates | Knowledge 05, Knowledge 13, Knowledge 18 | Knowledge 05, 13, 18 | script document review, Builder smoke cases | true | true |
| SCORING | Script scoring | `knowledge/06_Video_Script_Scoring_System.md` | Knowledge 06 | Knowledge 06 | scoring rubric review | false | false |
| SHOT | Shot planning | `knowledge/07_Professional_Shooting_Standard.md`, `knowledge/08_Shot_Production_Planning_Framework.md`, product shooting standards | Knowledge 07, Knowledge 08, Knowledge 13 | Knowledge 07, 08, 13 | shot contract review, HYBRID smoke case | true | true |
| PRODUCTION_TYPE | Production Type routing | `knowledge/08_Shot_Production_Planning_Framework.md`, product proof rules | Knowledge 08, Knowledge 13, Knowledge 18 | Knowledge 08, 13, 18 | Product Truth regression, Seedance boundary tests | true | true |
| SEEDANCE_PACKAGE | Seedance package | `knowledge/09_Seedance_Generation_Director.md`, `seedance_skills/reference-workflow.md`, runtime Knowledge 17 upload copy | Knowledge 09, Knowledge 17, Knowledge 18 | Knowledge 09, 17, 18; third-party Seedance source | Seedance regression cases SD-01 to SD-05 | true | true |
| AI_REVIEW | AI Review | `knowledge/10_AI_Generation_Quality_Review.md`, `knowledge/18_Deliverable_and_Output_Contract.md` | Knowledge 10, Knowledge 18 | Knowledge 10, 18 | AI drift review case, NOT_RUN timing check | true | true |
| DELIVERY | Final delivery contract | `knowledge/18_Deliverable_and_Output_Contract.md` | Knowledge 18 | Knowledge 18 | `tools/validate_knowledge_18.py`, file generation behavior review | true | true |
| BUILDER_CONFIGURATION | Builder upload/config | `custom_gpt_package/multi_category_gpt/03_BUILDER_SETUP/**`, Builder manual configuration | Builder setup docs | Online GPT Builder | Builder checklist and Preview smoke tests | true | true |
| BACKEND_ACTION | Backend Action | `backend/**`, backend OpenAPI/action schema | backend OpenAPI artifact only | Knowledge, Instructions unless GPT contract/routing is wrong | backend tests, OpenAPI validation, future Action Preview | true | true |
| MODEL_VARIANCE | Model behavior variance | no immediate source file; collect more evidence first | none until reproduced | Knowledge, Instructions | repeated Builder Preview runs | true | true |
| INPUT_QUALITY | Missing or ambiguous input | no source change by default; improve gap reporting only if reproducible | possibly Knowledge 18 | Knowledge 18 | BLOCKED/PARTIAL delivery review | true | true |
*** Add File: optimization/REGRESSION_MATRIX.md
# Regression Matrix

This matrix maps defect categories to targeted checks. It does not claim that
Builder Preview tests are automated.

## Test Type Legend

- `automated_repository_test`: existing script or deterministic repository check.
- `manual_document_review`: contributor reads documented test cases and verifies
  behavior manually.
- `builder_preview_test`: Project Owner or tester runs a real GPT Builder
  Preview test.
- `future_backend_test`: backend/API test for future Action-related issues.

## Category Router

| id | test_type | target |
| --- | --- | --- |
| R-01 | manual_document_review | Automotive car vacuum routes to `automotive_cleaning` and `car_vacuum`. |
| R-02 | manual_document_review | Generic automotive tool does not route to `car_vacuum`. |
| R-03 | manual_document_review | Unknown product returns `PARTIAL` or `UNSUPPORTED`. |
| R-04 | manual_document_review | Missing product details expose gaps instead of guessing. |
| R-05 | builder_preview_test | Steam cleaner routes to `home_cleaning -> steam_cleaner`. |
| R-06 | builder_preview_test | Beauty care tool routes to `beauty_care_tools`. |
| R-07 | builder_preview_test | Home cleaning is not defaulted to automotive. |
| CS-01 | manual_document_review | Cross-category guardrails remain active. |

## Product Truth

| id | test_type | target |
| --- | --- | --- |
| PT-01 | builder_preview_test | AI must not fake suction proof. |
| PT-02 | builder_preview_test | AI must not fake transparent bin/dirt intake result. |
| PT-03 | manual_document_review | Unverified SKU accessories are not invented. |
| PT-04 | manual_document_review | Human efficacy proof requires real demo. |
| PT-05 | manual_document_review | Before/After proof cannot be pure AI. |
| N-01 | automated_repository_test | `python3 tools/validate_knowledge_01_18.py`. |

## Seedance

| id | test_type | target |
| --- | --- | --- |
| E-01 | automated_repository_test | `python3 tools/validate_knowledge_18.py`. |
| E-02 | automated_repository_test | `python3 tools/validate_knowledge_01_18.py`. |
| SD-01 | builder_preview_test | Non-proof Seedance atmosphere hook can produce package. |
| SD-02 | builder_preview_test | Seedance package blocks core proof fabrication. |
| SD-03 | manual_document_review | `selected_model=other` does not generate Seedance package. |
| SD-04 | manual_document_review | HYBRID locks product structure and proof layer. |
| SD-05 | manual_document_review | AI Review remains `NOT_RUN` until actual media exists. |
| CS-03 | manual_document_review | Third-party Seedance source files remain unmodified. |

## Delivery

| id | test_type | target |
| --- | --- | --- |
| IR-03 | automated_repository_test | `python3 tools/validate_main_instructions.py`. |
| F-01 | manual_document_review | READY Task A/B returns four files or four fallback sections. |
| F-02 | manual_document_review | PROVISIONAL Task A/B returns conservative four-file output. |
| F-03 | manual_document_review | BLOCKED does not claim four-file completion. |
| F-04 | manual_document_review | File links are real or explicitly fallback sections. |
| N-04 | automated_repository_test | `python3 tools/check_markdown_references.py`. |

## Steam

| id | test_type | target |
| --- | --- | --- |
| R-05 | builder_preview_test | Steam routes to steam cleaner skeleton. |
| ST-01 | builder_preview_test | Unsupported sterilization claims are blocked. |
| ST-02 | builder_preview_test | Universal surface claims are blocked. |
| ST-03 | manual_document_review | `safety_level=high` remains visible. |
| ST-04 | manual_document_review | Steam remains `SKELETON_ONLY` / `PARTIAL`. |

## Beauty

| id | test_type | target |
| --- | --- | --- |
| R-06 | builder_preview_test | Beauty routes to beauty care tools skeleton. |
| BT-01 | builder_preview_test | AI Before/After is blocked as proof. |
| BT-02 | manual_document_review | `human_demo_required=true` remains visible. |
| BT-03 | manual_document_review | Human efficacy cannot be proven by AI-only output. |
| BT-04 | manual_document_review | Beauty remains `SKELETON_ONLY` / `PARTIAL`. |

## Full Validation Commands

```bash
python3 tools/validate_main_instructions.py
python3 tools/validate_knowledge_01_17.py
python3 tools/validate_knowledge_18.py
python3 tools/validate_knowledge_01_18.py
python3 tools/check_markdown_references.py
python3 tools/build_custom_gpt_package.py --check
git diff --check
```

For Backend Action defects, add backend tests and OpenAPI validation when the
backend phase is in scope. Do not present future backend tests as current
Builder Preview results.
*** Add File: optimization/RELEASE_GATE.md
# Release Gate

```yaml
release_gate:
  target_defects_fixed: true
  targeted_regression_passed: true
  repository_validation_passed: true
  builder_updated: true
  original_failure_cases_retested: true
  core_smoke_tests_passed: true
  open_s0: 0
  open_s1: 0
  open_s2: 0
  product_truth_not_weakened: true
  safety_not_weakened: true
  support_levels_not_silently_upgraded: true
```

## Required Meaning

- `target_defects_fixed`: all defects targeted by the release have a merged fix.
- `targeted_regression_passed`: each defect's targeted regression plan passed.
- `repository_validation_passed`: repository validators and build checks passed.
- `builder_updated`: Project Owner updated GPT Builder test configuration.
- `original_failure_cases_retested`: the exact failing prompts were rerun.
- `core_smoke_tests_passed`: core Builder smoke tests passed in Preview.
- `open_s0`, `open_s1`, `open_s2`: no unresolved blocker, critical, or major defects remain.
- `product_truth_not_weakened`: Product Truth guardrails remain equal or stronger.
- `safety_not_weakened`: safety and claim boundaries remain equal or stronger.
- `support_levels_not_silently_upgraded`: no skeleton or partial category was silently promoted to `COMPLETE`.

## Non-Equivalence Rules

- `MERGED` does not equal `CLOSED`.
- `REPOSITORY_VALIDATED` does not equal `BUILDER_RETESTED`.
- Repository PASS does not equal Builder PASS.

Only the Project Owner can approve release after Builder Preview retest.
*** Add File: optimization/defect_registry.yaml
registry:
  schema_version: "1.0"
  active_defects: []
  closed_defects: []

# Each real defect must use an independent Markdown file under
# optimization/defects/. This registry is only an index.
*** Add File: optimization/defects/README.md
# Defects

Create one Markdown file per real defect using:

- `optimization/defects/DEFECT_TEMPLATE.md`

Do not create fictional defects. Do not close a defect at `MERGED`; closure
requires Builder update and Preview retest.
*** Add File: optimization/defects/DEFECT_TEMPLATE.md
# Defect Template

```yaml
defect:
  defect_id: ""
  title: ""
  reporter: ""
  reported_at: ""
  severity: "S0_BLOCKER | S1_CRITICAL | S2_MAJOR | S3_MINOR | S4_SUGGESTION"
  status: "NEW"

  environment:
    custom_gpt_version: ""
    instructions_version: ""
    knowledge_version: ""
    builder_environment: ""

  evidence:
    test_case_id: ""
    original_prompt: ""
    complete_output: ""
    expected_result: ""
    actual_result: ""
    screenshots: []
    generated_files: []
    conversation_reference: ""
    reproduction_count: 0

  reproduction:
    reproducible: false
    attempts: 0
    reproduction_steps: []

  diagnosis:
    defect_type: ""
    suspected_layer: ""
    confirmed_root_cause: ""
    responsible_source_files: []
    affected_generated_files: []

  resolution:
    change_request_id: ""
    branch: ""
    pull_request: ""
    fixed_version: ""
    repository_validation: "NOT_RUN"
    builder_retest: "NOT_RUN"
```

Allowed status values:

- `NEW`
- `NEEDS_REPRODUCTION`
- `REPRODUCED`
- `DIAGNOSED`
- `FIX_IN_PROGRESS`
- `REPOSITORY_VALIDATED`
- `PR_OPEN`
- `MERGED`
- `BUILDER_UPDATED`
- `BUILDER_RETESTED`
- `CLOSED`
- `REOPENED`
*** Add File: optimization/change_requests/README.md
# Change Requests

Create one Change Request for each repair scope using:

- `optimization/change_requests/CHANGE_REQUEST_TEMPLATE.md`

A Change Request defines the smallest responsible layer, files in scope,
protected files, prohibited changes, risk, and validation plan.
*** Add File: optimization/change_requests/CHANGE_REQUEST_TEMPLATE.md
# Change Request Template

```yaml
change_request:
  change_id: ""
  defect_ids: []

  root_cause:
    responsible_layer: ""
    description: ""

  scope:
    source_files_to_modify: []
    generated_files_expected_to_change: []
    protected_files: []
    prohibited_changes: []
    owner_approval_required: false
    owner_approval_reference: ""

  intended_behavior: ""
  prohibited_behavior: ""

  risk:
    truth_risk: ""
    safety_risk: ""
    cross_category_risk: ""
    builder_impact: ""

  validation:
    targeted_tests: []
    full_repository_validation_required: true
    builder_retest_required: true
    original_failure_prompt_required: true
```
*** Add File: optimization/releases/OPTIMIZATION_RELEASE_TEMPLATE.md
# Optimization Release Template

```yaml
optimization_release:
  release_name: ""
  release_type: "PATCH | RC | MINOR"
  target_version: ""
  defects_fixed: []
  change_requests: []

  files_changed:
    source_files: []
    generated_files: []
    protected_files: []

  validation:
    targeted_regression: "NOT_RUN"
    repository_validation: "NOT_RUN"
    builder_retest: "NOT_RUN"
    original_failure_cases_retested: false
    core_smoke_tests_passed: false

  release_gate:
    target_defects_fixed: false
    targeted_regression_passed: false
    repository_validation_passed: false
    builder_updated: false
    original_failure_cases_retested: false
    core_smoke_tests_passed: false
    open_s0: 0
    open_s1: 0
    open_s2: 0
    product_truth_not_weakened: false
    safety_not_weakened: false
    support_levels_not_silently_upgraded: false

  builder:
    updated_by_project_owner: false
    preview_retested: false
    published: false
```
