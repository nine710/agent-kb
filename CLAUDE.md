# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 这是什么

**agent-kb 不是软件项目，而是一个内容仓库**——AI Agent 设计知识库。产出物是**策展决策卡**：每张卡是一个可反复遇到的设计问题，附带 ≥3 个真选项、权衡（tradeoffs）、应用规则和来源。目标是提升编程智能体（Claude Code / Codex 等）在设计阶段的设计上限。

核心思想：**蒸馏 ≠ 摘要**。蒸馏是把原始材料重构为决策单元（问题 + 选项 + 权衡），而不是压缩原文。这一点贯穿全库，是判断内容是否合格的根基。

复杂任务的设计文档放在本地 `planning/`，不入公开仓库；小任务不创建这些文档。

## 任务规模规则

- 单文件局部修改、同步、验证、路径或说明修正等小任务，直接执行，不写 spec，不写 plan。
- 只有跨文件多阶段、改变行为或契约、需要迁移，或无法局部验证的任务，才写简短 spec/plan，并在实施前确认。

## 核心约束（写卡 / 改卡 / 建源前必读，违反即不合格）

这 6 条是本仓库与普通 markdown 文档的根本区别，优先级最高：

1. **≥3 真选项**——必须是真正不同的设计路径，不是同一方案的变体或换皮。凑不出 3 叉的问题只进 `raw/sources.md` 的 raw-only 标注，**不建卡**（混合门槛）。
2. **零个人经验**——所有字段（尤其 `Apply to Agent Development`、`Anti-Patterns`）严禁出现任何个人项目经历、项目名、踩坑记录。只写外部可推导的通用规则。**永久不做个人经验入卡。**
3. **源可追溯**——每个选项、每条权衡、每条应用规则都必须能回溯到 `Sources` 中的具体源；优先使用 **markdown 章节号**，其他材料使用可复核的源原生定位（文件位置、锚点或页码）。
4. **问题可复用**——`problem` 是可反复遇到的设计问题模板，不绑定某一篇文章或某一本书。
5. **非摘要**——产出的是决策单元（问题 + 选项 + 权衡），不是文章或书籍的读后感式摘要。
6. **公开边界**——`raw/src-NNN-<source-slug>/`（每个来源的原材料、派生分析和 fair-use 摘录）与 `drafts/`（永久本地候选档案）必须被 `.gitignore` 排除，**永不进公开仓库**。

草稿进 `cards/` 前，还必须逐条过对抗审查清单（见 `SCHEMA.md`，共 5 条：真三叉、非摘要、零个人经验、源可追溯、问题可复用）。

## 架构

### 仓库布局与可见性

| 目录/文件 | 职责 | 公开 |
|----------|------|------|
| `cards/*.md` | 正式决策卡（`status: active`）；`development-agent-v1` 可直接指导编程 Agent，`decision-card-v0` 为迁移期知识卡 | ✅ |
| `eval/development-agent/` | v1 卡的典型、边界、反模式消费验收任务与审查记录 | ✅ |
| `templates/card.md` | 空白卡片模板 | ✅ |
| `SCHEMA.md` | 卡片 schema + 对抗审查清单 + 摘录规范 | ✅ |
| `raw/sources.md` | 必读源索引（源 ID + 章节→问题映射 + raw-only 问题标注） | ✅ |
| `skills/agent-kb-distill/` | 蒸馏 Skill 的唯一开发源；修改后经脚本同步到 `.agents/skills/` | ✅ |
| `.agents/skills/agent-kb-distill/` | Codex 项目级技能发现镜像，不直接编辑 | ✅ |
| `raw/src-NNN-<source-slug>/` | 一个来源的本地材料包：`source/` 放原始材料，`derived/` 放台账/候选/报告，`excerpts/` 放 fair-use 短摘录（单条 ≤500 字、单源 ≤2000 字） | ❌ gitignore |
| `drafts/<source_id>/` | 永久保留的候选草稿与 evidence sidecar；状态为 `draft` / `published` / `raw-only` / `out-of-scope` / `rejected` | ❌ gitignore |
| `scripts/validate_card.py` | 卡片 schema 验证脚本（Python 标准库 only） | ✅ |

### `raw/` 的来源材料包约定

`raw/` 是蒸馏输入层，按**来源**而不是按文件格式分类。`raw/sources.md` 中每一个可蒸馏的 `src-NNN`，在本地对应一个同 ID 开头的材料包：

```text
raw/
├── sources.md                              # 公开：来源索引与来源→问题映射
└── src-NNN-<source-slug>/                  # 本地且 gitignored：一个完整来源
    ├── source/                             # 不修改的上游输入材料及其原始组织
    │   ├── <项目仓库或配套文件夹>/
    │   └── <同源 PDF、Markdown、HTML 等文件>
    ├── derived/                            # Agent 生成的材料画像、证据、候选和报告
    └── excerpts/                           # fair-use 短摘录、定位和阅读笔记
```

