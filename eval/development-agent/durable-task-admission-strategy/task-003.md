---
card_id: durable-task-admission-strategy
task_id: durable-task-admission-003
difficulty: anti-pattern
review_status: pass
reviewer: Codex development-agent review
reviewed_at: 2026-08-03
---

## Project Background

一个夜间代码健康扫描要在工作日运行。扫描可能持续到下一次触发，偶发依赖故障需要暂停后由操作者决定恢复；系统停机后是否补跑取决于任务时效。

## Development Goal

为周期性维护任务建立明确的时间、重叠、补跑、暂停和容量边界，避免以常驻轮询替代调度策略。

## Known Constraints

运行时间可能超过下次触发；依赖故障需人工决定恢复；停机后的补跑受时效限制；峰值容量不能无限扩张。

## Expected Trigger

需要为周期任务声明时间、重叠、补跑、暂停和容量政策时读取本卡。

## Acceptable Decision

采用时间驱动调度。声明日历、时区、抖动、时效性 catchup window、最大动作数和重叠政策。扫描不可并发时选择 Skip 或 BufferOne；故障时暂停调度，并在恢复时有意识地选择 Backfill，而不是把任务暂停误当作调度暂停。

## Required Artifacts

- 调度规格、时区、抖动和 catchup window
- 重叠、失败暂停、最大动作和 Backfill 政策
- 扫描运行状态与暂停/取消/终止语义

## Required Verification

- 重叠触发遵循已声明政策
- 停机跨越 catchup window 的行为可观察
- 失败会暂停未来触发且恢复不隐式补跑
- 峰值容量下没有无界并发或高频轮询

## Failure Conditions

- 用无限常驻循环轮询时钟和任务状态
- 未声明重叠和补跑政策，任由故障恢复后积压执行
- 把当前运行的暂停与未来调度的暂停视为同一状态

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

选择时间驱动调度，不通过常驻循环每分钟检查时钟。扫描以时效决定 catchup window，以不可并发约束选择 BufferOne，并启用失败暂停。恢复流程显式决定是否 Backfill，同时记录暂停源和在途运行，避免静默积压或重复执行。
