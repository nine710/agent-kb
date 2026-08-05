---
card_id: durable-task-admission-strategy
task_id: durable-task-admission-002
difficulty: boundary
review_status: pass
reviewer: Codex development-agent review
reviewed_at: 2026-08-03
---

## Project Background

用户通过 IDE 命令要求一个已运行的重构 Agent “应用下一批文件”。调用方必须立即知道请求是否被接受；任务可能不存在，命令可能因并发版本冲突或参数错误被拒绝。

## Development Goal

为需要即时接受反馈的命令建立可验证的准入与完成边界，避免把已启动或已接收误报为已执行。

## Known Constraints

命令可能重复到达；任务状态有并发版本；参数需要写入前校验；带启动命令的请求可能只成功创建任务而未应用命令。

## Expected Trigger

需要让调用方取得接受/拒绝或局部结果，而不是仅发送后台通知时读取本卡。

## Acceptable Decision

采用同步命令准入。命令先经过非阻塞校验器验证任务状态、版本和参数；调用方区分 accepted 与 completed。请求携带命令 ID，并把“任务已启动”与“命令成功应用”分开处理，因为带启动命令可能启动任务但未成功送达命令。

## Required Artifacts

- 命令 schema、命令 ID 和冲突/幂等规则
- accepted/completed 响应状态与错误模型
- 任务不存在、冲突、超时和重试流程

## Required Verification

- 非法参数和版本冲突在接受前被拒绝
- 重复命令不重复修改文件
- 任务启动但命令未送达不会被报告为完成
- 客户端可分别处理 accepted、completed 和 timeout

## Failure Conditions

- 把异步接收确认直接展示为文件已修改
- 让校验器执行长时间或有副作用的工作
- 忽略任务启动和命令应用可能分离的失败状态

## Rubric

- trigger-recognition: pass
- decision-inputs: pass
- option-relationship: pass
- selection: pass
- artifacts: pass
- verification: pass
- anti-pattern: pass

## Review Record

- trigger-recognition: pass
- decision-inputs: pass
- option-relationship: pass
- selection: pass
- artifacts: pass
- verification: pass
- anti-pattern: pass

## Agent Response Summary

选择同步命令准入。校验器不阻塞且在写入前拒绝冲突，命令 ID 供重复请求附着已有结果。客户端只在完成阶段把文件批次标为完成；若带启动请求只创建任务但命令失败，状态明确标为未应用并可安全重试。
