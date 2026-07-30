# agent-kb：AI Agent 设计知识库方案

> 本文档是 grill-me 会话 `netagent-agent-capability`（22 问全部锁定）的设计产出。
> 实施计划见同目录 `agent-kb计划.md`。

## 1. 目标

**提升编程智能体（Claude Code / Codex）在设计阶段的设计上限。**

不是让它少犯错、少返工，而是让它在设计/brainstorm 时能**发明更好、更合适的方案**——看到更多的真选项分叉。

手段：建立一个**外部经典知识库**，在设计时被编程 agent 消费，提供经过蒸馏的决策卡（decision cards），而非原始全文。

### 适用范围
- 服务于**开发各种 AI Agent 项目**的编程智能体，不限于 NetAgent。
- NetAgent 是消费者，不是知识库的唯一服务对象。

## 2. 核心架构

### 2.1 知识形态：策展决策卡

知识库的面不是原始论文全文，而是**策展决策卡（curated decision cards）**。

决策卡 = 一个可反复遇到的设计问题 + ≥3 个真选项 + tradeoffs + 应用规则 + 来源。

**蒸馏 ≠ 摘要。** 蒸馏是把原始材料重构为决策单元；摘要是压缩原文。两者本质不同。

### 2.2 仓库布局

```
agent-kb/
├── README.md              # 项目说明 + 使用指引
├── SCHEMA.md              # 卡片 schema + 摘录规范 + 门禁清单
├── templates/
│   └── card.md            # 空白卡片模板
├── raw/
│   ├── sources.md         # 必读源清单（标题/作者/URL/许可/入选理由）
│   └── excerpts/          # 短摘录（gitignored，fair-use，不进公开仓库）
├── drafts/                # 未过门的草稿卡（gitignored）
├── cards/                 # 已过门的正式卡（公开）
│   └── *.md
└── .gitignore
```

### 2.3 目录职责

| 目录 | 内容 | 公开 |
|------|------|------|
| `cards/` | 通过全链路门禁的正式决策卡 | ✅ Public |
| `raw/sources.md` | 必读源索引（标题/作者/URL/DOI/许可/入选理由/关联 problem 候选） | ✅ Public |
| `raw/excerpts/` | 短摘录（fair-use 段落 + 精确定位：章节/小节/行号） | ❌ gitignored |
| `drafts/` | Agent 草拟、尚未过门的卡片 | ❌ gitignored |

### 2.4 GitHub 仓库

- **仓库名**：`agent-kb`
- **可见性**：Public
- **本地 clone**：`E:\ai\agent-kb`
- **访问方式**：设计时读本地文件；可选 `git pull` 更新

## 3. 卡片 Schema

### 3.1 字段定义

```markdown
---
id: <kebab-case-slug>              # 唯一标识，全库唯一
problem: <一句话设计决策问题>        # 卡的主键——可反复遇到的设计问题
tags: [harness, constitution, ...]  # 主题标签（不做深目录）
when_to_use: <什么场景下会遇到>      # 元数据
when_not: <什么场景不适用>           # 元数据
status: draft | active | deprecated # 生命周期
source_ids: [src-001, src-002]      # 关联 raw/sources.md 中的源 ID
---

## Options (≥3)

### Option A: <名称>
<描述：这个选项是什么、怎么做>

### Option B: <名称>
<描述>

### Option C: <名称>
<描述>

<!-- 可以有 D、E...，但最少 3 个 -->

## Tradeoffs

| | 优势 | 代价 |
|---|---|---|
| A | ... | ... |
| B | ... | ... |
| C | ... | ... |

## Apply to Agent Development

<外部可推导的通用决策规则。
 禁止写个人项目经历。
 内容须能回溯到 sources。
 示例：「若约束必须 fail-closed 且不可被模型省略 → 优先 hooks；若按任务加载 → skills」>

## Anti-Patterns

<源中或逻辑可证的反模式。
 同样禁止个人经验。
 示例：「把所有约束堆进 constitution → 上下文膨胀，模型遵守率下降」>

## Sources

- [src-001] 《书名》作者 — Chapter X, §Y.Z（markdown 定位，非 PDF 页码）
- [src-002] URL — Section "..."
```

### 3.2 字段约束

| 字段 | 硬约束 |
|------|--------|
| `problem` | 可反复遇到的设计决策问题，不绑定单篇文章 |
| `options` | **≥3 个真分歧**（不是同一方案的变体） |
| `apply_to_agent_dev` | **只写外部可推导规则**，禁止个人项目经验 |
| `anti_patterns` | 同上，源中或逻辑可证 |
| `sources` | 每条选项/tradeoff/rule 须可追溯到至少一个源 |
| `source_ids` | 与 `raw/sources.md` 中的 ID 对应 |

### 3.3 源↔卡映射

**多对多，problem 为卡主键。**

- 1 个源 → 0/1/N 张卡
- N 个源 → 1 张卡（合并）
- 优先合并/更新已有卡，不默认「一源一卡」

## 4. 蒸馏管线

```
人选源 + 选问题
       ↓
Agent 按 SCHEMA 草拟 → drafts/
       ↓
Agent 对抗审查（清单驱动）
       ↓
人工终审（放行 / 驳回 / 修改）
       ↓
cards/ 正式卡
```

### 4.1 蒸馏模式

**人工主导 + Agent 填草稿 + 门禁把关：**

