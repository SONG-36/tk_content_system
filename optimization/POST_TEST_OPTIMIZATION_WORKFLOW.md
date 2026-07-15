# Post-Test Optimization Workflow

```yaml
workflow_status: "ACTIVE_PROCESS_DOCUMENT"
scope: "Custom GPT post-test feedback, repository fixes, PR review, Builder update, retest, release"
phase: "Phase 1H-A"
automation_level: "manual_process_defined"
planned_automation: "Phase 1H-B"
```

## 1. Purpose

本流程用于把测试后发现的问题转化为可复现、可审查、可验证、可发布的闭环修复。适用反馈来源包括：

- Custom GPT 用户反馈。
- 测试人员反馈。
- 摄影团队反馈。
- 运营团队反馈。
- Product Truth 问题。
- 类目路由问题。
- Script / Shot / Production 问题。
- Builder 配置问题。
- 后续 Action / Backend 问题。

当前仓库是文档优先的 TikTok Shop Product Video Director 系统。正式 Builder 包位于 `custom_gpt_package/multi_category_gpt/`，仓库验证依赖现有 validator、Builder package build、Markdown reference check、Smoke Test Case 和 Smoke Test Result Template。线上 GPT Builder 不会被仓库自动更新。

## 2. Roles

### Reporter

Reporter 负责提交可复现证据，不负责判断根因。

Reporter 必须尽量提供：

- 原始 Prompt。
- 完整输出，不只截取错误片段。
- 截图或生成文件。
- 期望结果。
- 实际结果。
- 测试环境、Custom GPT 版本、Instructions 版本、Knowledge 版本。

### Maintainer

Maintainer 负责把反馈转成仓库层面的最小修复。

Maintainer 负责：

- 复现问题。
- 判断严重度。
- 定位根因。
- 创建修复分支。
- 使用 Codex 做最小范围修改。
- 增加或更新测试证据。
- 运行定向回归和全量仓库验证。
- 创建 Pull Request。

Maintainer 不能直接修改线上 Custom GPT，不能绕过 Project Owner 发布。

### Project Owner

Project Owner 负责最终发布控制。

Project Owner 负责：

- 审核 Pull Request。
- 合并修复。
- 重建 Builder Package。
- 更新 GPT Builder 测试版配置。
- 执行 Preview 回归。
- 发布线上 GPT。
- 关闭缺陷。

明确规则：仓库贡献者不能直接修改线上 Custom GPT。线上 Builder 更新、Preview 回归和发布由 Project Owner 执行。

## 3. End-to-End Workflow

1. 问题发现：Reporter 在 Custom GPT、测试、摄影执行、运营审核或后续 Backend Action 调用中发现问题。
2. 证据收集：Reporter 收集原始 Prompt、完整输出、截图、文件、版本和复现次数。
3. 缺陷登记：以 Planned 的 Defect Template 结构登记；Phase 1H-A 不创建模板文件。
4. 复现：Maintainer 使用相同输入和版本在仓库测试材料或 Builder Preview 中复现。
5. 严重度分类：按 `S0_BLOCKER` 至 `S4_SUGGESTION` 标记影响。
6. 根因定位：判断是 Task、Category、Support Level、Product Pack、Script、Shot、Production Type、Seedance、AI Review、Delivery、Builder 或 Backend Action 问题。
7. 最小责任层判断：执行 `Smallest Responsible Layer Wins`，只修最小能解决问题的层。
8. Change Request：记录缺陷 ID、目标文件、风险、验证命令和 Builder retest 用例。
9. 创建 Git 分支：从最新 `main` 创建 `fix/<defect-id>-<description>`。
10. Codex 最小范围修改：只修改根因层，不顺手重写无关 Knowledge 或 Builder package。
11. 定向回归：运行与缺陷相关的 validator、document test、Builder smoke case 或 backend test。
12. 全量仓库验证：运行当前项目要求的 repository validation。
13. Commit：仅提交明确相关文件。
14. Push 修复分支：推送到远端修复分支，不直接 push `main`。
15. Pull Request：提交 PR，附复现证据、修改范围和验证输出。
16. Owner 审核：Project Owner 检查 Product Truth、安全、路由、Builder 上传影响和回归证据。
17. 合并：Owner 批准后合并 PR。
18. 重建 Builder Package：运行 `python3 tools/build_custom_gpt_package.py`，必要时运行 `--check`。
19. 更新测试版 Custom GPT：Owner 将新 `MAIN_INSTRUCTIONS.md` 和 `01_KNOWLEDGE_UPLOAD/` 上传到 GPT Builder 测试版。
20. Preview 回归：在 Builder Preview 中重跑原失败用例和核心 Smoke Tests。
21. 发布：只有 Release Gate 通过后，Owner 才发布线上 GPT。
22. 关闭缺陷：Builder 更新完成且真实失败用例复测通过后，状态才能进入 `CLOSED`。

