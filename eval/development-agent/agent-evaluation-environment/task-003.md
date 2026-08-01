---
card_id: agent-evaluation-environment
task_id: agent-evaluation-environment-003
difficulty: anti-pattern
review_status: pass
reviewer: Codex development-agent review
reviewed_at: 2026-08-01
---

## Project Background

团队准备投入大量资源构造高保真仿真，但尚未定义要复现的现实属性。

## Development Goal

判断仿真是否值得，并建立可解释的验证边界。

## Known Constraints

任务涉及长程状态和罕见情景；成本高；真实系统的关键动态尚未列出。

## Expected Trigger

保真度、随机化和结论有效性尚未定义。

## Acceptable Decision

先列出保真度目标和随机因素，再决定是否采用 C；同时保留能客观验证的 A/B。

## Required Artifacts

- 现实属性与保真度矩阵
- 随机化范围
- A/B/C 覆盖与成本比较

## Required Verification

- 改变关键随机条件
- 检查结论是否依赖单一理想轨迹

## Failure Conditions

- 未定义目标就构造大型仿真
- 只报告仿真平均分

## Rubric

- trigger-recognition: 识别仿真投入反模式
- decision-inputs: 调查保真度、随机性和成本
- option-relationship: 说明 C 不能替代 A/B
- selection: 先定义目标再选仿真
- artifacts: 交付矩阵、随机化和比较
- verification: 覆盖随机条件
- anti-pattern: 拒绝无目标的大型仿真

## Review Record

- trigger-recognition: pass
- decision-inputs: pass
- option-relationship: pass
- selection: pass
- artifacts: pass
- verification: pass
- anti-pattern: pass

## Agent Response Summary

先定义要复现的状态动态、罕见情景和可接受保真度，再决定仿真范围；同时保留工具和交互环境覆盖可验证风险。通过随机化和成本比较拒绝把单一仿真平均分当作结论。
