# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 这是什么

**agent-kb 不是软件项目，而是一个内容仓库**——AI Agent 设计知识库。产出物是**策展决策卡**：每张卡是一个可反复遇到的设计问题，附带 ≥3 个真选项、权衡（tradeoffs）、应用规则和来源。目标是提升编程智能体（Claude Code / Codex 等）在设计阶段的设计上限。

核心思想：**蒸馏 ≠ 摘要**。蒸馏是把原始材料重构为决策单元（问题 + 选项 + 权衡），而不是压缩原文。这一点贯穿全库，是判断内容是否合格的根基。

设计文档：`agent-kb方案.md`（方案）、`agent-kb计划.md`（v0 实施计划，分 3 个 Phase）。

## 核心约束（写卡 / 改卡 / 建源前必读，违反即不合格）

这 6 条是本仓库与普通 markdown 文档的根本区别，优先级最高：

1. **≥3 真选项**——必须是真正不同的设计路径，不是同一方案的变体或换皮。凑不出 3 叉的问题只进 `raw/sources.md` 的 raw-only 标注，**不建卡**（混合门槛）。
2. **零个人经验**——所有字段（尤其 `Apply to Agent Development`、`Anti-Patterns`）严禁出现任何个人项目经历、项目名、踩坑记录。只写外部可推导的通用规则。**永久不做个人经验入卡。**
3. **源可追溯**——每个选项、每条权衡、每条应用规则都必须能回溯到 `Sources` 中的具体源；定位用 **markdown 章节号**，**不用 PDF 页码**。
4. **问题可复用**——`problem` 是可反复遇到的设计问题模板，不绑定某一篇文章或某一本书。
5. **非摘要**——产出的是决策单元（问题 + 选项 + 权衡），不是文章或书籍的读后感式摘要。
6. **公开边界**——`raw/excerpts/`（fair-use 短摘录）和 `drafts/`（未过门草稿）必须被 `.gitignore` 排除，**永不进公开仓库**。

草稿进 `cards/` 前，还必须逐条过对抗审查清单（见 `SCHEMA.md`，共 5 条：真三叉、非摘要、零个人经验、源可追溯、问题可复用）。

## 架构

### 仓库布局与可见性

| 目录/文件 | 职责 | 公开 |
|----------|------|------|
| `cards/*.md` | 通过全链路门禁的正式决策卡（`status: active`） | ✅ |
| `templates/card.md` | 空白卡片模板 | ✅ |
| `SCHEMA.md` | 卡片 schema + 对抗审查清单 + 摘录规范 | ✅ |
| `raw/sources.md` | 必读源索引（源 ID + 章节→问题映射 + raw-only 问题标注） | ✅ |
| `raw/excerpts/` | 短摘录（fair-use，单条 ≤500 字、单源 ≤2000 字） | ❌ gitignore |
| `drafts/` | 未过门的草稿卡（`status: draft`） | ❌ gitignore |
| `scripts/validate_card.py` | 卡片 schema 验证脚本（Python 标准库 only） | ✅ |

### 蒸馏管线（卡片如何从源材料走到 `cards/`）

```
人选源 + 选问题  →  Agent 按 SCHEMA 草拟 → drafts/  →  Agent 对抗审查（5 条清单）  →  人工终审  →  cards/
```

人工主导，不全自动：人定源、定问题；Agent 填草稿并自检；人做最终终审放行。

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

验证脚本是本仓库唯一的"测试"。每张卡进 `cards/` 前必须 PASS（退出码 0）。它检查：frontmatter 7 字段齐全、`cards/` 下 `status` 必须是 `active`、Options ≥3、5 个必填正文段、`id` 与文件名一致、Sources 含 `src-` 引用。

## 源材料工作流

当前唯一确认源：**《深入理解 AI Agent：设计原理与工程实践》（李博杰）**，编号 `src-001`，Apache 2.0。

- **用 markdown 源码蒸馏**（GitHub `bojieli/ai-agent-book`，已克隆到仓库内 `ai-agent-book/book/chapter*.md`），**不用 PDF/EPUB**——PDF 的结构/表格/代码块易丢，且无法精确章节定位。
- 仓库内的 `AI-Agents-in-Depth-zh-CN (1).pdf` 只是参考材料，**不应作为蒸馏主源**。
- 源材料格式优先级：markdown 源码 > GitHub 网页 > PDF（仅备选）> EPUB（不用）。
- 主题优先级：**A 主 = harness / 运行时工程**（constitution / skills / hooks / subagents / eval / memory 形态）；**B 辅 = 经典 agent 算法 / 论文**（仅在主域选项不够三叉时补充，不让知识库变成论文笔记）。

## 注意事项

- 蒸馏时**以源材料的术语和概念为准**；源中未必有 Claude Code 特有术语（如 hooks / constitution），在 `Apply to Agent Development` 中映射到编程智能体术语即可，但每个选项必须有源支撑——书中无支撑的候选**必须替换**，不可凭空编造。
- Git：本仓库已是 git 仓库，远端 `nine710/agent-kb`（Public），用户已授权自动 commit。**push 需 PAT 对 `agent-kb` 有 `Contents: write` 权限**——当前 fine-grained PAT（`GITHUB_PAT_TOKEN`）尚未覆盖此新建仓库，push 会 403；修复前本地 commit 正常、推送阻塞。GitHub 直连被墙，git/HTTP 操作走 Clash 代理 `127.0.0.1:7897`（已写入 Claude Code settings.json `env`）。
- v0 不做的事：消费侧 design-time skill（用户自行构建）、个人经验入卡（永久不做）。
- Phase 1（骨架）与 v0 蒸馏已在本地完成：`SCHEMA.md`、`scripts/validate_card.py`、`templates/card.md`、`raw/sources.md`、`README.md`、`.gitignore` 均已就位；`cards/` 含 2 张正式卡（`constraint-placement`、`context-loading-strategy`，`validate_card.py --all` 双 PASS）；`raw/sources.md` 含 1 个 raw-only 标注。**仅剩 push 待 PAT 写权限修复**（见上一条）。
