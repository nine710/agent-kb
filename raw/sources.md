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
| 本地路径 | `ai-agent-book/book/` |
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
