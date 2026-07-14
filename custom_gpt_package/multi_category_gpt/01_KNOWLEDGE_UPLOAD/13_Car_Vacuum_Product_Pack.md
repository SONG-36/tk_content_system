# Car Vacuum Product Pack

```yaml
product_pack:
  category: automotive_cleaning
  product_type: car_vacuum
  support_level: COMPLETE
  production_ready: true
  truth_dependency_default: high
  core_product_proof_requires_real_shoot: true
  ai_generated_suction_proof_prohibited: true
```

---

# SOURCE FILE: categories/automotive_cleaning/products/car_vacuum/README.md

---

# Car Vacuum Product Pack

## Status

```yaml
car_vacuum_product_pack_status:
  status: COMPLETE
  support_level: COMPLETE
  production_use: READY
  production_ready: true
  truth_dependency_default: high
  core_product_proof_requires_real_shoot: true
  ai_generated_suction_proof_prohibited: true
```

---

## Files

- `product_knowledge.md`
- `consumer_psychology.md`
- `hook_library.md`
- `visual_proof_protocol.md`
- `attachment_scenario_matrix.md`
- `claim_boundary.md`
- `professional_shooting_standard.md`
- `seedance_and_hybrid_rules.md`
- `script_templates.md`
- `test_cases.md`

## Cross-Category Guardrail

This Product Pack applies only to `car_vacuum`.

Do not route handheld home vacuums, steam cleaners, beauty tools or generic automotive tools into this Product Pack.
---

# SOURCE FILE: categories/automotive_cleaning/products/car_vacuum/product_knowledge.md

---

# Car Vacuum Product Knowledge

## Product Types

- pure vacuum
- blower-vacuum combo
- corded
- cordless
- handheld portable
- transparent dust-bin version
- multi-attachment kit

---

## Common Structure

- main body
- intake port
- dust bin
- filter
- battery
- charging port
- crevice nozzle
- brush nozzle
- wide nozzle
- blower port
- storage accessories

---

## Core User Jobs

- clean seat gaps
- clean floor-mat crumbs
- clean cup holder and console gaps
- remove snack crumbs
- remove pet hair
- restore fast interior tidiness
- reduce frequent detailing visits

---

## Capability Separation Rules

Do not mix these concepts:

- suction
- airflow
- blowing
- runtime
- noise
- dust-bin capacity
- filtration
- weight
- charging
- liquid pickup
- attachment compatibility

Each claim must map to its own proof requirement.

Only accessories verified in the actual SKU may appear in:

- scripts
- product demonstrations
- Seedance prompts
- Hero Shots
- attachment tests

---

## Product Truth Rule

Car vacuum outputs are high risk whenever they claim:

- dirt intake
- pet hair removal
- difficult-gap access
- transparent dust-bin collection
- blower effectiveness
- runtime or noise performance
- liquid pickup
- filter performance

These require real evidence and may not be inferred from appearance alone.

The following Product Proof must be `REAL_SHOOT`:

- dirt intake
- transparent-bin collection
- pet-hair removal
- gap access
- attachment performance
- blower function
- runtime test
- noise comparison
- liquid pickup
- filter performance

Blower function, runtime test, noise comparison, liquid pickup, and filter performance are allowed only when the SKU explicitly supports the claim and test evidence exists.
---

# SOURCE FILE: categories/automotive_cleaning/products/car_vacuum/consumer_psychology.md

---

# Car Vacuum Consumer Psychology

## Core Buyer Outcomes

Users buy results, not parameters.

Primary desired outcomes:

- hidden dirt gets removed
- the car feels controlled again
- the interior looks less embarrassing
- family mess becomes manageable
- pet hair stops building up
- cleanup becomes fast enough to repeat

---

## Psychology Angles

- Hidden Dirt Shock
- cleanliness satisfaction
- restored “new car feel”
- family-mess recovery
- pet-owner relief
- commuter reset
- social embarrassment avoidance
- DIY control
- money-saving rationalization
- fast order restoration

---

## Messaging Rule

Translate parameter talk into lived results.

Better:

- “seat-gap crumbs finally come out”

Worse:

- “high suction motor”
---

