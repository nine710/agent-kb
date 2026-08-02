---
id: workflow-autonomy-strategy
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
problem: 如何为代码 Agent 选择工作流、自主循环还是混合编排，使任务既可控又能适应不确定性？
tags: [agent-runtime, workflow, react, orchestration, recovery, budget]
when_to_use: 需要把用户目标拆成阶段、工具动作、停止条件和恢复记录，且任务包含确定步骤与未预见情况时。
when_not: 只实现一个确定性函数，或还没有定义任务成功条件、权限边界和失败转移时。
status: active
source_ids: [src-001]
---

## Options

### Option A: 确定性工作流

把目标映射为显式阶段、状态转换、工具入口和停止条件。每个阶段的输入、输出和失败转移由程序或 Harness 控制，适合高风险、可分解且验收条件明确的任务。

### Option B: 自主 ReAct 循环

让 Agent 根据当前观察、工具结果和剩余预算选择下一步行动，直到达到完成、失败或停止条件。它适合路径难以预先穷举的探索任务，但必须额外限制重试、循环和副作用。

### Option C: 阶段门控的混合编排

用工作流固定高风险、可验证和需要审批的阶段，在阶段内部允许 Agent 自主搜索、编辑或排错；阶段门只接受结构化结果和外部验证信号。

## Tradeoffs

| | 优势 | 代价 |
|---|---|---|
| A 工作流 | 停止、权限、回滚和验收边界最清楚，易复现 | 预见性不足时需要频繁修改流程，探索能力有限 |
| B 自主循环 | 能适应未知文件、工具结果和多步探索，流程扩展快 | 预算、循环、错误恢复和副作用控制更复杂，结果方差更高 |
| C 混合 | 把确定性安全门与局部探索结合，兼顾控制与适应性 | 阶段边界、状态移交和验证接口需要额外设计，可能重复编排 |

## Apply to Agent Development

- 先列出任务阶段、可验证完成条件、不可逆动作、环境不确定性、剩余预算和恢复成本，再选择主编排路径。
- 高风险动作、固定发布流程和必须审计的阶段选 A；探索面大、路径无法预先枚举且工具反馈能验证时选 B；同时存在固定安全门和局部未知路径时选 C。
- 无论路径如何选择，都把停止、重试上限、错误分类、用户停止、目标变更和恢复记录写成运行时状态，而不是依赖最终自然语言。
- 自主循环只能在 Harness/工具验证下运行；阶段门只接受实际工具结果、测试或结构化状态，不能接受 Agent 自称完成。

## Development Agent Procedure

### Trigger

当用户目标需要多步规划、工具循环、阶段验收、预算控制或从中断恢复时读取本卡。

### Decision Inputs

记录任务是否可预先分解、哪些阶段有不可逆副作用、完成条件能否程序验证、环境和路径的不确定性、工具反馈质量、预算、重试上限、用户停止/改目标路径和恢复所需状态。

### Option Relationship

A、B、C 是同一任务的主编排选择。A 固定全部阶段；B 让模型主导路径；C 在高风险或可验证边界使用 A、在阶段内部使用 B。即使选择 B，也不能省略 Harness 的停止、权限和验证层。

### Selection Rules

- 预先可枚举且副作用高、验收确定的任务选 A。
- 路径高度未知、外部观察能提供可靠反馈且副作用可隔离的任务选 B，并设置全局预算、循环指纹和断路器。
- 既有固定安全/发布门又有局部探索的任务选 C，为每个阶段定义输入、结构化输出、验证门和失败回退。
- 如果没有可靠验证信号或恢复状态，先补齐 Harness 和状态模型，不因“更自主”而选择 B/C。

### Required Artifacts

交付任务模型、状态转换、执行循环、停止与重试规则、预算/断路器、阶段门或工具验证接口、进度/所有权/恢复记录，以及正常完成、失败、暂停和目标变更场景。

### Verification

- 演练正常完成、工具失败、重复指纹、预算耗尽、用户停止、目标变更和进程重启，确认状态能停止、转移和恢复。
- 对 A 检查每个阶段都有显式输入/输出/停止条件；对 B 检查无界循环、重复副作用和全局上限；对 C 检查阶段门不会接受未经验证的文本结论。
- 比较计划状态与实际仓库、工具和测试状态，确认恢复不会重复已完成动作或遗漏未完成动作。

## Anti-Patterns

- 把“工作流、自主、混合”当成提示词风格，而不交付状态机、停止条件和失败转移。
- 给自主循环无限步数或无限重试，靠模型自己决定何时结束。
- 阶段门只检查 Agent 的自然语言“完成”，不读取测试、文件或外部状态。
- 进程重启后只重新发送原始目标，丢失所有权、已完成变更和下一步条件。
- 为了形式统一把本可确定验证的阶段全部交给自主循环。

## Sources

- [src-001] chapter1.md §编排模式：工作流与自主；§Harness 工程：模型之外的竞争力；§人工干预。
- [src-001] chapter5.md §Coding Agent 的工作流程；§Harness：把 Agent 变成可靠的执行系统；§故障与错误恢复。
