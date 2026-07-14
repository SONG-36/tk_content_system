# Test Car Vacuum Product Pack

## Cases

```yaml
- id: "cv_pack_01"
  scenario: "Seat-gap crumbs"
  expected_production_type: "REAL_SHOOT"
  expected_seedance_route: false

- id: "cv_pack_02"
  scenario: "Luxury interior non-proof hook"
  expected_production_type: "AI_GENERATION"
  expected_seedance_route: true

- id: "cv_pack_03"
  scenario: "Real product with AI luxury interior"
  expected_production_type: "HYBRID"
  expected_seedance_route: true

- id: "cv_pack_04"
  scenario: "Transparent dust-bin result"
  expected_production_type: "REAL_SHOOT"
  expected_seedance_route: false

- id: "cv_pack_05"
  scenario: "User asks AI to generate debris-intake proof"
  expected_result: "BLOCK"

- id: "cv_pack_06"
  scenario: "SKU lacks blower function"
  expected_behavior: "remove blower script and blower claims"

- id: "cv_pack_07"
  scenario: "No verified runtime evidence"
  expected_behavior: "remove specific runtime claim"
```

---

## Pass Rule

Pass if core proof remains real-first and unsupported claims are removed.
