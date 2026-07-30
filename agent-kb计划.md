# agent-kb 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在 `agent-kb` 仓库中完成 v0 里程碑——骨架 + ≥2 张正式卡 + ≥1 个 raw-only 问题，验证蒸馏闭环。

**Architecture:** GitHub Public 仓库 `agent-kb` + 本地 `E:\ai\agent-kb`；策展决策卡（distilled decision cards）；人工主导蒸馏 + Agent 草稿 + 对抗门禁 + 人工终审。源材料为《深入理解 AI Agent》（`bojieli/ai-agent-book`，Apache 2.0，markdown 源码）。

**Tech Stack:** Git/GitHub, Markdown, Python（仅验证脚本，stdlib-only）

---

## File Structure

| 文件 | 职责 | Phase | 公开 |
|------|------|-------|------|
| `.gitignore` | 排除 `raw/excerpts/` 和 `drafts/` | Alpha | ✅ |
| `README.md` | 项目说明 + 使用指引 | Alpha | ✅ |
| `SCHEMA.md` | 卡片规范 + 对抗审查清单 + 摘录规范 | Alpha | ✅ |
| `templates/card.md` | 空白卡片模板 | Alpha | ✅ |
| `raw/sources.md` | 必读源索引 + 章节→problem 映射 | Alpha | ✅ |
| `scripts/validate_card.py` | 卡片 schema 验证脚本（stdlib） | Alpha | ✅ |
| `drafts/constraint-placement.md` | 第 1 张卡草稿 | Phase 2 | ❌ gitignored |
| `cards/constraint-placement.md` | 第 1 张正式卡 | Phase 2 | ✅ |
| `raw/sources.md`（更新） | 追加 raw-only problem 标注 | Phase 2 | ✅ |
| `drafts/context-loading-strategy.md` | 第 2 张卡草稿 | Phase 3 | ❌ gitignored |
| `cards/context-loading-strategy.md` | 第 2 张正式卡 | Phase 3 | ✅ |

---

## Phase 1：Alpha（骨架就绪）

### Task 1：创建仓库 + 目录骨架

**Files:**
- Create: GitHub repo `nine710/agent-kb` (Public)
- Create: `E:\ai\agent-kb/` 目录树

- [ ] **Step 1：在 GitHub 创建 Public 仓库**

GitHub 网页 → New repository：
- Repository name: `agent-kb`
- Visibility: **Public**
- 不勾 Add README / .gitignore / license（后续手动创建）
- Create repository

- [ ] **Step 2：本地 clone + 创建目录骨架**

```bash
cd E:/ai
git clone git@github.com:nine710/agent-kb.git
cd agent-kb
mkdir -p templates raw/excerpts drafts cards scripts
```

- [ ] **Step 3：验证目录结构**

```bash
find . -type d | sort
```

Expected output:
```
.
./cards
./drafts
./raw
./raw/excerpts
./scripts
./templates
```

- [ ] **Step 4：Commit + push**

```bash
git add .
git commit -m "chore: scaffold agent-kb directory structure"
git push origin main
```

---

### Task 2：写 .gitignore

**Files:**
- Create: `.gitignore`

- [ ] **Step 1：写 .gitignore**

```
# fair-use 摘录不进公开仓库
raw/excerpts/

# 未过门的草稿
drafts/

# 系统文件
.DS_Store
Thumbs.db
*.swp
```

- [ ] **Step 2：验证忽略生效**

```bash
touch raw/excerpts/test.md drafts/test.md
git status
# 应显示 "nothing to commit"
rm raw/excerpts/test.md drafts/test.md
```

- [ ] **Step 3：Commit**

```bash
git add .gitignore
git commit -m "chore: add .gitignore for excerpts and drafts"
```

---

### Task 3：写 README.md

**Files:**
- Create: `README.md`

- [ ] **Step 1：写 README.md**

```markdown
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

## 验证

```bash
python scripts/validate_card.py --all   # 验证所有正式卡
```

## 许可

卡片内容（`cards/`）基于 Apache 2.0 源材料蒸馏。源材料许可各自独立，见 `raw/sources.md`。
```

