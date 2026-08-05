---
card_id: durable-task-admission-strategy
task_id: durable-task-admission-001
difficulty: typical
review_status: pass
reviewer: Codex development-agent review
reviewed_at: 2026-08-03
---

## Project Background

一个代码 Agent 代表用户处理部署审批。审批结果由外部系统在未知时间通过 Webhook 到达；同一审批事件可能被重复投递，Agent 必须在批准后继续部署并在拒绝后停止。

## Development Goal

为不可预测的外部审批结果建立可恢复、可去重且不重复产生发布副作用的任务唤醒机制。

## Known Constraints

Webhook 至少一次投递且可能乱序；部署有外部副作用；处理器可能与主任务并发；重启后必须保留审批和处理状态。

## Expected Trigger

需要选择不可预测外部结果如何唤醒持久任务，并定义重复投递、处理器并发和恢复状态时读取本卡。

## Acceptable Decision

采用异步事件准入。持久任务记录审批事件 ID、审批状态和处理状态；重复 Webhook 由事件 ID 去重。处理器只记录状态或投递主循环工作，不在阻塞处理器中直接执行部署。部署副作用使用幂等发布 ID。

## Required Artifacts

- Webhook 事件 schema、事件 ID 和去重状态
- 主任务状态转换与批准/拒绝后的下一步
- 幂等发布键、暂停/取消语义和审计记录

## Required Verification

- 重复和乱序 Webhook 不重复发布
- Agent 重启后能从已记录审批状态继续
- 拒绝后没有发布副作用
- 处理器阻塞不会使未完成状态丢失

## Failure Conditions

- 把 Webhook 当成可安全重复执行发布的直接命令
- 让阻塞处理器直接等待部署或执行长期副作用
- 重启后只凭最后一条通知判断审批和发布状态

## Rubric

- trigger-recognition: pass
- decision-inputs: pass
- option-relationship: pass
- selection: pass
- artifacts: pass
- verification: pass
- anti-pattern: pass

## Review Record

- trigger-recognition: pass
- decision-inputs: pass
- option-relationship: pass
- selection: pass
- artifacts: pass
- verification: pass
- anti-pattern: pass

## Agent Response Summary

选择异步事件准入，而非轮询审批 API 或等待同步请求。事件先以审批 ID 去重并记录，再由主循环按状态推进；批准后的发布使用独立幂等键，拒绝和用户取消都转入停止状态。测试覆盖重复、乱序、重启和拒绝。
