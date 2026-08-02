---
task_id: benchmark-development-agent-001
responsibility_id: goal-and-task-execution-architecture
difficulty: typical
review_status: pending
---

## Project Background

一个代码 Agent 接收“升级一个仓库的配置加载方式”的目标。任务涉及搜索多个目录、修改若干文件、运行测试，并可能因外部依赖暂时不可用而中断。用户希望 Agent 能报告当前进度，并在稍后继续，而不是重复已经完成的工作。

## Development Goal

设计一套从用户目标到可执行任务、执行循环、停止条件和恢复记录的方案，使 Agent 能在有限权限内完成迁移并清楚说明未完成部分。

## Known Constraints

- 文件修改必须可审查，测试失败不能被隐藏。
- 外部依赖可能超时或暂时不可用。
- 用户可能在中途改变目标或要求停止。
- 任务不能无限重试，也不能在状态不明确时继续产生副作用。

## Required Artifacts

- 任务模型和状态转换定义
- 执行循环与停止/重试规则
- 进度、所有权和恢复记录格式
- 正常完成、失败、暂停和用户改目标的测试场景

## Failure Risks

- 任务无限执行或无限重试
- 已完成工作丢失并被重复执行
- 用户要求停止后仍继续产生副作用
- 计划与实际仓库状态不一致

## Independent Rubric

- 能识别目标拆分、状态、停止和恢复是独立设计问题
- 能说明选择依据，而不是只给出单一流程描述
- 交付物能够表达任务所有权、完成条件和失败转移
- 验证覆盖成功、失败、暂停、重试上限和目标变更
- 没有把“自然语言回复完成”当作任务完成证明
