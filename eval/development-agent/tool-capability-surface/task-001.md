---
card_id: tool-capability-surface
task_id: tool-capability-001
difficulty: typical
review_status: pass
reviewer: Codex development-agent review
reviewed_at: 2026-08-02
---

## Project Background

一个代码 Agent 需要搜索仓库、读取文件、编辑代码、运行测试，并准备一次可能影响外部环境的发布操作。工具数量约 12 个，其中发布和删除有不可逆副作用。

## Development Goal

设计能力边界、工具 schema、发现方式和失败恢复协议。

## Known Constraints

读取和测试通常低风险；发布和删除需要权限与审计；调用可能超时、重复到达或返回部分结果；参数必须由程序验证。

## Expected Trigger

需要决定哪些能力做成专用工具、哪些规则按需加载以及如何暴露工具 schema 时读取本卡。

## Acceptable Decision

高风险发布/删除和复杂编辑使用静态专用工具；相似的搜索/读取规则可以由 Skill 加通用执行器承载。为工具保留结构化 schema、权限矩阵、幂等和恢复协议，不用无限通用命令接口。

## Required Artifacts

- 能力边界与权限/副作用矩阵
- 工具 schema、参数和返回格式
- 超时、重复、部分成功和恢复测试

## Required Verification

- 错误参数和越权必须在执行侧拒绝
- 重复发布不会产生第二次副作用
- 发布失败后状态可审计和恢复

## Failure Conditions

- 一个 shell 工具承担所有动作
- 只靠描述禁止越权
- 静默改写路径或参数

## Rubric

- trigger-recognition: 识别能力暴露和执行风险触发
- decision-inputs: 调查参数、变更、权限、幂等和恢复
- option-relationship: 区分专用执行、Skill/通用执行和发现层
- selection: 为高风险能力选择专用接口
- artifacts: 交付边界、schema、权限和恢复工件
- verification: 覆盖拒绝、重复、超时和部分成功
- anti-pattern: 拒绝无限通用命令接口

## Review Record

- trigger-recognition: pass
- decision-inputs: pass
- option-relationship: pass
- selection: pass
- artifacts: pass
- verification: pass
- anti-pattern: pass

## Agent Response Summary

把发布/删除和复杂编辑做成参数受限的专用工具，稳定暴露 schema、权限、预览和审计字段；搜索/读取等相似能力可以由 Skill 提供按需规则并调用受约束的通用执行器。每个工具定义返回格式、超时、幂等键和部分成功状态，执行侧重新校验参数和权限。测试覆盖越权、缺参、重复发布、超时和恢复，不用自由文本或无限 shell 作为安全边界。
