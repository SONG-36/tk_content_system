# 18. Deliverable and Output Contract

```yaml
knowledge_status:
  knowledge_id: 18
  name: "Deliverable and Output Contract"
  scope: "multi_category"
  runtime_role: "FINAL_DELIVERY_ASSEMBLER"
  production_ready: true
```

## 1. Purpose and Scope

Knowledge 18 负责最终输出格式与交付物组装。它将 Knowledge 01-17 的分析、类目路由、产品知识、脚本生成、专业镜头、生产方式、Seedance Package、AI 审核和商业评分结果，统一整理为用户可使用的 Markdown 交付文件。

Knowledge 18 不负责重新判断类目，不负责发明 Product Pack，不取代 Knowledge 08，不取代 Knowledge 09，不取代 Knowledge 10，不取代 Knowledge 06。它只负责把上游结果组装成最终交付物。

```yaml
delivery_contract_scope:
  assembles_final_outputs: true
  reroutes_category: false
  invents_product_pack: false
  replaces_knowledge_08: false
  replaces_knowledge_09: false
  replaces_knowledge_10: false
  replaces_knowledge_06: false
```

## 2. Authority and Conflict Resolution

优先级必须按以下顺序执行：

1. GPT Builder Main Instructions
2. Category and Product truth/safety rules in Knowledge 11-16
3. Knowledge 18 Deliverable and Output Contract
4. Knowledge 08-10 production and AI rules
5. Knowledge 01-07 analysis, creative, shooting and scoring rules
6. Examples and templates

规则说明：

- Product Truth 和 Safety 永远高于视觉创意。
- Product Pack 高于 Category 通用示例。
- Skeleton 只能限制输出，不能被视为完整知识。
- Knowledge 05 的简化时间轴不能覆盖 Knowledge 07 和 08。
- Knowledge 18 不能降低 REAL_SHOOT 要求。
- Knowledge 18 不能把 PARTIAL 写成 COMPLETE。
- High Truth Product Proof 必须遵守上游 REAL_SHOOT 或 HYBRID 真实层要求。

## 3. Builder Knowledge Alias Map

```yaml
builder_knowledge_aliases:
  viral_analysis: "01_TikTok_Viral_Analysis_Framework.md"
  automotive_psychology: "02_Car_Cleaning_Content_Psychology.md"
  automotive_hook_database: "03_Cleaning_Video_Hook_Database.md"
  automotive_visual_library: "04_Satisfying_Cleaning_Visual_Library.md"
  script_rules: "05_TikTok_Shop_Script_Writing_Rules.md"
  script_scoring: "06_Video_Script_Scoring_System.md"
  professional_shooting: "07_Professional_Shooting_Standard.md"
  production_planning: "08_Shot_Production_Planning_Framework.md"
  seedance_director: "09_Seedance_Generation_Director.md"
  ai_quality_review: "10_AI_Generation_Quality_Review.md"
  category_and_main_router: "11_Category_and_Main_Router.md"
  automotive_category_pack: "12_Automotive_Category_Pack.md"
  car_vacuum_product_pack: "13_Car_Vacuum_Product_Pack.md"
  home_cleaning_skeleton: "14_Home_Cleaning_Skeleton.md"
  steam_cleaner_skeleton: "15_Steam_Cleaner_Skeleton.md"
  beauty_tools_skeleton: "16_Beauty_Care_Tools_Skeleton.md"
  seedance_reference_pack: "17_Seedance_Reference_Pack.md"
  delivery_contract: "18_Deliverable_and_Output_Contract.md"
```

仓库路径只是 provenance。GPT Builder 运行时通过上述 Builder 文件名解析，不通过仓库相对路径解析。

## 4. Task Types and Deliverables

