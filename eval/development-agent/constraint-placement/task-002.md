---
card_id: constraint-placement
task_id: constraint-placement-002
difficulty: boundary
review_status: pass
reviewer: Codex development-agent review
reviewed_at: 2026-08-01
---

## Project Background

支持团队 Agent 必须限制退款额不超过订单金额，并对异常退款请求人工复核。

## Development Goal

区分业务解释规则与不可绕过的金额约束。

## Known Constraints

退款理由需要语言理解；金额上限可由订单数据确定；异常请求需要人工裁量。

## Expected Trigger

同一约束同时存在语言化、确定性和高风险部分。

## Acceptable Decision

理由指导用 A/B，金额上限用 C，异常退款经 D 审批。

## Required Artifacts

- 退款约束分层表
- 订单金额校验
- 异常退款预览与审批记录

## Required Verification

- 超额参数必须被 C 拒绝
- 异常退款未经审批不得执行

## Failure Conditions

- 让模型自行判断金额上限
- 因有审批就省略程序校验

## Rubric

- trigger-recognition: 识别混合约束
- decision-inputs: 调查可形式化边界和风险
- option-relationship: 说明分层而非单选
- selection: 选择 A/B+C+D 组合
- artifacts: 包含校验与审批工件
- verification: 检查超额和审批路径
- anti-pattern: 拒绝模型自由裁量金额

## Review Record

- trigger-recognition: pass
- decision-inputs: pass
- option-relationship: pass
- selection: pass
- artifacts: pass
- verification: pass
- anti-pattern: pass

## Agent Response Summary

将退款理由保留为可审查指令，使用订单金额的结构化校验拒绝超额参数，并为异常情况提供预览和人工审批。审批不能替代金额校验，验证覆盖超额、批准、拒绝和超时。
