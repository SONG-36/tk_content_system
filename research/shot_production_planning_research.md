# Shot Production Planning Research

## Purpose

本研究文件用于为 `Shot Production Planner` 建立逐镜头生产决策模型。

研究目标不是讨论泛泛的视频制作理论，而是回答一条脚本镜头在进入生产阶段时，应该如何完成以下链路：

`脚本镜头 -> 生产方式判断 -> 素材需求 -> Seedance 或实拍执行`

---

## Research Basis

本研究基于项目内现有内容整理：

- `knowledge/05_TikTok_Shop_Script_Writing_Rules.md`
- `knowledge/07_Professional_Shooting_Standard.md`
- `knowledge/04_Satisfying_Cleaning_Visual_Library.md`
- `research/cleaning_visual_research.md`
- `TikTok Shop Car Cleaning AI Video Production System V1.5.md`
- `seedance_skills/reference-workflow.md`
- `seedance_skills/seedance-prompt/SKILL.md`
- `seedance_skills/seedance-motion/SKILL.md`
- `seedance_skills/seedance-camera/SKILL.md`

现阶段仓库中没有独立落盘的 Snow Foam 三份脚本案例文件，但已有两类可直接使用的现有样本：

- Snow Foam 代表性样本：`红色跑车覆盖厚泡沫 -> AI Generate` 的 V1.5 示例
- 三版脚本结构样本：`爆款复刻版 / 低成本实拍版 / 商品转化优化版` 的现有脚本 schema

因此，本研究会把 Snow Foam 作为代表性镜头类型，把三版脚本理解为三种不同的生产偏好。

---

## 1. Core Finding

逐镜头生产判断，本质上是四个维度的平衡：

1. 这条镜头是否承担真实性证明
2. 这条镜头是否必须展示真实商品与真实结果
3. 这条镜头的场景和调度成本是否过高
4. 这条镜头是否可以被外部素材安全替代

对 TikTok Shop 车载清洁视频来说，最高优先级始终不是视觉炫技，而是：

- 证明问题真实存在
- 证明产品真实接触问题
- 证明结果真实发生
- 证明用户可以复制

这意味着：

- 证明型镜头优先真实拍摄
- 氛围型镜头优先低成本生产
- 高成本视觉型镜头优先 AI
- 通用补充型镜头优先 Stock
- 既要真实又要高规格的镜头优先 Hybrid

---

## 2. Shot-Level Decision Axes

Production Planner 不应只做主观判断，而应先给每条镜头打五个决策标签。

| Axis | Meaning | High Value Means |
|---|---|---|
| `proof_criticality` | 这条镜头对成交证明有多关键 | 必须真实可信 |
| `product_identity_criticality` | 是否必须看清真实商品、结构、品牌 | 必须使用真实商品 |
| `result_verifiability` | 是否需要让用户验证前后变化与真实效果 | 必须保留真实过程 |
| `environment_cost` | 是否依赖豪车、豪华场景、专业空间、危险机位 | 更适合 AI 或 Stock |
| `motion_complexity` | 是否依赖复杂运镜、慢动作、大幅移动、极难实拍调度 | 更适合 AI 或 Hybrid |

建议按以下标准理解：

- `proof_criticality = high`
  这条镜头直接决定用户信不信产品
- `product_identity_criticality = high`
  这条镜头必须看到真实包装、结构、安装接口、品牌信息
- `result_verifiability = high`
  这条镜头必须看到 before/after、同机位变化、真实残留物变化
- `environment_cost = high`
  这条镜头如果实拍，需要豪车、棚、特殊地点、额外许可或高制作成本
- `motion_complexity = high`
  这条镜头如果实拍，稳定执行难度明显偏高

---

## 3. Production Mode Classification

固定分类如下。

### 3.1 `REAL_SHOOT`

定义：

使用真实商品、真实车辆、真实污渍、真实动作进行拍摄，后期只做常规剪辑与色彩整理。

核心价值：

- 建立最高信任
- 完成功能证明
- 满足 TikTok Shop 商品真实性要求

适合承担：

- Product Proof
- Before/After
- 商品结构展示
- 商品安装与使用
- 品牌与包装确认
- 真实功能验证

