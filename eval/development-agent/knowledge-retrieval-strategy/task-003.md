---
card_id: knowledge-retrieval-strategy
task_id: knowledge-retrieval-strategy-003
difficulty: anti-pattern
review_status: pass
reviewer: Codex development-agent review
reviewed_at: 2026-08-01
---

## Project Background

现有 RAG 将整份文档粗暴切块，仅按向量分数返回内容，且不记录文档版本。

## Development Goal

纠正不可靠的检索设计。

## Known Constraints

chunk 经常跨主题；用户会询问 API 名和组件所有权；文档会更新。

## Expected Trigger

单一相似度、错误分块和无治理知识库触发本卡。

## Acceptable Decision

重建可理解分块，加入 B/C 和必要 D，返回来源与版本。

## Required Artifacts

- 重分块规范
- 标识符检索规则
- 版本和所有权索引

## Required Verification

- 对 API、关系和过期文档做回归查询
- 不接受无来源结果

## Failure Conditions

- 只调整向量模型
- 继续返回跨主题且无版本的 chunk

## Rubric

- trigger-recognition: 识别扁平单信号反模式
- decision-inputs: 调查分块、符号、结构和时效
- option-relationship: 说明检索与结构组合
- selection: 重构分块和信号
- artifacts: 交付三项工件
- verification: 覆盖回归与来源
- anti-pattern: 拒绝仅调向量模型

## Review Record

- trigger-recognition: pass
- decision-inputs: pass
- option-relationship: pass
- selection: pass
- artifacts: pass
- verification: pass
- anti-pattern: pass

## Agent Response Summary

将知识重分为主题完整的单元，加入标识符检索和组件/版本索引，并对混合排序建立回归集。Agent 拒绝仅调整 embedding，因为它不能解决跨主题 chunk、精确符号和过期知识问题。