- [ ] **Step 2：Commit**

```bash
git add README.md
git commit -m "docs: add README"
```

---

### Task 4：写 SCHEMA.md

**Files:**
- Create: `SCHEMA.md`

- [ ] **Step 1：写 SCHEMA.md**

```markdown
# SCHEMA.md — agent-kb 卡片规范

## 卡片文件

卡片是 `cards/` 目录下的 markdown 文件，文件名 = `id.md`。

## Frontmatter

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | string | 是 | kebab-case，全库唯一，等于文件名（不含 .md） |
| `problem` | string | 是 | 一句话设计决策问题（可反复遇到，不绑定单篇文章） |
| `tags` | string[] | 是 | 主题标签（如 harness, constitution, hooks） |
| `when_to_use` | string | 是 | 什么场景下会遇到此问题 |
| `when_not` | string | 是 | 什么场景不适用 |
| `status` | string | 是 | `draft`（草稿）/ `active`（正式）/ `deprecated`（废弃） |
| `source_ids` | string[] | 是 | 关联 `raw/sources.md` 中的源 ID |

## 正文章节

| 章节 | 必填 | 硬约束 |
|------|------|--------|
| **Options** | 是 | ≥3 个真分歧选项；每个选项有名称和描述 |
| **Tradeoffs** | 是 | 每个选项的优势与代价 |
| **Apply to Agent Development** | 是 | 外部可推导的通用决策规则；禁止个人项目经验 |
| **Anti-Patterns** | 是 | 源中或逻辑可证的反模式；禁止个人经验 |
| **Sources** | 是 | 每条含源 ID + 精确定位（markdown 章节号，非 PDF 页码） |

## 硬约束

1. **≥3 真选项**：不是同一方案的变体，是真正不同的设计路径
2. **零个人经验**：所有字段不含个人项目经历（项目名、踩坑记录等）
3. **源可追溯**：每个选项、tradeoff、应用规则都能回溯到 sources
4. **problem 可复用**：是设计问题模板，不是文章读后感

## 对抗审查清单（草稿进 cards/ 前必检）

| # | 检查项 | 通过标准 |
|---|--------|----------|
| 1 | 真三叉 | options ≥3 且是不同方案路径 |
| 2 | 非摘要 | 是决策单元，不是文章摘要 |
| 3 | 零个人经验 | 无任何个人项目经历 |
| 4 | 源可追溯 | 每条内容可回溯到 sources |
| 5 | problem 可复用 | 可反复遇到的设计问题 |

## raw/ 摘录规范

- `raw/sources.md`：公开，必读源索引
- `raw/excerpts/`：gitignored，短摘录（fair-use）
- 摘录长度上限：单条不超过 500 字，单源摘录总计不超过 2000 字
- 每条摘录必须标注精确来源定位（markdown 章节号 / 小节号）
- 不存全文、不存整书 PDF/EPUB

## 源材料格式优先级

1. markdown 源码（首选）
2. GitHub 网页（可用）
3. PDF（备选）
4. EPUB（不用）
```

- [ ] **Step 2：Commit**

```bash
git add SCHEMA.md
git commit -m "docs: add SCHEMA with card spec, review checklist, excerpt rules"
```

---

### Task 5：写 templates/card.md

**Files:**
- Create: `templates/card.md`

- [ ] **Step 1：写 templates/card.md**

```markdown
---
id: <kebab-case-slug>
problem: <一句话设计决策问题>
tags: [<主题标签>]
when_to_use: <什么场景下会遇到>
when_not: <什么场景不适用>
status: draft
source_ids: [src-001]
---

## Options

### Option A: <名称>

<这个选项是什么、怎么做>

### Option B: <名称>

<描述>

### Option C: <名称>

<描述>

## Tradeoffs

| | 优势 | 代价 |
|---|---|---|
| A | ... | ... |
| B | ... | ... |
| C | ... | ... |

## Apply to Agent Development

<外部可推导的通用决策规则。禁止个人项目经历。>

## Anti-Patterns

<源中或逻辑可证的反模式。禁止个人经验。>

## Sources

- [src-001] 《书名》作者 — Chapter X, Section Y
```