### 3.2 `AI_GENERATION`

定义：

用 Seedance 或其他 AI 视频生成方式直接完成镜头主体。

核心价值：

- 低成本获得高规格视觉
- 快速测试高吸引力 Hook
- 解决豪车、豪华场景、复杂运镜问题

适合承担：

- 高成本车辆镜头
- 高成本环境镜头
- 氛围镜头
- 非证明型 Hook
- 复杂镜头运动

### 3.3 `STOCK_ASSET`

定义：

使用可授权的现成视频、图片、声音素材作为镜头主体或补充层。

核心价值：

- 低成本补足信息密度
- 快速建立场景、情绪、转场
- 为 AI 或实拍提供动作、环境、音效参考

适合承担：

- 通用环境
- 通用驾驶与洗车氛围
- 非商品特异性的 B-roll
- 转场、背景、节奏补充
- 运镜和动作参考

### 3.4 `HYBRID`

定义：

同一镜头或同一镜头单元中，同时使用真实拍摄层与 AI/Stock 层完成最终结果。

核心价值：

- 保留商品真实性
- 获得更高视觉规格
- 降低某一单独生产方式的短板

适合承担：

- 真实商品 + AI 豪车环境
- 真实喷泡沫动作 + AI 强化氛围
- 真实 before/after + Stock 建立镜头
- 真实产品近景 + AI 复杂运动外壳

---

## 4. Applicability Conditions By Mode

### 4.1 `REAL_SHOOT` 的适用条件

当镜头满足以下任一条件时，默认优先 `REAL_SHOOT`：

- 镜头承担 Product Proof
- 镜头展示真实功能结果
- 镜头要求用户相信 before/after
- 镜头展示真实产品外观、结构、品牌
- 镜头展示安装、拆装、喷涂、擦拭、吸附等真实动作
- 镜头会被用户拿来判断“这产品是不是真的这样用”
- 镜头存在合规风险，不能让人怀疑虚假演示

### 4.2 `AI_GENERATION` 的适用条件

当镜头同时满足以下逻辑时，优先 `AI_GENERATION`：

- 镜头主要承担停留、氛围、爽感或高级感
- 镜头不承担真实商品证明
- 镜头不需要用户逐帧验证真假
- 实拍成本明显高于镜头对成交的实际价值
- 复杂运镜、空间调度或豪车场景更重要

### 4.3 `STOCK_ASSET` 的适用条件

当镜头更像“信息补充”而不是“商品证明”时，优先 `STOCK_ASSET`：

- 只是建立环境
- 只是交代气氛
- 只是补足城市、道路、洗车店、天气等背景信息
- 商品不需要清晰出镜
- 用户不会基于该镜头判断产品真实性
- 用于给 AI 提供动作参考、运镜参考、ASMR 音效

### 4.4 `HYBRID` 的适用条件

当镜头同时存在“真实性刚需”和“规格感刚需”时，优先 `HYBRID`：

- 商品必须真实，但环境可以替代
- 动作必须真实，但运镜或背景可增强
- before/after 必须真实，但开场高级视觉可虚拟
- 真正要证明的只有产品局部，其余画面层可以外包给 AI 或 Stock

---

## 5. Which Shots Must Be Real

以下镜头默认判定为必须 `REAL_SHOOT`，除非只作为极短辅助切片且不承担证明。

### 5.1 产品外观

必须实拍的原因：

- 用户会直接判断商品质感
- 包装、喷头、瓶身、颜色、标签属于真实商品识别信息
- AI 漂移会直接损伤信任

典型镜头：

- 产品瓶身 close-up
- 包装拆封
- 手持产品展示
- 品牌 logo、标签、结构件特写

### 5.2 产品安装

必须实拍的原因：

- 安装步骤是可复制性的证明
- 接口、卡扣、喷头切换、配件连接都属于真实操作
- 用户会判断自己是否能上手

典型镜头：

- 泡沫喷壶接入喷枪
- 刷头安装
- 吸头替换
- 喷嘴模式切换

### 5.3 产品真实功能

必须实拍的原因：

- 清洁产品的价值来自动作结果，而不是设定结果
- 过程比口播更有说服力

