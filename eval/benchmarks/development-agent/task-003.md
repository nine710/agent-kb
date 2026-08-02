---
task_id: benchmark-development-agent-003
responsibility_id: knowledge-and-memory-architecture
difficulty: typical
review_status: pending
---

## Project Background

一个代码和架构问答 Agent 需要同时处理自然语言概念、函数名、错误码、目录关系和历史设计记录。知识来源会更新，部分条目可能过期或互相冲突。

## Development Goal

设计可追溯的知识组织、查询、排序和治理方案，使 Agent 能返回与问题相关且可复核的证据。

## Known Constraints

- 精确符号不能被相似但错误的名称替代。
- 概念问题包含同义表达和改写。
- 结果必须能定位文件、版本或原始记录。
- 过期和冲突内容不能静默作为无条件结论。

## Required Artifacts

- 查询分类和评估集
- 分块、索引和排序规则
- 来源、版本、所有权和冲突字段
- 召回、精度、时效和冲突测试

## Failure Risks

- 只按语义相似度返回错误内容
- 跨主题内容拼接后无法形成可执行证据
- 过期规则覆盖当前规则
- Agent 无法回溯结论来源

## Independent Rubric

- 能区分语义、精确符号和结构关系三类查询信号
- 能把检索质量与知识治理分开设计
- 交付物包含来源定位、版本和冲突处理
- 验证覆盖改写查询、精确标识符、过期和冲突条目
- 方案没有把单一相似度分数当作全部质量依据
