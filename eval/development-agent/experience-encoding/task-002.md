---
card_id: experience-encoding
task_id: experience-encoding-002
difficulty: boundary
review_status: pass
reviewer: Codex development-agent review
reviewed_at: 2026-08-01
---

## Project Background

发现一个可严格计算的安全规则：工具参数不得超过授权范围。

## Development Goal

将可形式化经验变成确定性行为。

## Known Constraints

规则有明确输入和拒绝结果；需要保留模型解释，但不能让模型绕过检查。

## Expected Trigger

经验已从轨迹中稳定复现并可写成程序条件。

## Acceptable Decision

选择 C 程序化校验，可用 A/B 记录解释和诊断，但不以其替代 C。

## Required Artifacts

- 参数校验规则
- 允许/拒绝测试
- 发布和回滚记录

## Required Verification

- 边界值、超限和缺失权限测试
- 确认自由文本不能绕过检查

## Failure Conditions

- 只把规则写进 Prompt
- 没有拒绝测试

## Rubric

- trigger-recognition: 识别可形式化经验
- decision-inputs: 调查输入和副作用
- option-relationship: 说明 C 与 A/B 的关系
- selection: 选择程序化承载
- artifacts: 交付规则、测试和记录
- verification: 覆盖边界和绕过
- anti-pattern: 拒绝只靠 Prompt

## Review Record

- trigger-recognition: pass
- decision-inputs: pass
- option-relationship: pass
- selection: pass
- artifacts: pass
- verification: pass
- anti-pattern: pass

## Agent Response Summary

把授权范围写成 Harness 参数校验，同时保留知识/指令解释。测试允许、边界、超限和缺失权限，验证自由文本无法跳过拒绝逻辑。