- [ ] **Step 2：Commit**

```bash
git add templates/card.md
git commit -m "docs: add blank card template"
```

---

### Task 6：写 raw/sources.md

**Files:**
- Create: `raw/sources.md`

- [ ] **Step 1：写 raw/sources.md**

```markdown
# 必读源清单

本文件索引知识库的全部外部源材料。只有此清单中的源可被蒸馏为决策卡。

## 源 ID 规则

`src-NNN`（三位数字，零填充）

## 源列表

### src-001：《深入理解 AI Agent：设计原理与工程实践》

| 字段 | 值 |
|------|-----|
| 作者 | 李博杰 |
| URL | https://github.com/bojieli/ai-agent-book |
| 许可 | Apache License 2.0 |
| 格式 | markdown 源码（`book/chapter*.md`） |
| 本地路径 | `E:\ai\ai-agent-book\book\` |
| 入选理由 | 10 章覆盖 Agent 全链路（harness/上下文/记忆/工具/Coding Agent/评估/训练/进化/多模态/多 Agent），94 个配套实验，核心公式 Agent = LLM + 上下文 + 工具 |

#### 章节-候选 problem 映射

| 章 | markdown 文件 | 主题 | 候选 problem |
|----|--------------|------|-------------|
| 1 | `chapter1.md` | Agent 基础 + Harness 工程 | 约束放哪 / Agent 公式选型 |
| 2 | `chapter2.md` | 上下文工程 | 上下文加载策略 / skills 组织 |
| 3 | `chapter3.md` | 用户记忆和知识库 | 记忆形态 / RAG vs 结构化索引 |
| 4 | `chapter4.md` | 工具 | MCP 协议选择 / 工具发现策略 |
| 5 | `chapter5.md` | Coding Agent | 代码生成范围控制 |
| 6 | `chapter6.md` | Agent 评估 | 评估环境选择 / 指标设计 |

### src-002（待补充）

公开工程文档（Claude Code / Agent SDK 官方文档等）。在蒸馏卡片时如需补充第 3 真分歧再纳入。

---

## 因单源不够三叉暂不建卡的 problem

（在 Phase 2 Task 11 中填写）
```

- [ ] **Step 2：Commit**

```bash
git add raw/sources.md
git commit -m "docs: add required source list with ai-agent-book as src-001"
```

---

### Task 7：写 scripts/validate_card.py（卡片验证脚本）

**Files:**
- Create: `scripts/validate_card.py`

这是卡片 schema 的自动化测试。每张卡进 `cards/` 前必须通过。

- [ ] **Step 1：写 scripts/validate_card.py**