- 一个材料包可以同时含项目、文档、论文、网页存档或配套文件；只要它们共同构成同一个来源，就不得按“项目 / 文档 / 论文”拆到不同目录。
- `source/` 保持上游材料原样，不能把 Agent 的摘要、推断或改写混入其中；这些工作内容只放在 `derived/`、`excerpts/` 或 `drafts/`。
- 新增来源由 `skills/agent-kb-distill/` 自动分配 `src-NNN`、登记许可、建立材料包和生成材料画像；人工只提供或确认来源。修改 Skill 后先运行 `python scripts/sync_project_skill.py check`，确认无误后再运行 `python scripts/sync_project_skill.py sync`。

### 蒸馏管线（卡片如何从源材料走到 `cards/`）

```
人工选择来源
  → Agent 建立 raw/src-NNN-<source-slug>/{source,derived,excerpts} 与 drafts/<source_id>/
  → Agent 完整审读、建立证据台账、发现候选并语义去重
  → 每个候选建立草稿 + evidence sidecar，并记录生命周期状态
  → Agent 对抗审查、来源预检和 card schema 验证
  → 仅 published 候选进入 cards/；其余状态永久留存并记录原因

对 `development-agent-v1` 候选，在发布前还必须执行：定义 consumer / decision scope / option relationship → 写 Development Agent Procedure 六项 → 将 Procedure 绑定到证据 → 建立三项公开消费任务 → 由开发 Agent 实际回答、人工或 Agent 审查 rubric。仅创建任务文件不构成验收通过。
```

人工只选择来源；Agent 自主发现问题、草拟、审查和本地发布。Skill 不执行 Git 操作；项目开发流程单独负责提交和推送。

### 源↔卡映射

**多对多，`problem` 是卡的主键（不是源）。**
- 1 源 → 0/1/N 张卡；N 源 → 1 张卡（合并）。
- 优先合并/更新已有卡，**不默认「一源一卡」**。
- 同源不同章 = 同一个 `source_id`。

## 常用命令

```bash
python scripts/validate_card.py cards/<card>.md   # 验证单张卡
python scripts/validate_card.py --all             # 验证所有正式卡
```

验证器包括 `scripts/validate_card.py` 与 `scripts/validate_distillation.py`。前者检查正式卡结构和契约；后者检查来源包、候选与档案一对一关系、五种生命周期状态、证据 sidecar、进度、v1 Procedure 绑定和三项消费验收。`decision-card-v0` 是临时迁移契约；仅 `development-agent-v1` 可宣称为 Codex / Claude Code 的可执行开发参考。草稿不会因发布或拒绝而删除。

## 源材料工作流

当前唯一确认源：**《深入理解 AI Agent：设计原理与工程实践》（李博杰）**，编号 `src-001`，Apache 2.0。

- `src-001` 的材料包为 `raw/src-001-ai-agent-book/`：上游 Markdown 仓库与辅助 PDF 同属这一来源，因而共同放在其 `source/`，而不是放在仓库根目录。
- **用 markdown 源码蒸馏**（GitHub `bojieli/ai-agent-book`，位于 `raw/src-001-ai-agent-book/source/ai-agent-book/book/chapter*.md`），**不用 PDF/EPUB**——PDF 的结构/表格/代码块易丢，且无法精确章节定位。
- `raw/src-001-ai-agent-book/source/AI-Agents-in-Depth-zh-CN (1).pdf` 只是参考材料，**不应作为蒸馏主源**。
- 源材料格式优先级：markdown 源码 > GitHub 网页 > PDF（仅备选）> EPUB（不用）。
- 主题优先级：**A 主 = harness / 运行时工程**（constitution / skills / hooks / subagents / eval / memory 形态）；**B 辅 = 经典 agent 算法 / 论文**（仅在主域选项不够三叉时补充，不让知识库变成论文笔记）。

## 注意事项

- 蒸馏时**以源材料的术语和概念为准**；源中未必有 Claude Code 特有术语（如 hooks / constitution），在 `Apply to Agent Development` 中映射到编程智能体术语即可，但每个选项必须有源支撑——书中无支撑的候选**必须替换**，不可凭空编造。
- Git：本仓库是 git 仓库，远端 `nine710/agent-kb`（Public，SSH remote `git@github.com:nine710/agent-kb.git`），用户已授权自动 commit + push。**推送走 SSH 密钥认证（不经 PAT）+ Clash 代理**（HTTPS/PAT 推送会 403——fine-grained `GITHUB_PAT_TOKEN` 未覆盖此仓库的写权限；SSH 密钥已注册且可用）：`GIT_SSH_COMMAND="ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ProxyCommand='connect -H 127.0.0.1:7897 %h %p'" git push`。GitHub 直连被墙，git/HTTP 操作走 Clash 代理 `127.0.0.1:7897`（已写入 Claude Code settings.json `env`）。本地 `planning/`（方案/计划）、`CLAUDE.md`、`AGENTS.md`、`.gitignore` 均被 gitignore、**不入公开仓库**；公开仓库只含知识库产出（`cards/` `SCHEMA.md` `templates/` `raw/sources.md` `scripts/` `README.md`）。
- v0 不做的事：消费侧 design-time skill（用户自行构建）、个人经验入卡（永久不做）。
- 当前骨架与 `src-001` 首轮蒸馏已完成；`cards/` 含 6 张正式卡，来源包派生档案与候选生命周期档案仅本地保留。
