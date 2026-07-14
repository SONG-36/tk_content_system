# Test Cross-Category Guardrails

## Cases

```yaml
- id: "guard_01"
  scenario: "Seat-gap automotive hook applied to facial cleansing tool"
  expected_result: "FAIL_GUARDRAIL"

- id: "guard_02"
  scenario: "Automotive paint-safety rule applied to skin-safety conclusion"
  expected_result: "FAIL_GUARDRAIL"

- id: "guard_03"
  scenario: "Foam thickness treated as proof for steam-cleaning or beauty result"
  expected_result: "FAIL_GUARDRAIL"
```

---

## Pass Rule

Pass if the routing layer blocks mechanical cross-category reuse of proof logic.
