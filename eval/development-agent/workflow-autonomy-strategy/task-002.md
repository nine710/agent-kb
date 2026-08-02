---
card_id: workflow-autonomy-strategy
task_id: workflow-autonomy-002
difficulty: boundary
review_status: pass
reviewer: Codex development-agent review
reviewed_at: 2026-08-02
---

## Project Background

一个 Agent 负责生成数据库迁移并准备发布。迁移脚本的结构固定，但字段映射需要探索；执行生产发布不可逆，且审批可能超时。

## Development Goal

设计可控的编排和阶段门，避免探索便利性扩大生产副作用。

## Known Constraints

迁移必须先在隔离数据库验证；生产发布需要人工批准；审批拒绝或超时不能执行；失败需要可回滚。

## Expected Trigger

任务同时包含固定高风险阶段和不确定字段映射时读取本卡。

## Acceptable Decision

选择混合编排：字段映射在隔离环境用自主循环探索，生成/静态检查/影子迁移/回滚验证/生产审批由工作流阶段门控制。生产动作只能由审批后的专用工具执行。

## Required Artifacts

- 隔离探索任务与输出 schema
- 迁移阶段状态机和审批门
- 回滚脚本、超时转移和审计记录

## Required Verification

- 影子迁移和回滚通过后才可请求审批
- 审批拒绝/超时无生产副作用
- 探索输出不能直接执行生产命令

## Failure Conditions

- 让自主 Agent 直接决定生产发布
- 把审批界面当成执行控制
- 没有回滚状态就进入下一阶段

## Rubric

- trigger-recognition: 识别固定高风险阶段与局部探索
- decision-inputs: 调查不可逆性、验证、审批和回滚
- option-relationship: 说明工作流阶段门与自主阶段组合
- selection: 选择混合并隔离生产工具
- artifacts: 交付阶段、输出、审批和回滚工件
- verification: 覆盖隔离验证、拒绝、超时和不可绕过
- anti-pattern: 拒绝自主循环直接发布

## Review Record

- trigger-recognition: pass
- decision-inputs: pass
- option-relationship: pass
- selection: pass
- artifacts: pass
- verification: pass
- anti-pattern: pass

## Agent Response Summary

采用混合编排。自主循环只负责隔离数据库中的字段映射探索，并返回带版本和证据的结构化候选。工作流固定生成、静态检查、影子迁移、回滚验证、审批和发布阶段；阶段门检查实际数据库状态和测试，不接受自由文本。生产发布由审批后的专用工具执行，拒绝或超时转为暂停且无副作用，所有状态和回滚负责人写入审计记录。
