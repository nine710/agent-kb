---
card_id: workflow-autonomy-strategy
task_id: workflow-autonomy-003
difficulty: anti-pattern
review_status: pass
reviewer: Codex development-agent review
reviewed_at: 2026-08-02
---

## Project Background

一个 Agent 草案使用无限步数的 ReAct 循环执行仓库重构。它把测试失败重新提交给同一工具，重启后只重新发送用户目标，并以“已完成”作为唯一结束依据。

## Development Goal

审查该编排方案并给出可停止、可恢复的替代设计。

## Known Constraints

工具可能重复执行；测试失败可能来自外部依赖；用户要求停止必须立即生效；仓库修改需要可审查。

## Expected Trigger

看到无界循环、无重试上限、无状态检查点或自然语言完成声明时读取本卡。

## Acceptable Decision

拒绝草案。补充任务状态机、预算/重试上限、错误分类、断路器、停止信号、workspace 检查点和实际测试/仓库状态验收；按风险把固定阶段改成工作流，未知搜索保留有界自主阶段。

## Required Artifacts

- 状态转换和错误分类
- 全局预算、重试/断路器和停止协议
- 检查点、所有权和恢复 schema
- 完成状态验证

## Required Verification

- 重复错误触发降级或停止
- 用户停止后工具调用被拒绝
- 重启后按检查点继续而非重放副作用
- 未通过测试不能进入完成状态

## Failure Conditions

- 接受无限步数和无限重试
- 把原始目标当作恢复状态
- 只检查模型文本

## Rubric

- trigger-recognition: 识别无界执行和恢复缺口
- decision-inputs: 调查错误、预算、停止、检查点和验收状态
- option-relationship: 区分自主路径与必须补充的工作流/Harness 门
- selection: 拒绝草案并给出有界混合替代
- artifacts: 交付状态、预算、检查点和验证工件
- verification: 覆盖重复错误、停止、重启和测试失败
- anti-pattern: 明确拒绝无限循环和文本假完成

## Review Record

- trigger-recognition: pass
- decision-inputs: pass
- option-relationship: pass
- selection: pass
- artifacts: pass
- verification: pass
- anti-pattern: pass

## Agent Response Summary

拒绝无限 ReAct 草案。将任务拆成有状态阶段，给自主探索设置全局预算、重复指纹、重试上限和断路器；把用户停止、依赖失败和目标变更建模为状态转移。每次检查点记录当前所有权、已完成变更、失败原因和下一步条件；重启从检查点和实际仓库状态恢复。只有测试、文件和外部状态验证通过才进入完成。
