---
card_id: context-loading-strategy
task_id: context-loading-003
difficulty: anti-pattern
review_status: pass
reviewer: Codex development-agent review
reviewed_at: 2026-08-01
---

## Project Background

一个开发 Agent 的设计草案计划在每次请求的 system prompt 中注入当前时间戳、账户余额、请求计数和重新排序后的工具定义，理由是“模型随时都能看到最新状态”。

## Development Goal

审查该上下文方案，指出是否应接受，并提供保持最新状态而不破坏静态前缀的替代设计。

## Known Constraints

需要保留 Prompt Cache/KV Cache 的静态前缀收益；动态状态会在每轮变化；工具可通过调用获取实时数据。

## Expected Trigger

必须读取 `context-loading-strategy`，因为动态数据被错误放入静态前缀。

## Acceptable Decision

拒绝该设计。A 仅保留稳定身份、核心规则和稳定工具定义；动态状态放上下文末尾的状态区，或由工具按需读取；不得每轮重排工具定义。

## Required Artifacts

- 静态前缀字段清单与动态字段拒绝清单
- 动态状态的尾部注入或工具读取接口
- 工具定义稳定排序规则

## Required Verification

- 比较多轮请求静态前缀哈希或字节序列
- 断言动态状态不在 system prompt
- 验证工具读取能返回当前状态

## Failure Conditions

- 接受将时间戳、余额或计数写入 system prompt
- 逐请求改变工具定义顺序
- 以“需要最新信息”为理由放弃缓存稳定性

## Rubric

- trigger-recognition: 识别动态静态前缀污染
- decision-inputs: 调查状态变化频率、缓存要求和工具可用性
- option-relationship: 区分 A 的稳定边界与工具/尾部状态承载
- selection: 拒绝草案并选择稳定前缀加动态替代
- artifacts: 交付字段清单、状态接口和排序规则
- verification: 验证前缀稳定、动态字段隔离和实时读取
- anti-pattern: 明确拒绝动态 system prompt 与工具重排

## Review Record

- trigger-recognition: pass
- decision-inputs: pass
- option-relationship: pass
- selection: pass
- artifacts: pass
- verification: pass
- anti-pattern: pass

## Agent Response Summary

拒绝在 system prompt 注入时间戳、余额、请求计数或每轮重排工具定义。A 只保留稳定身份、核心规则和固定排序的工具 schema；时间、余额和计数由上下文末尾状态区提供，或经专用工具按需读取。交付静态前缀允许/拒绝字段清单、状态读取接口和工具 schema 稳定排序规则。验证多轮静态前缀哈希相同，system prompt 不含动态字段，并通过工具调用获得当前余额和计数。该方案避免以“最新状态”为由击穿缓存。
