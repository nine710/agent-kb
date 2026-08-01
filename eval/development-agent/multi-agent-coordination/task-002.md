---
card_id: multi-agent-coordination
task_id: multi-agent-coordination-002
difficulty: boundary
review_status: pass
reviewer: Codex development-agent review
reviewed_at: 2026-08-01
---

## Project Background

故障处理任务会在诊断、数据库和安全专长之间动态转交，且每个 Agent 只持有局部上下文。

## Development Goal

设计不会丢失任务的去中心化移交。

## Known Constraints

没有长期管理者；需记录所有权；消息和文件是主要通信媒介。

## Expected Trigger

控制权必须随能力与状态动态流动。

## Acceptable Decision

选择 C，并定义最小移交状态、所有权、超时和失败回退。

## Required Artifacts

- 移交协议和状态 schema
- 所有权登记
- 超时/失败回退路径

## Required Verification

- 演练重复移交、超时和接收者失败
- 任务不得丢失或重复完成

## Failure Conditions

- 无所有权或状态记录
- 把文件通信误当控制拓扑

## Rubric

- trigger-recognition: 识别动态移交需求
- decision-inputs: 调查能力、状态和局部上下文
- option-relationship: 区分 C 与通信轴
- selection: 选择去中心化移交
- artifacts: 交付协议、登记和回退
- verification: 覆盖超时和重复
- anti-pattern: 拒绝无状态移交

## Review Record

- trigger-recognition: pass
- decision-inputs: pass
- option-relationship: pass
- selection: pass
- artifacts: pass
- verification: pass
- anti-pattern: pass

## Agent Response Summary

定义任务 ID、当前所有者、最小上下文摘要、完成条件和超时回退；文件和消息只承载信息，不改变 C 的控制语义。超时、接收失败和重复移交测试均保持单一所有权与可恢复状态。
