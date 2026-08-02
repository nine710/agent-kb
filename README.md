# agent-kb

AI Agent 设计知识库：策展决策卡（curated decision cards），用于提升编程智能体在设计阶段的设计上限。

## 这是什么

不是论文全文库，而是**决策卡**——每张卡是一个可反复遇到的设计问题，附带 ≥3 个真选项、tradeoffs、应用规则和来源。

## 怎么用

1. 在设计/brainstorm 时，先从 `DECISION-MAP.md` 选择正在承担的一级开发责任，再进入其关联的 `cards/` 子决策卡
2. 每张卡提供多个真实方案分叉，帮助看到更多可能性和对应的架构交付物
3. `raw/sources.md` 列出全部源材料索引；来源目录不决定卡片目录

## 卡片结构

详见 `SCHEMA.md`。空白模板见 `templates/card.md`。

`card_type` 区分单一原子决策和可按条件组合的策略；`status: active` 表示结构与来源门禁通过，`utility_status` 单独记录是否通过独立开发任务的效用验证。

## 任务规模

单文件局部修改、同步、验证、路径或说明修正等小任务直接执行，不写 spec 或 plan。跨文件多阶段、改变行为/契约、需要迁移或难以局部验证的任务，才使用简短 spec/plan。

## 开发 Agent 消费

`development-agent-v1` 卡片是供 Codex、Claude Code 等编程 Agent 在开发 Agent 项目时直接执行的设计参考。它绑定 `DECISION-MAP.md` 中的一级责任，并声明架构交付物和失败风险；除 Options 与 Tradeoffs 外，还包含 Trigger、Decision Inputs、Option Relationship、Selection Rules、Required Artifacts 和 Verification。每张 v1 卡在 `eval/development-agent/` 下有典型、边界和反模式三项公开任务；任务必须由开发 Agent 实际回答并经过 rubric 审查。`decision-card-v0` 是尚未完成该迁移的过渡卡，仍可提供来源可追溯的设计知识，但不宣称可直接执行。

独立任务基准位于 `eval/benchmarks/development-agent/`。它不指定卡片或选项，用于比较无卡片基线与提供卡片后的设计结果；七项典型任务是第一阶段的基准格式试点，扩展到十四项后才适合全面执行每张卡的三任务效用门禁。

## 蒸馏 Skill

`skills/agent-kb-distill/` 是 Skill 的唯一开发源；`.agents/skills/agent-kb-distill/` 是 Codex 项目级镜像。只修改源目录，确认后同步：

```bash
python scripts/sync_project_skill.py check
python scripts/sync_project_skill.py sync
python scripts/sync_project_skill.py check
```

Skill 只在本仓库会话中发现，不安装到用户级目录。人工选择来源；Skill 建立材料画像、证据台账、决策地图对齐、候选和审查档案。只有通过卡片与蒸馏门禁的候选才进入 `cards/`；其他候选保留为 `raw-only`、`out-of-scope` 或 `rejected`。Skill 不执行 Git 操作。

## 本地蒸馏材料

`raw/` 是蒸馏输入层。`raw/sources.md` 是公开的来源索引；每个实际来源的原始文件、配套项目、派生台账和 fair-use 摘录都收纳在同一个本地材料包中：`raw/src-NNN-<source-slug>/{source,derived,excerpts}/`。材料包和 `drafts/` 由 `.gitignore` 排除，不进入公开仓库；它们共同构成可追溯的本地蒸馏档案。

## 验证

```bash
python scripts/validate_card.py --all   # 验证所有正式卡
python scripts/validate_benchmark.py eval/benchmarks/development-agent  # 验证独立基准任务
python scripts/validate_distillation.py raw/<source-package> --drafts drafts --cards cards
```

## 许可

卡片内容（`cards/`）基于 Apache 2.0 源材料蒸馏。源材料许可各自独立，见 `raw/sources.md`。
