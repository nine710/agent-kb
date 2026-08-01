---
card_id: multi-agent-coordination
task_id: multi-agent-coordination-001
difficulty: typical
review_status: pass
reviewer: Codex development-agent review
reviewed_at: 2026-08-01
---

## Project Background

软件交付 Agent 需要分解需求、让执行者修改代码，并统一汇总测试与发布结论。

## Development Goal

设计有明确最终责任的协作拓扑。

## Known Constraints

存在总计划、资源约束和最终交付负责人；中间结果需要验证。

## Expected Trigger

任务需要集中分派、汇总与质量门。

## Acceptable Decision

选择 A 管理者模式，可通过文件或消息与执行者通信。

## Required Artifacts

- 拓扑图和角色矩阵
- 状态与汇总协议
- 关键中间结果验证门

## Required Verification

- 演练执行者失败与管理者纠正
- 追踪控制权和关键结果

## Failure Conditions

- 管理者只转发文本
- 没有最终汇总责任

## Rubric

- trigger-recognition: 识别集中协调需求
- decision-inputs: 调查总计划、责任和资源
- option-relationship: 说明 A 为主控制拓扑
- selection: 选择管理者模式
- artifacts: 交付拓扑、协议和验证门
- verification: 覆盖失败与追踪
- anti-pattern: 拒绝无验证转发

## Review Record

- trigger-recognition: pass
- decision-inputs: pass
- option-relationship: pass
- selection: pass
- artifacts: pass
- verification: pass
- anti-pattern: pass

## Agent Response Summary

设置管理者负责分解、资源分配和最终汇总，执行者通过明确工件交付；关键中间结果必须经管理者验证。故障演练表明控制权、失败原因和修正路径均可追踪。
