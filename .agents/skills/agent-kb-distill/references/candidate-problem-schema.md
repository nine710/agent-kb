# Candidate Problem Schema

Each candidate section uses a stable ID and includes:

- `problem`: reusable design question.
- `design_task_id`: a `core` task from `DECISION-MAP.md`, required for a mapped publishable candidate.
- `design_goal`: exact goal copied from the design task.
- `required_artifact_types`: at least one artifact type allowed by the design task.
- `failure_risks`: at least one risk allowed by the design task.
- `mapping_status`: `emerging` or `excluded` only when no `design_task_id` is possible.
- `mapping_reason`: required when `mapping_status` is present.
- `status`: `new`, `merge-with-existing`, `evidence-only`, `raw-only`, or `out-of-scope`.
- `target_contract`: `decision-card-v0` during migration, or `development-agent-v1` when the candidate will include a consumer Procedure and three evaluation tasks.
- `decision_scope`: required for `development-agent-v1`; one of the formal card scope values.
- `option_relationship`: required for `development-agent-v1`; states whether its options are exclusive, composable, layered, sequential, or composable by information type.
- `card_type`: required for `development-agent-v1`; `atomic-decision` or `composition-strategy`.
- `benchmark_task_ids`: independent benchmark tasks that expose or exercise this decision; card-specific tasks do not count as utility evidence.
- `claim_refs`: evidence ledger claim IDs.
- `three_way_assessment`: `pass` only when three mechanisms, layers, or topologies are genuinely distinct.
- `options`: the three or more paths and their supporting claim IDs.
- `agent_relevance`: direct benefit to programming Agent design.
- `existing_card_comparison`: cards compared and the deduplication conclusion.
- `priority`: high, medium, or low.
- `next_action`: draft, merge, add evidence, request source, or stop.

Use `raw-only` when the source does not support three real paths. Treat design disagreements as options. Treat incompatible factual claims as `conflict` and do not publish until resolved.

The candidate queue is not a chapter outline. Discover a problem only after mapping claims to a development responsibility and reviewing affected cards.
