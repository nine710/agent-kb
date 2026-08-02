---
id: constraint-placement
card_contract: development-agent-v1
card_type: atomic-decision
utility_status: unverified
consumer: development-agent
decision_scope: agent-runtime-architecture
option_relationship: layered
design_task_id: safety-and-human-control-architecture
design_goal: 让 Agent 的约束、验证和高风险人工控制形成可审计闭环。
required_artifact_types: [constraint-layering-table, guardrail-test-matrix, approval-audit-flow]
failure_risks: [unauthorized-side-effect, bypassable-constraint, unreviewable-action]
problem: 如何把代码 Agent 的规则分别放入常驻指令、按需 Skill、Harness 强制和专用工具/人工审批，使约束可执行、可审计且与动作风险匹配？
tags: [harness, constitution, skills, guardrails, permissions, human-control]
when_to_use: 设计 Agent 的规则、权限、工具校验、默认拒绝和高风险审批承载层时。
when_not: 业务规则尚未定义，或只是一次性提示而没有可反复执行的安全责任时。
status: active
source_ids: [src-001]
---

## Options

### Option A: 常驻系统指令（Constitution）

把身份、稳定行为准则和可语言化的规则写入 system prompt 或仓库级 constitution，使其在每轮推理中位于稳定前缀并持续生效。它适合解释“应该如何行为”，不适合承担不可绕过的数值和权限检查。

### Option B: 按需 Skill

把领域规则、流程和操作指南拆成按需加载的 Skill。前缀只保留名称与描述，Agent 触发后加载完整规则。它适合任务或领域相关的知识，避免把所有规则永久塞入上下文，但依赖路由和指令遵循质量。

### Option C: Harness 程序强制

把可形式化的权限、参数、默认拒绝、输入/执行/输出校验写入 Harness 或工具执行层。模型不能通过改写自然语言或跳过步骤绕过确定性检查，规则结果可测试、可审计。

### Option D: 专用工具与人工控制

把删除、发布、支付或其他不可逆动作封装为参数明确、权限受限、可预览和可审计的专用工具；在高风险或失败阈值命中时把控制权升级给人，并让拒绝、超时和撤回都停止副作用。

## Tradeoffs

| | 优势 | 代价 |
|---|---|---|
| A 常驻指令 | 位置稳定、全场景生效、语言策略容易表达 | 会膨胀上下文；文本规则可被误解，不能保证不可绕过 |
| B 按需 Skill | 规则模块化、按任务加载、前缀更稳定 | 路由错误会漏加载或误触发；加载内容位于中间位置，需评估模型差异 |
| C Harness 强制 | 确定性、可测试、可审计且模型无法跳过 | 只适合可形式化条件；开发和维护成本高，阈值错误会误拦截 |
| D 工具与人工 | 对不可逆动作最稳，接口形状和审批门形成最后防线 | 增加人工延迟和通量成本；审批太频繁会削弱自主性 |

## Apply to Agent Development

- 先把规则标记为语言策略、可形式化约束或不可逆动作，再选择承载层。
- 身份、稳定行为准则和解释性规则使用 A；任务/领域流程使用 B；权限、参数和默认拒绝使用 C；不可逆或高影响动作使用 D。
- 不要把 C 或 D 的安全责任退化为 Prompt 中的一句禁止语句。
- D 的审批必须绑定实际执行接口和审计记录，不能只显示一个确认界面。
- 一个真实安全闭环通常组合多个层：A/B 提供语义规则，C 执行确定性检查，D 控制高风险动作。

## Development Agent Procedure

### Trigger

当 Agent 将读取、编辑、测试、删除、发布或外部 API 操作映射到规则、权限、校验和人工控制层时读取本卡。

### Decision Inputs

为每条规则记录是否需要语言理解、是否能形式化、动作的副作用和可逆性、执行环境、权限边界、审批主体、失败/超时行为、审计要求和误拦截成本。

### Option Relationship

A、B、C、D 是分层承载位，不是四选一。规则可以用 A/B 解释和路由，用 C 强制可计算条件，再用 D 控制不可逆动作；后层不能替代前层的解释，前层也不能替代后层的强制。

### Selection Rules

- 可语言化且稳定、每轮需要的规则选 A。
- 按任务或领域触发、会膨胀的规则选 B，并在描述中写清触发条件和反例。
- 能写成参数、权限、状态或输出断言的规则选 C，默认拒绝并在执行侧校验。
- 不可逆、高影响或超过失败阈值的动作选 D，提供预览、审批、超时停止和审计。

### Required Artifacts

交付约束分层表、Harness 允许/拒绝规则和边界测试、专用高风险工具的参数与权限 schema、预览/审批/审计流程，以及拒绝和超时后的状态处理。

### Verification

- 对允许、边界、越权、缺参和错误环境执行校验测试。
- 确认自由文本、改写提示或跳过 Skill 不能绕过 C 的拒绝逻辑。
- 演练 D 的批准、拒绝、超时、撤回和执行者失败，确认没有副作用残留。
- 审查每条规则的承载层、实际执行点和审计记录是否一致。

## Anti-Patterns

- 仅用 system prompt 禁止删除、发布或越权操作。
- 把所有规则堆进常驻提示，导致优先级和适用范围不可辨认。
- Skill 没有触发反例，导致规则误加载或漏加载。
- Harness 只校验模型文本，不校验结构化参数和实际执行状态。
- 审批门与执行接口脱节，审批拒绝或超时后仍能产生副作用。

## Sources

- [src-001] chapter1.md §现代 Agent = LLM + 上下文 + 工具；§Harness 工程：模型之外的竞争力；§工具：Agent 的手脚；§人工干预。
- [src-001] chapter2.md §动态提示词与 Agent Skills；§Skills 的实现方式与权衡；§KV Cache 友好的上下文设计。