典型镜头：

- 喷出泡沫并覆盖脏污
- 刷毛进入缝隙带出灰尘
- 灰尘吸入透明尘盒
- 擦拭后表面恢复

### 5.4 `Product Proof`

必须实拍的原因：

- `knowledge/05` 与 `knowledge/07` 已明确把 Proof 作为成交核心
- 任何 proof 镜头一旦被怀疑造假，整条视频信任会崩

典型镜头：

- Usage Proof
- Result Proof
- Comparison Proof

### 5.5 `Before/After`

必须实拍的原因：

- 这是最强信任镜头
- 用户会默认拿这个镜头判断真假
- 最优形式是同机位、同光线、同区域

典型镜头：

- 一半脏一半净
- 擦拭前后对比
- 同机位泡沫覆盖后擦净

### 5.6 商品结构和品牌

必须实拍的原因：

- 品牌和结构是 TikTok Shop 购买决策的重要确认点
- AI 最容易在这些细节上出现错字、错形、错配件

典型镜头：

- 品牌名 close-up
- 结构亮点特写
- 喷头、刷毛、接头、透明仓等结构展示

---

## 6. Which Shots Fit `AI_GENERATION`

以下镜头优先适合 `AI_GENERATION`。

### 6.1 高成本车辆

适合 AI 的原因：

- 豪车不是产品真实性本体
- 豪车主要承担高级感和停留
- 实拍豪车成本高，复用价值低

典型镜头：

- 红色跑车被厚泡沫覆盖
- 高级 SUV 在专业 detailing 店被打光
- 低角度 hero shot 展现“专业洗护感”

### 6.2 高成本环境

适合 AI 的原因：

- 高端车库、专业 detailing bay、光影复杂空间主要服务视觉规格
- 对成交是加分项，不是信任底座

典型镜头：

- 棚拍级洗车店氛围
- 商业级灯光映射在车漆上的场景
- 清晨或夜间 cinematic 车库环境

### 6.3 氛围镜头

适合 AI 的原因：

- 这类镜头不要求逐帧验证真实性
- 重点是 mood、节奏和开场吸引力

典型镜头：

- 泡沫慢慢滑落的解压镜头
- 水珠与高光的过渡镜头
- 车身细节与灯光扫过镜头

### 6.4 非真实性证明型 Hook

适合 AI 的原因：

- Hook 的任务是停留，不一定是成交证明
- 只要不冒充真实效果演示，就可以承担更夸张的画面职责

典型镜头：

- “看起来像新买的一辆车” 的开场气氛镜头
- 豪车厚泡沫覆盖的冲击镜头
- 夸张但不宣称真实产品结果的清洁仪式感镜头

### 6.5 复杂镜头运动

适合 AI 的原因：

- 复杂滑轨、跟拍、俯冲、超近距移动实拍成本高
- 这类镜头常常是表现层，不是证明层

典型镜头：

- 从轮毂快速推至泡沫表面的微距运动
- 沿车身连续 tracking
- 模拟机械臂式的丝滑过渡镜头

### 6.6 Snow Foam 代表性判断

对于类似 `红色跑车覆盖厚泡沫` 这类镜头，应先问：

- 它是在证明“我们的产品真实能喷出这个泡沫”吗
- 还是在制造“专业、高级、过瘾”的开场冲击

如果答案是前者，改为 `REAL_SHOOT` 或 `HYBRID`。

如果答案是后者，优先 `AI_GENERATION`。

---

## 7. Which Shots Fit `STOCK_ASSET`

以下镜头更适合优先寻找 Stock。

### 7.1 通用环境建立镜头

例如：

- 洗车店外景
- 车库环境
- 驾车进入 driveway
- 天气、路面、水滴环境

### 7.2 通用生活方式补充镜头

例如：

- 用户开门上车
- 手拿毛巾准备清洁
- 车内杂物一闪而过

前提：

- 不特写商品
- 不承担 proof

### 7.3 非商品特异性 B-roll

例如：

- 水流、泡沫、擦布、喷雾的抽象近景
- 环境反光与材料表面过渡
- 洗车工具摆放场景

### 7.4 音频与动作参考素材

