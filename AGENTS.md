# AGENTS.md

## 项目

`agent-kb` 是 AI Agent 设计知识库，不是软件项目。产出物是策展决策卡：可复用问题、至少三个真实选项、权衡、应用规则和可追溯来源。蒸馏不是摘要。

## 任务规模

- 单文件局部修改、同步、验证、路径或说明修正等小任务：直接执行，不写 spec，不写 plan。
- 跨文件多阶段、改变行为/契约、需要迁移或难以局部验证的任务：才写简短 spec/plan，并在实施前确认。

## 卡片硬约束

1. 至少三个真正不同的设计选项；不足三叉只进 `raw/sources.md` 的 `raw-only`，不建卡。
2. 不写个人项目经验、项目名或踩坑记录，只写可由外部来源推导的通用规则。
3. 每个选项、权衡、应用规则和反模式都必须能回溯到 `Sources` 的稳定定位。
4. `problem` 必须是可复用的设计问题，不绑定某一章或某一本书；卡片是决策单元，不是摘要。
5. 草稿进入 `cards/` 前必须通过 `SCHEMA.md` 的五项对抗审查。

## 目录边界

- `cards/`：公开正式卡；`eval/development-agent/`：v1 卡的典型、边界、反模式验收任务。
- `eval/benchmarks/development-agent/`：与卡片解耦的独立设计任务基准；不透露卡片答案，用于验证卡片是否改善陌生任务中的设计结果。
- `DECISION-MAP.md`：一级开发责任；卡片以 `problem` 为主键，源与卡是多对多关系。
- `raw/sources.md`：公开源索引；`raw/src-NNN-<slug>/`：原材料、派生台账、摘录，保持上游材料不变且不进 Git。
- `drafts/<source_id>/`：永久本地候选和 evidence sidecar，不进 Git；状态为 `draft`、`published`、`raw-only`、`out-of-scope` 或 `rejected`。
- `skills/agent-kb-distill/`：Skill 唯一开发源；`.agents/skills/agent-kb-distill/`：Codex 项目级运行镜像，不直接编辑。

## Skill 修改与蒸馏

修改 Skill 只改 `skills/`，确认后执行：

```bash
python scripts/sync_project_skill.py check
python scripts/sync_project_skill.py sync
python scripts/sync_project_skill.py check
```

蒸馏顺序：人工选源 → 建立材料包和进度 → 本次从头到尾完整审读全部原材料并建立 evidence ledger → 对齐 `DECISION-MAP.md` → 发现候选并语义去重 → 建草稿和 sidecar → 对抗审查与验证 → 仅发布通过门禁的卡。首次蒸馏、重蒸馏、卡片刷新及 Skill/schema/基准变更都必须重新完整审读；旧卡片、草稿、台账、报告或指纹不能替代本次阅读。新增来源只由人工选择；Skill 不执行 Git 操作。

候选问题必须先绑定 `DECISION-MAP.md` 的一级责任，再由跨章节证据和独立基准需求决定；章节标题不能直接变成卡片。三叉证据不足时保留 `raw-only`，不得为了覆盖率补造选项；辅助 PDF/图片只按材料清单记录并交叉核对，不能替代主源证据。

`development-agent-v1` 还必须有 `consumer`、`card_type`、`utility_status`、`decision_scope`、`option_relationship`、一级责任绑定、六项 Development Agent Procedure、六项 evidence 绑定，以及三项已实际审查的公开消费任务。`status: active` 只表示结构/来源门禁通过；`utility_status: validated` 还需要至少三项独立基准任务的无卡/有卡对照。

卡片专属任务只验收 Procedure 是否可执行；独立基准任务不得透露卡片答案，且只有完成基线对照后才能改变 `utility_status`。

## 常用命令

```bash
python scripts/validate_card.py cards/<card>.md
python scripts/validate_card.py --all
python scripts/validate_benchmark.py eval/benchmarks/development-agent
python scripts/validate_distillation.py raw/<source-package> --drafts drafts --cards cards
```

源格式优先级：Markdown 源码 > GitHub 页面 > PDF；当前 `src-001` 的主源是其 Markdown 章节。Git 提交和推送属于项目开发流程，按用户授权执行。
