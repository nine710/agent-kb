---
id: durable-task-admission-strategy
card_contract: development-agent-v1
card_type: atomic-decision
utility_status: unverified
consumer: development-agent
decision_scope: agent-runtime-architecture
option_relationship: exclusive
design_task_id: goal-and-task-execution-architecture
design_goal: 让 Agent 能够把目标转换为有边界、可停止和可恢复的任务执行。
required_artifact_types: [task-model, execution-loop, stop-condition]
failure_risks: [unbounded-execution, invalid-plan, lost-task-state]
problem: 如何为长时间运行的代码 Agent 选择异步事件、同步命令或时间驱动调度来接收工作，并明确并发、暂停、补偿和恢复语义？
tags: [agent-runtime, durable-execution, scheduling, event-driven, pause, recovery]
when_to_use: 代码 Agent 需要在启动后等待用户输入、外部系统事件、周期性检查或补跑任务，并且必须避免无界轮询、重复副作用和不可恢复中断时。
when_not: 任务只在一次同步请求内完成且没有外部等待、重复执行或后台恢复需求时。
status: active
source_ids: [src-002]
---

## Options

### Option A: 异步事件准入

让外部系统或用户以异步事件唤醒持久任务，任务记录事件后在自己的执行循环中处理。适合到达时间不可预测、调用方不应等待结果、或多个事件需要累积和去重的工作。

### Option B: 同步命令准入

让调用方提交一个需要验证并返回结果的命令，任务在接受或完成阶段给出可观察反馈。适合调用方必须知道请求是否已被接纳、是否通过业务校验或能否立即返回局部结果的工作。

### Option C: 时间驱动调度

用明确的日历或间隔规则创建工作，并为补跑、抖动、重叠、失败暂停和最大动作数声明政策。适合周期性维护、批处理、到期检查和可预测的容量窗口。

## Tradeoffs

| | 优势 | 代价 |
|---|---|---|
| A 异步事件 | 调用方无需等待；可在任务持久状态中累积事件并在条件满足时处理 | 阻塞处理器会交错执行；必须初始化状态、去重并决定任务关闭前如何处理未完成事件 |
| B 同步命令 | 可在接受或完成阶段向调用方返回校验结果，适合需要即时确认的控制操作 | 调用方被请求生命周期约束；带启动的同步命令不是原子操作，必须处理冲突、超时和幂等 ID |
| C 时间驱动 | 补跑、重叠和容量行为可在运行前声明，能用抖动和批量控制可预测峰值 | 时间不是暂停边界；暂停中的执行仍会影响重叠策略，遗漏窗口和错误政策会导致意外跳过、积压或并发 |

## Apply to Agent Development

- 先记录触发来源、调用方是否需要同步确认、时效、可容忍的遗漏或重复、并发上限、暂停/取消语义和恢复状态，再选择一个主准入路径。
- 用户输入、Webhook、构建完成等不可预测通知选 A；把事件 ID、去重键、处理状态和任务关闭前的未处理事件策略写入状态模型。
- 需要立即校验、接受回执或局部结果的用户命令选 B；区分“已接纳”和“已完成”，不要把带启动命令当成原子提交。
- 周期性检查、批处理或可预估容量窗口选 C；明确时间规格、时区、抖动、补跑窗口、重叠、失败暂停及最大执行数。
- 任何路径都把外部副作用置于可重试、幂等的活动边界；暂停、取消和终止必须是不同状态转换，不能以一条自然语言“停止”代替。

## Development Agent Procedure

### Trigger

当代码 Agent 的任务需要等待外部事件、接受可验证命令、按时间自动启动或在中断后继续，且调用方、并发或副作用语义必须被设计时读取本卡。

### Decision Inputs

记录触发者、到达是否可预测、调用方是否等待结果、延迟与遗漏容忍度、重复到达可能性、并发和容量预算、暂停/取消/终止语义、补跑需求、外部副作用和恢复所需状态。

### Option Relationship

A、B、C 是同一任务的主准入方式，只选择一个作为默认唤醒路径。它们可以在不同任务类型共存，但不能隐含地同时处理同一事件；C 可补跑预先定义的时间点，不能替代 A/B 的事件或命令去重协议。

### Selection Rules

- 到达时间未知且调用方不等待结果时选 A，并交付事件 ID、去重和处理器完成策略。
- 调用方需要接受回执、校验拒绝或同步结果时选 B，并区分接受与完成、为冲突和重试提供幂等 ID。
- 触发时间可预先描述且需要批量、周期或容量整形时选 C，并声明重叠、补跑、抖动和失败暂停政策。
- 如果外部副作用不可安全重复，先定义幂等键、补偿或人工升级，再允许任何路径重试。

### Required Artifacts

交付任务模型和状态转换、主准入接口及其请求/事件 schema、去重键或幂等策略、并发与容量规则、暂停/取消/终止语义、时间准入时的规格与补跑/重叠政策，以及恢复和验证记录。

### Verification

- 对 A 演练重复与乱序事件、处理器阻塞、任务续跑和任务关闭前的未处理事件。
- 对 B 演练接受、拒绝、超时、重复命令和带启动请求失败，确认调用方不会把“已启动”误判为“已完成”。
- 对 C 演练重叠、停机后补跑、暂停、失败暂停、时钟边界和峰值容量，确认无意外并发或静默遗漏。
- 对所有选项演练 Worker 中断、活动重试、暂停、取消和终止，确认状态、幂等键和外部副作用能被恢复或审计。

## Anti-Patterns

- 用高频轮询代替能够发送异步事件的外部系统，既不声明容量成本也不定义停止条件。
- 把同步命令的“已启动”视为原子成功，而不处理请求未送达、冲突或重复到达。
- 用默认重叠行为处理周期任务，不声明跳过、缓冲、取消、终止或并发的业务语义。
- 暂停任务却不暂停其调度源，导致周期触发被意外跳过或积压。
- 把暂停、取消和终止混为同一个停止标志，忽略在途工作、时间推进和立即终止的差异。

## Sources

- [src-002] `source/docs/encyclopedia/workflow-message-passing/sending-messages.mdx` §Sending Signals, §Sending Updates, §Update-With-Start, §Sending Queries.
- [src-002] `source/docs/encyclopedia/workflow-message-passing/handling-messages.mdx` §Message handler concurrency, §Message handler patterns, §Message IDs and handling Continue-As-New.
- [src-002] `source/docs/encyclopedia/workflow/schedule.mdx` §What is a Schedule?, §Spec, §Pause, §Policies, §Catchup Window, §Backfill.
- [src-002] `source/docs/encyclopedia/workflow/workflow-pause.mdx` §What happens when you Pause a Workflow, §Important considerations.
- [src-002] `source/docs/encyclopedia/architecture/how-temporal-works.mdx` §Worker, §End-to-end lifecycle of a Workflow and Activity.
- [src-002] `source/docs/best-practices/error-handling.mdx` §Design Activities for idempotence.