例如：

- 泡沫喷射音
- 擦拭 ASMR
- 吸尘器工作音
- 复杂运镜参考视频

### 7.5 转场和节奏层

例如：

- 开头 0.5 秒环境强调
- 章节切换
- 节奏补强

`STOCK_ASSET` 最适合承担“让视频更完整”，不适合承担“让用户更相信产品”。

---

## 8. Which Shots Need `HYBRID`

以下类型建议优先采用 `HYBRID`。

### 8.1 真实商品 + AI 豪车环境

适合场景：

- 必须看到真实产品
- 但不值得真实租豪车和棚

执行方式：

- 实拍产品手部、喷头、出泡局部
- AI 生成豪车或 detailing bay 外层环境

### 8.2 真实功能 + AI 运镜增强

适合场景：

- 功能必须真实
- 但镜头运动要求过高

执行方式：

- 先实拍核心 proof
- 再用 AI 完成连接段、过渡段、运动壳层

### 8.3 真实 before/after + Stock 建立镜头

适合场景：

- 结果镜头必须真实
- 但前后环境不需要全都自己拍

执行方式：

- Stock 承担环境建立
- 实拍承担前后对比和功能段

### 8.4 真实产品近景 + AI Hook 外壳

适合场景：

- 爆款复刻版需要强停留
- 商品转化优化版又必须补强真实展示

执行方式：

- 开头 AI 做冲击
- 中段和结尾实拍 proof

### 8.5 真实操作 + AI 视觉强化

适合场景：

- 核心动作真实完成
- 后期只增强光感、背景、节奏

注意：

- 不得把真实效果增强到超出商品真实边界

---

## 9. Script-Version Bias

现有三版脚本结构，不只是文案差异，也会天然影响镜头生产偏好。

| Script Version | Production Bias | Planner Implication |
|---|---|---|
| `爆款复刻版` | 更接受 AI Hook、复杂视觉、强节奏 | 可提高 `AI_GENERATION` 与 `HYBRID` 比例 |
| `低成本实拍版` | 更强调可执行、普通车辆、手机拍摄 | 优先 `REAL_SHOOT + STOCK_ASSET` |
| `商品转化优化版` | 更强调商品露出、功能证明、购买理由 | 优先 `REAL_SHOOT`，必要时 `HYBRID` |

因此同一条镜头目的，在不同脚本版本下可能有不同的最佳生产方式。

例如 Snow Foam Hook：

- 爆款复刻版：可用 `AI_GENERATION`
- 低成本实拍版：更可能改写为普通车辆实拍泡沫覆盖
- 商品转化优化版：更应把重点放在真实喷泡、真实擦净、真实产品近景

---

## 10. Production Decision Tree

建议 Planner 按以下顺序判断。

### Step 1: 这条镜头是否承担真实性证明

如果是以下任意一种，直接进入真实优先路径：

- Product Proof
- Before/After
- Usage Proof
- 结构展示
- 品牌确认
- 安装演示

输出：

- 默认 `REAL_SHOOT`
- 若环境或运镜成本过高，则 `HYBRID`

### Step 2: 用户是否需要看清真实商品本体

若需要清楚看到以下信息：

- 包装
- logo
- 标签
- 喷头
- 刷毛
- 接口
- 透明仓

输出：

- `REAL_SHOOT`
- 除非只是插入极短辅助画面，否则不建议纯 AI

### Step 3: 结果是否需要可验证

若需要：

- 同机位对比
- 一半脏一半净
- 脏污被带出
- 泡沫覆盖后真实擦净

输出：

- `REAL_SHOOT`
- 或 `HYBRID`，但 proof 层必须真实

### Step 4: 镜头是否主要承担氛围、停留、高级感

若是：

- Hook
- 氛围
- 豪车感
- 高级 detailing 感
- 解压运动感

继续判断成本。

### Step 5: 环境成本和运镜复杂度是否过高

若过高：

- 豪车
- 高端 detailing 店
- 复杂滑轨或机械臂感
- 不易重复的慢动作环境

输出：

- `AI_GENERATION`
- 或 `HYBRID`

### Step 6: 这条镜头能否被授权的通用素材替代

