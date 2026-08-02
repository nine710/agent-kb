---
id: experience-encoding
card_contract: development-agent-v1
card_type: atomic-decision
utility_status: unverified
consumer: development-agent
decision_scope: continuous-improvement
option_relationship: layered
design_task_id: continuous-improvement-and-collaboration-architecture
design_goal: 让 Agent 在可验证、可回滚的条件下沉淀经验并协调多方工作。
required_artifact_types: [experience-release-record, rollback-policy]
failure_risks: [unverified-capability-regression, irreversible-improvement]
problem: 如何决定一条 Agent 运行经验进入可检索知识、按需指令、确定性程序或模型参数，并用证据、评估、发布和回滚控制改进风险？
tags: [continuous-improvement, experience, skills, harness, release, rollback]
when_to_use: Agent 轨迹中出现可复用成功路径、稳定失败模式或诊断线索，团队准备让后续任务受益时。
when_not: 只有一次偶然成功、问题尚未定位、适用范围未知或没有隔离评估和回滚能力时。
status: active
source_ids: [src-001]
---

## Options

### Option A: 沉淀为可检索知识

把经验记录为带来源、适用范围和失效条件的事实、案例、模式或诊断条目，在相关任务中按需取回。它适合仍需 Agent 结合当前仓库进行判断的经验。

### Option B: 写成按需指令

把稳定的步骤、偏好或检查方法写入 Prompt、Skill 或其他按需指令，使模型在触发相关任务时直接遵循。它适合可语言化但仍需要模型裁量的经验。

### Option C: 写成确定性程序

把经验形式化为 Harness 条件、工具校验、工作流、规则或自动化脚本，使它通过确定性执行影响行为。它适合安全边界、参数约束和重复性高的行为。

### Option D: 写入模型参数

通过训练或后训练把经验内化到模型参数，使运行时不依赖显式检索或指令加载。它只有在数据、环境、隔离评估、发布和回滚能力充分时才是可接受路径，不能作为运行时问题的默认升级。

## Tradeoffs

| | 优势 | 代价 |
|---|---|---|
| A 知识 | 可审计、可检索、局部更新和回滚容易 | 取回依赖检索质量；经验到行动仍需推理 |
| B 指令 | 对行为步骤影响直接，部署快，可按需加载 | 指令可能膨胀或冲突，效果依赖模型遵循 |
| C 程序 | 可验证、可测试、可审计，模型不能绕过形式化条件 | 开发维护成本高，难表达模糊策略，过度约束会降低自主性 |
| D 参数 | 能内化经过验证的能力，运行时不需显式加载 | 训练成本、解释和回滚难度最高，未充分评估会扩大回归 |

## Apply to Agent Development

- 把经验发布当成能力变更决策，而不是存储格式选择；先确认来源、可复现性、适用范围、预期收益和回滚影响。
- 可检索事实、案例和诊断线索优先 A；需要模型判断的稳定步骤选 B；可写成条件、校验或工作流的经验选 C。
- 只有训练数据、隔离评估、发布门槛和回滚机制齐全时才考虑 D；编程 Agent 的运行时问题不得默认转成参数更新。
- A/B/C 可组合，例如知识保存诊断事实、程序执行安全检查；D 不得绕过前置证据、评估和回滚闭环。
- 一次任务完成不等于能力提升；未验证的经验保持候选状态，不进入永久能力。

## Development Agent Procedure

### Trigger

当运行轨迹显示重复成功路径、稳定失败模式或可复用诊断线索，并准备改变后续 Agent 行为时读取本卡。

### Decision Inputs

记录证据轨迹、可复现性、任务范围、经验是事实/案例/步骤/确定性条件的哪一种、是否具备训练数据与隔离评估、发布后副作用、回滚成本和停止条件。

### Option Relationship

A 到 D 按可执行性和发布风险分层。A 供检索，B 指导模型裁量，C 强制可形式化行为，D 内化经过充分验证的能力。它们可组合，但 D 不得绕过 A/B/C 的证据、评估和回滚要求。

### Selection Rules

- 事实、案例和诊断线索选 A，保留来源、适用范围和失效条件。
- 语言化步骤、偏好和策略选 B，并按任务触发，避免永久常驻。
- 参数边界、权限条件、检查和工作流选 C，并交付允许/拒绝测试。
- 只有数据分布、隔离评估、发布和回滚全部存在时选 D；否则降级到 A/B/C 候选。

### Required Artifacts

交付经验登记和证据轨迹、适用范围、承载位选择、预期收益、发布门槛、回滚负责人和停止条件；再交付对应知识条目、指令变更、程序规则或训练变更说明。

### Verification

- 在代表性、边界和回归任务上比较沉淀前后结果，并绑定版本和回滚记录。
- 对 A/B 检查来源、适用范围和失效条件；对 C 执行允许/拒绝和绕过测试；对 D 只在隔离评估通过后逐步发布。
- 演练撤回知识、指令、规则或模型版本，确认后续任务恢复到已知安全版本。
- 拒绝把单次完成或单一任务成功率当作能力提升证明。

## Anti-Patterns

- 把未经验证的单次成功轨迹直接写入长期知识或系统指令。
- 用冗长指令替代可以形式化的程序校验。
- 没有数据分布、隔离评估、发布门槛和回滚就更新模型参数。
- 把需要按任务检索的细节永久常驻，造成陈旧规则和上下文膨胀。
- 把“任务完成”误当作“能力已经提升”。

## Sources

- [src-001] chapter8.md §从运行轨迹中获得学习信号；§Agent 持续进化的四种方法 > §将经验沉淀为知识；§将经验写成指令；§将经验写成程序；§将经验写入参数。
- [src-001] chapter8.md §构建可长期运行的持续进化闭环；§验证、发布与回滚；§可验证闭环的边界：当“完成”不等于“进步”；§持续进化的安全边界。
