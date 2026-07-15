# Regression Matrix

This matrix maps defect categories to targeted checks. It does not claim that
Builder Preview tests are automated.

## Test Type Legend

- `automated_repository_test`: existing script or deterministic repository check.
- `manual_document_review`: contributor reads documented test cases and verifies behavior manually.
- `builder_preview_test`: Project Owner or tester runs a real GPT Builder Preview test.
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