```python
#!/usr/bin/env python3
"""validate_card.py — Validate a decision card against SCHEMA.md rules.

Usage:
    python scripts/validate_card.py cards/constraint-placement.md
    python scripts/validate_card.py --all
"""
import os
import re
import sys


REQUIRED_FRONTMATTER = [
    "id", "problem", "tags", "when_to_use", "when_not", "status", "source_ids",
]
REQUIRED_SECTIONS = [
    "## Options",
    "## Tradeoffs",
    "## Apply to Agent Development",
    "## Anti-Patterns",
    "## Sources",
]


def parse_frontmatter(text):
    """Extract YAML frontmatter as dict (minimal parser, no PyYAML)."""
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    fm_text = text[3:end].strip()
    result = {}
    for line in fm_text.splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip()
            if val.startswith("[") and val.endswith("]"):
                items = [
                    v.strip().strip("'\"")
                    for v in val[1:-1].split(",")
                    if v.strip()
                ]
                result[key] = items
            else:
                result[key] = val
    return result


def extract_body(text):
    """Return text after frontmatter."""
    if not text.startswith("---"):
        return text
    end = text.find("\n---", 3)
    if end == -1:
        return text
    return text[end + 4:]


def count_options(body):
    """Count '### Option' headings."""
    return len(re.findall(r"^### Option", body, re.MULTILINE))


def validate(path):
    """Return (errors, warnings) for a card file."""
    errors = []
    warnings = []

    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    fm = parse_frontmatter(text)
    body = extract_body(text)

    # 1. Required frontmatter fields
    for field in REQUIRED_FRONTMATTER:
        if field not in fm or not fm[field]:
            errors.append(f"missing or empty frontmatter field: {field}")

    # 2. status must be 'active' in cards/
    if fm.get("status") and fm["status"] != "active":
        errors.append(f"status must be 'active' in cards/, got: '{fm.get('status')}'")

    # 3. Options >= 3
    opt_count = count_options(body)
    if opt_count < 3:
        errors.append(f"Options must be >= 3, found {opt_count}")

    # 4. Required sections
    for sec in REQUIRED_SECTIONS:
        if sec not in body:
            errors.append(f"missing section: {sec}")

    # 5. Sources must contain src- references
    sources_idx = body.find("## Sources")
    if sources_idx != -1:
        sources_text = body[sources_idx:]
        if "src-" not in sources_text:
            warnings.append("Sources section has no src- ID references")

    # 6. id should match filename
    filename = os.path.splitext(os.path.basename(path))[0]
    if fm.get("id") and fm["id"] != filename:
        errors.append(f"id '{fm['id']}' does not match filename '{filename}'")

    return errors, warnings


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/validate_card.py <card.md>")
        print("       python scripts/validate_card.py --all")
        sys.exit(2)

    if sys.argv[1] == "--all":
        card_dir = os.path.join(os.path.dirname(__file__), "..", "cards")
        if not os.path.isdir(card_dir):
            print("No cards/ directory found")
            sys.exit(0)
        cards = sorted(
            os.path.join(card_dir, f)
            for f in os.listdir(card_dir)
            if f.endswith(".md")
        )
        if not cards:
            print("No cards to validate")
            sys.exit(0)
    else:
        cards = [sys.argv[1]]

    has_errors = False
    for card in cards:
        errors, warnings = validate(card)
        rel = os.path.relpath(card)
        if errors:
            has_errors = True
            print(f"FAIL: {rel}")
            for e in errors:
                print(f"  ERROR: {e}")
        elif warnings:
            print(f"WARN: {rel}")
            for w in warnings:
                print(f"  WARN: {w}")
        else:
            print(f"PASS: {rel}")

    sys.exit(1 if has_errors else 0)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2：验证脚本能运行（空 cards/ 目录）**

```bash
python scripts/validate_card.py --all
```

Expected output:
```
No cards to validate
```

- [ ] **Step 3：Commit**

```bash
git add scripts/validate_card.py
git commit -m "tool: add validate_card.py for schema validation"
git push origin main
```

---

### ✅ Alpha 检查点

逐条确认：

- [ ] 仓库 `nine710/agent-kb` 已创建且 Public
- [ ] 本地 `E:\ai\agent-kb` 可 push/pull
- [ ] 目录结构完整：`templates/` `raw/excerpts/` `drafts/` `cards/` `scripts/`
- [ ] `.gitignore` 排除 `raw/excerpts/` 和 `drafts/`
- [ ] `README.md` 存在且含使用说明
- [ ] `SCHEMA.md` 含卡片规范 + 对抗清单 5 条 + 摘录规范
- [ ] `templates/card.md` 存在
- [ ] `raw/sources.md` 含 src-001（ai-agent-book）
- [ ] `scripts/validate_card.py` 运行不报错
- [ ] 全部已 commit + push

**Alpha 完成 → 进入 Phase 2。**

---

## Phase 2：流程验证（第 1 张正式卡 + raw-only 问题）

### Task 8：clone 源材料仓库

**Files:**
- Clone: `E:\ai\ai-agent-book/`（外部仓库，不属于 agent-kb）

- [ ] **Step 1：clone 源书仓库**

```bash
cd E:/ai
git clone https://github.com/bojieli/ai-agent-book.git
```

- [ ] **Step 2：确认 markdown 源码可读**

```bash
ls E:/ai/ai-agent-book/book/chapter*.md
```

Expected: `chapter1.md` through `chapter10.md` + `introduction.md` + `afterword.md`

- [ ] **Step 3：不 commit（外部仓库）**

---

### Task 9：读源材料并蒸馏第 1 张卡草稿

**Files:**
- Read: `E:\ai\ai-agent-book\book\chapter1.md`、`chapter2.md`
- Create: `drafts/constraint-placement.md`（gitignored）

**Problem：** Agent 硬约束应放在 constitution（CLAUDE.md 类）/ skills / hooks 强制门 / subagent 专岗，如何选？

- [ ] **Step 1：读 chapter1.md（Agent 基础 + Harness 工程）**

先用 `grep -n "Harness\|约束\|constraint\|上下文\|Skills\|技能"` 定位相关小节，再精读命中段落。

重点寻找：
- "Harness" 概念定义——为什么 harness 工程是竞争力
- Agent 公式（Agent = LLM + 上下文 + 工具）中"上下文"和"工具"如何承载约束
- 不同约束承载位的讨论（常驻上下文 vs 按需加载 vs 硬编码流程）

记录找到的章节定位（如 `chapter1.md §1.2 Harness 工程`）。

- [ ] **Step 2：读 chapter2.md（上下文工程）**

先用 `grep -n "Skills\|技能\|上下文\|context\|加载\|压缩"` 定位相关小节，再精读。

重点寻找：
- Agent Skills 是什么、何时用（按需加载的约束/指令）
- 上下文常驻 vs 按需加载的 tradeoff
- 提示工程与 skills 的关系

记录章节定位。

- [ ] **Step 3：识别 ≥3 真选项**

从源材料中提取至少 3 个真正不同的约束承载方式。以下为**候选假设**，最终选项以源材料实际内容为准——如果某个候选在书中没有支撑，**必须替换为书中有支撑的其他选项**，不可凭空编造：

- **候选 A: Constitution 常驻**——约束写进系统提示/CLAUDE.md 类文件，总是加载到上下文
- **候选 B: Skills 按需加载**——约束封装为 Agent Skills，触发条件满足时才进上下文
- **候选 C: Hooks/流程强制**——约束编码为不可绕过的流程控制（hooks/中间件/拦截器），模型无法省略
- **候选 D: Subagent 专岗隔离**——约束通过子 agent 角色隔离实现

⚠️ **源适配原则**：书中的术语可能不同（如用「系统提示」「中间件」而非「constitution」「hooks」）。以书的概念为准，在 `apply_to_agent_dev` 中映射到编程智能体术语。每个最终选项须标注源章节定位。

- [ ] **Step 4：按 templates/card.md 填草稿 → `drafts/constraint-placement.md`**

草稿要求：
- frontmatter `status: draft`，`source_ids: [src-001]`
- 所有 `apply_to_agent_dev` 内容只写外部可推导规则
- 所有 `anti_patterns` 内容只写源中或逻辑可证的反模式
- 不含任何 NetAgent 或个人项目名称、踩坑经历
- Sources 每条标注 `[src-001] chapter1.md §X.Y` 或 `chapter2.md §X.Y`

- [ ] **Step 5：人工检查草稿完整性**

确认草稿包含：
- frontmatter 7 个字段全填
- Options ≥3 个 `### Option` 标题
- Tradeoffs 表格覆盖每个选项
- Apply to Agent Development 段落非空
- Anti-Patterns 段落非空
- Sources 段落含 `src-` 引用