# SOURCE FILE: categories/automotive_cleaning/products/car_vacuum/hook_library.md

---

# Car Vacuum Hook Library

## Hook Entries

```yaml
hook_entry:
  hook_type: "Hidden Dirt Reveal"
  first_second_visual: "Macro POV into a seat gap packed with crumbs and lint."
  subtitle_template: "你车里最脏的不是脚垫，是这个缝。"
  stop_scroll_reason: "Hidden contamination shock."
  target_user: ["commuter", "family", "pet_owner"]
  compatible_product_features: ["crevice nozzle", "portable use"]
  required_truth_proof: ["real dirt intake", "real reach"]
  production_type: "REAL_SHOOT"
  failure_patterns: ["starts with product beauty shot", "no visible dirt target"]
```

```yaml
hook_entry:
  hook_type: "Product Test"
  first_second_visual: "Single seat-gap challenge framed as one focused test."
  subtitle_template: "我只测这个座椅缝，看它到底能吸出多少。"
  stop_scroll_reason: "Concrete challenge with measurable result."
  target_user: ["skeptical_buyer", "tidy_driver"]
  compatible_product_features: ["suction", "transparent bin"]
  required_truth_proof: ["continuous intake", "visible collected debris"]
  production_type: "REAL_SHOOT"
  failure_patterns: ["cuts too fast", "only sound, no visual proof"]
```

```yaml
hook_entry:
  hook_type: "Difficult Area Challenge"
  first_second_visual: "Normal hand or larger tool fails to reach a narrow gap."
  subtitle_template: "普通吸头进不去的位置，它能不能处理？"
  stop_scroll_reason: "Solves an annoying hard-to-reach problem."
  target_user: ["detail_oriented_user", "car_owner"]
  compatible_product_features: ["crevice nozzle", "slim form factor"]
  required_truth_proof: ["real access", "real removal"]
  production_type: "REAL_SHOOT"
  failure_patterns: ["no baseline failure shown", "gap not actually narrow"]
```

```yaml
hook_entry:
  hook_type: "Transparent Bin Proof"
  first_second_visual: "Empty clear dust bin shown before test."
  subtitle_template: "别听吸力参数，看尘盒里吸进去什么。"
  stop_scroll_reason: "Visible evidence replaces abstract specs."
  target_user: ["skeptical_buyer", "spec_fatigued_user"]
  compatible_product_features: ["transparent bin"]
  required_truth_proof: ["bin starts empty", "debris visibly enters bin"]
  production_type: "REAL_SHOOT"
  failure_patterns: ["pre-filled bin", "bin never shown clearly"]
```

```yaml
hook_entry:
  hook_type: "Family Mess"
  first_second_visual: "Snack crumbs under child seat or back seat."
  subtitle_template: "孩子吃一次零食，座椅下面就变成这样。"
  stop_scroll_reason: "Parents immediately relate to the mess."
  target_user: ["family", "parent"]
  compatible_product_features: ["portable use", "quick cleanup"]
  required_truth_proof: ["real crumb removal"]
  production_type: "REAL_SHOOT"
  failure_patterns: ["generic clean car", "no lived-in family cue"]
```

```yaml
hook_entry:
  hook_type: "Pet Hair Challenge"
  first_second_visual: "Hair embedded along seat edge or fabric seam."
  subtitle_template: "宠物毛最难清的不是表面，是边角。"
  stop_scroll_reason: "High-friction problem for pet owners."
  target_user: ["pet_owner"]
  compatible_product_features: ["brush nozzle", "wide nozzle"]
  required_truth_proof: ["real hair adhesion", "real collection"]
  production_type: "REAL_SHOOT"
  failure_patterns: ["loose staged hair", "hair disappears off frame"]
```

```yaml
hook_entry:
  hook_type: "Before/After"
  first_second_visual: "Split area with one side untouched."
  subtitle_template: "同一个位置，只吸一半。"
  stop_scroll_reason: "Immediate contrast and proof expectation."
  target_user: ["all"]
  compatible_product_features: ["general vacuum function"]
  required_truth_proof: ["same angle", "same lighting", "half-clean boundary"]
  production_type: "REAL_SHOOT"
  failure_patterns: ["lighting change", "different area comparison"]
```