```yaml
task_types:
  task_a:
    name: "Viral Video Analysis and Product Transfer"
    accepted_inputs:
      - viral video
      - video link
      - video screenshots
      - key frames
      - video description
      - user product
    required_files:
      - "<name>_analysis.md"
      - "<name>_script_01_replicate.md"
      - "<name>_script_02_low_cost.md"
      - "<name>_script_03_conversion.md"
  task_b:
    name: "Product-to-Video Generation"
    accepted_inputs:
      - user product information
      - available resources
      - optional product images or videos
    required_files:
      - "<name>_analysis.md"
      - "<name>_script_01_replicate.md"
      - "<name>_script_02_low_cost.md"
      - "<name>_script_03_conversion.md"
    replicate_meaning: "Reuse validated Hook, Retention and Visual Mechanism from the routed category/product knowledge; do not pretend an original viral video exists."
  task_c:
    name: "Existing Script Audit"
    default_files:
      - "<name>_script_audit.md"
    conditional_files:
      - "<name>_script_revised.md"
    four_file_required: false
  task_d:
    name: "Hook or Visual Mechanism Analysis"
    required_files:
      - "<name>_hook_visual_analysis.md"
    full_script_required: false
  task_e:
    name: "Approved Shot to Seedance Production Package"
    required_files:
      - "<name>_seedance_production_package.md"
    prerequisite: "Only shots approved by Knowledge 08, routed as AI_GENERATION or HYBRID, and assigned selected_model=Seedance may proceed to Task E."
```

Task A 和 Task B 在 input_readiness=READY 或 PROVISIONAL 时属于完整任务，必须生成四个交付文件。当 input_readiness=BLOCKED 时，不适用四文件强制规则，只输出分析与信息缺口报告。Task C、Task D、Task E 是局部任务，不强制四文件。

Task E 只有在以下条件同时成立时执行：

1. 镜头经过 Knowledge 08 批准。
2. Production Type 为 AI_GENERATION 或 HYBRID。
3. selected_model=Seedance。

REAL_SHOOT、STOCK_ASSET、AI_GENERATION + selected_model=other、HYBRID + selected_model=other 不得生成 Seedance Production Package。

## 5. Input Readiness Contract

```yaml
input_readiness:
  status: "READY | PROVISIONAL | BLOCKED"
  sufficient_for_strategy: false
  sufficient_for_product_proof: false
  sufficient_for_claims: false
  missing_information: []
  assumptions_allowed: []
  blocked_outputs: []
```

READY 表示信息足够生成策略、脚本和证明。Task A 或 Task B 必须生成四个文件，可以生成完整 Product Proof，但所有 Claims 仍须有证据。

PROVISIONAL 表示可以生成保守脚本。Task A 或 Task B 仍生成四个文件，但未验证 Claim 必须删除或标记，缺失配件不得出现，Product Proof 必须降级或改为待实测，Unsupported Gaps 必须清晰显示。

BLOCKED 表示缺失信息影响产品身份、SKU、实际配件、核心功能、人体功效、安全、材质兼容、杀菌、真实性证明或可测量参数。BLOCKED 时不得生成最终证明型脚本，只能输出信息缺口报告、补充拍摄清单、测试计划或 Claim 验证计划。

`BLOCKED` is not a completed full-generation state. BLOCKED is not a completed full-generation state. Do not create empty, placeholder or fabricated scripts merely to satisfy the four-file count.

BLOCKED 状态下，Task A 或 Task B 不强制生成四个文件，不得生成虚假的证明型脚本，不得用空模板凑足四文件，不得把阻断任务标记为 COMPLETE。只生成 `<name>_analysis.md`，作为信息缺口报告、SKU 补充清单、Product Claim 验证清单、实拍测试计划、资源补充清单、安全或兼容性验证计划。补齐阻断信息后，再重新执行 Task A 或 Task B。

## 6. Knowledge Routing Summary

每个最终结构化输出必须包含：

```yaml
knowledge_routing_summary:
  task_type: ""
  primary_category: ""
  secondary_category: ""
  product_type: ""
  category_pack: ""
  product_pack: ""
  category_support_level: ""
  product_support_level: ""
  routing_status: "ROUTED | GENERIC_SUPPORTED | PARTIAL | UNSUPPORTED"
  knowledge_used: []
  resources_assessed: true
  product_truth_reviewed: true
  human_demo_required: false
  safety_level: "low | medium | high"
  seedance_routed_shots: []
  ai_quality_review_status: "NOT_REQUIRED | NOT_RUN | PASS | REGENERATE | SWITCH_TO_HYBRID | SWITCH_TO_REAL_SHOOT"
  unsupported_gaps: []
  generated_files: []
```

没有实际 AI 素材时，不能输出 AI Review PASS。Skeleton 必须显示 PARTIAL。Unknown Product 不能默认 automotive。Product Pack 缺失必须显示 gap。

## 7. Resource Alignment

最终交付必须先评估用户实际资源：