---

### Task 10：验证 + 对抗审查 + 过门

**Files:**
- Read: `drafts/constraint-placement.md`
- Create: `cards/constraint-placement.md`

- [ ] **Step 1：复制草稿到 cards/ 并改 status**

```bash
cp drafts/constraint-placement.md cards/constraint-placement.md
```

编辑 `cards/constraint-placement.md`，将 frontmatter 中 `status: draft` 改为 `status: active`。

- [ ] **Step 2：运行验证脚本**

```bash
python scripts/validate_card.py cards/constraint-placement.md
```

Expected: `PASS: cards/constraint-placement.md`

如果有 ERROR → 修复 → 重新运行，直到 PASS。

- [ ] **Step 3：对抗审查清单（按 SCHEMA.md 逐条检查）**

逐条自检，每条写 PASS 或 FAIL：

| # | 检查项 | 通过标准 | 结果 |
|---|--------|----------|------|
| 1 | 真三叉 | options ≥3 且是不同方案路径，不是变体 | ☐ |
| 2 | 非摘要 | 是决策单元（problem + options + tradeoffs），不是文章摘要 | ☐ |
| 3 | 零个人经验 | 所有字段不含个人项目经历 | ☐ |
| 4 | 源可追溯 | 每个选项/tradeoff/rule 能回溯到 sources | ☐ |
| 5 | problem 可复用 | 是可反复遇到的设计问题，不绑定某一篇文章 | ☐ |

