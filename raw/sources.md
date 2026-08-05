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
| 本地材料包 | `raw/src-001-ai-agent-book/`（gitignored） |
| 主蒸馏路径 | `raw/src-001-ai-agent-book/source/ai-agent-book/book/` |
| 辅助材料 | `raw/src-001-ai-agent-book/source/AI-Agents-in-Depth-zh-CN (1).pdf`（仅核对，不作主蒸馏源） |
| 入选理由 | 10 章覆盖 Agent 全链路（harness/上下文/记忆/工具/Coding Agent/评估/训练/进化/多模态/多 Agent），94 个配套实验，核心公式 Agent = LLM + 上下文 + 工具 |

#### 章节-设计责任证据覆盖

章节只提供证据，不能直接决定卡片或 problem。正式卡从 `DECISION-MAP.md` 的一级开发责任与跨章节证据中发现。

| 章 | markdown 文件 | 主要证据覆盖的设计责任 |
|----|--------------|------------------------|
| 1 | `chapter1.md` | 安全与人工控制；目标与任务执行 |
| 2 | `chapter2.md` | 上下文与状态；工具与行动 |
| 3 | `chapter3.md` | 知识与记忆；上下文与状态 |
| 4 | `chapter4.md` | 工具与行动；目标与任务执行 |
| 5 | `chapter5.md` | 上下文与状态 |
| 6 | `chapter6.md` | 评估与可观测性 |
| 7 | `chapter7.md` | 当前范围外（模型后训练） |
| 8 | `chapter8.md` | 持续改进与协作 |
| 9 | `chapter9.md` | 当前范围外（多模态与机器人） |
| 10 | `chapter10.md` | 持续改进与协作 |

#### 全书覆盖盘点

| 章 | 处理状态 | 结果 |
|----|----------|------|
| 1 | completed | `constraint-placement` 已覆盖；`workflow-autonomy-strategy` 跨章发布，覆盖工作流 / 自主 / 混合编排 |
| 2 | completed | `context-loading-strategy` 已覆盖；Skills 和主动发现为 `tool-capability-surface` 提供能力暴露证据 |
| 3 | completed | 发布 `knowledge-retrieval-strategy` |
| 4 | completed | 发布 `tool-capability-surface`；长时间任务调度仍因不足三叉保持 raw-only |
| 5 | completed | Coding Agent 会话状态与恢复缺少三叉比较，保持 raw-only |
| 6 | completed | 发布 `agent-evaluation-environment` |
| 7 | completed | 后训练主要属于模型训练，不纳入当前运行时 Agent 卡片范围 |
| 8 | completed | 发布 `experience-encoding` |
| 9 | completed | 多模态、GUI 与机器人控制超出当前编程 Agent 主域 |
| 10 | completed | 发布 `multi-agent-coordination` |

`src-001` 的完整本地证据台账、决策地图对齐、地图变更提议、既有卡重审、候选队列、进度和蒸馏报告位于 `raw/src-001-ai-agent-book/derived/`，由 `.gitignore` 排除。

### src-002：Temporal Documentation 完整仓库快照

| 字段 | 值 |
|------|-----|
| 组织 | Temporal Technologies |
| URL | https://github.com/temporalio/documentation |
| 许可 | MIT License |
| 格式 | 固定 Git commit 的完整 GitHub repository 快照（文档、示例、实现、测试、工具与配置） |
| 本地材料包 | `raw/src-002-temporal-documentation/`（gitignored） |
| 主蒸馏路径 | 人工策展的 `source/docs/` 重要材料清单，见材料包 `derived/selected-materials.md`；完整快照仅作溯源与按需交叉核对 |
| 工程证据路径 | 完整快照中的 `source/sample-apps/`、`source/src/`、`source/plugins/`、`source/tests/`、`source/fixtures/`、`source/scripts/`、`source/bin/`、`source/.github/`、`source/vale/` 保留作溯源，不构成本 run 的独立蒸馏边界 |
| 资产与元数据 | `source/static/`、`source/visuals/`、根目录配置与锁文件；二进制/生成文件只作库存和交叉核对，不独立支撑文本结论 |
| 快照 | `cca0ebdd7d801c8a2f8ac8751d37b2a202a61aa8` |
| 入选理由 | 作为完整工程参考源，覆盖 Temporal 文档、代码示例、实现、测试、信息架构和维护约束；蒸馏时按开发责任筛选可复用设计决策，不把章节或仓库目录直接当作卡片。 |

该源在固定提交上保留完整 1,565 个跟踪文件。依照人工确认的“只蒸馏重要文件”边界，本 run 的完整阅读边界是 `BND-004` 中列出的 35 篇人类编写文档；1,426 个可读文件和 139 个二进制或生成文件仍保留作库存、溯源和交叉核对，不自动构成卡片证据。逐文件哈希、profile、边界和状态位于 `raw/src-002-temporal-documentation/derived/`，由 `.gitignore` 排除。

---

## 已由后续源解除的 raw-only 候选

| problem 候选 | 新增证据 | 当前状态 |
|-------------|----------|----------|
| 长时间任务与外部事件的调度架构：事件驱动异步 / 同步请求-响应 / 时间驱动调度 | src-002 的 BND-004 以 Signals、Updates 和 Schedules 分别提供三种可区分的任务准入机制与操作语义 | 已发布为 `durable-task-admission-strategy` |
