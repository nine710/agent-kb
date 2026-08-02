---
card_id: tool-capability-surface
task_id: tool-capability-003
difficulty: anti-pattern
review_status: pass
reviewer: Codex development-agent review
reviewed_at: 2026-08-02
---

## Project Background

一个 Agent 只有一个 `run_command(text)` 工具。它允许模型通过自由文本执行任意 shell、删除文件、发布服务和发送外部请求。工具描述写着“请谨慎使用”，执行层不校验参数、权限或重复请求。

## Development Goal

审查该能力面并设计可发现、可验证、可恢复的替代方案。

## Known Constraints

删除和发布不可逆；自由文本可能绕过提示；命令可能重复到达；失败和部分成功必须可审计。

## Expected Trigger

发现无限通用命令接口、仅靠描述保护副作用或静默参数转换时读取本卡。

## Acceptable Decision

拒绝草案。把搜索/读取/编辑/测试拆为参数明确的能力，删除/发布使用专用权限受限工具；领域规则用按需 Skill，工具规模大时再加带版本和权限的主动发现。执行侧做 schema、权限、幂等、审计和恢复校验。

## Required Artifacts

- 能力拆分和风险矩阵
- 结构化工具 schema 与拒绝规则
- 删除/发布审批、审计和重复/部分失败测试

## Required Verification

- 自由文本不能执行未声明动作
- 越权、缺参和不合法路径被拒绝
- 重复和超时不会扩大副作用

## Failure Conditions

- 接受 `run_command(text)` 作为全部能力边界
- 只增加更长的提示词
- 让发现层直接授予生产权限

## Rubric

- trigger-recognition: 识别通用接口和副作用触发
- decision-inputs: 调查动作、参数、权限、幂等和恢复
- option-relationship: 区分专用工具、Skill/通用执行器和发现层边界
- selection: 拒绝草案并拆分受限能力
- artifacts: 交付 schema、矩阵、审批和测试
- verification: 覆盖自由文本、越权、重复和超时
- anti-pattern: 明确拒绝只靠描述或无限 shell

## Review Record

- trigger-recognition: pass
- decision-inputs: pass
- option-relationship: pass
- selection: pass
- artifacts: pass
- verification: pass
- anti-pattern: pass

## Agent Response Summary

拒绝 `run_command(text)`。按能力和风险拆成结构化搜索、读取、编辑、测试、删除和发布工具；删除/发布使用专用权限、预览、审批和审计接口，Skill 只承载按任务加载的语言规则，主动发现只负责带版本的能力查找。执行侧拒绝未声明参数、越权和不合法路径，记录幂等键与部分成功状态，并测试自由文本、重复、超时和恢复。