如有 FAIL → 修改卡片 → 重跑 Step 2 → 重新审查。

- [ ] **Step 4：人工终审**

通读完整卡片，判断：
- 选项是否真的不同（不是同一方案的换皮）？
- 应用规则是否通用（不绑死某个项目）？
- 是否值得公开？

- [ ] **Step 5：Commit**

```bash
git add cards/constraint-placement.md
git commit -m "card: constraint-placement — where to put agent hard constraints (src-001 ch1-2)"
```

---

### Task 11：验证 raw-only 问题（混合门槛在跑）

**Files:**
- Read: `E:\ai\ai-agent-book\book\chapter4.md`（工具章）
- Modify: `raw/sources.md`（追加 raw-only 标注）
- **不创建** cards/ 文件

- [ ] **Step 1：选一个候选 problem**

从 `chapter4.md`（工具）选一个候选，例如「事件驱动异步 Agent vs 轮询调度」。

- [ ] **Step 2：尝试抽选项**

读 chapter4.md 相关段落。如果只有 src-001 单源覆盖此问题，且无法凑出 ≥3 个真分歧（需要外部源补第 3 叉）→ 混合门槛判定：**只进 raw/，不建卡**。

- [ ] **Step 3：在 raw/sources.md 追加 raw-only 标注**

编辑 `raw/sources.md`，将末尾的占位段替换为：

```markdown
## 因单源不够三叉暂不建卡的 problem

| problem 候选 | 已有源 | 缺什么 | 状态 |
|-------------|--------|--------|------|
| 事件驱动异步 Agent vs 轮询调度 | src-001 ch4 | 需 ≥1 个外部工程实践源提供第 3 真分歧 | raw-only |
```

（如实际选了其他 problem，替换为实际内容。）

- [ ] **Step 4：验证 raw-only 问题确实不在 cards/ 中**

```bash
ls cards/
# 应只有 constraint-placement.md，没有事件驱动相关的卡
```

- [ ] **Step 5：Commit**

```bash
git add raw/sources.md
git commit -m "docs: mark event-driven-vs-polling as raw-only (single-source, <3 forks)"
git push origin main
```

---

### ✅ 流程验证检查点

- [ ] `cards/constraint-placement.md` 通过 `validate_card.py`
- [ ] 对抗审查清单 5/5 PASS
- [ ] `raw/sources.md` 含 ≥1 个 raw-only problem 标注
- [ ] 卡片零个人经验（人工确认）
- [ ] 全部已 commit + push

**流程验证完成。** 如果蒸馏过程中发现 SCHEMA 或模板需要微调，**此时修改**（Alpha 产出不是不可变的），然后进入 Phase 3。

---

## Phase 3：v0 完成（第 2 张正式卡）

### Task 12：读源材料并蒸馏第 2 张卡草稿

**Files:**
- Read: `E:\ai\ai-agent-book\book\chapter2.md` 或 `chapter3.md`
- Create: `drafts/context-loading-strategy.md`（gitignored）

**Problem：** Agent 上下文应常驻加载 / 按需 skill 加载 / 运行时压缩，如何选？

（这是与「约束放哪」不同的子问题，证明模板可复用 + 多对多映射。）

