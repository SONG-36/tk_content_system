# TikTok Shop Product Video Director
# 视频生成后台开发任务交接

## 一、为什么建议换新聊天

当前聊天已经完成：

- Custom GPT Main Instructions
- Knowledge 01–18
- Builder 上传包
- 测试方案
- Product Truth / Seedance / AI Review 规则

下一阶段属于新的工程任务：

```text
Custom GPT Action
→ Python FastAPI Backend
→ Mock Video Job API
→ Seedance Adapter
→ 状态查询与结果 URL
→ Knowledge 10 审核
```

建议新开聊天，原因：

1. 当前上下文很长，继续开发代码容易混淆冻结文档和新后台代码。
2. 后台开发需要独立的架构、接口、测试和安全边界。
3. 新聊天可以明确禁止修改已经完成的 Instructions 和 Knowledge 01–18。
4. 后续 Action、Mock、Seedance 真实接口可以形成单独版本线。

---

## 二、当前项目状态

```yaml
project_status:
  custom_gpt_name: "TikTok Shop Product Video Director"
  main_instructions_ready: true
  knowledge_01_18_ready: true
  builder_package_ready: true
  builder_preview_tested: false
  action_backend_started: false
  seedance_api_connected: false
```

正式 Builder 材料：

```text
custom_gpt_package/multi_category_gpt/
├── 00_INSTRUCTIONS/
│   └── MAIN_INSTRUCTIONS.md
└── 01_KNOWLEDGE_UPLOAD/
    ├── 01_...
    ├── ...
    └── 18_Deliverable_and_Output_Contract.md
```

以下规则已经冻结，后台不得削弱：

- Task A–E
- Category Router
- READY / PROVISIONAL / BLOCKED
- Product Truth
- REAL_SHOOT / AI_GENERATION / HYBRID / STOCK_ASSET
- `selected_model=Seedance` 才调用 Knowledge 09
- 真实 AI 素材存在后才执行 Knowledge 10
- AI 不得伪造吸力、清洁结果、Before/After、人体功效、安全或杀菌证明
- HYBRID 的 Proof Layer 必须是真实层

---

## 三、后台开发目标

开发一个 Python FastAPI 后台，供 Custom GPT Action 调用。

后台必须：

1. 提供公开 HTTPS JSON API；
2. 接收 Seedance Production Package；
3. 验证 Production Type 和 Truth Dependency；
4. 创建异步视频任务；
5. 立即返回 `job_id`；
6. 支持查询状态；
7. 支持取消与重试；
8. 支持幂等，避免重复收费；
9. 支持素材上传或素材 URL；
10. 返回真实视频 URL；
11. 区分后台任务状态与 Knowledge 10 审核状态；
12. 先完成 Mock，再连接真实 Seedance。

---

## 四、推荐架构

```text
User
  ↓
Custom GPT
  ↓ Knowledge 08
  ↓ Knowledge 09
GPT Action
  ↓ HTTPS / OpenAPI
Python FastAPI Backend
  ├── Auth
  ├── Request Validation
  ├── Truth & Safety Gate
  ├── Idempotency
  ├── Job Store
  ├── Asset Store
  ├── Mock Provider
  ├── Seedance Provider
  ├── Status Polling
  ├── Retry / Cancel
  └── Secure Result URL
```

---

## 五、建议目录

```text
backend/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── api/
│   │   ├── health.py
│   │   ├── assets.py
│   │   └── video_jobs.py
│   ├── schemas/
│   │   ├── common.py
│   │   ├── assets.py
│   │   └── video_jobs.py
│   ├── services/
│   │   ├── truth_gate.py
│   │   ├── idempotency.py
│   │   ├── job_manager.py
│   │   ├── storage.py
│   │   └── providers/
│   │       ├── base.py
│   │       ├── mock.py
│   │       └── seedance.py
│   ├── repositories/
│   │   ├── jobs.py
│   │   └── assets.py
│   └── security/
│       └── auth.py
├── openapi/
│   └── custom_gpt_action.openapi.yaml
├── tests/
├── .env.example
├── pyproject.toml
├── README.md
└── Dockerfile
```

---

## 六、第一阶段 API

### 1. 健康检查

```http
GET /health
```

### 2. 获取素材上传地址

```http
POST /v1/assets/upload-url
```

### 3. 创建视频任务

```http
POST /v1/video-jobs
```

示例请求：

```json
{
  "shot_number": "Shot 03",
  "production_type": "HYBRID",
  "selected_model": "Seedance",
  "generation_mode": "R2V",
  "prompt": "Production-ready prompt",
  "negative_constraints": [],
  "preservation_constraints": [],
  "reference_assets": [
    {
      "asset_id": "asset_001",
      "role": "product_identity"
    }
  ],
  "truth_dependency": "low",
  "product_proof_owner": "real_shoot",
  "hybrid_layers": {
    "real_layer": ["real product"],
    "ai_layer": ["AI garage background"],
    "ai_must_not_rewrite": ["logo", "shape", "controls"]
  },
  "duration_seconds": 8,
  "aspect_ratio": "9:16",
  "idempotency_key": "conversation-shot03-v1"
}
```

响应：

```json
{
  "job_id": "job_001",
  "status": "QUEUED",
  "provider": "mock"
}
```

### 4. 查询任务

```http
GET /v1/video-jobs/{job_id}
```

### 5. 取消任务

```http
POST /v1/video-jobs/{job_id}/cancel
```

### 6. 重试任务

```http
POST /v1/video-jobs/{job_id}/retry
```

---

## 七、状态必须分开

后台任务状态：

