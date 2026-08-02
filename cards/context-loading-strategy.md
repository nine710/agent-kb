---
id: context-loading-strategy
card_contract: development-agent-v1
card_type: composition-strategy
utility_status: unverified
consumer: development-agent
decision_scope: agent-runtime-architecture
option_relationship: composable-by-information-type
design_task_id: context-and-state-architecture
design_goal: 让 Agent 在任务全过程获得正确、足够、可恢复的信息。
required_artifact_types: [context-layering-table]
failure_risks: [context-corruption]
problem: 如何为代码 Agent 的每类信息选择常驻、按需加载、轨迹压缩或外部隔离，并保持上下文预算、缓存稳定性和信息可恢复性？
tags: [context-engineering, prompt-cache, skills, compression, isolation]
when_to_use: 设计或审查代码 Agent 的 system prompt、项目规则、工具输出、Skill、子 Agent 结果和长期知识如何进入或离开主上下文时。
when_not: 需要决定完整的跨会话检查点或任务队列状态机时；该卡只决定信息承载方式，不替代长期状态恢复协议。
status: active
source_ids: [src-001]
---

## Options

### Option A: 常驻静态前缀

把稳定、全场景都需要的信息放入 system prompt 和稳定的工具定义，并在每轮请求中保持前缀不变。适合身份、核心规则和稳定能力边界；动态时间、计数、余额、当前任务状态不应放入这一层。

### Option B: 按需加载（渐进式披露）

只把 Skill 或工具的名称和描述放入稳定前缀，完整规则、领域知识或工具 schema 在 Agent 判断需要时加载。适合按项目、任务或领域变化的信息，加载规则本身必须能被模型路由和审查。

### Option C: 运行时压缩

让已经进入轨迹的工具结果或历史记录在接近预算阈值时批量压缩，以降低长度和提高信息密度。压缩只处理可替换的轨迹内容，不能改写 system prompt、工具定义、架构决策、约束理由、失败路径或精确标识符。

### Option D: 外部隔离

让大规模仓库探索、长期知识或 bulk 工具输出不进入主 Agent 上下文：交给隔离的子 Agent，或放在可检索的外部存储，只返回结论、必要片段和来源定位。外部化优先于把 bulk 先塞入主上下文再压缩。

## Tradeoffs

| | 优势 | 代价 |
|---|---|---|
| A 常驻 | 指令位置稳定，缓存命中和全场景一致性最好 | 前缀膨胀会稀释注意力；任何动态值或重排都会破坏缓存 |
| B 按需 | 只加载相关能力，规则可模块化、版本化和复用 | 依赖路由描述质量，多一次加载往返，加载后的中间位置指令需验证 |
| C 压缩 | 控制轨迹长度并提高信息密度，摘要可被审查 | 有损且需要额外调用；容易丢失早期决策、失败路径和标识符 |
| D 隔离 | bulk 不占主上下文，可承载远超窗口的探索和长期知识 | 子 Agent 需要自包含输入；检索精度、时效、冲突和返回协议成为新风险 |

## Apply to Agent Development

- 先为每类信息填写稳定性、使用频率、增长速度、是否跨会话、预算、标识符精度和是否会产生 bulk 输出，再选择承载方式。
- 身份、核心规则和固定工具定义使用 A；项目或任务特定规则使用 B；已经进入轨迹且仍需保留的工具结果使用 C；大规模探索和长期知识使用 D。
- 动态状态不进入 A。把它放在请求末尾的状态区，或通过工具实时读取。
- 能不进入主上下文的信息优先采用 D；C 是已经进入轨迹后的有损管理手段，不是 bulk 隔离的替代品。
- 压缩时直接删除噪声，保留架构决策、约束理由、失败路径、hash、UUID、URL 和文件定位。

## Development Agent Procedure

### Trigger

当代码 Agent 需要决定规则、项目知识、工具轨迹、子 Agent 结果或长期知识的承载位置，且上下文预算、缓存或信息丢失会影响任务可靠性时读取本卡。

### Decision Inputs

建立信息清单，记录每类信息的稳定性、每轮使用频率、增长速度、跨会话要求、预算、时效/冲突风险、精确标识符要求、是否产生 bulk 输出，以及静态前缀是否要求字节稳定。

### Option Relationship

A、B、C、D 按信息类型组合，不是整个 Agent 的单选题。A 负责稳定前缀，B 负责场景化加载，C 负责已进入轨迹的压缩，D 负责隔离 bulk 或长期知识。D 优先于 C：能不进入主上下文的信息不应先进入后再压缩。

### Selection Rules

- 稳定、全场景、每轮都需要的信息选 A，并禁止注入动态字段。
- 按项目、任务或领域触发的信息选 B，并写清加载条件和反例。
- 已进入本会话、持续增长但仍需保留的信息选 C，在预算接近阈值时批量压缩。
- 大规模仓库探索、长期知识或 bulk 工具结果选 D，并规定隔离任务的自包含输入和返回格式。

### Required Artifacts

交付上下文分层表，逐项列出信息类别、承载方式、加载条件、预算、来源/时效和所有者；同时列出静态前缀允许与禁止字段、压缩保留字段，以及子 Agent 或检索层的返回格式。

### Verification

- 对多轮请求比较静态前缀快照，确认时间戳、余额、计数和动态工具排序不会进入前缀。
- 用长工具输出和大范围仓库探索检查预算，确认 bulk 通过 D 隔离而非永久占据轨迹。
- 对压缩前后记录断言架构决策、约束理由、失败路径和 hash/UUID/URL 未丢失或改写。
- 对按需加载和外部返回检查来源定位、时效、冲突状态和返回 schema。

## Anti-Patterns

- 把偶尔使用的项目知识每轮常驻，导致上下文腐化。
- 在 system prompt 注入时间戳、余额、计数或动态工具重排。
- 每轮压缩或对噪声做摘要，而不是接近阈值批量处理并直接删除噪声。
- 让主 Agent 亲自读取大量文件，再依靠压缩补救 bulk 污染。
- 压缩时丢失架构决策、失败路径或精确标识符。
- RAG 或外部返回不保留来源、版本和冲突状态。

## Sources

- [src-001] chapter2.md §从 API 视角看上下文的构成；§KV Cache 友好的上下文设计；§动态提示词与 Agent Skills；§工具定义的设计；§上下文压缩策略；§隔离优于压缩：子 Agent 上下文隔离。
- [src-001] chapter3.md §用户记忆系统；§记忆的层次结构；§RAG 基础：构建 Agent 的知识获取管道；§知识库的时效与治理。
