# Candidate Problem Schema

Each candidate section uses a stable ID and includes:

- `problem`: reusable design question.
- `status`: `new`, `merge-with-existing`, `evidence-only`, `raw-only`, or `out-of-scope`.
- `target_contract`: `decision-card-v0` during migration, or `development-agent-v1` when the candidate will include a consumer Procedure and three evaluation tasks.
- `decision_scope`: required for `development-agent-v1`; one of the formal card scope values.
- `option_relationship`: required for `development-agent-v1`; states whether its options are exclusive, composable, layered, sequential, or composable by information type.
- `claim_refs`: evidence ledger claim IDs.
- `three_way_assessment`: `pass` only when three mechanisms, layers, or topologies are genuinely distinct.
- `options`: the three or more paths and their supporting claim IDs.
- `agent_relevance`: direct benefit to programming Agent design.
- `existing_card_comparison`: cards compared and the deduplication conclusion.
- `priority`: high, medium, or low.
- `next_action`: draft, merge, add evidence, request source, or stop.

Use `raw-only` when the source does not support three real paths. Treat design disagreements as options. Treat incompatible factual claims as `conflict` and do not publish until resolved.
