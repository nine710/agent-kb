---
card_id: context-loading-strategy
task_id: context-loading-002
difficulty: boundary
review_status: pass
reviewer: Codex development-agent review
reviewed_at: 2026-08-01
---

## Project Background

正在开发一个架构审查 Agent。它要分析数千个仓库文件，并在后续会话复用组件关系、架构决策和来源定位。主 Agent 的上下文预算固定且较紧。

## Development Goal

设计大规模仓库探索和跨会话架构知识的上下文方案。

## Known Constraints

仓库探索会产生海量中间内容；主上下文预算有限；跨会话知识必须治理时效和冲突；少量已进入主会话的工具结果仍可能需要压缩。

## Expected Trigger

必须读取 `context-loading-strategy`，因为信息规模与跨会话要求改变了上下文承载位的选择。

## Acceptable Decision

采用 B+D；已经进入主轨迹且必须保留的少量输出可选 C。通过子 Agent 隔离仓库扫描、通过检索层保存跨会话架构知识；不得把仓库探索 bulk 注入主上下文。

## Required Artifacts

- 探索子 Agent 的任务输入与结论返回格式
- 检索知识的来源定位、时效和冲突处理规则
- 主上下文预算分配与少量轨迹压缩策略

## Required Verification

- 用大范围文件探索检查主上下文不接收原始 bulk
- 对检索结果检查来源、时效和冲突处理
- 检查返回摘要保留架构决策、组件关系和文件定位

## Failure Conditions

- 主 Agent 直接读取并保留全部文件内容
- 将跨会话知识放在静态系统前缀
- 子 Agent 只返回无来源的泛化摘要

## Rubric

- trigger-recognition: 识别大规模探索与跨会话知识触发本卡
- decision-inputs: 调查预算、探索规模、持久性、时效与冲突
- option-relationship: 说明 B/D 为主且 C 只处理已进入轨迹的内容
- selection: 选择 B+D 并限制 C 的适用范围
- artifacts: 交付返回格式、治理规则和预算策略
- verification: 验证隔离、来源、时效、冲突和返回保真
- anti-pattern: 拒绝将探索 bulk 放进主上下文

## Review Record

- trigger-recognition: pass
- decision-inputs: pass
- option-relationship: pass
- selection: pass
- artifacts: pass
- verification: pass
- anti-pattern: pass

## Agent Response Summary

选择 B+D 为主：以按需 Skill 提供当前审查任务所需的方法和规范；将仓库扫描交给隔离子 Agent，并将跨会话架构知识放入带来源定位、更新时间和冲突状态的检索层。C 仅压缩已经进入主会话、仍需保留的少量工具轨迹，不能替代 D。交付子 Agent 输入/返回 schema，返回必须包含结论、组件关系、文件定位、证据与不确定项；同时交付检索治理规则和主上下文预算。验证主 Agent 不接收文件 bulk，检索返回有来源/时效/冲突字段，且返回摘要保留架构决策、组件关系与文件定位。拒绝主 Agent 直接长期保留全部文件内容。
