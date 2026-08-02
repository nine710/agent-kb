---
task_id: benchmark-development-agent-004
responsibility_id: tool-and-action-architecture
difficulty: typical
review_status: pending
---

## Project Background

一个代码 Agent 需要搜索仓库、读取文件、编辑代码、运行测试，并准备一次可能影响外部环境的发布操作。不同能力的副作用、权限和失败恢复成本不同。

## Development Goal

设计工具能力边界和行动接口，使 Agent 能发现适用能力、传递可验证参数，并在失败或拒绝时保持状态可恢复。

## Known Constraints

- 读取和测试通常是低风险，发布或删除可能不可逆。
- 工具调用可能超时、重复到达或返回部分结果。
- 参数需要被程序验证，不能只依赖自然语言说明。
- 高风险动作需要审计和明确的控制权转移。

## Required Artifacts

- 能力清单和工具 schema
- 权限、副作用和审批矩阵
- 超时、重试、幂等和恢复协议
- 允许、拒绝、重复和部分失败测试

## Failure Risks

- Agent 发现不到必要工具或误用工具
- 自由文本绕过参数和权限约束
- 重试造成重复副作用
- 工具失败后任务状态无法继续或审计

## Independent Rubric

- 能根据能力、风险和可恢复性划分工具边界
- 能说明接口形状如何降低行动风险
- 交付物包含参数、权限、审计和失败协议
- 验证覆盖拒绝、超时、重复请求和部分成功
- 方案没有用一个无限能力的通用命令接口承担全部动作
