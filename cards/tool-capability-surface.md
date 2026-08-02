---
id: tool-capability-surface
card_contract: development-agent-v1
card_type: composition-strategy
utility_status: unverified
consumer: development-agent
decision_scope: agent-runtime-architecture
option_relationship: layered
design_task_id: tool-and-action-architecture
design_goal: 让 Agent 通过可发现、可维护且受限的接口可靠采取行动。
required_artifact_types: [tool-capability-boundary, tool-schema, tool-discovery-policy]
failure_risks: [tool-call-failure, unsafe-capability-surface, undiscoverable-tool]
problem: 如何设计代码 Agent 的工具能力暴露、发现和执行接口，使能力可见、参数可验证且能随规模演进？
tags: [tools, aci, skills, discovery, mcp, permissions, idempotency]
when_to_use: Agent 需要搜索、读写、测试、发布或调用外部能力，并且工具数量、参数复杂度、变更频率或副作用正在影响可靠性时。
when_not: 只有一个内部确定性函数且不由模型选择，或动作还没有定义权限、参数和结果 schema 时。
status: active
source_ids: [src-001]
---

## Options

### Option A: 静态专用工具

为高价值或高风险能力提供参数明确的专用工具，稳定地把 schema 暴露给模型。适合参数结构复杂、权限敏感、需要精确审计或调用频率高的能力。

### Option B: Skill 加通用执行器

把领域方法、边界和示例放在按需加载的 Skill，把相对稳定的底层执行能力收敛到通用执行器。适合能力变化快、操作模式相似且可以用结构化参数约束执行的场景。

### Option C: 分层主动发现

先通过能力目录、服务端声明、关键词/向量检索或协议发现候选能力，再只把选中的工具 schema 动态加入当前轨迹。适合工具生态大、能力按项目变化或静态注入会超过上下文预算的场景。

## Tradeoffs

| | 优势 | 代价 |
|---|---|---|
| A 静态专用 | 参数和权限边界清楚，调用与审计容易，适合高风险动作 | 工具数量增长会膨胀上下文，新增能力需要维护 schema 和路由 |
| B Skill/通用 | 规则可复用、按需加载，底层执行器减少重复接口 | 依赖模型正确触发 Skill，通用执行器若过宽会扩大副作用面 |
| C 主动发现 | 能扩展到大规模或远程能力生态，减少静态 schema 负担 | 发现、排序、版本、信任边界和动态 schema 注入增加延迟与失败点 |

## Apply to Agent Development

- 先记录能力的参数复杂度、变更频率、调用频率、权限/副作用、延迟和恢复成本；工具粒度是输入，不要与能力暴露路径混为一谈。
- 复杂参数、敏感权限、不可逆动作和需要逐次审计的能力优先 A；同类操作可由统一 schema 表达、规则需要按任务加载时选 B；能力数量大、远程或动态变化显著时加 C。
- A/B 是执行接口的基础选择，C 是发现和注入层；可以用 C 发现 A 或 B，但每次动态注入都要保留版本、来源和权限边界。
- 无论路径如何选择，描述必须写清何时使用、不能做什么、参数/返回格式、延迟和失败；执行侧必须校验结构化参数，不能静默转换或让自由文本绕过权限。

## Development Agent Procedure

### Trigger

当新增或重构 Coding Agent 的搜索、读写、测试、发布、外部 API 或协作能力，且需要决定接口形状、发现方式和副作用控制时读取本卡。

### Decision Inputs

建立能力清单，记录参数复杂度、调用频率、变更频率、工具数量、发现延迟、权限与副作用、可逆性、幂等性、超时/部分成功行为、审计要求和模型可见范围。

### Option Relationship

A、B 是执行能力的两种基础暴露方式，C 是可叠加的发现层，不是把所有能力做成一个无限通用命令。高风险能力可用 C 发现，但最终应落到参数受限的 A 或受约束的 B 执行接口。

### Selection Rules

- 参数复杂或权限敏感、动作不可逆或需要稳定审计时选 A。
- 操作模式相似、底层执行能力稳定且领域规则适合按需加载时选 B，并限制通用执行器的 schema 和权限。
- 工具规模、远程能力或变更频率使静态 schema 不可维护时加 C，建立目录/服务端声明、检索、版本和动态注入策略。
- 只要参数不能被程序校验、拒绝路径没有状态记录或重复请求会产生未知副作用，就先收紧接口，不发布更宽的通用能力。

### Required Artifacts

交付能力边界清单、工具 schema 与示例、工具粒度和权限/副作用矩阵、Skill 或目录的触发/发现规则、版本与信任边界、超时/幂等/部分成功/恢复协议，以及允许、拒绝、重复和发现失败测试。

### Verification

- 用正确、缺失、越权、类型错误和边界参数验证 schema 与执行侧拒绝一致。
- 演练工具未发现、版本不匹配、超时、重复到达和部分成功，确认状态可审计且不会产生未预期的重复副作用。
- 对动态发现检查候选排序、schema 来源/版本/权限和上下文预算；对高风险能力检查预览、审批、自动验证或沙箱门。
- 比较专用接口、通用执行器和主动发现的延迟、调用正确率、维护成本和失败恢复，而不是只比较一次成功调用。

## Anti-Patterns

- 用一个无限能力的 shell 或通用命令接口承担所有文件、发布和外部通信动作。
- 只靠工具描述或 Skill 文本禁止越权，不在执行侧校验参数和权限。
- 静态注入全部工具 schema，导致模型看不到真正相关能力和上下文预算失控。
- 动态发现返回没有版本、来源、权限和失效状态的 schema。
- 静默修改模型参数、路径或默认值，使模型以为执行了一个动作而工具实际执行了另一个动作。

## Sources

- [src-001] chapter4.md §能力表达形式的选择：专用工具还是 Skill + 通用执行器；§工具粒度的权衡；§工具描述的艺术；§参数传递的保真性。
- [src-001] chapter4.md §工具执行的安全：从输入校验到沙箱隔离；§主动工具发现；§工具生态：MCP 与工具选择的挑战。
