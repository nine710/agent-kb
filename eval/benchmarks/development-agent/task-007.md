---
task_id: benchmark-development-agent-007
responsibility_id: continuous-improvement-and-collaboration-architecture
difficulty: typical
review_status: pending
---

## Project Background

一个交付 Agent 需要把需求拆给不同专长的执行者，汇总代码和测试结果，并从重复失败中形成后续改进。团队要求任何能力改进都能验证、发布和撤回。

## Development Goal

设计协作控制、共享工件、经验沉淀、发布门槛和回滚机制，使系统能持续改进而不把未验证行为扩散给后续任务。

## Known Constraints

- 执行者可能失败、超时或只掌握局部上下文。
- 多个参与者可能同时修改相关工件。
- 一次成功不一定表示能力已经泛化。
- 经验进入知识、指令、程序或参数后，撤回成本不同。

## Required Artifacts

- 角色、所有权和控制权转移协议
- 共享工件版本和冲突规则
- 经验登记、评估、发布和回滚记录
- 执行者失败、分歧、超时和回滚测试

## Failure Risks

- 任务或工件在移交中丢失或重复执行
- 错误结果未经验证级联到下游
- 单次成功被永久发布为能力
- 改进无法回滚或引入不可观测回归

## Independent Rubric

- 能分别处理控制拓扑、信息通信和工件所有权
- 能根据证据、适用范围和回滚影响选择改进承载位
- 交付物包含移交、冲突、发布和回滚协议
- 验证覆盖执行者失败、分歧、超时、回滚和回归
- 方案没有把多 Agent 拆分或单次成功本身当作改进目标