## 4. Defect Lifecycle

```yaml
defect_status:
  - NEW
  - NEEDS_REPRODUCTION
  - REPRODUCED
  - DIAGNOSED
  - FIX_IN_PROGRESS
  - REPOSITORY_VALIDATED
  - PR_OPEN
  - MERGED
  - BUILDER_UPDATED
  - BUILDER_RETESTED
  - CLOSED
  - REOPENED
```

状态规则：

- `NEW`: 已收到反馈，但证据可能不完整。
- `NEEDS_REPRODUCTION`: 证据不足或尚未复现。
- `REPRODUCED`: 使用相同输入或等价测试用例复现。
- `DIAGNOSED`: 根因层已定位。
- `FIX_IN_PROGRESS`: 修复分支已创建，正在修改。
- `REPOSITORY_VALIDATED`: 仓库验证通过。
- `PR_OPEN`: Pull Request 已创建。
- `MERGED`: PR 已合并到主线。
- `BUILDER_UPDATED`: GPT Builder 测试版已更新。
- `BUILDER_RETESTED`: Preview 已重跑失败用例和必要 Smoke Tests。
- `CLOSED`: Builder 复测通过，线上发布或明确无需发布。
- `REOPENED`: 复测失败、线上复发或修复引入回归。

`MERGED` 不等于 `CLOSED`。只有 Builder 更新且真实失败用例复测通过后才能 `CLOSED`。

## 5. Severity

```yaml
severity:
  S0_BLOCKER: "必须立即阻断发布或回滚"
  S1_CRITICAL: "核心 Product Truth、安全或交付合同错误"
  S2_MAJOR: "重要流程错误，但可通过人工规避"
  S3_MINOR: "局部质量或格式问题，不影响核心安全"
  S4_SUGGESTION: "优化建议或增强项"
```

本项目示例：

- `S0_BLOCKER`: AI 伪造车载吸尘器吸力、碎屑吸入、透明尘盒结果，导致 Product Truth 被破坏。
- `S0_BLOCKER`: Steam Cleaner 输出“100% 杀菌”或“所有表面都能用”等未经证明的高风险 Claim。
- `S0_BLOCKER`: Beauty AI Before/After 被当作真实人体功效证明。
- `S1_CRITICAL`: Home Cleaning 被错误路由为 Automotive，导致套用汽车场景、材料和 Product Pack。
- `S1_CRITICAL`: Task A/B READY 或 PROVISIONAL 时四文件交付合同错误，或 BLOCKED 状态虚构完成。
- `S1_CRITICAL`: `selected_model=other` 仍生成 Seedance Package，或非 Seedance 任务错误进入 Knowledge 09。
- `S2_MAJOR`: HYBRID 分层缺失，未明确 real_layer、ai_layer、proof owner 和 ai_must_not_rewrite。
- `S2_MAJOR`: AI Review 在没有实际 AI media 时输出 `PASS`。
- `S3_MINOR`: 输出字段顺序或 Markdown 格式不一致，但核心路由、Truth 和交付正确。
- `S4_SUGGESTION`: Hook 表达可更强、示例可更贴近运营语言。

## 6. Evidence Requirements

