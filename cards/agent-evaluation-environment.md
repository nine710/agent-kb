---
id: agent-evaluation-environment
card_contract: development-agent-v1
card_type: composition-strategy
utility_status: unverified
consumer: development-agent
decision_scope: evaluation
option_relationship: composable
design_task_id: evaluation-and-observability-architecture
design_goal: 让 Agent 的能力、失败模式和改进结果得到可信验证。
required_artifact_types: [evaluation-matrix, task-dataset, trajectory-observability-spec]
failure_risks: [invalid-evaluation-conclusion, unobservable-failure, metric-gaming]
problem: 如何把代码 Agent 的失败风险映射到工具调用、人机交互或仿真环境，并同时定义任务分布、轨迹信号和失败归因？
tags: [evaluation, benchmarks, tool-calling, interaction, simulation, observability]
when_to_use: 开发 Agent 的新能力、工具接口、用户协作流程或长程策略后，需要可重复验收并解释失败原因时。
when_not: 只检查 Markdown 格式或单个确定性函数输出时；那类问题不需要 Agent 评估环境架构。
status: active
source_ids: [src-001]
---

## Options

### Option A: 工具调用型环境

为 Agent 提供可验证的工具接口、初始状态和结果判定器，检查它是否选择正确工具、传递正确参数、遵守调用顺序并达到可观察的仓库或外部状态。

### Option B: 人机交互型环境

用模拟用户或分支化交互环境评估澄清、引导、协商、改目标、拒绝和安全终止。评价对象不只是最终任务完成，还包括多轮交互中的决策质量。

### Option C: 仿真环境

构造包含状态变化、随机性或现实约束的模拟世界，评估 Agent 的长程决策、罕见情景和状态演化。必须先声明需要复现的现实属性和保真度，再决定仿真规模。

## Tradeoffs

| | 优势 | 代价 |
|---|---|---|
| A 工具调用 | 状态和参数通常可客观断言，易自动运行和定位工具错误 | 覆盖不了复杂用户行为和现实动态；接口会限制任务形态 |
| B 人机交互 | 能覆盖澄清、协作、拒绝和用户驱动分支 | 用户模拟和主观评分较难校准，成本和方差更高 |
| C 仿真 | 能测试状态演化、长程策略和罕见情景，可复用于压力测试 | 保真度、随机化和环境构建成本直接决定结论有效性 |

## Apply to Agent Development

- 先从失败风险定义需要观察的事件和断言，再选择环境；环境不是目的，必须支持归因和基线比较。
- 工具选择、参数和仓库状态是主要风险时选 A，并把期望状态写成断言。
- 澄清、协商、改目标或用户拒绝决定成败时增加 B，明确模拟用户状态和评分标准。
- 时间、随机性、连续状态或罕见风险决定成败时增加 C，先定义保真度目标和随机化范围。
- A/B/C 可以组合，但一种环境的分数不能替代另一种风险的验证；所有环境共享任务、Agent、环境和评估器的记录边界。

## Development Agent Procedure

### Trigger

当需要为 Agent 的能力、工具、交互或长程策略建立可重复验收，且必须知道失败发生在工具、用户分支、状态演化还是评估器时读取本卡。

### Decision Inputs

记录结果能否由工具状态客观断言、是否依赖多轮用户分支、是否受连续世界或随机条件影响、所需保真度、运行成本、任务分布、难度、可验证性和失败代价。

### Option Relationship

A、B、C 按风险组合：A 覆盖确定性工具结果，B 覆盖交互分支，C 覆盖状态演化和长程策略。它们共享任务、环境、Agent 和评估器记录，但不能互相代替。

### Selection Rules

- 工具和外部状态风险优先选 A，并断言工具、参数、顺序和最终状态。
- 人机协作风险增加 B，并准备合作、拒绝、改目标和终止分支。
- 长程状态、随机性或罕见风险增加 C，并声明现实属性、保真度和随机化。
- 无论选择哪种环境，都按任务分布和失败模式分组，不以平均分作为唯一结论。

### Required Artifacts

交付评估矩阵、任务数据集和初始状态、动作接口或用户脚本、轨迹事件 schema、评估器、失败归因规则；使用仿真时还要交付保真度目标和随机化范围。

### Verification

- 为每个主要失败风险安排可观测轨迹和边界任务，确认环境能区分原因。
- 在 A 中断言工具调用、参数和最终状态，不只检查自然语言回复。
- 在 B 中运行分支化用户脚本，检查澄清、拒绝、改目标和终止行为。
- 在 C 中改变关键随机条件，检查结论不依赖单一理想轨迹。
- 按难度和失败模式比较结果，记录环境覆盖、成本和结论边界。

## Anti-Patterns

- 用只检查最终自然语言的环境评价工具型 Agent。
- 用单一理想用户脚本代表全部多轮交互。
- 未定义保真度目标就构造大型仿真。
- 任务不可验证却把失败归因于模型能力。
- 只报告平均分，不检查分布、失败模式和归因。

## Sources

- [src-001] chapter6.md §自动评估环境 > §评估环境的基本组成；§工具调用型评估环境；§人机交互型评估环境；§评估任务数据集的设计；§评估指标体系；§自动化评估方法。
- [src-001] chapter6.md §仿真环境：从评估到后训练的桥梁；§保真度权衡与领域随机化；§Agent 的可观测性。
- [src-001] chapter6.md §评估对象：模型与 Harness 的组合；§从失败轨迹到可复用评估任务；§统计显著性与对照分析。
