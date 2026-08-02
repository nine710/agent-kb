---
card_id: workflow-autonomy-strategy
task_id: workflow-autonomy-001
difficulty: typical
review_status: pass
reviewer: Codex development-agent review
reviewed_at: 2026-08-02
---

## Project Background

一个代码 Agent 接收“升级一个仓库的配置加载方式”的目标。任务涉及搜索多个目录、修改若干文件、运行测试，并可能因外部依赖暂时不可用而中断。

## Development Goal

设计从用户目标到执行循环、停止条件和恢复记录的编排方案。

## Known Constraints

文件修改必须可审查；测试失败不能被隐藏；外部依赖可能超时；用户可能中途停止或改变目标。

## Expected Trigger

需要决定确定性阶段、局部探索、停止/重试和恢复边界时读取本卡。

## Acceptable Decision

采用阶段门控的混合编排：任务澄清、备份/权限、测试和完成验收固定为工作流；仓库搜索和局部排错在阶段内使用受预算限制的自主循环。所有阶段写入状态、所有权、失败转移和恢复记录。

## Required Artifacts

- 任务模型和状态转换
- 阶段执行循环、预算和重试上限
- 停止、目标变更和恢复记录
- 成功、失败、暂停、依赖超时场景

## Required Verification

- 依赖超时后不得无限重试
- 用户停止后不得继续修改
- 重启后不重复已完成文件修改
- 完成必须由测试和仓库状态证明

## Failure Conditions

- 用一个无限 ReAct 循环覆盖全部阶段
- 只记录最终自然语言，不记录状态和所有权
- 把依赖超时当作可无限重试的普通错误

## Rubric

- trigger-recognition: 识别多阶段、预算、停止和恢复触发
- decision-inputs: 调查副作用、验证信号、不确定性和恢复状态
- option-relationship: 说明工作流固定阶段、自主循环局部使用、混合为主架构
- selection: 选择阶段门控混合并给出边界
- artifacts: 交付任务模型、循环、停止和恢复工件
- verification: 覆盖依赖失败、停止、重启和完成证明
- anti-pattern: 拒绝无限循环和自然语言假完成

## Review Record

- trigger-recognition: pass
- decision-inputs: pass
- option-relationship: pass
- selection: pass
- artifacts: pass
- verification: pass
- anti-pattern: pass

## Agent Response Summary

采用混合编排。澄清、权限、备份、测试和验收是显式工作流阶段；搜索和局部排错在有预算、循环指纹和工具反馈的自主阶段内执行。状态记录任务 ID、当前阶段、所有权、已完成文件、失败类型、重试次数和下一步条件。依赖超时进入暂停/降级而不是无限重试；用户停止立即终止副作用；恢复时以仓库和测试状态校验已完成动作，不能把最终文本当完成证明。
