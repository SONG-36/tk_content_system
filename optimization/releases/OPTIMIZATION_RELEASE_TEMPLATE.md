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
