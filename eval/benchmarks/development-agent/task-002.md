---
task_id: benchmark-development-agent-002
responsibility_id: context-and-state-architecture
difficulty: typical
review_status: pending
---

## Project Background

一个代码 Agent 需要执行持续两小时的仓库重构。它会读取大量文件、调用测试工具、接收用户反馈，并可能被进程重启或上下文窗口限制打断。

## Development Goal

设计上下文和状态架构，使稳定规则、当前任务状态、工具轨迹、外部知识和恢复信息在成本、完整性与可恢复性之间保持可控。

## Known Constraints

- 动态状态会频繁变化，稳定规则不应随每轮请求改变。
- 大规模文件内容不能永久占据主上下文。
- 恢复时必须知道已完成的变更、当前所有权和下一步条件。
- 压缩或摘要不能静默改写路径、版本号和关键架构决定。

## Required Artifacts

- 上下文分层与加载规则
- 状态 schema、检查点或恢复协议
- 预算、压缩和外部化策略
- 中断、重启和信息丢失测试

## Failure Risks

- 上下文膨胀导致关键约束不可见
- 动态状态污染稳定前缀
- 恢复后重复修改或遗漏未完成工作
- 压缩丢失关键决策或精确标识符

## Independent Rubric

- 能区分信息承载位置与任务状态持久化问题
- 能根据稳定性、增长速度、恢复要求和副作用选择方案
- 交付物明确所有权、版本、预算和保留字段
- 验证覆盖长轨迹、压缩、重启和恢复后的仓库状态
- 方案没有把所有信息都常驻主上下文作为默认答案
