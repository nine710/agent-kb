# agent-kb

AI Agent 设计知识库：策展决策卡（curated decision cards），用于提升编程智能体在设计阶段的设计上限。

## 这是什么

不是论文全文库，而是**决策卡**——每张卡是一个可反复遇到的设计问题，附带 ≥3 个真选项、tradeoffs、应用规则和来源。

## 怎么用

1. 在设计/brainstorm 时，按问题关键词翻 `cards/` 下的卡片
2. 每张卡提供多个真实方案分叉，帮助看到更多可能性
3. `raw/sources.md` 列出全部源材料索引

## 卡片结构

详见 `SCHEMA.md`。空白模板见 `templates/card.md`。

## 开发 Agent 消费

`development-agent-v1` 卡片是供 Codex、Claude Code 等编程 Agent 在开发 Agent 项目时直接执行的设计参考。它除 Options 与 Tradeoffs 外，还包含 Trigger、Decision Inputs、Option Relationship、Selection Rules、Required Artifacts 和 Verification。每张 v1 卡在 `eval/development-agent/` 下有典型、边界和反模式三项公开任务；任务必须由开发 Agent 实际回答并经过 rubric 审查。`decision-card-v0` 是尚未完成该迁移的过渡卡，仍可提供来源可追溯的设计知识，但不宣称可直接执行。

## 蒸馏 Skill

仓库内的 `skills/agent-kb-distill/` 是统一蒸馏入口。人工提供来源后，Skill 建立材料画像、证据台账和候选问题队列，并为每个候选在 `drafts/<source_id>/` 建立永久本地草稿与 evidence sidecar。目标为 `development-agent-v1` 的候选还必须完成开发 Agent 适配、Procedure 证据绑定和三项公开任务审查。只有同时通过语义门禁、`python scripts/validate_distillation.py <source-package> --drafts drafts --cards cards` 与 `python scripts/validate_card.py --all` 的候选才会以 `published` 状态进入 `cards/`；`raw-only`、`out-of-scope`、`rejected` 也会保留并记录原因。Skill 不执行 Git 操作。

## 本地蒸馏材料

`raw/` 是蒸馏输入层。`raw/sources.md` 是公开的来源索引；每个实际来源的原始文件、配套项目、派生台账和 fair-use 摘录都收纳在同一个本地材料包中：`raw/src-NNN-<source-slug>/{source,derived,excerpts}/`。材料包和 `drafts/` 由 `.gitignore` 排除，不进入公开仓库；它们共同构成可追溯的本地蒸馏档案。

## 验证

```bash
python scripts/validate_card.py --all   # 验证所有正式卡
```

## 许可

卡片内容（`cards/`）基于 Apache 2.0 源材料蒸馏。源材料许可各自独立，见 `raw/sources.md`。
