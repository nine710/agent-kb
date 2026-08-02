---
id: knowledge-retrieval-strategy
card_contract: development-agent-v1
card_type: atomic-decision
utility_status: unverified
consumer: development-agent
decision_scope: knowledge-retrieval
option_relationship: composable-by-information-type
design_task_id: knowledge-and-memory-architecture
design_goal: 让 Agent 获取可追溯、及时且与任务相关的外部知识。
required_artifact_types: [knowledge-organization-schema, retrieval-evaluation-set, freshness-conflict-policy]
failure_risks: [stale-or-conflicting-knowledge, unsupported-retrieval, missing-provenance]
problem: 如何为代码 Agent 设计同时处理自然语言、精确符号和结构关系的检索管道，并让每个结果保留来源、版本和冲突状态？
tags: [rag, retrieval, sparse-search, dense-search, structured-index, provenance]
when_to_use: Agent 需要检索代码、文档、规范、错误码或长期知识，并且回答必须能回链到文件、版本或原始记录时。
when_not: 知识规模很小、内容固定且可以直接放入稳定上下文时。
status: active
source_ids: [src-001]
---

## Options

### Option A: 稠密语义检索

用嵌入和向量相似度召回语义相近的内容，适合自然语言改写、概念询问和同义表达。必须配合可解释的分块和来源定位，否则相似片段不等于可支持结论的证据。

### Option B: 稀疏精确检索

用关键词、名称、函数、错误码和配置键进行精确匹配，适合代码符号、版本号和必须保持字符准确的查询。它保护精确性，但对同义表达和概念改写的召回较弱。

### Option C: 混合检索

把稠密语义信号与稀疏精确信号结合，并通过融合或重排处理不同查询类型。混合不是默认更好，必须用查询分类集证明额外复杂度改善了召回、精度或排序。

### Option D: 结构化索引

用目录、组件关系、实体/属性、依赖或文件系统组织知识，使 Agent 能按结构关系定位内容。它是知识组织和关系检索轴，可以与 A/B/C 组合，不能被单一相似度分数替代。

## Tradeoffs

| | 优势 | 代价 |
|---|---|---|
| A 稠密 | 覆盖同义表达和概念改写，适合开放式问题 | 可能误命中相似符号或跨主题片段，依赖嵌入和分块质量 |
| B 稀疏 | 精确名称、错误码和配置键可解释且不易被近义文本替代 | 同义表达召回弱，查询规范化和索引维护成本更高 |
| C 混合 | 同时覆盖语义召回和精确匹配，可按查询类型调节 | 引入融合、重排、延迟和调参成本；没有评测就只是复杂化 |
| D 结构 | 保留组件、目录和实体关系，适合关系约束与归属查询 | 建模和维护成本高；结构不完整会产生系统性漏召回 |

## Apply to Agent Development

- 先把查询分为语义改写、精确标识符和结构关系，再决定信号，而不是先选一个向量模型。
- 概念和同义表达使用 A；函数名、错误码、版本号和配置键至少保留 B；查询同时含两者时以 C 为候选并用数据集验证。
- 组件关系、目录所有权和实体属性使用 D；D 可与 A/B/C 组合，但返回必须仍然包含来源定位。
- 分块必须保持主题完整，不能让一个 chunk 跨越互不相关的决策；每个结果记录来源、版本、所有者、更新时间和冲突状态。
- 过期或冲突知识不能静默成为无条件结论，应升级、过滤或要求人工确认。

## Development Agent Procedure

### Trigger

当 Agent 需要从代码、文档或历史知识中取回证据，且查询同时包含概念、精确符号、结构关系、时效或冲突约束时读取本卡。

### Decision Inputs

建立查询样本集，标注语义改写、精确标识符和结构关系；记录语料主题、版本、所有权、更新频率、冲突规则、来源定位要求、延迟预算和可接受的误召回/漏召回成本。

### Option Relationship

A、B、C 是检索信号轴，D 是知识组织/关系轴。A/B/C 可按查询类型组合，D 可与任一信号组合；它们不是用一个总体相似度分数替代所有查询。

### Selection Rules

- 以概念和同义表达为主选 A。
- 以函数名、错误码、配置键或版本号为主选 B。
- 同时需要语义召回和精确约束时选 C，但保留融合规则和对照评估。
- 组件、目录、实体和依赖关系决定结果时加入 D。
- 任何组合都必须返回来源、版本、所有权和冲突状态；没有治理证据时不得作为高影响设计结论。

### Required Artifacts

交付查询分类与样本集、主题完整的分块规范、A/B/C 信号与融合/重排规则、D 的结构化索引 schema，以及来源/版本/时效/冲突治理策略。

### Verification

- 用语义改写、精确标识符和结构关系三组查询分别测召回、精度和排序。
- 比较混合检索与单信号基线，没有改进证据时不保留额外复杂度。
- 用跨主题 chunk、过期条目和冲突条目做反例，确认结果保留来源和冲突状态。
- 检查精确符号不会被语义相近内容替代，且无来源结果不能进入设计结论。

## Anti-Patterns

- 把全部知识扁平切块后只依赖单一相似度分数。
- 用跨主题 chunk 让 Agent 得到片段却无法形成可执行上下文。
- 用稀疏检索处理所有同义表达，或用语义近似替代精确符号。
- 引入混合检索却没有融合规则和回归集。
- 不记录版本、所有者和冲突，让 Agent 静默采用过期规则。

## Sources

- [src-001] chapter3.md §RAG 基础：构建 Agent 的知识获取管道；§文档分块（Chunking）；§稠密嵌入：从词汇关联到语义理解；§稀疏嵌入：精确匹配的关键词检索；§混合检索：两全其美的艺术。
- [src-001] chapter3.md §超越扁平文本：知识的组织与检索；§结构化索引；§文件系统范式：用目录结构组织知识；§知识库的时效与治理。
- [src-001] chapter3.md §上下文检索：让检索结果更懂语境；§双层记忆系统：概览与细节分离。