- [ ] **Step 1：读 chapter2.md（上下文工程）**

先用 `grep -n "KV Cache\|Skills\|上下文\|压缩\|窗口\|加载"` 定位相关小节，再精读。

重点寻找：
- KV Cache 与上下文窗口的关系
- Agent Skills 的按需加载机制
- 上下文压缩的时机和方法
- 常驻 vs 按需 vs 压缩三种策略的讨论

记录章节定位。

- [ ] **Step 2：如需第 3 叉，补充读 chapter3.md（记忆和知识库）**

chapter3 讨论 RAG 和外部知识库——这是「把信息放到上下文外」的第 4 种策略。如果 chapter2 只给出常驻 vs 按需两叉，chapter3 可以补充「外部化」作为第 3 或第 4 叉。

- [ ] **Step 3：识别 ≥3 真选项**

以下为**候选假设**，最终选项以 chapter2/chapter3 实际内容为准——如果某个候选在书中没有支撑，**必须替换为书中有支撑的其他选项**：

- **候选 A: 常驻上下文**——关键指令总是加载（系统提示/全局配置）
- **候选 B: 按需加载**——通过 Skills/工具/触发条件动态加载
- **候选 C: 运行时压缩**——上下文过长时动态压缩/摘要
- **候选 D: 外部化（RAG/知识库）**——不在上下文中放，按需检索

⚠️ **源适配原则**：以书的概念和术语为准。每个最终选项标注源章节定位。`source_ids` 为 `[src-001]`（同源不同章 = 同一 source_id）。

- [ ] **Step 4：按 templates/card.md 填草稿 → `drafts/context-loading-strategy.md`**

同样的零个人经验、源可追溯标准。

---

### Task 13：验证 + 对抗审查 + 过门

**Files:**
- Read: `drafts/context-loading-strategy.md`
- Create: `cards/context-loading-strategy.md`

- [ ] **Step 1：复制到 cards/ 并改 status**

```bash
cp drafts/context-loading-strategy.md cards/context-loading-strategy.md
```

编辑 `cards/context-loading-strategy.md`，将 `status: draft` 改为 `status: active`。

- [ ] **Step 2：运行验证脚本**

```bash
python scripts/validate_card.py cards/context-loading-strategy.md
```

Expected: `PASS: cards/context-loading-strategy.md`

- [ ] **Step 3：对抗审查清单（5 条全过）**

| # | 检查项 | 结果 |
|---|--------|------|
| 1 | 真三叉 | ☐ |
| 2 | 非摘要 | ☐ |
| 3 | 零个人经验 | ☐ |
| 4 | 源可追溯 | ☐ |
| 5 | problem 可复用 | ☐ |

- [ ] **Step 4：人工终审**

- [ ] **Step 5：验证两张卡覆盖不同子问题**

```bash
python scripts/validate_card.py --all
```

Expected:
```
PASS: cards/constraint-placement.md
PASS: cards/context-loading-strategy.md
```

确认两张卡的 `problem` 字段不同，且 `tags` 有差异（证明多对多 + 模板复用）。

- [ ] **Step 6：Commit**

```bash
git add cards/context-loading-strategy.md
git commit -m "card: context-loading-strategy — resident vs on-demand vs compress (src-001 ch2-3)"
git push origin main
```

---

### ✅ v0 完成检查点

- [ ] `cards/` 含 ≥2 张正式卡
- [ ] 两张卡 `validate_card.py --all` 全 PASS
- [ ] 两张卡覆盖不同子问题（problem 字段不同）
- [ ] 两张卡都通过对抗审查 5/5
- [ ] `raw/sources.md` 含 ≥1 个 raw-only 标注
- [ ] 卡片零个人经验
- [ ] `cards/` 全部 Public 可见（push 到 GitHub）
- [ ] `raw/excerpts/` 和 `drafts/` 被 .gitignore 排除（未泄露）

**v0 完成。**

---

## 后续里程碑（不在本计划范围）

