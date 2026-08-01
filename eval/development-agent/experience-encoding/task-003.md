---
card_id: experience-encoding
task_id: experience-encoding-003
difficulty: anti-pattern
review_status: pass
reviewer: Codex development-agent review
reviewed_at: 2026-08-01
---

## Project Background

团队想把几条成功轨迹立即写入模型参数，以减少运行时检索。

## Development Goal

阻止没有闭环证据的参数更新。

## Known Constraints

轨迹数量少；没有隔离评估、发布或回滚方案；任务分布未知。

## Expected Trigger

把单次完成误认为能力进步，且跳过验证发布。

## Acceptable Decision

暂存为 A/B/C 候选，先完成问题定位、代表性评估和回滚设计；不选择 D。

## Required Artifacts

- 经验证据登记
- 隔离评估计划
- 发布门槛与回滚方案

## Required Verification

- 比较泛化、失败副作用和回滚
- 评估未通过则保持未发布

## Failure Conditions

- 直接训练更新参数
- 只看单任务成功率

## Rubric

- trigger-recognition: 识别参数更新反模式
- decision-inputs: 调查数据、分布和回滚
- option-relationship: 说明 D 需经过前置层和门禁
- selection: 拒绝立即更新参数
- artifacts: 交付评估与回滚工件
- verification: 覆盖泛化和副作用
- anti-pattern: 拒绝单次成功即发布

## Review Record

- trigger-recognition: pass
- decision-inputs: pass
- option-relationship: pass
- selection: pass
- artifacts: pass
- verification: pass
- anti-pattern: pass

## Agent Response Summary

将轨迹保留为待验证的知识、指令或程序候选，先构造隔离评估、发布门槛和回滚方案。由于没有足够数据与分布证据，拒绝直接更新参数，也拒绝用单任务成功率宣称进步。