```text
QUEUED
PROCESSING
SUCCEEDED
FAILED
CANCELLED
```

Knowledge 10 审核状态：

```text
NOT_REQUIRED
NOT_RUN
PASS
REGENERATE
SWITCH_TO_HYBRID
SWITCH_TO_REAL_SHOOT
```

示例：

```yaml
generation_job:
  status: SUCCEEDED

ai_quality_review:
  status: NOT_RUN
```

表示视频已生成，但尚未经过 Knowledge 10。

---

## 八、后台 Truth Gate

后台必须作为第二层保险。

直接阻断：

```yaml
block_when:
  - truth_dependency == "high" and production_type == "AI_GENERATION"
  - AI suction proof
  - AI dirt-intake proof
  - AI cleaning Before/After
  - AI transparent-bin proof
  - AI beauty efficacy
  - AI grooming efficacy
  - AI sterilization proof
  - AI safety proof
  - unverified product accessory
  - unverified product structure
```

HYBRID 必须满足：

```yaml
hybrid_requirements:
  real_layer_required: true
  ai_layer_required: true
  product_proof_owner: "real_shoot"
  ai_must_not_rewrite_required: true
```

错误响应示例：

```json
{
  "error_code": "HIGH_TRUTH_AI_BLOCKED",
  "message": "High-truth proof cannot use pure AI.",
  "required_production_type": "REAL_SHOOT_OR_HYBRID"
}
```

---

## 九、幂等和费用保护

创建任务必须支持：

```text
Idempotency-Key
```

规则：

- 同一 key + 同一 payload：返回已有任务；
- 同一 key + 不同 payload：返回冲突；
- GPT 重试不能重复创建收费任务；
- 提交真实 Seedance 前必须让用户确认模型、时长和可能费用。

---

## 十、素材流程

推荐：

```text
请求预签名上传 URL
→ 用户上传素材
→ 后台返回 asset_id
→ 创建视频任务时传 asset_id
```

每个素材必须记录：

```yaml
asset:
  asset_id: ""
  owner_id: ""
  content_type: ""
  size_bytes: 0
  role: ""
  checksum: ""
  status: "PENDING | READY | REJECTED"
```

参考角色：

- product_identity
- environment
- first_frame
- last_frame
- camera_motion
- action_motion
- audio_tempo

每个素材只分配一个主要角色。

---

## 十一、开发阶段

### Phase 2A：API Contract + Mock Backend

先完成：

- FastAPI 项目
- 请求/响应 Schema
- Truth Gate
- Idempotency
- Mock Provider
- OpenAPI Action Schema
- 单元测试
- 接口测试

暂时不连接真实 Seedance。

### Phase 2B：Custom GPT Action + Mock

测试：

- GPT 是否正确调用 Action
- 是否正确传参数
- 是否返回 job_id
- 是否正确查询状态
- 是否避免重复提交
- 是否阻断高真实性 AI

### Phase 2C：Seedance Adapter

在公共 API 不变的前提下，替换或新增 Provider Adapter。

### Phase 2D：端到端测试

```text
Task E
→ Knowledge 08
→ Knowledge 09
→ Action
→ Backend
→ Seedance
→ Result URL
→ Knowledge 10
```

---

## 十二、第一阶段验收

```yaml
phase_2a_acceptance:
  backend_directory_created: true
  fastapi_app_created: true
  health_endpoint_working: true
  create_job_working: true
  get_job_working: true
  cancel_job_working: true
  retry_job_working: true
  mock_provider_working: true
  truth_gate_working: true
  hybrid_gate_working: true
  idempotency_working: true
  openapi_action_schema_created: true
  tests_passed: true
  custom_gpt_files_modified: false
  real_seedance_connected: false
```

---

## 十三、新聊天首条任务指令

把本文件上传或粘贴到新聊天，然后发送：

```text
请先读取这份任务交接，检查仓库结构和所有 AGENTS.md。

执行 Phase 2A：API Contract and Mock Backend Skeleton。

要求：
1. 不修改已冻结的 MAIN_INSTRUCTIONS.md。
2. 不修改 Knowledge 01–18。
3. 在 backend/ 下创建独立 FastAPI 后台。
4. 先完成 Mock Provider，不连接真实 Seedance。
5. 实现 health、asset upload URL、create job、get job、cancel、retry。
6. 实现 Product Truth Gate、HYBRID Gate 和 Idempotency。
7. 创建 Custom GPT Action 的 OpenAPI Schema。
8. 创建单元测试和 API Contract 测试。
9. 不执行 git add、commit、push。
10. 完成后给出文件清单、接口清单、测试结果和下一阶段计划。
```

---

## 十四、完成报告格式

```yaml
phase_2a:
  status: "PASS | FAIL"
  backend_directory_created: false
  fastapi_app_created: false
  mock_provider_created: false
  truth_gate_created: false
  hybrid_gate_created: false
  idempotency_created: false
  openapi_action_schema_created: false
  tests_created: false
  tests_passed: false
  custom_gpt_files_modified: false
  real_seedance_connected: false
  staged: false
  committed: false
  pushed: false
```

必须同时列出：

- 创建和修改的文件
- 所有公开端点
- 请求/响应 Schema
- 错误码
- 测试结果
- 剩余风险
- 下一阶段

---

## 十五、最终交接原则

Custom GPT Knowledge 系统是：

```text
决策层 + 创意层 + Truth/Safety 层
```

Python 后台是：

```text
执行层 + 任务层 + Provider 层
```

后台不得削弱 Custom GPT 已定义的 Product Truth、安全、支持等级和 AI Proof 限制。