问题反馈至少包括：

- Custom GPT 版本。
- Instructions 版本。
- Knowledge 版本。
- 原始 Prompt。
- 完整输出。
- 期望结果。
- 实际结果。
- 截图。
- 生成文件。
- 会话引用。
- 复现次数。
- 测试用例 ID。

无法复现时不得直接修改 Knowledge。未复现的问题应保持 `NEEDS_REPRODUCTION`，可以补充观察记录、设计额外测试或要求 Reporter 提供完整上下文。

## 7. Smallest Responsible Layer

`Smallest Responsible Layer Wins` 是本流程的核心修复原则。

含义：先修最小、最靠近根因、影响面最小的责任层。不得因为某个输出错误就直接重写 `MAIN_INSTRUCTIONS.md` 或大范围改 Knowledge。

路由矩阵说明：

| 问题类型 | 优先检查层 | 典型修复位置 |
| --- | --- | --- |
| Task 判断错误 | Task Router | `MAIN_INSTRUCTIONS` 或 Knowledge 18 交付分支；需要 Owner 审批 |
| Category Router 错误 | Category Router | Knowledge 11 / `workflows/Category_Router.md` source |
| Support Level 错误 | Category/Product support rules | Knowledge 11-16 或对应 category skeleton source |
| Product Pack 错误 | Product Pack | Knowledge 13 或 `categories/.../products/...` source |
| Script 错误 | Script writing/scoring | Knowledge 05、06、18 或对应 source |
| Shot 错误 | Production planning | Knowledge 07、08 或 product shooting source |
| Production Type 错误 | Production Type rules | Knowledge 08、13、18 |
| Seedance 错误 | Seedance Routing | Knowledge 09、17、18；不得修改第三方 Seedance 原始 Skill |
| AI Review 错误 | AI Review timing/status | Knowledge 10、18 |
| Delivery 错误 | Final delivery contract | Knowledge 18 |
| Builder 错误 | Builder upload/config | `custom_gpt_package/multi_category_gpt/03_BUILDER_SETUP/` and Builder manual update |
| Backend Action 错误 | Backend API contract/runtime | `backend/` |

未来 Phase 1H-B 可把此表拆成 `DEFECT_ROUTING_MATRIX.md`，本阶段只在本文档中定义。

## 8. Protected Files and Change Boundaries

必须遵守：

- 不直接修改线上 Builder。
- 不在 `main` 分支直接开发。
- 不顺便修改无关 Knowledge。
- 不降低 Product Truth。
- 不把 `SKELETON_ONLY` 或 `PARTIAL` 未经充分知识建设升级为 `COMPLETE`。
- 不修改第三方 Seedance 原始 Skill。
- 不修改生成文件而忽略 Source of Truth。
- 不通过删除 Validator 或弱化测试来解决失败。
- 不把 Repository PASS 当作 Builder PASS。
- 不为了修复 Backend Action 问题随意修改 Knowledge。

若必须修改冻结或 Builder runtime 文件，应在 Change Request 中明确说明原因、风险和 Owner 审批要求。

## 9. Git Workflow

推荐流程：

```bash
git checkout main
git pull
git checkout -b fix/<defect-id>-<description>
```

修复后：

```bash
git add <explicit-files>
git commit
git push -u origin <branch>
```

Git 规则：

- 不建议 `git add .`。
- 不直接 push `main`。
- 使用 Pull Request。
- 核心文件由 Project Owner 审核。
- PR 描述必须包含缺陷 ID、复现步骤、修改文件、验证命令、Builder retest 计划。
- 若修复影响 Builder package，PR 必须说明是否需要重新上传 Instructions 或 Knowledge。

## 10. Validation Layers

### Repository Validation

Repository Validation 证明仓库文件和生成包一致，不证明线上 GPT Builder 已更新。

当前可用验证层：

```bash
python3 tools/validate_main_instructions.py
python3 tools/validate_knowledge_01_17.py
python3 tools/validate_knowledge_18.py
python3 tools/validate_knowledge_01_18.py
python3 tools/check_markdown_references.py
python3 tools/build_custom_gpt_package.py
python3 tools/build_custom_gpt_package.py --check
git diff --check
```

