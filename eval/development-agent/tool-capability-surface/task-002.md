---
card_id: tool-capability-surface
task_id: tool-capability-002
difficulty: boundary
review_status: pass
reviewer: Codex development-agent review
reviewed_at: 2026-08-02
---

## Project Background

一个企业 Coding Agent 可连接 300 个远程工具服务。工具按项目动态启用，部分服务拥有生产写权限，schema 版本会变化；主上下文预算有限。

## Development Goal

设计分层主动发现和高风险能力执行方案。

## Known Constraints

静态注入全部 schema 会超过上下文预算；发现结果必须可审计；生产写操作需要审批；远程调用可能不可用或返回旧版本 schema。

## Expected Trigger

工具生态大且能力按项目变化，静态 schema 已不可维护时读取本卡。

## Acceptable Decision

使用能力目录/服务端声明和查询检索发现候选工具，只把带版本、来源、权限和失效时间的 schema 注入当前轨迹。生产写能力最终落到参数受限专用接口，并经过预览、审批、幂等和自动验证。

## Required Artifacts

- 能力目录和发现/排序协议
- 动态 schema 版本、来源和权限字段
- 生产操作审批、幂等、超时和回滚协议

## Required Verification

- 旧版本或无权限 schema 不得执行
- 发现失败和服务超时不产生副作用
- 动态注入不超过预算且保留审计链

## Failure Conditions

- 把 300 个 schema 永久放进 system prompt
- 发现服务返回未签名/无版本的任意工具
- 让主动发现绕过专用执行和审批

## Rubric

- trigger-recognition: 识别规模、动态变化和发现触发
- decision-inputs: 调查预算、版本、信任、权限和远程失败
- option-relationship: 说明主动发现是叠加层，执行仍需受限接口
- selection: 选择分层发现并保护生产动作
- artifacts: 交付目录、schema、权限和审批工件
- verification: 覆盖旧版本、无权限、超时和预算
- anti-pattern: 拒绝静态全量注入和发现绕过执行门

## Review Record

- trigger-recognition: pass
- decision-inputs: pass
- option-relationship: pass
- selection: pass
- artifacts: pass
- verification: pass
- anti-pattern: pass

## Agent Response Summary

采用分层主动发现：目录/服务端声明先按项目和意图检索候选，动态加入当前轨迹的 schema 必须带版本、来源、权限、失效时间和信任状态。生产写能力不是通用动态执行器，而是参数受限专用接口；发现后仍需预览、审批、幂等键、超时和自动验证。测试旧版本、无权限、服务超时、发现失败和上下文预算，确保发现只减少 schema 负担而不绕过安全门。