```yaml
hook_entry:
  hook_type: "Multi-Attachment Test"
  first_second_visual: "Three real attachments placed beside three real mess types."
  subtitle_template: "三个吸头，分别解决三个死角。"
  stop_scroll_reason: "Clear functional mapping."
  target_user: ["comparison_shopper"]
  compatible_product_features: ["attachment kit"]
  required_truth_proof: ["real attachment mapping", "real result by task"]
  production_type: "REAL_SHOOT"
  failure_patterns: ["attachment shown without task proof", "SKU mismatch"]
```
---

# SOURCE FILE: categories/automotive_cleaning/products/car_vacuum/visual_proof_protocol.md

---

# Car Vacuum Visual Proof Protocol

## Protocols

```yaml
proof_protocol:
  feature: "Dirt Intake Proof"
  problem_setup: "Visible crumbs or dust remain inside a reachable but dirty target area."
  approved_test_materials: ["real crumbs", "real dust", "real lint", "real floor grit"]
  prohibited_test_materials: ["invisible dust only", "off-screen debris pull", "reverse-play staging"]
  camera_requirement: "Intake port, dirt, and movement path in frame."
  continuity_requirement: "Continuous intake action."
  pass_condition: "Debris enters the intake through real contact or clear suction range."
  failure_condition: "Debris disappears without visible intake or via reversed motion."
  required_production_type: "REAL_SHOOT"
```

```yaml
proof_protocol:
  feature: "Transparent Dust Bin Proof"
  problem_setup: "Dust bin starts visibly empty before use."
  approved_test_materials: ["crumbs", "dust", "lint", "pet hair"]
  prohibited_test_materials: ["pre-filled dust bin", "off-camera refill"]
  camera_requirement: "Show empty bin before and collected debris after."
  continuity_requirement: "Collection sequence remains credible."
  pass_condition: "Viewer can see collected material inside the real dust bin."
  failure_condition: "Bin contents are unclear or appear staged."
  required_production_type: "REAL_SHOOT"
```

```yaml
proof_protocol:
  feature: "Difficult Area Proof"
  problem_setup: "Show that hand or ordinary tool cannot easily reach the gap."
  approved_test_materials: ["seat-gap crumbs", "console dust", "track debris"]
  prohibited_test_materials: ["easy open surfaces marketed as hard-to-reach"]
  camera_requirement: "Baseline failure, entry, and removal should all be legible."
  continuity_requirement: "Keep target area consistent through the sequence."
  pass_condition: "Specialized attachment enters and removes visible debris."
  failure_condition: "No real access challenge or no visible removal."
  required_production_type: "REAL_SHOOT"
```

```yaml
proof_protocol:
  feature: "Half-Clean Comparison"
  problem_setup: "One region stays untouched while one matched region is cleaned."
  approved_test_materials: ["dust line", "crumb line", "pet hair line"]
  prohibited_test_materials: ["different surfaces", "lighting swap", "exposure cheat"]
  camera_requirement: "Stable angle with clear comparison border."
  continuity_requirement: "Same frame, same light, same area."
  pass_condition: "Difference is visible without suspicion of cheat."
  failure_condition: "Comparison depends on framing, light, or location change."
  required_production_type: "REAL_SHOOT"
```

```yaml
proof_protocol:
  feature: "Attachment Proof"
  problem_setup: "Each attachment is mapped to a real task."
  approved_test_materials: ["real dashboard dust", "real mat crumbs", "real seam debris"]
  prohibited_test_materials: ["attachment beauty shot only"]
  camera_requirement: "Show attachment install, contact, and outcome."
  continuity_requirement: "One attachment, one task, one result."
  pass_condition: "Viewer understands why this attachment exists."
  failure_condition: "Attachment shown with no task-specific result."
  required_production_type: "REAL_SHOOT"
```

```yaml
proof_protocol:
  feature: "Blower Function Proof"
  problem_setup: "Loose dust is displaced from a difficult gap and later collected."
  approved_test_materials: ["loose dust", "fine debris with collection plan"]
  prohibited_test_materials: ["dust blown away and called cleaned"]
  camera_requirement: "Show blow-out and later collection plan."
  continuity_requirement: "Do not end on blown dust alone."
  pass_condition: "Blowing is framed as displacement, not completed cleaning."
  failure_condition: "Displacement is misrepresented as final clean result."
  required_production_type: "REAL_SHOOT"
```