定向测试材料：

- `tests/test_category_router.md`
- `tests/test_car_vacuum_product_pack.md`
- `tests/test_incomplete_category_fallback.md`
- `tests/test_cross_category_guardrails.md`
- `tests/builder_smoke_test_cases.md`
- `custom_gpt_package/multi_category_gpt/04_TESTS/SMOKE_TEST_CASES.md`

若问题属于 Backend Action，则还应运行 `backend/` 对应测试。本流程只定义边界，不新增 backend 自动化。

### Builder Validation

Builder Validation 证明 GPT Builder 测试版或线上配置真的使用了新材料，并且模型行为通过复测。

Builder Validation 包括：

- 上传新 Instructions 或 Knowledge。
- 按 `custom_gpt_package/multi_category_gpt/03_BUILDER_SETUP/UPLOAD_ORDER.md` 更新。
- Preview 重跑失败用例。
- 运行核心 Smoke Tests。
- 检查文件链接真实性。
- 检查实际模型行为，而不是只检查仓库文本。
- 使用 `SMOKE_TEST_RESULT_TEMPLATE.md` 记录结果。

明确：Repository PASS 不等于 Builder PASS。只有 Builder Preview 中真实失败用例通过，才能进入 `BUILDER_RETESTED`。

## 11. Release Gate

允许发布条件：

- 所有目标缺陷已修复。
- 定向回归通过。
- 全量仓库验证通过。
- open `S0_BLOCKER` = 0。
- open `S1_CRITICAL` = 0。
- open `S2_MAJOR` = 0。
- Builder 已更新。
- 失败用例已重测。
- 核心 Smoke Tests 已通过。
- Product Truth、安全、Skeleton/Partial 边界没有被削弱。
- Builder upload manifest 和实际上传文件一致。

若任一条件不满足，不发布。`MERGED` 后仍可能停留在 `BUILDER_UPDATED` 或 `BUILDER_RETESTED` 前，不能关闭缺陷。

## 12. Custom GPT Update Responsibility

协作者负责：

- 仓库修复。
- Push 修复分支。
- Pull Request。
- 测试证据。

Project Owner 负责：

- 合并。
- 更新 Builder。
- Preview 回归。
- 发布。
- 缺陷关闭。

仓库不会自动修改 GPT Builder。任何“已发布”“已上传”“线上已修复”的声明必须来自 Project Owner 的 Builder 操作记录。

## 13. Action / Backend Boundary

未来 Backend 问题应优先修改：

- `backend/`

不能为了修复 API 问题随意修改 Knowledge。只有以下情况才修改 GPT 层：

- Custom GPT 发送的 Action payload 违反正式 API contract。
- GPT 路由把不该进入 Backend 的任务送入 Backend。
- GPT 对 Backend 返回错误的解释或降级处理错误。
- API contract 变更需要同步 Instructions / Knowledge / Builder Action schema。

Backend Action 缺陷的 Repository Validation 应包含 backend tests、OpenAPI 检查和相关 contract 验证；Builder Validation 应包含 Action Preview 或实际 GPT Action 调用复测。

## 14. Versioning

建议版本线：

- `V2.6-BASELINE`: 当前 Builder-ready 基线。
- `V2.6.1-RC`: 单轮缺陷修复候选。
- `V2.6.1`: 通过 Builder retest 后的补丁发布。
- `V2.7`: 涉及新类目、新 Product Pack 或较大流程变化的版本。

每次发布记录：

- 修复 Defect。
- 修改文件。
- Knowledge 是否变化。
- Instructions 是否变化。
- Repository Validation。
- Builder Retest。
- Published 状态。

版本记录可以先写入现有 `version/` 或 release manifest 体系；Phase 1H-A 不新增版本工具。

## 15. Example Walkthrough: Home Cleaning 被错误路由为 Automotive

### 15.1 登记

Reporter 提交：

