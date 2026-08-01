---
card_id: context-loading-strategy
task_id: context-loading-001
difficulty: typical
review_status: pass
reviewer: Codex development-agent review
reviewed_at: 2026-08-01
---

## Project Background

正在开发一个代码维护 Agent。每轮任务都需要安全边界、工具定义和仓库身份；只有排查特定模块时才需要该模块的约定；测试、搜索和构建工具会持续返回长输出。

## Development Goal

设计这个 Agent 的上下文承载方案，既保持稳定前缀，又避免长任务中的工具输出降低主上下文质量。

## Known Constraints

系统提示词前缀应稳定；仓库约定可按模块变化；工具输出会随会话增长；任务不需要跨会话知识库。

## Expected Trigger

必须读取 `context-loading-strategy`，因为需要为稳定规则、低频知识和累积轨迹分别选择承载位。

## Acceptable Decision

采用 A+B+C：稳定安全边界和工具定义用 A，模块约定按需用 B，已进入会话且增长的工具输出用 C。不得把全部模块约定常驻到 A。

## Required Artifacts

- 上下文分层表
- 静态前缀边界与禁止动态字段清单
- 模块约定的 Skill 加载规则
- 工具输出压缩阈值与保留字段清单

## Required Verification

- 比较两轮请求的静态前缀，确认字节稳定
- 用长测试输出验证压缩前后保留失败路径和命令标识符

## Failure Conditions

- 把所有仓库约定、测试输出都放入系统提示词
- 每轮都压缩全部历史而无阈值
- 压缩后丢失失败原因、文件路径或命令参数

## Rubric

- trigger-recognition: 识别上下文分类决策触发本卡
- decision-inputs: 调查稳定性、频率、增长与预算
- option-relationship: 说明 A/B/C 按信息类型组合
- selection: 选择 A+B+C 且说明各自承载的信息
- artifacts: 交付全部四项工件
- verification: 包含前缀稳定和压缩保真检查
- anti-pattern: 拒绝将所有约定与输出常驻

## Review Record

- trigger-recognition: pass
- decision-inputs: pass
- option-relationship: pass
- selection: pass
- artifacts: pass
- verification: pass
- anti-pattern: pass

## Agent Response Summary

将信息分为三类：稳定安全边界和固定工具 schema 进入 A；模块级仓库约定作为 B 的按需 Skill；测试、搜索和构建输出进入 C，并只在预算阈值或信息密度下降时批量压缩。交付上下文分层表、静态前缀字段/动态字段拒绝清单、模块约定加载条件，以及保留失败路径、命令、文件路径和参数的压缩规则。验证两轮静态前缀字节相同，并对压缩前后断言失败原因和命令标识符仍存在。拒绝把全部模块约定和工具输出常驻到 system prompt。
