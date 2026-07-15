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