```yaml
proof_protocol:
  feature: "Hair And Fabric Proof"
  problem_setup: "Hair is attached to realistic fabric or seam surfaces."
  approved_test_materials: ["real pet hair", "real fabric contact"]
  prohibited_test_materials: ["ultra-loose staged hair that does not represent adhesion"]
  camera_requirement: "Show fabric texture and hair engagement."
  continuity_requirement: "Keep contact readable."
  pass_condition: "Viewer sees believable hair pickup from real adhesion."
  failure_condition: "Hair behaves unrealistically easy."
  required_production_type: "REAL_SHOOT"
```
---

# SOURCE FILE: categories/automotive_cleaning/products/car_vacuum/attachment_scenario_matrix.md

---

# Car Vacuum Attachment Scenario Matrix

| Attachment | Scenario | Dirt Type | Best Shot | Proof Requirement |
| --- | --- | --- | --- | --- |
| Crevice Nozzle | Seat Gap | Crumbs / Dust | Macro POV | Dirt enters nozzle |
| Brush Nozzle | Dashboard Vent | Fine Dust | Close-up side | Dust lifted then collected |
| Wide Nozzle | Floor Mat | Sand / Crumbs | Top-down | Continuous path |
| Soft Brush | Console / Buttons | Fine Dust | Macro | No surface scratching claim without proof |
| Blower Nozzle | Deep Gap | Loose Dust | Side macro | Must show later collection |

---

## SKU Rule

- different SKUs have different attachment sets
- scripts may only use attachments included in the real SKU
- if an attachment is missing, remove the associated shot and claim
---

# SOURCE FILE: categories/automotive_cleaning/products/car_vacuum/claim_boundary.md

---

# Car Vacuum Claim Boundary

## Claim Levels

### Level A: Directly Demonstrable

- product powers on
- an attachment enters a shown gap
- transparent dust bin shows collected debris
- attachments can be installed
- one-hand holding is possible

### Level B: Controlled-Test Claims

- picking up sand, hair, or heavier debris
- runtime
- noise
- filtration performance
- blower performance
- multi-scene consistency

### Level C: Do Not State Without Evidence

- strongest suction in the market
- suction never fades
- completely silent
- works for all vehicles and all scenarios
- supports liquid pickup unless explicitly supported
- medical-grade HEPA unless certified
- removes all pet hair in one pass
- cleaner than professional detailing
- never clogs
- absolute battery safety
- compatible with all chargers
- runtime that differs from verified product evidence

---

## Review Schema

```yaml
claim_review:
  proposed_claim: ""
  claim_level: "A | B | C"
  evidence_required: []
  approved_wording: ""
  prohibited_wording: ""
  production_proof_required: true
```

---

## Output Rule

If evidence is missing:

- downgrade wording
- remove absolute language
- avoid comparative superlatives
---

# SOURCE FILE: categories/automotive_cleaning/products/car_vacuum/professional_shooting_standard.md

---

# Car Vacuum Professional Shooting Standard

## Required Shot Fields

Every shot should include:

- Shot Number
- Duration
- Shot Purpose
- Production Type
- Visual Description
- Shot Size
- Camera Angle
- Camera Movement
- Action
- Dirt Type
- Attachment Used
- Visual Change
- Sound Design
- Subtitle
- User Psychology
- Product Proof
- Truth Risk
- Required Preparation
- Alternative
- Production Notes

---

## Product-Specific Priorities

- macro and close-up are preferred
- intake-to-dirt contact point is preferred
- vacuum sound may support the shot but cannot be the only proof
- dust bin should avoid glare
- logo, buttons, interfaces, and attachments must remain real
- dirt intake should not be cut into fragments that break trust

---

## Execution Standard

Use shot language that lets the crew know:

- what dirt exists
- what attachment is used
- where contact happens
- what visible change proves the result
- what truth risk could invalidate the shot
---

