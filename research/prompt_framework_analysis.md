# awesome-chatgpt-prompts Prompt Framework Analysis

## Scope

本分析基于 `source/open_source/awesome-chatgpt-prompts` 的 prompt engineering 教程内容，而不是只看 `PROMPTS.md` 中的社区 prompt 列表。对我们最有价值的是其中可系统化复用的方法，而不是单条 prompt 文案。

重点参考章节：

- `zh/03-core-prompting-principles.mdx`
- `zh/04-role-based-prompting.mdx`
- `zh/05-structured-output.mdx`
- `zh/07-few-shot-learning.mdx`
- `zh/08-iterative-refinement.mdx`
- `zh/10-system-prompts-personas.mdx`
- `zh/11-prompt-chaining.mdx`
- `zh/13-multimodal-prompting.mdx`
- `zh/14-context-engineering.mdx`
- `zh/25-agents-and-skills.mdx`

---

## 1. 适合视频分析 Agent 的 Prompt 设计方法

### 1.1 多模态引导式分析

最适合直接进入系统的能力。

原因：

- 车载清洁视频本质上是视觉驱动任务，不能只靠文本总结。
- `awesome-chatgpt-prompts` 强调多模态任务不能只问“你看到了什么”，而要明确引导模型关注哪些区域、哪些信号、哪些异常。

建议落地方式：

- 明确要求模型关注：
  - 0-3 秒 hook
  - 脏污类型
  - 清洁动作与工具接触点
  - before/after 反差
  - 口播/字幕/OCR
  - CTA 是否清晰
- 输出结构固定为 JSON，避免自由发挥。

适用来源：

- `zh/13-multimodal-prompting.mdx`
- `zh/05-structured-output.mdx`

### 1.2 角色化分析

适合。

原因：

- 视频分析不是“通用总结”，而是带业务目的的分析。
- 同一个视频，从“视觉导演”“电商转化分析师”“平台审核员”三个视角看，结论不同。

建议角色堆叠：

- `TikTok Shop 短视频分析师`
- `DTC 车品转化策略师`
- `多模态内容审核助手`

作用：

- 聚焦术语
- 提高判断维度稳定性
- 减少泛泛点评

适用来源：

- `zh/04-role-based-prompting.mdx`
- `zh/10-system-prompts-personas.mdx`

### 1.3 并行链分析

非常适合。

原因：

- 一个视频往往要同时分析多个维度：视觉、文案、卖点、节奏、情绪、信任感。
- 单提示容易把这些混在一起，输出不稳定。

建议链路：

1. 分支 A：镜头与场景拆解
2. 分支 B：字幕/口播/OCR 提取
3. 分支 C：卖点与使用场景抽取
4. 分支 D：情绪与转化信号判断
5. 合并：生成统一视频诊断报告

适用来源：

- `zh/11-prompt-chaining.mdx` 中的 parallel chain

### 1.4 Few-shot 标签校准

适合。

原因：

- “强 hook”“弱 hook”“可信 demo”“过度夸张”这些标签非常主观。
- few-shot 可以用 2-5 个标注样例校准模型的判断边界。

适合做示例的字段：

- hook 类型分类
- 脏污类型分类
- 演示可信度分级
- CTA 强弱
- 视频风格标签：UGC / demo / testimonial / before-after / voiceover

适用来源：

- `zh/07-few-shot-learning.mdx`

### 1.5 上下文工程与 RAG

必须进入系统。

原因：

- 视频分析不能脱离商品事实、品牌限制、平台合规、目标受众。
- 模型本身不知道我们的 SKU、材质、禁用词、清洁适用场景。

应接入的上下文：

- 商品卖点库
- 不可说 claims 清单
- 目标人群画像
- 竞品标签
- 历史爆款分析结果

适用来源：

- `zh/14-context-engineering.mdx`

### 1.6 结构化输出

必须进入系统。

原因：

- 后续脚本 Agent 和评估 Agent 都要消费分析结果。
- 如果分析输出是散文，后续链路很难可靠复用。

推荐字段：

```json
{
  "hook_type": "",
  "dirty_surface": [],
  "product_actions": [],
  "benefits_shown": [],
  "proof_signals": [],
  "cta_present": true,
  "risks": [],
  "overall_score": 0
}
```

适用来源：

- `zh/05-structured-output.mdx`

### 1.7 核心结论

视频分析 Agent 最应该吸收的不是“写一个分析 prompt”，而是以下组合：

- 多模态引导
- 角色堆叠
- 并行链
- 结构化 JSON 输出
- few-shot 标签校准
- RAG 上下文注入

---

## 2. 适合脚本生成 Agent 的 Prompt 设计方法

### 2.1 角色堆叠式创作

非常适合。

建议复合角色：

- `TikTok Shop 车品短视频编导`
- `Direct-response copywriter`
- `UGC 口播脚本作者`

作用：

- 保证文案不是“会写”，而是“会卖”
- 让镜头语言、口播语言、转化语言统一

适用来源：

- `zh/04-role-based-prompting.mdx`
- `zh/10-system-prompts-personas.mdx`

### 2.2 提取 -> 转换 -> 生成

非常适合，是脚本 Agent 的主链。

建议链路：

1. 从商品与视频分析结果中提取：
   - pain points
   - benefits
   - proof
   - objections
2. 转换为某一营销框架的 beat list
3. 生成最终脚本

优点：

- 可控
- 易 debug
- 可切换不同营销框架

适用来源：

- `zh/11-prompt-chaining.mdx`

### 2.3 Few-shot 风格示例

非常适合。

原因：

- TikTok 脚本的差异主要体现在语气、节奏、信息密度和镜头组织上。
- 抽象要求“更像 UGC”“更像爆款”不够稳定，示例更有效。