若镜头只是：

- 环境
- 节奏层
- B-roll
- 音效
- 运镜参考

输出：

- `STOCK_ASSET`

### Step 7: 是否同时存在真实性刚需和规格感刚需

若同时存在：

- 商品必须真实
- 但车、环境、光效、运镜不必全实拍

输出：

- `HYBRID`

### 简化决策规则

可以压缩成一句话：

`凡是用户会据此判断商品真假和效果真假，优先 REAL_SHOOT；凡是用户只会据此判断视频够不够抓人，优先 AI_GENERATION 或 STOCK_ASSET；两者同时存在时，用 HYBRID。`

---

## 11. Asset Checklist By Production Mode

### 11.1 `REAL_SHOOT` 素材清单

必须准备：

- 真实商品
- 真实车辆或真实清洁部位
- 真实污渍或可控脏污
- 拍摄脚本中的 shot purpose
- 机位方案
- 光线方案
- 现场音或拟音方案

建议补充：

- 同机位 before 素材
- 同机位 after 素材
- 半边对比 masking 方案
- 微距细节机位

输出给执行层的字段应包括：

- 产品准备清单
- 场景准备清单
- 污渍准备方式
- 机位与景别
- 动作顺序
- 结果定格要求

### 11.2 `AI_GENERATION` 素材清单

必须准备：

- `subject_reference`
- `environment_reference`
- `camera_reference`
- `motion_reference`
- `audio_reference`
- `do_not_transfer_constraints`

结合现有 `seedance_skills`，建议显式区分：

- `@Image`: 控制产品、车辆、环境身份
- `@Video`: 控制动作、运镜、节奏
- `@Audio`: 控制 tempo、ASMR、能量感

额外要求：

- 明确哪些内容允许转移
- 明确哪些内容不允许转移
- 不能让参考素材同时控制身份、动作、环境、品牌四个角色

### 11.3 `STOCK_ASSET` 素材清单

必须准备：

- 可授权来源
- 搜索关键词
- 使用目的
- 预计时长
- 是否允许二次剪辑
- 是否可商用

建议字段：

- `stock_query`
- `usage_context`
- `license_status`
- `model_release_status`
- `brand_risk`

### 11.4 `HYBRID` 素材清单

必须拆成两层：

- `real_layer`
- `synthetic_layer`

`real_layer` 需要：

- 真实商品
- 真实 proof 动作
- 真实 before/after
- 真实结构细节

`synthetic_layer` 需要：

- AI 环境参考
- Stock 补充镜头
- AI 运镜或节奏参考
- 音效与气氛层

还必须定义：

- 哪一层承担 proof
- 哪一层只能承担 atmosphere
- 哪些细节不能被 AI 改写

---

## 12. Risk Judgment

### 12.1 商品真实性风险

最高风险场景：

- 用 AI 直接生成产品外观与功能证明
- 用 AI 伪造 before/after
- 用 AI 生成品牌结构细节

控制原则：

- 商品本体、结构、功能结果优先真实拍摄
- Hybrid 中明确 proof 层只能来自实拍

### 12.2 AI 一致性风险

常见问题：

- 产品外形漂移
- logo 漂移
- 泡沫质感前后不一致
- 车辆颜色或线条变化
- 手部与喷头接触不稳定

控制原则：

- 把 AI 用于氛围，不用于关键商品识别
- 使用明确的 identity anchor
- 限制单镜头动作复杂度

### 12.3 版权风险

常见问题：

- 无授权 Stock
- 未授权 reference video
- 借用他人豪车、logo、空间、音乐风格

控制原则：

- 只用可商用、可授权素材
- 在 Seedance 参考工作流中明确“可转移”和“不可转移”
- 音乐、人物、logo 不默认视为可授权

### 12.4 合规风险

常见问题：

- 夸大真实效果
- AI 镜头被误解为真实产品演示
- before/after 不真实
- 暗示所有用户都能达到同样结果却没有真实依据

控制原则：

- 证明型镜头必须真实
- 氛围型 AI 镜头不能放在关键 proof 位
- 不能让高级感镜头替代真实演示

### 12.5 视觉可信度风险

常见问题：