```yaml
resource_alignment:
  available_products: []
  available_skus: []
  available_accessories: []
  available_locations: []
  available_people: []
  available_vehicles_or_rooms: []
  available_surfaces_or_body_areas: []
  available_shooting_equipment: []
  available_lighting: []
  available_images: []
  available_videos: []
  available_audio: []
  available_stock_licenses: []
  budget_level: "unknown | low | medium | high"
  shooting_time: ""
  editing_capability: ""
  ai_generation_capability: ""
  unavailable_requirements: []
  information_gaps: []
  adaptation_strategy: []
```

不得虚构演员、场地、车辆或房间、配件、用户已有素材。不可用资源必须提供替代方案。低成本版必须优先使用实际可用资源。已上传素材必须指出具体用于哪个镜头。

## 8. Product Truth Review

最终交付必须包含产品真实性审查：

```yaml
product_truth_review:
  verified_product_identity: []
  verified_features: []
  verified_claims: []
  features_requiring_test: []
  measurable_claims_requiring_evidence: []
  unsupported_claims: []
  actual_included_accessories: []
  compatibility_information: []
  material_or_body_area_boundaries: []
  safety_boundaries: []
  human_efficacy_boundaries: []
  missing_product_information: []
  proof_allowed: []
  proof_blocked: []
```

缺失信息不能转成正面 Claim。不能根据产品外观推断性能。不能虚构 SKU 配件。吸力、风量、续航、噪音、温度、压力、杀菌、过滤、防水、兼容性和人体功效需要证据。High Truth Product Proof 必须 REAL_SHOOT。HYBRID 必须保留真实证明层。AI 不得伪造吸力或人体功效，不得伪造结构、配件、功效、结果或安全证据。

## 9. Deliverable 1 - Analysis Report

文件名：

```text
<name>_analysis.md
```

必须包含以下章节：

1. Executive Summary
2. Task and Input Summary
3. Knowledge Routing Summary
4. Input Readiness
5. Product Truth Review
6. Resource Alignment
7. Target Audience and JTBD
8. User Psychology
9. First-Three-Second Hook Analysis
10. Retention Mechanism
11. Visual Satisfaction and Proof Mechanism
12. PAS / AIDA Logic
13. Transferable Viral Mechanisms
14. Non-Transferable Elements
15. Category and Product-Pack Constraints
16. Production Strategy
17. Unsupported Gaps
18. Final Recommendation

分析报告必须回答：用户为什么停留、为什么继续看、为什么相信、为什么购买、哪个机制可以迁移、哪些元素不能复制、哪些证明必须实拍、哪些 Claim 不支持、用户资源如何改变拍摄方案。

Task B 没有对标视频时，分析拟采用的爆款机制，不能假装分析了原视频。

## 10. Deliverables 2-4 - Three Script Versions

```yaml
script_versions:
  script_01:
    filename: "<name>_script_01_replicate.md"
    goal:
      - retain strongest Hook structure
      - retain Retention Progression
      - retain visual change
      - transfer to the real product
      - remove fake proof
  script_02:
    filename: "<name>_script_02_low_cost.md"
    goal:
      - use available user resources
      - reduce location, actor and equipment cost
      - remain phone-shootable
      - keep at least one strong Hook
      - keep at least one credible Product Proof
      - provide alternatives for missing resources
  script_03:
    filename: "<name>_script_03_conversion.md"
    goal:
      - strengthen product identity
      - show real use
      - prove core value
      - handle purchase objections
      - explain SKU, accessories and compatibility
      - provide CTA based on real results
```

## 11. Mandatory Script Header

每份脚本必须以以下 Schema 开始：

```yaml
script_summary:
  version_name: ""
  task_type: ""
  primary_category: ""
  product_type: ""
  category_pack: ""
  product_pack: ""
  category_support_level: ""
  product_support_level: ""
  routing_status: ""
  target_user: []
  core_job_to_be_done: ""
  video_theme: ""
  viral_mechanism: []
  framework_logic: []
  core_selling_points: []
  product_truth_boundaries: []
  video_goal: ""
  recommended_duration: ""
  available_resources_used: []
  missing_resources: []
  unsupported_gaps: []
```

脚本正文必须包括 Strategic Direction、Hook Plan、Proof Plan、Shot Script、Production Summary、Script Evaluation、Optimization Record、Final Recommendation。

