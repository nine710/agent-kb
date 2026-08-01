---
card_id: agent-evaluation-environment
task_id: agent-evaluation-environment-001
difficulty: typical
review_status: pass
reviewer: Codex development-agent review
reviewed_at: 2026-08-01
---

## Project Background

代码 Agent 需要验证是否正确搜索、编辑和运行测试。

## Development Goal

设计第一阶段的可重复评估环境。

## Known Constraints

工具调用和最终仓库状态都可断言；不需要模拟用户或现实世界。

## Expected Trigger

主要风险是工具选择、参数和结果状态。

## Acceptable Decision

选择 A 工具调用环境，并预留后续 B/C 的能力矩阵位置。

## Required Artifacts

- 任务集和初始仓库状态
- 工具接口与期望状态断言
- 失败归因规则

## Required Verification

- 检查工具、参数、顺序和最终状态
- 按任务难度报告结果

## Failure Conditions

- 只比较最终文本答案
- 没有可验证的期望状态

## Rubric

- trigger-recognition: 识别工具结果风险
- decision-inputs: 调查可验证性和任务分布
- option-relationship: 说明 A 与其他环境的关系
- selection: 选择工具调用环境
- artifacts: 交付任务、接口、断言和归因
- verification: 覆盖调用与状态
- anti-pattern: 拒绝只看文本

## Review Record

- trigger-recognition: pass
- decision-inputs: pass
- option-relationship: pass
- selection: pass
- artifacts: pass
- verification: pass
- anti-pattern: pass

## Agent Response Summary

使用隔离仓库和可验证工具接口，断言搜索、编辑、测试命令的参数和最终状态，并按难度归因失败。没有把自然语言最终答案当作唯一指标。
