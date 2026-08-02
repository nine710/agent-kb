---
id: multi-agent-coordination
card_contract: development-agent-v1
card_type: atomic-decision
utility_status: unverified
consumer: development-agent
decision_scope: multi-agent-topology
option_relationship: exclusive
design_task_id: continuous-improvement-and-collaboration-architecture
design_goal: 让 Agent 在可验证、可回滚的条件下沉淀经验并协调多方工作。
required_artifact_types: [coordination-topology, rollback-policy]
failure_risks: [coordination-error-cascade, unverified-capability-regression]
problem: 如何为需要分工的代码 Agent 选择管理者、对等协作或去中心化移交，并把控制权、任务状态、共享工件和失败恢复写成可验证协议？
tags: [multi-agent, subagents, coordination, topology, handoff, ownership]
when_to_use: 单 Agent 已不足以完成分工、独立审查、结果汇总或跨专长移交，且必须明确控制权、信息流和工件所有权时。
when_not: 单 Agent 在有限上下文和工具范围内已能可靠完成任务，拆分只会增加通信和协调成本时。
status: active
source_ids: [src-001]
---

## Options

### Option A: 管理者模式

由管理者 Agent 分解任务、分派执行者、分配资源、验证关键中间结果并汇总最终结果。它把全局优先级、控制流和最终责任集中在一个协调节点。

### Option B: 对等协作

多个 Agent 直接相互审查、协商和迭代，不预设唯一控制中心。它把制衡、质疑和改进分散到协作成员之间，但必须显式规定终止和冲突裁决。

### Option C: 去中心化移交

Agent 根据能力、任务状态或协议把控制权直接移交给下一位协作者。所有权随任务状态流动，而不是长期固定在管理者或对等群体中；移交必须携带最小可恢复状态。

## Tradeoffs

| | 优势 | 代价 |
|---|---|---|
| A 管理者 | 全局调度、资源分配和最终汇总责任明确 | 管理者是瓶颈或单点错误来源，错误可能向下游级联 |
| B 对等 | 适合独立质疑、交叉审查和迭代改进，减少单一判断偏差 | 协商、一致性、终止和裁决成本更高 |
| C 去中心化移交 | 控制权随能力和状态流动，避免长期中心依赖 | 路由、所有权、可观测性和失败恢复复杂，协议质量决定可靠性 |

## Apply to Agent Development

- 先证明单 Agent 的能力或可验证性不足，并确认协作会引入新信息或外部反馈，再选择协作拓扑；多 Agent 数量不是架构目标。
- 有统一计划、资源约束和最终汇总责任时选 A，并要求管理者验证关键中间结果。
- 主要价值来自独立审查、相互质疑和迭代改进时选 B，预先规定终止、轮次上限和冲突裁决。
- 任务会按专长或状态动态流转时选 C，定义所有权、最小移交状态、超时和失败回退。
- 控制拓扑与通信方式是两条独立轴；任何拓扑都可以通过共享上下文、文件或消息通信。
- 共享工件必须有写入所有权、版本或串行化规则，否则协作会放大并发覆盖和错误级联。

## Development Agent Procedure

### Trigger

当任务需要分工、独立审查、汇总或跨专长移交，并且控制权、工件所有权和失败恢复必须可追踪时读取本卡。

### Decision Inputs

记录单 Agent 基线、是否引入新信息/外部反馈、是否存在统一计划和最终责任、是否需要独立互审、任务是否动态流转、上下文是否共享、共享工件的并发风险、失败传播范围、预算、终止条件和恢复负责人。

### Option Relationship

A、B、C 是主控制拓扑的互斥选择：集中管理、对等协商或协议化移交。共享上下文、文件或消息是独立的信息流轴，不能被当作第四种拓扑；同一协作单元必须明确唯一主拓扑。

### Selection Rules

- 有全局计划、资源约束、最终整合责任或统一质量门时选 A，并设置中间结果验证门。
- 需要独立质疑、交叉审查或多轮改进时选 B，并设置最大轮次、终止和裁决。
- 按专长或状态动态交接时选 C，并记录任务 ID、当前所有者、最小状态、超时和失败回退。
- 共享工件时为每个写入者定义所有权和版本规则；如果协调成本超过单 Agent 收益，停止拆分。

### Required Artifacts

交付协作拓扑、角色和所有权矩阵、任务状态与控制权转移协议、共享上下文/文件/消息接口、终止与冲突裁决规则、错误升级和恢复路径，以及共享工件的并发写入约定。

### Verification

- 与单 Agent 基线比较通信成本、可验证性收益和错误传播范围。
- 演练正常完成、执行者失败、管理者错误、对等分歧、移交超时和接收者失败，确认任务不会丢失、重复或无限循环。
- 对共享文件和消息执行并发冲突测试，确认所有权和版本规则会阻止覆盖。
- 追踪每次控制权转移和关键中间结果，确认错误不会未经验证级联到下游。
- 与等量预算的单 Agent 基线比较新增信息、验证收益和通信成本；没有外部反馈时不得用多轮辩论单独证明多 Agent 有益。

## Anti-Patterns

- 管理者只转发子 Agent 文本，却不验证中间结果和错误传播。
- 对等协作没有终止条件、责任边界或冲突裁决，导致无限循环。
- 去中心化移交不记录所有权和状态，导致任务丢失或重复。
- 多个 Agent 无所有权约定地并发写同一文件。
- 为了“多 Agent”拆分单 Agent 已能可靠完成的简单任务。

## Sources

- [src-001] chapter10.md §多 Agent 协作的分类框架；§共享上下文的多 Agent 协作；§不共享上下文的多 Agent 协作；§Agent 眼中的文件系统；§Agent 间的通信与控制。
- [src-001] chapter10.md §对等协作模式：相互制衡与迭代改进；§管理者模式：中心化协调；§去中心化模式：对等移交；§多 Agent 协作的失败模式。
- [src-001] chapter10.md §多 Agent 的真正价值：引入新信息；§多 Agent 的成本与收益；§多 Agent 协作的失败模式。