建议示例库：

- 强问题开场型
- before-after 演示型
- 车主吐槽型
- 一镜到底口播型
- 主播导购型

适用来源：

- `zh/07-few-shot-learning.mdx`

### 2.4 明确输出结构

必须进入系统。

脚本 Agent 不应该直接输出一大段文案，而应该输出结构化脚本。

推荐格式：

- 镜头编号
- 时间段
- 画面动作
- 口播/字幕
- 卖点目标
- 情绪目标
- CTA

适用来源：

- `zh/05-structured-output.mdx`

### 2.5 生成 -> 评审 -> 优化

非常适合。

原因：

- 短视频脚本的一次生成质量波动很大。
- 先产草稿，再按转化标准打分，再局部重写，通常比“直接要终稿”更稳。

建议评审维度：

- hook 强度
- 痛点清晰度
- demo 可拍性
- 利益点密度
- 信任建立
- CTA 清晰度
- TikTok 风格匹配度

适用来源：

- `zh/11-prompt-chaining.mdx`
- `zh/08-iterative-refinement.mdx`

### 2.6 系统提示词分层

适合，建议作为 Skill 内核。

建议分层：

- 核心规则：不能编造产品功能、不能越过平台合规
- 角色：你是谁
- 任务背景：当前 SKU、受众、视频目标
- 输出规范：脚本格式、时长、镜头数量

适用来源：

- `zh/10-system-prompts-personas.mdx`

### 2.7 核心结论

脚本生成 Agent 最应该吸收的组合：

- 角色堆叠
- ETG 主链
- few-shot 风格示例
- 结构化脚本输出
- 生成后自评再优化
- 分层 system prompt

---

## 3. 适合自我评估 Agent 的 Prompt 设计方法

### 3.1 专门的评审角色

必须进入系统。

不要让生成 Agent 顺手评价自己，而要单独定义“批判者”角色。

推荐角色：

- `TikTok Shop 创意审核官`
- `短视频转化审稿人`
- `平台合规与真实性检查员`

适用来源：

- `zh/04-role-based-prompting.mdx`
- `zh/10-system-prompts-personas.mdx`

### 3.2 评分 rubric + 结构化输出

必须进入系统。

自评最怕“感觉还不错”。

应该强制输出：

```json
{
  "hook_score": 0,
  "clarity_score": 0,
  "benefit_score": 0,
  "proof_score": 0,
  "cta_score": 0,
  "compliance_score": 0,
  "issues": [],
  "rewrite_priority": []
}
```

适用来源：

- `zh/05-structured-output.mdx`

### 3.3 生成 -> 评审 -> 优化闭环

必须进入系统。

`awesome-chatgpt-prompts` 里最适合自评 Agent 的，就是 iterative chain。

推荐规则：

- 先评分
- 分数低于阈值才触发改写
- 每轮只改最差的 1-2 个维度
- 最多 3 轮

适用来源：

- `zh/11-prompt-chaining.mdx`
- `zh/08-iterative-refinement.mdx`

### 3.4 Few-shot 评分校准

适合。

原因：

- 自评维度如果没有示例，模型会漂。
- 给出“高分脚本”“低分脚本”“典型违规脚本”样例，评估标准会稳定得多。

推荐示例类型：

- hook 强 vs 弱
- benefits 具体 vs 空泛
- CTA 明确 vs 模糊
- 演示可信 vs 夸张

适用来源：

- `zh/07-few-shot-learning.mdx`

### 3.5 上下文约束式评估

必须进入系统。

自评不能只看文案本身，还要看是否符合：

- 商品真实参数
- 品牌语气
- 平台规则
- 目标受众认知水平

适用来源：

- `zh/14-context-engineering.mdx`

### 3.6 核心结论

自我评估 Agent 最应该吸收的组合：

- 专门 critic 角色
- rubric 化评分
- 结构化 JSON
- few-shot 评分校准
- 迭代式改稿闭环
- RAG 约束校验

---

## 4. 应该进入我们 Skill 系统的方法总表

### 必须进入

- 分层 system prompt
- 角色堆叠
- 多模态引导式分析
- 结构化 JSON 输出
- prompt chaining
- 自评迭代闭环
- 上下文工程 / RAG

### 强烈建议进入

- few-shot 风格样例
- few-shot 评分样例
- 条件路由链
- Prompt versioning / prompt log

### 可后续增强

- 自动摘要长期对话
- 更复杂的 tool-use 编排
- 多版本脚本并行生成后择优

---

## 5. 对 Skill 系统的具体建议

### 建议的三 Agent 架构

1. `video_analysis_agent`
   - 输入：视频帧、字幕、商品信息
   - 输出：结构化分析 JSON

2. `script_generation_agent`
   - 输入：分析 JSON + 商品上下文 + 选定营销框架
   - 输出：结构化脚本

3. `self_evaluation_agent`
   - 输入：脚本 + 商品事实 + 平台约束
   - 输出：评分、问题清单、改写建议

### 统一的设计原则

- 所有 Agent 都不要直接输出大段自由文本作为系统接口。
- 所有 Agent 都应有明确角色、明确输入字段、明确输出 schema。
- 所有 Agent 都应支持 few-shot 示例注入。
- 所有 Agent 都应接入商品知识和平台规则。

### 最终判断

`awesome-chatgpt-prompts` 对我们最有价值的，不是某条“神 prompt”，而是它提供的这套可工程化方法：

- `Role`
- `Context`
- `Structure`
- `Chain`
- `Evaluation`
- `Iteration`

这 6 层应该成为 TikTok Shop 车载清洁 AI 导演 Skill 系统的基础设计。
