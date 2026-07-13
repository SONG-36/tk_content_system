# TikTok Shop Car Cleaning AI Director System V2

## System Design Document

Version: V2.0

Status: Architecture Design


---

# 1. 系统定位

## 1.1 产品名称

TikTok Shop Car Cleaning AI Director System


中文：

车载清洁爆款内容智能导演系统


---

## 1.2 系统定位


TikTok Shop Car Cleaning AI Director System 是一个面向车载清洁类目的 AI 内容智能系统。


系统目标：

通过采集全球社交媒体爆款视频，

利用 AI 视频理解、营销分析、用户心理分析、内容检索和自动生成能力，

建立一个持续学习的车载清洁内容生产系统。


系统不是：

- 普通视频脚本生成工具
- 视频总结工具
- AI文案工具


系统是：

一个模拟专业 TikTok Shop Creative Director 的 AI 内容生产平台。


---

## 1.3 核心能力


系统具备：

### 爆款发现能力

自动发现：

- 高播放视频
- 高互动视频
- 高转化内容模式


### 爆款分析能力

理解：

- 为什么爆
- 为什么停留
- 为什么购买


### 内容迁移能力

将：

爆款机制

转换为：

自己的商品视频方案。


### 视频生产能力

生成：

- 视频脚本
- 镜头设计
- 拍摄方案
- 广告素材方向


### 数据学习能力

根据：

- 播放
- 点击
- 转化
- GMV

持续优化内容策略。


---

# 2. 总体架构


系统整体架构：

                社交媒体内容源

   TikTok / Instagram / YouTube / Ads Library

                     |

                     ↓

            数据采集层

      Scrape Creators / API / Upload

                     |

                     ↓

            原始素材数据库

    Video / Metadata / Comments / Metrics

                     |

                     ↓

            AI内容分析层

   Vision Agent / Psychology Agent / Script Agent

                     |

                     ↓

            Knowledge系统

             01-07 Framework

                     |

                     ↓

            内容案例数据库

              Examples Library

                     |

                     ↓

            RAG检索系统

                     |

                     ↓

            GPT Director Agent

                     |

                     ↓

         视频方案 / 拍摄脚本 / 优化建议

                     |

                     ↓

            投放数据反馈

                     |

                     ↓

            系统持续优化

---

# 3. 数据采集层


## 3.1 目标


持续获取全球车载清洁相关内容资产。


数据来源包括：


## TikTok

采集：

- Viral Videos
- Product Videos
- UGC Videos
- Ads Creative


关键词：

car cleaning

car detailing

foam cannon

car vacuum

cleaning hacks

auto detailing

---

## Instagram Reels


采集：

- 达人内容
- 品牌内容
- 爆款短视频


---

## YouTube Shorts


采集：

- 教程内容
- 长生命周期内容


---

## Facebook Ads Library


采集：

- 广告素材
- 转化型视频


---

## 数据采集工具


主要：

- Scrape Creators
- Apify
- API接口
- 手动上传


---

# 4. 原始素材数据库


## 4.1 数据库目标


保存所有原始内容资产。


包括：

视频文件

图片

字幕

评论

互动数据

商品信息


---

## 4.2 数据结构

dataset/

raw/

videos/

images/

metadata/

comments/

metrics/

---

## 4.3 Video数据字段


示例：

