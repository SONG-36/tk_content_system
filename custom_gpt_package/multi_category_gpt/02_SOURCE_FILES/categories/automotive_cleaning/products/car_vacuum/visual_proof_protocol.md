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
