---
card_id: knowledge-retrieval-strategy
task_id: knowledge-retrieval-strategy-001
difficulty: typical
review_status: pass
reviewer: Codex development-agent review
reviewed_at: 2026-08-01
---

## Project Background

代码问答 Agent 需要回答自然语言架构问题，也要定位函数名、错误码和配置键。

## Development Goal

设计文档与代码知识库的检索层。

## Known Constraints

查询同时包含同义表达和精确符号；答案必须回链文件位置。

## Expected Trigger

需要在语义与精确检索之间作组合决策。

## Acceptable Decision

使用 C 组合 A/B，并按目录与组件关系增加 D。

## Required Artifacts

- 查询分类样本集
- 分块和来源定位规范
- 融合规则与结构化索引 schema

## Required Verification

- 分别测量改写、标识符和结构关系查询
- 结果保留来源定位

## Failure Conditions

- 仅依赖向量相似度
- 对融合规则没有评测

## Rubric

- trigger-recognition: 识别检索信号决策
- decision-inputs: 调查查询类型与知识关系
- option-relationship: 说明 C 组合 A/B、D 独立
- selection: 选择混合与结构方案
- artifacts: 交付四项工件
- verification: 覆盖三类查询和来源
- anti-pattern: 拒绝单一相似度

## Review Record

- trigger-recognition: pass
- decision-inputs: pass
- option-relationship: pass
- selection: pass
- artifacts: pass
- verification: pass
- anti-pattern: pass

## Agent Response Summary

为概念问答使用语义信号，为函数名和错误码使用关键词信号，再用融合排序；组件和目录关系由结构索引提供。测试集分别验证三类查询，所有命中保留文件、段落和版本定位。