```json
{
"id":"",
"platform":"TikTok",
"url":"",
"title":"",
"duration":"",
"views":"",
"likes":"",
"comments":"",
"share":"",
"category":"car cleaning",
"product":"foam cannon"
}

4.4 Metadata

包含：

* 发布时间
* 作者
* 标签
* 音乐
* 字幕
* 商品链接

⸻

4.5 Metrics

包含：

* Views
* Engagement Rate
* Completion Rate
* CTR
* CVR
* GMV

⸻

5. AI分析 Agent体系

系统采用多Agent架构。

⸻

5.1 Video Understanding Agent

职责：

理解视频内容。

分析：

* 场景
* 产品
* 人物
* 动作
* 镜头
* 变化

输入：

视频

输出：

结构化视频理解结果。

⸻

5.2 Viral Analysis Agent

对应：

Knowledge 01

职责：

分析爆款机制。

输出：

* Hook
* Retention
* Viral Pattern
* Transfer Logic

回答：

为什么爆？

⸻

5.3 Psychology Agent

对应：

Knowledge 02

职责：

分析用户购买心理。

输出：

* 用户画像
* JTBD
* Purchase Motivation

回答：

为什么买？

⸻

5.4 Hook Agent

对应：

Knowledge 03

职责：

分析前三秒。

输出：

* Hook类型
* 第一视觉刺激
* 停留原因

⸻

5.5 Visual Mechanism Agent

对应：

Knowledge 04

职责：

分析视觉爽点。

输出：

* Transformation
* Before/After
* Product Proof

⸻

5.6 Script Generation Agent

对应：

Knowledge 05

职责：

生成：

* 爆款复刻版
* 低成本版本
* 转化优化版

⸻

5.7 Shooting Agent

对应：

Knowledge 07

职责：

转换：

创意

↓

拍摄执行方案

输出：

* 镜头
* 机位
* 动作
* 声音
* 字幕

⸻

5.8 Evaluation Agent

对应：

Knowledge 06

职责：

评分：

* 爆款概率
* 转化能力
* 执行质量

⸻

6. Knowledge 01-07体系

Knowledge负责：

稳定方法论。

不是案例库。

⸻

01_TikTok_Viral_Analysis_Framework

作用：

爆款分析框架。

分析：

* Hook
* Retention
* Visual Mechanism
* Marketing Logic

⸻

02_Car_Cleaning_Content_Psychology

作用：

用户心理。

包含：

* JTBD
* 用户画像
* 购买动机

⸻

03_Cleaning_Video_Hook_Database

作用：

Hook数据库。

包含：

* Hidden Dirt Reveal
* Before After
* Product Test
* Challenge

⸻

04_Satisfying_Cleaning_Visual_Library

作用：

视觉机制库。

包含：

* 泡沫覆盖
* 黑水流出
* 污垢出现
* 前后变化

⸻

05_TikTok_Shop_Script_Writing_Rules

作用：

脚本生成规则。

生成：

三个视频方向。

⸻

06_Video_Script_Scoring_System

作用：

脚本评分。

评分：

* Hook
* Visual
* Product Proof
* Conversion

⸻

07_Professional_Shooting_Standard

作用：

拍摄执行标准。

要求：

每个镜头包含：

* 时间
* 景别
* 机位
* 动作
* 声音
* 视觉变化

⸻

7. Examples案例库

7.1 作用

Examples用于：

告诉AI：

优秀结果是什么样。

区别：

Knowledge = 方法

Examples = 样本

⸻

7.2 案例结构

examples/


viral_cases/


snowfoam_case_001.md

vacuum_case_001.md

brush_case_001.md


winning_scripts/


failed_scripts/

7.3 单案例内容

包含：

Video Information

Performance Data

Hook Analysis

Visual Mechanism

Psychology

Script

Score

Optimization

Final Version

8. RAG检索架构

目标

让GPT生成内容时调用历史爆款经验。

⸻

工作流程

用户：

“我的车载吸尘器怎么拍？”

↓

RAG查询：

搜索：

* Vacuum
* Dust Removal
* Hidden Dirt

↓

返回：

相关案例：

* Hook
* Visual
* Script Pattern

↓

GPT生成：

新的商品方案。

⸻

9. GPT Director Agent工作流

完整流程：

用户输入

↓

任务识别

↓

调用Knowledge

↓

检索Examples

↓

爆款分析

↓

用户心理分析

↓

Hook设计

↓

视觉设计

↓

脚本生成

↓

拍摄执行

↓

评分优化

↓

输出文件

10. 三类业务流程

Flow 1

爆款视频复刻

输入：

爆款视频

流程：

分析

↓

提炼机制

↓

商品迁移

↓

生成三个方案

⸻

Flow 2

新产品内容生成

输入：

产品资料

流程：

产品分析

↓

用户心理

↓

Hook匹配

↓

视觉设计

↓

脚本生成

⸻

Flow 3

数据反馈优化

输入：

投放数据

数据：

* CTR
* CVR
* GMV

输出：

优化：

* Hook
* Script
* Visual

⸻

11. 技术架构

Backend

Python

FastAPI

⸻

Database

PostgreSQL

存储：

结构化内容数据。

⸻

Vector Database

推荐：

* Qdrant
* Pinecone
* Chroma

用于：

RAG检索。

⸻

Storage

推荐：

* AWS S3
* Cloudflare R2

存储：

视频文件。

⸻

AI能力

OpenAI API

使用：

* Vision
* Embedding
* Structured Output

⸻

Automation

推荐：

* n8n
* Airflow
* Make

负责：

数据Pipeline。

⸻

12. 开发阶段规划

V1

目标：

AI内容导演。

完成：

* Knowledge 01-07
* GPT Builder
* 手动案例分析

状态：

完成。

⸻

V2

目标：

建立自动内容数据库。

新增：

* Scrape Creators
* 自动采集
* 自动分析
* 数据库
* RAG

⸻

V3

目标：

建立自学习系统。

新增：

* 投放数据连接
* 自动优化
* 内容趋势预测

⸻

13. 商业价值

当前市场问题

传统模式：

人工找素材

↓

人工分析

↓

人工写脚本

↓

人工测试

效率低。

⸻

AI Director模式

自动：

发现爆款

↓

理解机制

↓

生成方案

↓

测试优化

效率提升。

⸻

核心资产

最终资产不是视频。

而是：

经过AI结构化后的：

车载清洁内容知识库。

包括：

* 爆款规律
* 用户心理
* Hook模式
* 视觉机制
* 转化逻辑

⸻

最终愿景

建立：

全球领先的：

TikTok Shop Car Cleaning Content Intelligence Platform

服务：

* 品牌方
* 广告团队
* 达人机构
* 电商卖家

成为车载清洁类目的：

AI内容基础设施。