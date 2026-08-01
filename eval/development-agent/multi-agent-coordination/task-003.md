---
card_id: multi-agent-coordination
task_id: multi-agent-coordination-003
difficulty: anti-pattern
review_status: pass
reviewer: Codex development-agent review
reviewed_at: 2026-08-01
---

## Project Background

多个对等 Agent 同时编辑同一部署配置，互相要求继续审查，但没有写入所有权、终止或裁决机制。

## Development Goal

修复并发冲突与无终止协作。

## Known Constraints

共享文件系统会覆盖修改；意见可能冲突；单 Agent 已可完成简单编辑。

## Expected Trigger

无所有权的并发写入和无限对等循环触发本卡。

## Acceptable Decision

为真正需要互审的部分选择 B 并加入终止/裁决；为文件规定所有权或串行化；简单编辑退回单 Agent。

## Required Artifacts

- 角色、终止和裁决规则
- 文件所有权/版本约定
- 单 Agent 基线比较

## Required Verification

- 并发写入冲突测试
- 对等分歧和终止测试

## Failure Conditions

- 继续无约定并发写同一文件
- 为简单任务强制多 Agent

## Rubric

- trigger-recognition: 识别并发和循环反模式
- decision-inputs: 调查冲突、分歧和单 Agent 基线
- option-relationship: 区分 B 与文件通信
- selection: 选择有限互审或回退单 Agent
- artifacts: 交付规则、所有权和比较
- verification: 覆盖冲突和终止
- anti-pattern: 拒绝无约定并发

## Review Record

- trigger-recognition: pass
- decision-inputs: pass
- option-relationship: pass
- selection: pass
- artifacts: pass
- verification: pass
- anti-pattern: pass

## Agent Response Summary

仅在需要独立审查时采用 B，并规定裁决者、最大轮次和终止条件；共享配置使用明确写入所有权和版本检查。并发与分歧演练显示不再覆盖或无限循环，简单编辑回退单 Agent。
