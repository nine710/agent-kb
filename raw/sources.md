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

### src-002（待补充）

公开工程文档（Claude Code / Agent SDK 官方文档等）。在蒸馏卡片时如需补充第 3 真分歧再纳入。

---

## 因单源不够三叉暂不建卡的 problem

| problem 候选 | 已有源 | 缺什么 | 状态 |
|-------------|--------|--------|------|
| 长时间任务与外部事件的调度架构：事件驱动异步 / 同步请求-响应 / 定时轮询·批处理 / 混合监督 | src-001 chapter4（§事件驱动的异步 Agent 深度展开事件驱动方案 L334–595；§工具生态>MCP 的局限性 以请求-响应式为对照 L124） | ch4 把事件驱动作为既定方案深入工程实现，未把"定时轮询/批处理调度""混合事件+轮询监督"作为可比较的独立设计路径展开。需 ≥1 个外部工程实践源（如运维型 Agent 的轮询/批处理实践、不同调度架构的对比）提供第 3 真分歧 | raw-only |