1. **人**选定源材料 + 选定 problem
2. **Agent** 按模板填充草稿 → `drafts/`
3. **Agent 对抗审查**（按下文清单）
4. **人**做最终终审 → 放行进 `cards/` 或驳回

### 4.2 对抗审查清单

草稿进 `cards/` 前，Agent 必须逐条自检：

| # | 检查项 | 通过标准 |
|---|--------|----------|
| 1 | **真三叉** | options ≥3 且是真正不同的方案路径，不是同一方案的变体 |
| 2 | **非摘要** | 这是决策单元（problem + options + tradeoffs），不是文章/书籍摘要 |
| 3 | **零个人经验** | 所有字段（尤其 `apply_to_agent_dev`、`anti_patterns`）不含个人项目经历 |
| 4 | **源可追溯** | 每个选项、tradeoff、应用规则都能回溯到 `sources` 中的具体源 |
| 5 | **problem 可复用** | problem 是可反复遇到的设计问题，不绑定某一篇文章 |

### 4.3 门禁策略

**Agent 对抗审查 + 人工终审。** 不全自动，不只靠人。

## 5. 内容策略

### 5.1 冷启动内容

**全部外部经典**。个人经验不写入卡片。

内容来源：
- 书籍：《深入理解 AI Agent：设计原理与工程实践》（李博杰 著，Apache 2.0，markdown 源码在 `bojieli/ai-agent-book`）
- 公开工程文档：Claude Code / Agent SDK 官方文档、开源 agent 项目
- 经典论文/算法：仅用于补充选项分叉，不当主料

### 5.2 主题优先级

**A 主：harness / 运行时工程**
- constitution（CLAUDE.md / AGENTS.md 类）
- skills / 工具
- hooks / 权限门禁
- subagents / 编排
- eval / 验证
- memory 形态

**B 辅：经典 agent 算法 / 论文**
- ReAct / Plan-then-Execute / 多 agent 编排
- 仅在 harness 主域选项不够三叉时补充
- 不把知识库变成论文笔记

### 5.3 入选门槛（混合门槛）

两道关同时跑：

1. **必读源清单**：只有被公认为高影响力的源才进 `raw/sources.md`
2. **问题驱动建卡**：只有当一个 problem 能从清单内源抽出 ≥3 真分歧时才建卡；单源不够三叉的只进 `raw/`，不进 `cards/`

### 5.4 raw/ 存储规范

- **只存索引 + 短摘录**，不存全文
- 摘录带精确来源定位（章节/小节/行号，非 PDF 页码）
- 摘录长度有上限（写进 SCHEMA.md）
- `raw/excerpts/` 通过 `.gitignore` 不进公开仓库（fair-use 保护）

### 5.5 蒸馏源材料格式

| 格式 | 蒸馏优先级 | 原因 |
|------|-----------|------|
| **markdown 源码** | ✅ 首选 | Agent 直接 Read，精确、完整、结构化 |
| GitHub 网页 | ✅ 可用 | WebFetch/webReader 提取 |
| PDF | ⚠️ 备选 | 结构/表格/代码块易丢 |
| EPUB | ❌ 不用 | 需解压解析，Agent 不能直接读 |

对于《深入理解 AI Agent》一书：**使用 `book/chapter*.md` markdown 源码蒸馏**，不用 PDF/EPUB。

## 6. 第一批源材料

### 已确认

| 源 | 许可 | 格式 | 覆盖章节 |
|----|------|------|----------|
| 《深入理解 AI Agent：设计原理与工程实践》李博杰 | Apache 2.0 | markdown（GitHub `bojieli/ai-agent-book`） | 10 章，覆盖 harness 全主域 |

### 章节→problem 映射

| 章 | 主题 | 候选 problem |
|----|------|-------------|
| 1 | Agent 基础 + Harness 工程是竞争力 | 约束放哪（constitution/hooks/skills/subagent） |
| 2 | 上下文工程（KV Cache、Agent Skills、压缩） | 上下文加载策略 / skills 组织 |
| 3 | 用户记忆和知识库（RAG、知识图谱） | 记忆形态选择 |
| 4 | 工具（MCP 协议、主动发现） | 工具协议选择 |
| 5 | Coding Agent 与代码生成 | 直接服务目标 |
| 6 | Agent 评估 | 验证策略选择 |

## 7. v0 里程碑

### 完成标准（分阶段打卡）

| 阶段 | 交付物 | 状态 |
|------|--------|------|
| **Alpha** | 骨架就绪：仓库创建 + clone + README + SCHEMA + 模板 + .gitignore + `raw/sources.md` 必读清单 | 待做 |
| **流程验证** | 第 1 张正式卡走完全链路（源→草稿→对抗+人工门→`cards/`）+ ≥1 个 problem 因单源不够三叉只进 `raw/` | 待做 |
| **v0 完成** | 第 2 张正式卡（不同子问题）走完全链路，证明多对多映射与模板可复用 | 待做 |

### 不在 v0 范围

- 消费侧 skill（用户之后单独做）
- ≥5 张卡的「首批可用库」（属于后续里程碑）
- 个人经验入卡（永久不做）

## 8. 推迟项

| 项目 | 状态 | 说明 |
|------|------|------|
| 消费侧 design-time skill | 方向 A 已定，实施推迟 | 用户之后自行构建；grill 中不展开 |
| 更多书籍/论文源 | 后续按混合门槛 C 纳入 | v0 先用已确认源 |
| 卡片间的交叉引用图谱 | 后续 | v0 先验证单卡闭环 |