## 12. Mandatory Final Shot Contract

每个 Shot 必须包含：

```yaml
shot:
  shot_number: ""
  time_range: ""
  duration: ""
  shot_purpose: ""
  production_type: "REAL_SHOOT | AI_GENERATION | HYBRID | STOCK_ASSET"
  truth_dependency: "low | medium | high"
  production_type_reason: ""
  visual_description: ""
  camera_direction:
    shot_size: ""
    camera_angle: ""
    camera_movement: ""
    framing_and_focus: ""
  action: ""
  visual_change:
    before: ""
    transition: ""
    after: ""
  sound_design:
    product_sound: ""
    material_sound: ""
    music_or_ambience: ""
  subtitle: ""
  voiceover: ""
  user_psychology: ""
  retention_function: ""
  product_proof:
    proof_type: ""
    proof_subject: ""
    proof_method: ""
    evidence_visible: ""
    claim_supported: ""
  required_preparation: []
  required_assets: []
  available_resource_usage: []
  continuity_requirements: []
  risk_and_truth_notes: []
  alternative: ""
  production_notes: []
```

Shot Purpose 合法类型只有 Hook、Problem Reveal、Product Introduction、Product Proof、Transformation、Satisfaction Moment、Objection Handling、CTA。

以下描述无效：展示产品、开始清洁、展示效果、用 AI 做高级感、增加一个爽感镜头。

缺少 Shot Number、Duration、Shot Purpose、Production Type、Production Type Reason、Visual Description、Camera Direction、Action、Visual Change、Product Proof、Required Preparation、Alternative、Production Notes 中任一字段，Shot 判定为不合格。

Production Type 只有四种：REAL_SHOOT、AI_GENERATION、HYBRID、STOCK_ASSET。不得创建第二套 Production Type。

## 13. Shot Production Plan

每个 Shot 还必须追加 Knowledge 08 的生产计划：

```yaml
shot_production_plan:
  selected_model: "Seedance | none | other"
  model_routing_required: false
  decision_reason:
    why_this_type_fits: []
    why_other_types_are_weaker: []
    truth_guardrails: []
  real_shoot_requirements: []
  stock_asset_brief:
    usage_purpose: ""
    search_queries: []
    license_requirements: []
  ai_planning:
    workflow_type: "T2V | I2V | V2V | R2V | FLF2V | Edit | Extend | N/A"
    reference_strategy: ""
    environment_requirement: ""
    camera_requirement: ""
    motion_requirement: ""
    preservation_requirements: []
    product_truth_boundaries: []
  hybrid_boundary:
    real_layer: []
    ai_layer: []
    proof_layer_owner: "real_shoot | n/a"
    ai_must_not_rewrite: []
  routing_output:
    knowledge_09_required: false
    seedance_input_ready: false
    knowledge_10_review_required: false
    ai_quality_review_status: "NOT_REQUIRED | NOT_RUN"
  fallback: ""
```

REAL_SHOOT 不输出 Seedance Package，Knowledge 10 = NOT_REQUIRED。STOCK_ASSET 不输出 Seedance Package，不承担核心 Product Proof，Knowledge 10 = NOT_REQUIRED。

AI_GENERATION + selected_model=Seedance 或 HYBRID + selected_model=Seedance 才需要 Knowledge 09，并且必须生成 Seedance Production Package；Knowledge 10 required，AI Review 初始状态 = NOT_RUN。

AI_GENERATION + selected_model=other 或 HYBRID + selected_model=other 不调用 Knowledge 09，不生成 Seedance Production Package，不伪造 Seedance Prompt；但实际 AI 素材生成后仍须 Knowledge 10 审核，AI Review 初始状态 = NOT_RUN。HYBRID + selected_model=other 仍必须定义 real_layer、ai_layer、proof_layer_owner 和 ai_must_not_rewrite。

