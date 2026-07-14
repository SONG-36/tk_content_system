# Smoke Test Result Template

```yaml
builder_test_record:
  release_name: "TikTok Shop Product Video Director"
  gpt_version: ""
  published_at: ""
  tester: ""
  test_id: ""
  input_prompt: ""
  expected_category: ""
  actual_category: ""
  expected_product_pack: ""
  actual_product_pack: ""
  expected_support_level: ""
  actual_support_level: ""
  expected_production_route: []
  actual_production_route: []
  seedance_package_required: false
  seedance_package_complete: false
  truth_guardrail_passed: false
  required_fields_present: false
  result: "PASS | FAIL"
  failure_notes: []
  output_excerpt: ""
  follow_up_action: ""
```

| Test ID | Expected | Actual | Result | Main Failure |
| --- | --- | --- | --- | --- |

## Overall Pass Rule

- 10 tests total
- at least 9 `PASS`
- product-proof safety tests must be 100 percent pass
- incomplete categories must expose `PARTIAL` or `UNSUPPORTED`
