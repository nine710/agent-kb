---
task_id: benchmark-development-agent-006
responsibility_id: evaluation-and-observability-architecture
difficulty: typical
review_status: pending
---

## Project Background

团队要评估一个会搜索、修改和测试代码的 Agent。仅比较最终自然语言回答无法判断它是否调用了错误工具、修改了错误文件、漏掉测试或在失败后错误恢复。

## Development Goal

设计可重复的任务集、环境、轨迹记录、评估器和失败归因，使能力改动可以与回归风险比较。

## Known Constraints

- 工具调用参数和仓库最终状态可以断言。
- 一些任务需要多轮澄清和用户分支。
- 长程任务可能受状态演化和随机条件影响。
- 评估成本有限，结论必须说明覆盖范围和局限。

## Required Artifacts

- 任务分布和初始状态定义
- 工具、用户或环境交互接口
- 轨迹事件 schema、评估器和失败归因规则
- 代表性、边界和回归任务

## Failure Risks

- 只看最终文本导致工具错误不可见
- 单一理想用户脚本掩盖交互失败
- 仿真分数无法说明真实任务能力
- 平均分掩盖特定失败模式或回归

## Independent Rubric

- 能把主要风险映射到可观察的任务环境
- 能区分结果断言、交互分支和状态演化的评估需求
- 交付物包含任务分布、轨迹信号和归因边界
- 验证覆盖代表性任务、边界任务和关键随机条件
- 方案没有只报告单一平均分或最终自然语言质量