```yaml
production_model_routing:
  real_shoot:
    production_type: "REAL_SHOOT"
    routing_output:
      knowledge_09_required: false
      seedance_input_ready: false
      knowledge_10_review_required: false
      ai_quality_review_status: "NOT_REQUIRED"
  stock_asset:
    production_type: "STOCK_ASSET"
    core_product_proof_allowed: false
    routing_output:
      knowledge_09_required: false
      seedance_input_ready: false
      knowledge_10_review_required: false
      ai_quality_review_status: "NOT_REQUIRED"
  seedance_ai:
    production_type: "AI_GENERATION"
    selected_model: "Seedance"
    routing_output:
      knowledge_09_required: true
      seedance_input_ready: true
      knowledge_10_review_required: true
      ai_quality_review_status: "NOT_RUN"
  seedance_hybrid:
    production_type: "HYBRID"
    selected_model: "Seedance"
    required_layers:
      - Real Shoot Layer
      - AI Layer
      - Proof Layer Owner
      - AI Must Not Rewrite
      - Seedance Production Package
    routing_output:
      knowledge_09_required: true
      seedance_input_ready: true
      knowledge_10_review_required: true
      ai_quality_review_status: "NOT_RUN"
  non_seedance_ai:
    production_type: "AI_GENERATION"
    selected_model: "other"
    seedance_production_package_allowed: false
    routing_output:
      knowledge_09_required: false
      seedance_input_ready: false
      knowledge_10_review_required: true
      ai_quality_review_status: "NOT_RUN"
  non_seedance_hybrid:
    production_type: "HYBRID"
    selected_model: "other"
    seedance_production_package_allowed: false
    hybrid_boundary_required: true
    routing_output:
      knowledge_09_required: false
      seedance_input_ready: false
      knowledge_10_review_required: true
      ai_quality_review_status: "NOT_RUN"
```

## 14. Seedance Production Package

只有 Knowledge 08 将镜头路由为 AI_GENERATION 或 HYBRID，并明确设置 selected_model=Seedance 后，才输出 Seedance Production Package。

Production Type alone does not trigger Knowledge 09. Knowledge 09 is model-specific routing for Seedance. selected_model=other 不生成 Seedance Package，即使 Production Type 是 AI_GENERATION 或 HYBRID。

```yaml
seedance_production_package:
  shot_number: ""
  selected_model: "Seedance"
  generation_mode: "T2V | I2V | V2V | R2V | FLF2V | Edit | Extend"
  commercial_purpose: ""
  reference_role_map:
    images: []
    videos: []
    audios: []
  final_seedance_prompt: ""
  chinese_compressed_prompt: ""
  first_frame_requirement: ""
  last_frame_requirement: ""
  camera_instruction: ""
  motion_instruction: ""
  lighting_instruction: ""
  sound_instruction: ""
  preservation_constraints: []
  negative_constraints: []
  parameter_suggestion: {}
  continuity_locks: []
  risk_warning: []
  regeneration_strategy: []
  hybrid_fallback: ""
```

HYBRID 额外输出：

```yaml
hybrid_layers:
  real_layer: []
  ai_layer: []
  proof_layer_owner: "REAL_SHOOT"
  ai_must_not_rewrite: []
```

Seedance 禁止伪造吸力、污垢吸入、污垢移除、透明尘盒结果、清洁 Before/After、美妆人体功效、护理效果、商品结构、Logo、控件、配件、包装、安全、杀菌、兼容性、可测量性能。

## 15. AI Quality Review Status

```yaml
ai_quality_review_status:
  status: "NOT_REQUIRED | NOT_RUN | PASS | REGENERATE | SWITCH_TO_HYBRID | SWITCH_TO_REAL_SHOOT"
  reason: ""
```

没有 AI 镜头：NOT_REQUIRED。有 AI 计划但没有真实成片：NOT_RUN。只有真实生成素材经过 Knowledge 10 审核后，才可以输出 PASS、REGENERATE、SWITCH_TO_HYBRID、SWITCH_TO_REAL_SHOOT。

禁止 Prompt 判 PASS，禁止 Storyboard 判 PASS，禁止 Seedance Package 判 PASS，禁止尚未生成素材却声明 AI Review 完成。

```yaml
ai_review_state_meaning:
  NOT_REQUIRED: "The shot contains no AI-generated material requiring Knowledge 10."
  NOT_RUN: "AI is planned or generated material is expected, but no actual AI output has been reviewed."
  PASS: "Actual generated material passed Knowledge 10."
  REGENERATE: "Actual generated material requires regeneration."
  SWITCH_TO_HYBRID: "AI atmosphere may remain, but the proof layer must return to real footage."
  SWITCH_TO_REAL_SHOOT: "AI generation cannot safely support the required truth level."
```

不得使用模糊的 FAILED 作为 AI Quality Review 正式状态。

## 16. Product-Pack Extensions