- Hook 很强，但中段证据断裂
- 豪车氛围与普通商品实拍之间风格断层
- Stock 与实拍之间光色不统一

控制原则：

- 把强视觉放在 Hook
- 把强证明放在中后段
- Hybrid 需要统一色彩、镜头语言和节奏

---

## 13. Unified Schema Recommendation

Production Planner 的输出 schema 应直接服务于后续执行，而不是只输出一句主观判断。

建议结构如下：

```yaml
shot_id: ""
script_version: "" # viral_remake | low_cost_live_action | conversion_optimized
shot_purpose: "" # Hook | Problem Reveal | Product Introduction | Product Proof | Transformation | Satisfaction Moment | CTA
duration: ""
visual_description: ""
action_description: ""

decision_axes:
  proof_criticality: "" # high | medium | low
  product_identity_criticality: "" # high | medium | low
  result_verifiability: "" # high | medium | low
  environment_cost: "" # high | medium | low
  motion_complexity: "" # high | medium | low

production_decision:
  primary_mode: "" # REAL_SHOOT | AI_GENERATION | STOCK_ASSET | HYBRID
  secondary_mode: "" # optional fallback
  decision_reason: []
  proof_layer_owner: "" # real_shoot | ai_generation | stock_asset | n/a
  authenticity_requirement: "" # must_be_real | can_be_synthetic | mixed

must_be_real_elements:
  - ""

can_be_synthetic_elements:
  - ""

required_assets:
  real_shoot:
    product: []
    vehicle_or_surface: []
    dirt_or_stain_setup: []
    props: []
    camera_setup: []
    lighting_setup: []
    sound_setup: []
  ai_generation:
    subject_references: []
    environment_references: []
    motion_references: []
    camera_references: []
    audio_references: []
    transfer_constraints: []
  stock_asset:
    stock_queries: []
    license_requirements: []
    intended_usage: []
  hybrid:
    real_layer_requirements: []
    synthetic_layer_requirements: []
    compositing_notes: []

execution_output:
  live_action_brief: ""
  seedance_mode: "" # T2V | I2V | V2V | R2V | FLF2V | edit | extend
  seedance_reference_role_map: []
  seedance_prompt_brief: ""
  stock_search_brief: []

risk_flags:
  authenticity_risk: "" # high | medium | low
  ai_consistency_risk: "" # high | medium | low
  copyright_risk: "" # high | medium | low
  compliance_risk: "" # high | medium | low
  credibility_risk: "" # high | medium | low
  mitigation_actions: []
```

---

## 14. Planner Output Rules

为了让这个研究能直接落到 `Shot Production Planner`，建议增加以下硬规则。

### Rule 1

任何 `Product Proof` 镜头都必须输出：

- 为什么必须真实
- 哪些元素必须真实
- 如何拍到可验证结果

### Rule 2

任何 `AI_GENERATION` 镜头都必须输出：

- 为什么它不承担真实性证明
- 参考素材角色分配
- 禁止转移项

### Rule 3

任何 `STOCK_ASSET` 镜头都必须输出：

- 素材用途
- 商用授权要求
- 是否只是辅助层

### Rule 4

任何 `HYBRID` 镜头都必须输出：

- 哪部分实拍
- 哪部分 AI 或 Stock
- 哪一层承担 proof

### Rule 5

任何镜头如果存在 `before/after`、`brand`、`installation`、`real function` 任一标签，都不允许默认纯 AI。

---

## 15. Final Conclusion

`Shot Production Planner` 的核心不是给每条镜头贴一个“拍法标签”，而是判断这条镜头究竟在完成哪一种商业任务：

- 停留
- 证明
- 转化
- 补充

对应的最稳判断原则是：

- `证明 = REAL_SHOOT`
- `高成本吸引力 = AI_GENERATION`
- `通用补充 = STOCK_ASSET`
- `既要真实又要高级 = HYBRID`

对于 Snow Foam 这类内容，最关键的不是“泡沫画面应该用什么技术做”，而是先分清：

- 这是在卖视觉冲击
- 还是在卖真实清洁能力

一旦这个问题判断错了，后面的素材准备、Seedance 生成和实拍执行都会偏离目标。
