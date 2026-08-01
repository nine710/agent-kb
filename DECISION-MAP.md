# Development Agent Decision Map

## goal-and-task-execution-architecture

id: goal-and-task-execution-architecture
name: 如何设计 Agent 的目标、规划与任务执行架构？
status: core
design_goal: 让 Agent 能够把目标转换为有边界、可停止和可恢复的任务执行。
required_artifacts: [task-model, execution-loop, stop-condition]
failure_risks: [unbounded-execution, invalid-plan, lost-task-state]
child_problems: [workflow-autonomy-architecture, async-task-scheduling]
coverage_status: no-published-card
coverage_cards: []
coverage_raw_only: [workflow-autonomy-architecture, async-task-scheduling]
coverage_evidence_needed: [hybrid-orchestration-source, polling-or-supervision-source]

## context-and-state-architecture

id: context-and-state-architecture
name: 如何设计 Agent 的上下文与状态架构？
status: core
design_goal: 让 Agent 在任务全过程获得正确、足够、可恢复的信息。
required_artifacts: [context-layering-table, state-model, budget-and-recovery-policy]
failure_risks: [context-corruption, lost-state, unrecoverable-long-task]
child_problems: [context-loading-strategy, coding-session-recovery]
coverage_status: partial
coverage_cards: [context-loading-strategy]
coverage_raw_only: [coding-session-recovery]
coverage_evidence_needed: [stateful-vs-sessionless-vs-checkpointed-source]

## knowledge-and-memory-architecture

id: knowledge-and-memory-architecture
name: 如何设计 Agent 的知识、记忆与检索架构？
status: core
design_goal: 让 Agent 获取可追溯、及时且与任务相关的外部知识。
required_artifacts: [knowledge-organization-schema, retrieval-evaluation-set, freshness-conflict-policy]
failure_risks: [stale-or-conflicting-knowledge, unsupported-retrieval, missing-provenance]
child_problems: [knowledge-retrieval-strategy]
coverage_status: covered
coverage_cards: [knowledge-retrieval-strategy]
coverage_raw_only: []
coverage_evidence_needed: []

## tool-and-action-architecture

id: tool-and-action-architecture
name: 如何设计 Agent 的工具能力边界与行动接口？
status: core
design_goal: 让 Agent 通过可发现、可维护且受限的接口可靠采取行动。
required_artifacts: [tool-capability-boundary, tool-schema, tool-discovery-policy]
failure_risks: [tool-call-failure, unsafe-capability-surface, undiscoverable-tool]
child_problems: [tool-capability-surface]
coverage_status: no-published-card
coverage_cards: []
coverage_raw_only: [tool-capability-surface]
coverage_evidence_needed: [third-capability-packaging-path-source]

## safety-and-human-control-architecture

id: safety-and-human-control-architecture
name: 如何设计 Agent 的安全边界与人工控制？
status: core
design_goal: 让 Agent 的约束、验证和高风险人工控制形成可审计闭环。
required_artifacts: [constraint-layering-table, guardrail-test-matrix, approval-audit-flow]
failure_risks: [unauthorized-side-effect, bypassable-constraint, unreviewable-action]
child_problems: [constraint-placement]
coverage_status: covered
coverage_cards: [constraint-placement]
coverage_raw_only: []
coverage_evidence_needed: []

## evaluation-and-observability-architecture

id: evaluation-and-observability-architecture
name: 如何设计 Agent 的评估与可观测性架构？
status: core
design_goal: 让 Agent 的能力、失败模式和改进结果得到可信验证。
required_artifacts: [evaluation-matrix, task-dataset, trajectory-observability-spec]
failure_risks: [invalid-evaluation-conclusion, unobservable-failure, metric-gaming]
child_problems: [agent-evaluation-environment]
coverage_status: covered
coverage_cards: [agent-evaluation-environment]
coverage_raw_only: []
coverage_evidence_needed: []

## continuous-improvement-and-collaboration-architecture

id: continuous-improvement-and-collaboration-architecture
name: 如何设计 Agent 的持续改进与协作架构？
status: core
design_goal: 让 Agent 在可验证、可回滚的条件下沉淀经验并协调多方工作。
required_artifacts: [experience-release-record, coordination-topology, rollback-policy]
failure_risks: [unverified-capability-regression, coordination-error-cascade, irreversible-improvement]
child_problems: [experience-encoding, multi-agent-coordination]
coverage_status: covered
coverage_cards: [experience-encoding, multi-agent-coordination]
coverage_raw_only: []
coverage_evidence_needed: []