### 16.1 Car Vacuum Extension

Car Vacuum Product Pack 为 COMPLETE。相关镜头必须追加：

```yaml
car_vacuum_extension:
  dirt_type: ""
  attachment_used: ""
  sku_attachment_verified: false
  intake_path_visible: false
  collection_result_visible: false
  transparent_bin_protocol: ""
  truth_risk: ""
```

Dirt Intake、Transparent Bin、Pet Hair、Gap Access、Attachment Performance、Blower Function、Runtime Test、Noise Test、Liquid Pickup、Filtration Test 必须 REAL_SHOOT。Blower Function、Runtime Test、Noise Test、Liquid Pickup、Filtration Test 只有 SKU 支持且有真实测试时才允许。

### 16.2 Home Cleaning

Home Cleaning 必须声明 SKELETON_ONLY 和 PARTIAL。必须识别房间、表面、材质、湿度、清洁剂和风险。不能假装有完整表面兼容协议。

### 16.3 Steam Cleaner

Steam Cleaner 必须声明 SKELETON_ONLY、PARTIAL、safety_level=high。无证据时阻断 100% 杀菌、完全消毒、除螨、杀死所有细菌、所有表面通用、所有玻璃安全、所有织物安全。

### 16.4 Beauty Care Tools

Beauty Care Tools 必须声明 SKELETON_ONLY、PARTIAL、human_demo_required=true。Before/After 必须同一人物、同一部位、同一角度、同一光线、同一基础准备。AI 不得承担人体核心功效证明。

## 17. Script Evaluation

每个脚本必须单独评分：

```yaml
script_evaluation:
  hook: 0
  visual_satisfaction: 0
  product_value: 0
  conversion: 0
  production_feasibility: 0
  innovation: 0
  total: 0
  grade: ""
  weakest_module: ""
  optimization_required: false
  optimization_action: ""
```

权重：Hook 30，Visual Satisfaction 20，Product Value 20，Conversion 15，Production Feasibility 10，Innovation 5。

等级：90-100 爆款测试级，85-89 可投放测试级，75-84 继续优化，Below 75 重新设计。

优化规则：低于 85 时只修改最低分模块，每轮只改一个模块，最多三轮，不破坏其他高分模块，修改后必须重新评分，不得虚构新分数。

## 18. File Naming

```yaml
file_naming:
  allowed_characters: "letters, numbers, Chinese characters, hyphen, underscore"
  replace_spaces_with: "_"
  remove_characters:
    - "/"
    - "\\"
    - ":"
    - "*"
    - "?"
    - "\""
    - "<"
    - ">"
    - "|"
  fallback_name: "product_video"
```

完整任务必须统一使用同一个 `<name>`。

## 19. File Generation Behavior

有文件生成能力时，创建真实 UTF-8 Markdown 文件，每个文件非空，文件名正确，返回真实链接，不在聊天窗口重复粘贴完整正文。actual file links only: 只有文件实际存在、非空、文件名正确且链接真实可用时，才能返回文件链接。

无文件生成能力时，不得声称创建成功，必须明确说明没有文件生成能力，用四个独立 Markdown fallback sections 作为 fallback，fallback section 标题仍使用四个文件名，不生成虚假的下载链接，不得使用 fabricated download links。

files_created 必须与实际生成文件数量一致。没有文件生成能力时，files_created 必须为 0。BLOCKED 状态不得声称四文件完成。

## 20. Final Chat Response

READY / PROVISIONAL 且有文件生成能力时，完整 Task A 或 Task B 的聊天窗口只输出：

1. 完成状态
2. 核心战略结论
3. 类目和 Product Pack 支持等级
4. 三套方案区别
5. Unsupported Gaps
6. 四个真实文件链接
7. Knowledge Routing Summary

必须确认四个文件实际存在、每个文件非空、文件名正确、链接真实可用。

READY / PROVISIONAL 但无文件生成能力时，完整 Task A 或 Task B 的聊天窗口只输出：

1. 完成状态
2. 核心战略结论
3. 类目和 Product Pack 支持等级
4. 三套方案区别
5. Unsupported Gaps
6. 四个 fallback section 名称
7. Knowledge Routing Summary

不得生成虚假链接，不得声称文件已创建，不得填写 `files_created: 4`。Fallback section 标题仍为 `<name>_analysis.md`、`<name>_script_01_replicate.md`、`<name>_script_02_low_cost.md`、`<name>_script_03_conversion.md`。