| 里程碑 | 内容 | 前提 |
|--------|------|------|
| 首批可用库 | ≥5 张 harness 主域卡，覆盖 ≥3 个 problem 模式 | v0 完成 |
| 消费侧 skill | design-time 消费 skill，硬门禁接入 brainstorm | 用户自行构建 |
| 更多源 | 按混合门槛纳入工程文档、论文 | 单源不够三叉时补充 |
| 交叉引用 | 卡片间 `[[id]]` 链接 | 卡数够多时 |

---

## Self-Review（方案覆盖 + 审查修复记录）

### 第一轮：方案覆盖审查

逐条检查方案 `agent-kb方案.md` 的每个章节是否有对应 Task：

| 方案章节 | 对应 Task | 覆盖 |
|----------|-----------|------|
| §1 目标 | 全局目标行 | ✅ |
| §2.1 知识形态：决策卡 | Task 4 (SCHEMA) + Task 5 (模板) | ✅ |
| §2.2 仓库布局 | Task 1 (目录) + Task 2 (.gitignore) | ✅ |
| §2.3 目录职责 | Task 2 (.gitignore 区分公开/私有) | ✅ |
| §2.4 GitHub 仓库 | Task 1 (创建+clone) | ✅ |
| §3.1 字段定义 | Task 4 (SCHEMA) + Task 5 (模板) | ✅ |
| §3.2 字段约束 | Task 4 (SCHEMA 硬约束) + Task 7 (验证脚本) | ✅ |
| §3.3 源↔卡映射 | Task 10/13 (多源→1 卡，同源不同章) | ✅ |
| §4.1 蒸馏模式 | Task 9-10, 12-13 (人选题→Agent 草拟→审查→终审) | ✅ |
| §4.2 对抗审查清单 | Task 10 Step 3, Task 13 Step 3 (5 条清单) | ✅ |
| §4.3 门禁策略 | Task 10/13 (Agent 审查 + 人工终审) | ✅ |
| §5.1 冷启动全外部 | Task 9/12 (只读 ai-agent-book) | ✅ |
| §5.2 主题优先级 | Task 9 (ch1-2 harness) + Task 12 (ch2-3 harness) | ✅ |
| §5.3 混合门槛 | Task 11 (raw-only 验证) | ✅ |
| §5.4 raw 存储规范 | Task 4 (SCHEMA 摘录规范) + Task 2 (.gitignore) | ✅ |
| §5.5 蒸馏格式 | Task 8 (clone markdown 源码，不用 PDF/EPUB) | ✅ |
| §6 第一批源材料 | Task 6 (sources.md) + Task 8 (clone) | ✅ |
| §7 v0 里程碑 | Phase 1 (Alpha) + Phase 2 (流程验证) + Phase 3 (v0) | ✅ |
| §8 推迟项 | 「后续里程碑」表 | ✅ |

### 第二轮：审查发现并修复的问题

| # | 问题 | 严重度 | 修复 |
|---|------|--------|------|
| 1 | Task 6 `raw/sources.md` 占位段写「Phase 2 Task 10」，实际 raw-only 填写发生在 Task 11 | 中（交叉引用错误） | 已改为「Phase 2 Task 11」 |
| 2 | Task 9 Step 3 预设 4 个选项（Constitution/Skills/Hooks/Subagent），但 Hooks 是 Claude Code 特有概念，《深入理解 AI Agent》不一定讨论 | 高（源可追溯硬约束可能被违反） | 改为「候选假设」+「源适配原则」：以书实际内容为准，书中无支撑的候选必须替换 |
| 3 | Task 12 Step 3 同样的预设问题 | 高 | 同上修复 |
| 4 | Task 9/12 读源步骤粒度偏粗（「读 chapter1.md」不是 2-5 min 动作） | 低（内容任务固有限制） | 增加 `grep -n` 关键词定位步骤，先缩小范围再精读 |

**Placeholder scan:** 无 TBD/TODO。所有文件内容完整写出。

**Type consistency:** `validate_card.py` 检查的字段名与 SCHEMA.md 定义的字段名一致。模板 frontmatter 字段与 SCHEMA.md 一致。

**无遗漏。**
