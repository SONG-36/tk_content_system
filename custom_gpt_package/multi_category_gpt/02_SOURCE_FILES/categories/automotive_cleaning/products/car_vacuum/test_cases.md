# Car Vacuum Product-Pack Test Cases

```yaml
test_case:
  id: "cv_01"
  input: "Seat-gap snack crumbs."
  expected_category_route: "automotive_cleaning"
  expected_product_pack: "car_vacuum"
  expected_production_type: "REAL_SHOOT"
  expected_seedance_route: false
  required_proof: ["real dirt intake"]
  prohibited_behavior: ["AI intake proof"]
  expected_result: "PASS"
```

```yaml
test_case:
  id: "cv_02"
  input: "Floor-mat sand cleanup."
  expected_category_route: "automotive_cleaning"
  expected_product_pack: "car_vacuum"
  expected_production_type: "REAL_SHOOT"
  expected_seedance_route: false
  required_proof: ["continuous path"]
  prohibited_behavior: ["off-screen cleanup"]
  expected_result: "PASS"
```

```yaml
test_case:
  id: "cv_03"
  input: "Cup-holder dust."
  expected_category_route: "automotive_cleaning"
  expected_product_pack: "car_vacuum"
  expected_production_type: "REAL_SHOOT"
  expected_seedance_route: false
  required_proof: ["real contact"]
  prohibited_behavior: ["AI dust disappearance"]
  expected_result: "PASS"
```

```yaml
test_case:
  id: "cv_04"
  input: "Vent dust with brush nozzle."
  expected_category_route: "automotive_cleaning"
  expected_product_pack: "car_vacuum"
  expected_production_type: "REAL_SHOOT"
  expected_seedance_route: false
  required_proof: ["brush task mapping"]
  prohibited_behavior: ["scratch-safe claim without proof"]
  expected_result: "PASS"
```

```yaml
test_case:
  id: "cv_05"
  input: "Pet hair on seat edge."
  expected_category_route: "automotive_cleaning"
  expected_product_pack: "car_vacuum"
  expected_production_type: "REAL_SHOOT"
  expected_seedance_route: false
  required_proof: ["real hair adhesion"]
  prohibited_behavior: ["easy staged hair treated as universal proof"]
  expected_result: "PASS"
```

```yaml
test_case:
  id: "cv_06"
  input: "Transparent dust-bin collection proof."
  expected_category_route: "automotive_cleaning"
  expected_product_pack: "car_vacuum"
  expected_production_type: "REAL_SHOOT"
  expected_seedance_route: false
  required_proof: ["empty bin before", "visible collected debris after"]
  prohibited_behavior: ["pre-filled bin"]
  expected_result: "PASS"
```

```yaml
test_case:
  id: "cv_07"
  input: "Three-attachment comparison."
  expected_category_route: "automotive_cleaning"
  expected_product_pack: "car_vacuum"
  expected_production_type: "REAL_SHOOT"
  expected_seedance_route: false
  required_proof: ["real task per attachment"]
  prohibited_behavior: ["missing-SKU attachment"]
  expected_result: "PASS"
```

```yaml
test_case:
  id: "cv_08"
  input: "Blower function use case."
  expected_category_route: "automotive_cleaning"
  expected_product_pack: "car_vacuum"
  expected_production_type: "REAL_SHOOT"
  expected_seedance_route: false
  required_proof: ["dust displacement plus later collection"]
  prohibited_behavior: ["blown dust called cleaned"]
  expected_result: "PASS"
```

```yaml
test_case:
  id: "cv_09"
  input: "Single-hand portability."
  expected_category_route: "automotive_cleaning"
  expected_product_pack: "car_vacuum"
  expected_production_type: "REAL_SHOOT"
  expected_seedance_route: false
  required_proof: ["real grip demonstration"]
  prohibited_behavior: ["weight claim without evidence"]
  expected_result: "PASS"
```

```yaml
test_case:
  id: "cv_10"
  input: "In-car storage shot."
  expected_category_route: "automotive_cleaning"
  expected_product_pack: "car_vacuum"
  expected_production_type: "REAL_SHOOT"
  expected_seedance_route: false
  required_proof: ["real storage context"]
  prohibited_behavior: ["invented accessory case"]
  expected_result: "PASS"
```

```yaml
test_case:
  id: "cv_11"
  input: "No product reference image, but user wants AI luxury hook."
  expected_category_route: "automotive_cleaning"
  expected_product_pack: "car_vacuum"
  expected_production_type: "AI_GENERATION"
  expected_seedance_route: true
  required_proof: []
  prohibited_behavior: ["AI product proof"]
  expected_result: "FALLBACK"
```

```yaml
test_case:
  id: "cv_12"
  input: "User asks AI to generate suction proof."
  expected_category_route: "automotive_cleaning"
  expected_product_pack: "car_vacuum"
  expected_production_type: "REAL_SHOOT"
  expected_seedance_route: false
  required_proof: ["real suction evidence"]
  prohibited_behavior: ["AI-generated intake proof"]
  expected_result: "BLOCK"
```