BLOCKED 时只输出：

1. BLOCKED 状态
2. 阻断原因
3. 缺失商品信息
4. 缺失资源
5. 需要补充的证明或安全信息
6. 实际生成的 `<name>_analysis.md` 链接，或分析 fallback section
7. Knowledge Routing Summary

不得输出三套完整脚本已完成，不得输出四文件已创建，不得标记 COMPLETE，不得输出不存在的下载链接。

建议包含：

```yaml
delivery_status:
  status: "COMPLETE | PROVISIONAL | BLOCKED"
  files_created: 0
  generated_file_names: []
  fallback_sections_provided: []
  category_support_level: ""
  product_support_level: ""
  unsupported_gaps: []
```

```yaml
delivery_status_rules:
  complete_with_real_files:
    files_created: 4
    generated_file_names:
      - "<name>_analysis.md"
      - "<name>_script_01_replicate.md"
      - "<name>_script_02_low_cost.md"
      - "<name>_script_03_conversion.md"
  provisional_without_file_capability:
    files_created: 0
    generated_file_names: []
    fallback_sections_provided:
      - "<name>_analysis.md"
      - "<name>_script_01_replicate.md"
      - "<name>_script_02_low_cost.md"
      - "<name>_script_03_conversion.md"
  blocked:
    files_created: "0 or 1"
    generated_file_names:
      - "<name>_analysis.md when actually created"
```

没有真实文件时，不能填写 `files_created: 4`。不得虚报文件数量。

## 21. Final Quality Gate

出现以下任何问题，必须拒绝并重建交付物：

- input_readiness=READY 或 PROVISIONAL 的完整 Task A/B 没有四份交付物或四个 fallback sections。
- input_readiness=BLOCKED，却强行生成证明型脚本。
- input_readiness=BLOCKED，却生成空白或占位脚本凑足四文件。
- selected_model=other，却生成 Seedance Production Package。
- selected_model=Seedance，却遗漏 Knowledge 09。
- 没有文件生成能力，却输出虚假文件链接。
- files_created 与实际生成文件数量不一致。
- ai_quality_review_status 使用不支持的 FAILED 状态。
- 文件名错误。
- 缺少 Routing Summary。
- 隐藏支持缺口。
- 没有 Resource Alignment。
- 没有 Product Truth Review。
- Shot 缺少必填字段。
- Shot 没有 Production Type。
- High Truth Proof 被分配给纯 AI。
- HYBRID 没有 Real/AI Layer。
- Seedance Shot 缺少完整 Package。
- 没有 AI 素材却输出 Knowledge 10 PASS。
- 三个脚本没有独立评分。
- 一轮优化修改多个模块。
- Skeleton 被写成 Production Ready。
- 虚构文件已经生成。
- 虚构 SKU、配件、Claim 或结果。

## 22. Final Assembly Checklist

```yaml
final_assembly_checklist:
  task_type_confirmed: false
  file_name_normalized: false
  knowledge_routing_summary_included: false
  input_readiness_included: false
  resource_alignment_included: false
  product_truth_review_included: false
  support_level_visible: false
  unsupported_gaps_visible: false
  four_file_contract_satisfied_when_required: false
  input_readiness_delivery_branch_correct: false
  blocked_output_restriction_applied: false
  every_script_has_script_summary: false
  every_script_has_script_evaluation: false
  every_shot_has_mandatory_shot_contract: false
  every_shot_has_shot_production_plan: false
  seedance_package_included_only_when_routed: false
  selected_model_routing_correct: false
  seedance_package_model_gate_passed: false
  ai_quality_review_status_correct: false
  product_pack_extensions_applied: false
  generated_file_links_verified: false
  files_created_count_verified: false
  fallback_sections_used_when_needed: false
  file_generation_honesty_applied: false
  final_quality_gate_passed: false
```

four_file_contract_satisfied_when_required 仅适用于 READY 或 PROVISIONAL 的 Task A/B。BLOCKED 不得因为该字段而强制生成四脚本。

Knowledge 18 的最终职责是把上游判断变成一致、可验证、可上传、可交付的文件结构。任何真实性、路由、安全、生产类型、AI 审核或评分冲突，都必须回到对应上游 Knowledge，而不是由 Knowledge 18 自行覆盖。
