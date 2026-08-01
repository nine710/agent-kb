---
card_id: knowledge-retrieval-strategy
task_id: knowledge-retrieval-strategy-002
difficulty: boundary
review_status: pass
reviewer: Codex development-agent review
reviewed_at: 2026-08-01
---

## Project Background

运维知识库包含同义故障描述、精确错误码、过期运行手册和互相冲突的部署规则。

## Development Goal

让 Agent 检索结果可用于高影响操作前的设计判断。

## Known Constraints

过期内容不可静默采用；错误码必须精确；冲突需显式暴露。

## Expected Trigger

检索设计同时涉及精确匹配、时效与冲突治理。

## Acceptable Decision

以 B 保证错误码精度，必要时以 C 补语义召回，并加入 D 的版本/所有权结构。

## Required Artifacts

- 错误码与改写查询集
- 文档版本和冲突状态字段
- 冲突升级规则

## Required Verification

- 过期或冲突条目不能作为无条件结论
- 错误码查询不被相近文本替代

## Failure Conditions

- 把过期结果当作最新事实
- 用语义近似取代精确错误码

## Rubric

- trigger-recognition: 识别治理边界
- decision-inputs: 调查版本、冲突与标识符
- option-relationship: 说明 B/C/D 组合
- selection: 选择精确与治理机制
- artifacts: 交付查询和治理工件
- verification: 检查过期、冲突和精度
- anti-pattern: 拒绝静默采用旧知识

## Review Record

- trigger-recognition: pass
- decision-inputs: pass
- option-relationship: pass
- selection: pass
- artifacts: pass
- verification: pass
- anti-pattern: pass

## Agent Response Summary

使用关键词索引保护错误码精度，混合信号只补充同义描述，并通过结构化元数据返回版本、所有者和冲突状态。验证显示冲突和过期条目会被标记并升级，而不会作为无条件结论。
