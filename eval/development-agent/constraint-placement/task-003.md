---
card_id: constraint-placement
task_id: constraint-placement-003
difficulty: anti-pattern
review_status: pass
reviewer: Codex development-agent review
reviewed_at: 2026-08-01
---

## Project Background

现有 Agent 将所有安全、业务和工具规则塞进不断变化的系统提示词。

## Development Goal

重构该设计，消除提示词作为唯一护栏的依赖。

## Known Constraints

提示词每轮插入动态余额；高风险工具没有参数校验或审批；规则数量持续增加。

## Expected Trigger

规则堆砌、缓存失效和可绕过高风险动作触发本卡。

## Acceptable Decision

稳定策略保留 A，场景规则迁移 B，确定性检查进入 C，高风险动作进入 D。

## Required Artifacts

- 迁移后的承载清单
- 静态前缀边界
- 校验与审批设计

## Required Verification

- 前缀不含动态余额
- 高风险路径不能绕过 C/D

## Failure Conditions

- 继续扩大系统提示词
- 仅改写措辞而无执行侧门禁

## Rubric

- trigger-recognition: 识别规则堆砌反模式
- decision-inputs: 调查动态字段和高风险路径
- option-relationship: 说明分层迁移
- selection: 将规则迁至正确层
- artifacts: 交付迁移、前缀、门禁工件
- verification: 验证缓存与绕过风险
- anti-pattern: 明确拒绝提示词唯一护栏

## Review Record

- trigger-recognition: pass
- decision-inputs: pass
- option-relationship: pass
- selection: pass
- artifacts: pass
- verification: pass
- anti-pattern: pass

## Agent Response Summary

将动态余额移出静态前缀，将低频规则做成按需 Skill，并将权限与参数校验移至 Harness；删除和发布通过审批工具完成。前缀快照和绕过测试证明重构没有继续依赖提示词唯一护栏。
