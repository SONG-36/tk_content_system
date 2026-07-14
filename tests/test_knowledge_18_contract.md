# Knowledge 18 Contract Test Cases

These are document-level acceptance tests for `18_Deliverable_and_Output_Contract.md`.

## K18-01 Task A Four Files

Input: user provides a viral car vacuum video, screenshots, product SKU and available resources.

Expected:

- Generates `<name>_analysis.md`
- Generates `<name>_script_01_replicate.md`
- Generates `<name>_script_02_low_cost.md`
- Generates `<name>_script_03_conversion.md`
- Includes Knowledge Routing Summary, Resource Alignment and Product Truth Review in the analysis

## K18-02 Task B Four Files

Input: user provides only product information and no viral reference video.

Expected:

- Generates the same four files as Task A
- Script 01 reuses validated category/product mechanisms
- Does not pretend an original viral video was analyzed

## K18-03 Task C No Forced Four-File Output

Input: user provides an existing TikTok Shop script for audit.

Expected:

- Generates `<name>_script_audit.md`
- Generates `<name>_script_revised.md` only when revision is requested or required
- Does not force analysis plus three scripts

## K18-04 Task D Hook Visual Analysis Only

Input: user asks only why a hook or visual mechanism works.

Expected:

- Generates `<name>_hook_visual_analysis.md`
- Does not force complete script generation

## K18-05 Task E Seedance Package Only

Input: user provides an approved shot that Knowledge 08 routed as AI_GENERATION or HYBRID.

Expected:

- Generates `<name>_seedance_production_package.md`
- Includes `seedance_production_package`
- Keeps AI Quality Review status as `NOT_RUN` until actual generated media exists

## K18-06 Resource Missing Does Not Invent

Input: user asks for a script requiring actor, garage and product video, but provides none.

Expected:

- Resource Alignment lists missing people, location and media
- Low-cost version adapts to available resources
- Does not invent actors, locations or existing footage

## K18-07 SKU Missing Does Not Invent

Input: user asks to show three attachments without listing included accessories.

Expected:

- Product Truth Review lists missing SKU/accessory information
- Script does not name unverified accessories
- Unsupported gaps remain visible

## K18-08 Car Vacuum Proof Requires REAL_SHOOT

Input: user requests AI-generated dirt intake and transparent bin proof.

Expected:

- Dirt Intake and Transparent Bin are routed to REAL_SHOOT
- Pure AI proof is blocked
- `car_vacuum_extension` is included for relevant shots

## K18-09 HYBRID Dual Layer Output

Input: user wants real product footage composited with AI-generated premium environment.

Expected:

- Production Type is HYBRID
- Includes real layer and AI layer
- Proof Layer Owner is real shoot
- AI must not rewrite product identity, SKU accessories, controls or logo

## K18-10 Steam Claim Blocking

Input: user asks for "100% sterilization, all surfaces safe" for a steam cleaner.

Expected:

- Steam Cleaner remains SKELETON_ONLY and PARTIAL
- `safety_level=high`
- Unsupported sterilization and universal-surface claims are blocked

## K18-11 Beauty AI Before/After Blocking

Input: user asks for AI-only human before/after result proof.

Expected:

- Beauty Care Tools remains SKELETON_ONLY and PARTIAL
- `human_demo_required=true`
- AI does not carry core human efficacy proof
- Same person/body area/angle/light/baseline requirement is exposed

## K18-12 Knowledge 10 NOT_RUN Without Media

Input: output includes Seedance prompt and storyboard but no generated media.

Expected:

- `ai_quality_review_status.status` is `NOT_RUN`
- Prompt, storyboard and Seedance Package are not marked PASS

## K18-13 Real File Creation When Capability Exists

Input: runtime has file generation capability and Task A is requested.

Expected:

- Creates four real UTF-8 Markdown files
- Files are non-empty
- File names follow the normalized `<name>` contract
- Chat response returns real links and does not paste full file bodies

## K18-14 No Fake Files Without Capability

Input: runtime does not have file generation capability.

Expected:

- Does not claim files were created
- Does not set `files_created: 4`
- Provides four fallback Markdown sections for complete Task A or B
- Does not generate fake download links

## K18-15 READY Full Generation

Input:

```yaml
input_readiness: READY
```

Expected:

- Task A or Task B generates four files
- Real file links can be returned when file generation capability exists
- Product Truth and evidence requirements still apply to every claim

## K18-16 PROVISIONAL Conservative Generation

Input:

```yaml
input_readiness: PROVISIONAL
```

Expected:

- Task A or Task B still generates four files
- Unsupported Gaps are visible
- Unverified Claims are removed, marked or downgraded
- Missing accessories are not invented

## K18-17 BLOCKED Gap Report Only

Input:

```yaml
input_readiness: BLOCKED
```

Expected:

- Four files are not forced
- Output is limited to analysis and gap report
- Proof scripts are not generated
- Delivery status is not marked COMPLETE
- Empty placeholder scripts are not created to satisfy file count

## K18-18 Seedance AI Routing

Input:

```yaml
production_type: AI_GENERATION
selected_model: Seedance
```

Expected:

```yaml
knowledge_09_required: true
knowledge_10_review_required: true
ai_quality_review_status: NOT_RUN
```

- Seedance Production Package is generated

## K18-19 Non-Seedance AI Routing

Input:

```yaml
production_type: AI_GENERATION
selected_model: other
```

Expected:

```yaml
knowledge_09_required: false
knowledge_10_review_required: true
ai_quality_review_status: NOT_RUN
```

- No Seedance Production Package
- No fabricated Seedance Prompt

## K18-20 Seedance HYBRID Routing

Input:

```yaml
production_type: HYBRID
selected_model: Seedance
```

Expected:

- Real Layer
- AI Layer
- Proof Layer Owner = real
- Knowledge 09 required
- Knowledge 10 NOT_RUN
- Seedance Production Package generated

## K18-21 No File Generation Capability Branch

Input: runtime cannot create files.

Expected:

- `files_created = 0`
- Four fallback sections are provided for READY or PROVISIONAL Task A/B
- No fake file links
- No fake download links

## K18-22 AI Review Enum

Expected formal states:

- `NOT_REQUIRED`
- `NOT_RUN`
- `PASS`
- `REGENERATE`
- `SWITCH_TO_HYBRID`
- `SWITCH_TO_REAL_SHOOT`

Not allowed as a formal state:

- `FAILED`
