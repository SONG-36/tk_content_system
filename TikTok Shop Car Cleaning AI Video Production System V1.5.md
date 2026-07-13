# TikTok Shop Car Cleaning AI Video Production System V1.5

## AI车载清洁短视频生产系统调整方案

Version:

V1.5


Status:

Production Workflow Design



---

# 1. 系统定位调整


## 原始目标

之前系统目标：

建立：

TikTok Shop Car Cleaning AI Director System


核心：

分析爆款视频

↓

生成视频脚本


---

## 新阶段目标


升级为：

TikTok Shop Car Cleaning AI Video Production System


核心目标：

将：

爆款机制

↓

视频脚本

↓

拍摄方案

↓

素材需求

↓

视频成片


形成完整生产流程。


---

# 2. 当前阶段核心问题


目前已经完成：

✅ 爆款分析

✅ 用户心理分析

✅ Hook设计

✅ 视觉机制分析

✅ 三套视频脚本生成

✅ 拍摄执行规范


但是缺少：

## Production Layer


即：

从脚本到视频之间的生产系统。



---

# 3. 新系统核心流程


调整后：

爆款视频

↓

AI分析

↓

脚本生成

↓

镜头拆解

↓

Production Planner Agent

↓

判断生产方式

↓

素材需求清单

↓

素材获取

↓

AI生成/实拍/剪辑

↓

成片

↓

发布测试

↓

数据反馈

---

# 4. 新增核心模块

## Production Planner Agent


这是下一阶段最重要Agent。


职责：

把视频脚本转换为：

可执行生产计划。


---

## 输入


来自：

Script Generation Agent


例如：

Shot 01

红色跑车覆盖厚泡沫

展示视觉冲击
---

## 输出


生成：
Shot 01

Production Mode:

AI Generate

Reason:

需要豪车、高质感环境，
实拍成本过高。

Required Assets:

Reference Image:

红色跑车45度照片

Reference Video:

泡沫喷射慢动作

Background:

专业洗车店

Sound:

泡沫喷射ASMR

AI Prompt:

cinematic car detailing,
red sports car,
foam coverage,
macro shot

---

# 5. 视频生产模式判断


每个镜头必须判断：


## Mode A

# Real Shooting


适合：

产品真实性展示。


例如：

- 产品使用
- 功能证明
- 安装过程
- 效果验证


优势：

信任高。


缺点：

成本高。


---

## Mode B

# AI Generation


适合：

高成本视觉。


例如：

- 豪车
- 专业场景
- 极端视觉
- 梦幻环境


优势：

低成本。


缺点：

真实性不足。


---

## Mode C

# Stock / Reference Assets


适合：

辅助素材。


例如：

- 环境
- B-roll
- 动作参考
- 运镜参考


---

# 6. 推荐生产比例


当前养号阶段：

AI生成视觉:

60%

真实产品拍摄:

30%

素材引用:

10%
原因：

需要快速测试大量内容。


---

# 7. Asset Intelligence Layer


当前系统新增核心：

素材智能层。



目标：

管理：

AI生成需要什么素材。

视频制作需要什么素材。



---

# 8. 素材资产库设计


目录：
Car_Content_Assets/

01_Vehicles/

sports_car/

suv/

sedan/
02_Cleaning_Actions/
spraying/

vacuuming/

brushing/

wiping/
03_Visual_Hooks/
foam/

dirt_reveal/

before_after/

transformation/
04_Backgrounds/
garage/

driveway/

detailing_shop/
05_Camera_Movement/
macro/

close_up/

slow_motion/

tracking/
06_Audio/
spray_sound/

vacuum_sound/

cleaning_asmr/
07_Reference_Videos/
---

# 9. 素材数据库字段


每个素材必须记录：
asset_id

type:

image/video/audio

category:

vehicle

action

background

camera

source:

AI generated

real shooting

stock

usage:

hook

transition

proof

tags:

foam

luxury

cleaning

macro
---

# 10. 当前阶段不优先建设的系统


## 暂缓：

完整RAG系统。


原因：

当前瓶颈不是：

“找不到知识”。

而是：

“生产素材困难”。


---

## 暂缓：

复杂数据库。


包括：

- PostgreSQL
- Vector Database
- S3


原因：

当前素材量还不足。


---

# 11. 当前Mac mini服务器定位


当前：

不是AI数据库服务器。


而是：

内容生产服务器。


用途：


## 1.

素材存储


## 2.

AI生成任务管理


## 3.

视频处理


## 4.

自动化任务


---

# 12. 当前推荐架构
             Custom GPT


                 |


                 |


          Script Generator


                 |


                 |


      Production Planner Agent


                 |


      ----------------------


      |          |          |


   Real      AI Gen     Assets

   Shoot     Video      Library


      |          |          |


      ----------------------


                 |


          Video Editing


                 |


            Final Video


                 |


          TikTok Testing

---

# 13. 后续数据库路线


## Phase 1

当前阶段


目标：

快速生产。


建设：

- Asset Library
- Production Planner


---

## Phase 2


素材规模增加后：


加入：

PostgreSQL


管理：

素材信息。


---

## Phase 3


案例规模达到：

1000+

加入：

Vector Database


实现：

RAG检索。


---

# 14. 与原Knowledge系统关系


Knowledge 01-07：

负责：

内容决策。


新增Production Layer：

负责：

生产执行。


关系：

Knowledge

(知道拍什么)

    ↓

Production Planner

(知道怎么拍)

    ↓

Video Production

(生成视频)

---

# 15. 最终系统演进路线


## V1

AI内容导演


完成：

Knowledge 01-07

Custom GPT


---

## V1.5

AI视频生产系统


新增：

Production Planner

Asset Library


当前阶段。


---

## V2

内容智能数据库


新增：

- Scraping
- Database
- RAG


---

## V3

商业化平台


新增：

- Web Frontend
- User System
- SaaS


---

# 16. 核心判断


当前最大价值不是：

拥有最多视频。


而是：

建立：

爆款机制

生产方法

素材资产

形成：

车载清洁短视频生产能力。


---

# Conclusion


当前阶段正确路线：

不是马上建设复杂RAG系统。


而是：

先解决：

Script

↓

Production Plan

↓

Asset Requirement

↓

Asset Library

↓

Video

让AI导演真正具备：

从创意到成片的生产能力。