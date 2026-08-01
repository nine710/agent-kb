---
card_id: experience-encoding
task_id: experience-encoding-001
difficulty: typical
review_status: pass
reviewer: Codex development-agent review
reviewed_at: 2026-08-01
---

## Project Background

Agent 多次遇到同一种配置错误，并积累了带来源的诊断轨迹。

## Development Goal

选择低风险、可回滚的经验沉淀方式。

## Known Constraints

诊断事实可检索；修复步骤仍需结合仓库上下文；尚无稳定的形式化条件。

## Expected Trigger

出现可复用但需要模型裁量的经验。

## Acceptable Decision

将证据整理为 A 知识，必要的通用步骤写成 B，不直接更新参数。

## Required Artifacts

- 经验登记和来源
- 知识条目与失效条件
- 指令变更草案（如需要）

## Required Verification

- 在代表性任务中比较取回前后效果
- 检查过期条目可撤回

## Failure Conditions

- 单次成功直接写入系统指令
- 没有来源和回滚

## Rubric

- trigger-recognition: 识别经验沉淀触发
- decision-inputs: 调查可复用性和证据
- option-relationship: 说明 A/B 分层
- selection: 选择知识并谨慎补指令
- artifacts: 交付登记、条目和草案
- verification: 覆盖效果与回滚
- anti-pattern: 拒绝未验证发布

## Review Record

- trigger-recognition: pass
- decision-inputs: pass
- option-relationship: pass
- selection: pass
- artifacts: pass
- verification: pass
- anti-pattern: pass

## Agent Response Summary

把有来源的诊断事实作为可检索知识，稳定步骤才进入按需指令；保留适用和失效条件，不更新模型参数。通过代表性任务和撤回演练验证改进。