# SOURCE FILE: categories/automotive_cleaning/products/car_vacuum/seedance_and_hybrid_rules.md

---

# Car Vacuum Seedance And Hybrid Rules

## Must Be `REAL_SHOOT`

- real suction proof
- dirt intake
- pet hair removal
- crumb collection
- transparent dust-bin result
- product buttons, ports, and attachments
- attachment installation
- before/after proof
- runtime, noise, or performance tests

---

## Allowed `AI_GENERATION`

- non-proof luxury interior hook
- premium garage environment
- pure atmosphere transition
- abstract dust-anxiety visual
- opening visual that does not prove product ability

AI may only carry non-proof Hook, premium environment, lighting, transition, and supporting atmosphere.

---

## Allowed `HYBRID`

- real product plus AI premium car interior
- real hand and product plus non-proof environment enhancement
- real hero product plus AI lighting or background
- real cleaning action surrounded by non-proof atmosphere enhancement

---

## Hybrid Boundary

```yaml
hybrid_layer_definition:
  real_layer:
    - product
    - attachments
    - human_hand
    - product_contact
    - dirt_intake
    - result_proof
  ai_layer:
    - background_environment
    - non-functional atmosphere
    - lighting_enhancement
    - non-proof transition
  proof_layer_owner: "REAL_SHOOT"
  ai_must_not_rewrite:
    - actual product
    - actual SKU structure
    - actual proof
    - accessories
    - buttons
    - logo
```

---

## Prohibited

- Seedance generating core debris-intake proof
- AI changing attachment structure
- AI adding nonexistent accessories
- AI generating wrong logo or wrong buttons
- AI making untouched dirt disappear
- AI generating fake before/after

## Template Priority

Car Vacuum script templates provide product-specific structure only.

They must not override:

- Knowledge 07 professional shot requirements
- Knowledge 08 production type decisions
- Knowledge 10 AI review timing
---

# SOURCE FILE: categories/automotive_cleaning/products/car_vacuum/script_templates.md

---

# Car Vacuum Script Templates

```yaml
script_template:
  version_name: "Viral Remake"
  product_type: "car_vacuum"
  target_user: ["commuter", "pet_owner", "family"]
  core_job: "remove hidden car-interior debris fast"
  hook_type: "Hidden Dirt Reveal"
  product_truth_requirements: ["real dirt", "real intake", "real collection"]
  required_proof_shots: ["seat-gap intake", "transparent dust bin", "result reveal"]
  optional_seedance_shots: ["non-proof premium opening hook", "environment transition"]
  forbidden_ai_shots: ["debris intake proof", "before/after proof"]
  shot_schema: {}
  cta_logic: "Turn embarrassment and friction into fast control."
  scoring_target: 85
```

```yaml
script_template:
  version_name: "Low-Cost Live Action"
  product_type: "car_vacuum"
  target_user: ["budget_buyer", "ordinary_car_owner"]
  core_job: "clean one real annoying interior mess with minimal setup"
  hook_type: "Product Test"
  product_truth_requirements: ["phone-shootable real proof"]
  required_proof_shots: ["one difficult gap", "one intake proof", "one result shot"]
  optional_seedance_shots: []
  forbidden_ai_shots: ["all proof shots"]
  shot_schema: {}
  cta_logic: "Show one believable win ordinary users can repeat."
  scoring_target: 85
```

```yaml
script_template:
  version_name: "Conversion Optimized"
  product_type: "car_vacuum"
  target_user: ["comparison_shopper", "skeptical_buyer"]
  core_job: "understand product, accessories, use, and believable results"
  hook_type: "Transparent Bin Proof"
  product_truth_requirements: ["real product body", "real accessories", "real proof", "claim boundary respected"]
  required_proof_shots: ["product body", "attachment mapping", "real intake", "bin result", "storage or charging"]
  optional_seedance_shots: ["non-proof hero environment", "non-proof intro transition"]
  forbidden_ai_shots: ["attachment installation proof", "performance proof", "before/after"]
  shot_schema: {}
  cta_logic: "Reduce doubt through product clarity plus proof."
  scoring_target: 85
```
---

# SOURCE FILE: categories/automotive_cleaning/products/car_vacuum/test_cases.md

---

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
