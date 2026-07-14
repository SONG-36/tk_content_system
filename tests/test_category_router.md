# Test Category Router

## Purpose

Validate category and product-pack resolution before downstream script or AI routing begins.

---

## Cases

```yaml
- id: "router_01"
  input: "Car Vacuum"
  expected_primary_category: "automotive_cleaning"
  expected_product_pack: "car_vacuum"
  expected_status: "ROUTED"

- id: "router_02"
  input: "Snow Foam Cannon"
  expected_primary_category: "automotive_cleaning"
  expected_product_pack: ""
  expected_status: "PARTIAL"

- id: "router_03"
  input: "Steam Cleaner"
  expected_primary_category: "home_cleaning"
  expected_product_pack: "steam_cleaner"
  expected_status: "PARTIAL"
  expected_safety_level: "high"

- id: "router_04"
  input: "Straightening Brush"
  expected_primary_category: "beauty_care_tools"
  expected_product_pack: ""
  expected_status: "PARTIAL"
  expected_human_demo_required: true

- id: "router_05"
  input: "Unknown cleaning gadget"
  expected_primary_category: ""
  expected_product_pack: ""
  expected_status: "PARTIAL"
```

---

## Pass Rule

Pass if routing resolves:

- correct category
- correct product-pack status
- no fake support for missing packs
