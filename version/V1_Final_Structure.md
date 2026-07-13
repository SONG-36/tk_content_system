# V1 Final Structure

## Purpose

本文件记录 `TikTok Shop Car Cleaning AI Knowledge System` 的最终 Knowledge 架构、文件职责和调用关系。

---

## 1. Final Knowledge Structure

`knowledge/`

- `01_TikTok_Viral_Analysis_Framework.md`
- `02_Car_Cleaning_Content_Psychology.md`
- `03_Cleaning_Video_Hook_Database.md`
- `04_Satisfying_Cleaning_Visual_Library.md`
- `05_TikTok_Shop_Script_Writing_Rules.md`
- `06_Video_Script_Scoring_System.md`

---

## 2. Layering

### 2.1 AI 能力层

- `01_TikTok_Viral_Analysis_Framework.md`
- `05_TikTok_Shop_Script_Writing_Rules.md`
- `06_Video_Script_Scoring_System.md`

职责：

- 定义视频分析方法
- 定义脚本生成方法
- 定义脚本审核和优化方法

### 2.2 行业知识层

- `02_Car_Cleaning_Content_Psychology.md`
- `03_Cleaning_Video_Hook_Database.md`
- `04_Satisfying_Cleaning_Visual_Library.md`

职责：

- 提供用户心理与 JTBD 输入
- 提供 Hook 选择库
- 提供视觉证明与满足感机制库

---

## 3. File Responsibilities

### 3.1 `01_TikTok_Viral_Analysis_Framework.md`

职责：

- 拆解爆款视频机制
- 输出 Hook、Retention、Visual Proof、Psychology、Framework、Transfer Logic

产出给：

- `05_TikTok_Shop_Script_Writing_Rules.md`
- `06_Video_Script_Scoring_System.md`

### 3.2 `02_Car_Cleaning_Content_Psychology.md`

职责：

- 定义购买动机
- 提供用户分层 JTBD
- 提供心理触发器到 Hook/镜头/产品的映射

产出给：

- `01`
- `05`
- `06`

### 3.3 `03_Cleaning_Video_Hook_Database.md`

职责：

- 定义 Hook 分类
- 解释每类 Hook 的机制、有效原因、适配场景和迁移方法

产出给：

- `01`
- `05`

### 3.4 `04_Satisfying_Cleaning_Visual_Library.md`

职责：

- 定义高停留、高爽感、高信任视觉机制
- 指导脚本和拍摄中的 visual proof 设计

产出给：

- `01`
- `05`
- `06`

### 3.5 `05_TikTok_Shop_Script_Writing_Rules.md`

职责：

- 把分析层和行业知识层转成三版本脚本
- 规定镜头设计、UGC、Proof、CTA 规则

产出给：

- 创作阶段
- `06`

### 3.6 `06_Video_Script_Scoring_System.md`

职责：

- 审核脚本质量
- 按权重打分
- 识别最弱模块
- 在 3 轮内优化

---

## 4. Call Flow

推荐调用顺序：

1. `02`、`03`、`04` 提供行业和创意底层知识
2. `01` 对标视频并输出结构化分析
3. `05` 根据分析结果生成三版本脚本
4. `06` 对脚本评分、诊断和迭代优化

---

## 5. Upload Readiness

这 6 个 `knowledge` 文件已经按 GPT Builder Knowledge 的可上传形态整理：

- 文件名稳定
- 内容职责清晰
- 结构化标题明显
- 没有依赖运行时变量才能理解
- 可被模型直接作为知识文档读取

---

## 6. Duplicate Control

重复控制原则：

- `02` 负责心理，不展开完整脚本规则
- `03` 负责 Hook，不做完整视觉机制库
- `04` 负责视觉，不重复完整 JTBD
- `05` 负责生成，不重复完整行业研究
- `06` 负责评分，不重写生成规则

---

## 7. Supporting Research Files

`research/`

- `prompt_framework_analysis.md`
- `marketing_framework_analysis.md`
- `car_cleaning_psychology_research.md`
- `cleaning_hook_research.md`
- `cleaning_visual_research.md`

这些研究文件为最终 Knowledge 文件提供策略依据，但最终上传优先使用 `knowledge/` 下的 6 个文件。
