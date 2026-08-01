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
| `card_contract` | string | 是 | `decision-card-v0`（迁移期）或 `development-agent-v1`（开发 Agent 可执行卡） |
| `consumer` | string | v1 必填 | 固定为 `development-agent` |
| `decision_scope` | string | v1 必填 | `agent-runtime-architecture` / `knowledge-retrieval` / `evaluation` / `continuous-improvement` / `multi-agent-topology` |
| `option_relationship` | string | v1 必填 | `exclusive` / `composable` / `layered` / `sequential` / `composable-by-information-type` |
| `design_task_id` | string | v1 必填 | `DECISION-MAP.md` 中状态为 `core` 的一级开发责任 ID |
| `design_goal` | string | v1 必填 | 必须逐字匹配所绑定一级任务的 `design_goal` |
| `required_artifact_types` | string[] | v1 必填 | 至少一个；必须属于该一级任务允许的工件类型 |
| `failure_risks` | string[] | v1 必填 | 至少一个；必须属于该一级任务允许的失败风险 |

## 正文章节

| 章节 | 必填 | 硬约束 |
|------|------|--------|
| **Options** | 是 | ≥3 个真分歧选项；每个选项有名称和描述 |
| **Tradeoffs** | 是 | 每个选项的优势与代价 |
| **Apply to Agent Development** | 是 | 外部可推导的通用决策规则；禁止个人项目经验 |
| **Development Agent Procedure** | v1 必填 | Trigger、Decision Inputs、Option Relationship、Selection Rules、Required Artifacts、Verification 六项齐全且非空 |
| **Anti-Patterns** | 是 | 源中或逻辑可证的反模式；禁止个人经验 |
| **Sources** | 是 | 每条含源 ID + 源原生稳定定位（Markdown 标题优先；其他格式用可复核页码、锚点或文件位置） |

## 硬约束

1. **≥3 真选项**：不是同一方案的变体，是真正不同的设计路径
2. **零个人经验**：所有字段不含个人项目经历（项目名、踩坑记录等）
3. **源可追溯**：每个选项、tradeoff、应用规则都能回溯到 sources
4. **problem 可复用**：是设计问题模板，不是文章读后感

## 开发 Agent 消费契约

- `decision-card-v0` 是迁移期卡片：保留有效的设计知识，但尚未声明可直接指导开发 Agent 完成设计交付。
- `development-agent-v1` 是供 Codex、Claude Code 等编程 Agent 使用的执行型决策卡。它必须具有 consumer 元数据、选项关系和完整的 Development Agent Procedure。
- `option_relationship` 不允许默认省略。它说明同一张卡中的选项是互斥、可组合、分层、顺序执行，或按信息类型组合。
- `design_task_id` 将卡片绑定到开发 Agent 的一级设计责任；来源章节、论文段落或项目目录不能替代此绑定。
- `design_goal`、`required_artifact_types` 和 `failure_risks` 让卡片明确其架构交付和不做决策时的独立风险；验证器拒绝与 `DECISION-MAP.md` 不一致的值。
- v1 卡的 Procedure 必须使 Agent 能识别触发、收集输入、选择方案、交付工件并验证设计；它不替代 Options 或 Tradeoffs。

## 决策地图

`DECISION-MAP.md` 是公开的一级开发责任 registry。每个 `## <task-id>` 条目使用扁平字段，包含 `status`、`design_goal`、允许的 `required_artifacts` / `failure_risks`、子问题和 coverage。任务状态为 `core`、`emerging` 或 `excluded`；正式 v1 卡只能绑定 `core`。

- `covered`：至少有一张正式卡。
- `partial`：至少有一张正式卡和一项明确的 raw-only 缺口。
- `no-published-card`：尚无正式卡，且必须记录补证需求。

一级任务由开发 Agent 的独立设计责任定义，而非某份来源的章节或技术主题。新增、拆分、合并或排除一级任务必须在来源本地档案中说明独立工件、失败风险、候选子问题和不能归入现有任务的原因。

### Development Agent Procedure

| 小节 | Agent 必须获得的内容 |
|---|---|
| Trigger | 何种项目任务或设计信号要求读取本卡 |
| Decision Inputs | 选择前必须调查的事实与约束 |
| Option Relationship | 选项之间的互斥、组合、层级或顺序关系 |
| Selection Rules | 根据输入选择某个选项或组合的条件 |
| Required Artifacts | 必须产出的架构、配置、接口、测试或设计记录 |
| Verification | 检验选择有效并防止相应风险的动作 |

## 对抗审查清单（草稿进 cards/ 前必检）

| # | 检查项 | 通过标准 |
|---|--------|----------|
| 1 | 真三叉 | options ≥3 且是不同方案路径 |
| 2 | 非摘要 | 是决策单元，不是文章摘要 |
| 3 | 零个人经验 | 无任何个人项目经历 |
| 4 | 源可追溯 | 每条内容可回溯到 sources |
| 5 | problem 可复用 | 可反复遇到的设计问题 |

## 本地蒸馏档案

- `drafts/<source_id>/`：永久保留的来源级候选档案，不进入公开仓库。每个候选必须有一份草稿和一份 `.evidence.md` sidecar。
- 草稿 frontmatter 必须包含 `source_id`、`candidate_id` 和生命周期状态：`draft`、`published`、`raw-only`、`out-of-scope` 或 `rejected`。
- `published` 必须有 `published_card`，且目标正式卡 `status: active`；其他状态必须记录 `decision_reason`，且不得设置 `published_card`。
- 草稿不会因发布或拒绝而删除；正式卡只存在于公开的 `cards/`。

## raw/ 原材料与摘录规范

- `raw/sources.md`：公开，必读源索引
- `raw/src-NNN-<source-slug>/`：每个来源的本地材料包，由 `.gitignore` 排除
- `raw/src-NNN-<source-slug>/source/`：不修改的上游原始材料；项目、配套文件、PDF 或文档属于同一来源时放在同一个材料包中
- `raw/src-NNN-<source-slug>/derived/`：Agent 生成的材料画像、提取文本、证据台账、候选问题、进度和蒸馏报告
- `raw/src-NNN-<source-slug>/excerpts/`：该来源的 fair-use 短摘录和定位笔记
- 摘录长度上限：单条不超过 500 字，单源摘录总计不超过 2000 字
- 每条摘录必须标注精确来源定位（优先 Markdown 章节 / 小节；其他格式使用源原生稳定定位）
- `excerpts/` 不复制来源全文、整书 PDF 或 EPUB；原始材料可原样保留在同一材料包的 `source/` 中，但材料包不进入公开仓库

## 源材料格式优先级

1. markdown 源码（首选）
2. GitHub 网页（可用）
3. PDF（备选）
4. EPUB（不用）
