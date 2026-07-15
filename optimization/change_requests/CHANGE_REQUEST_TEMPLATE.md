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