```yaml
defect_id: "DEF-001"
summary: "Home Cleaning mop prompt routed as automotive_cleaning"
severity: "S1_CRITICAL"
custom_gpt_version: "V2.6-BASELINE"
instructions_version: "MAIN_INSTRUCTIONS 7195 chars"
knowledge_version: "Knowledge 01-18 current upload package"
test_case_id: "BST-home-routing-manual"
original_prompt: "这是一个家用地板清洁工具，请生成 TikTok Shop 视频方案。"
expected_result: "route=home_cleaning, support=SKELETON_ONLY or PARTIAL"
actual_result: "route=automotive_cleaning, uses car interior assumptions"
reproduction_count: 2
attachments: ["screenshot", "full_output.md"]
```

### 15.2 复现

Maintainer 使用相同 Prompt 在 Builder Preview 或本地文档测试语境中复现。若无法复现，状态保持 `NEEDS_REPRODUCTION`，不得直接修改 Knowledge。

### 15.3 定位

根因层判断：

- Task 判断正确：用户要求 Product-to-Video Generation。
- Category Router 错误：home cleaning 被路由到 automotive。
- Support Level 也错误：home cleaning 应声明 `SKELETON_ONLY` / `PARTIAL`。
- 最小责任层：Knowledge 11 / `workflows/Category_Router.md` source，而不是重写全套 Knowledge。

### 15.4 建分支

```bash
git checkout main
git pull
git checkout -b fix/DEF-001-home-cleaning-routing
```

### 15.5 修改

Maintainer 使用 Codex 做最小范围修改：

- 修改 Category Router source 或正式 Knowledge 11 对应规则。
- 不修改 car vacuum Product Pack。
- 不把 Home Cleaning 升级为 `COMPLETE`。
- 不修改第三方 Seedance Skill。

### 15.6 定向回归

建议运行：

```bash
python3 tools/validate_knowledge_01_17.py
python3 tools/validate_knowledge_01_18.py
python3 tools/check_markdown_references.py
python3 tools/build_custom_gpt_package.py --check
git diff --check
```

人工复查：

- `tests/test_category_router.md`
- `tests/test_incomplete_category_fallback.md`
- `tests/test_cross_category_guardrails.md`
- `tests/builder_smoke_test_cases.md` 中 Unknown Category、Steam、Beauty 和 Car Vacuum 相关用例。

### 15.7 PR

PR 必须写明：

- `DEF-001` 已复现。
- 修改层是 Category Router。
- 未修改 Instructions。
- 未削弱 Product Truth。
- Repository Validation 输出。
- Builder Preview 需重跑原失败 Prompt 和核心 Smoke Tests。

### 15.8 Builder 更新

Project Owner 合并后：

1. 运行 `python3 tools/build_custom_gpt_package.py`。
2. 按 `UPLOAD_ORDER.md` 更新测试版 GPT Builder。
3. 不上传 `02_SOURCE_FILES/`、`04_TESTS/`、`05_AUDIT/`。
4. 在 Preview 中重跑 `DEF-001` 原 Prompt。
5. 运行核心 Smoke Tests。

### 15.9 关闭

只有以下条件全部满足，`DEF-001` 才能进入 `CLOSED`：

- PR merged。
- Builder test version updated。
- 原失败 Prompt 在 Preview 中返回 `home_cleaning`。
- 输出声明 `SKELETON_ONLY` / `PARTIAL`，不套用 automotive。
- 核心 Smoke Tests 没有 S0/S1/S2 回归。

## 16. Planned Next Phase

Phase 1H-B:
根据已审核的流程文档，创建 Defect Template、Change Request、Routing Matrix、Regression Matrix、Release Gate、验证工具和 GitHub 协作模板。

Phase 1H-A 不创建：

- `defect_registry.yaml`
- `DEFECT_ROUTING_MATRIX.md`
- `REGRESSION_MATRIX.md`
- `RELEASE_GATE.md`
- Python 工具
- GitHub Issue Template
- Pull Request Template
- `CODEOWNERS`
