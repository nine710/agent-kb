# Draft Evidence Binding

For every candidate, create one archive pair under
`drafts/<source_id>/<candidate-id>-<slug>.md` and
`drafts/<source_id>/<candidate-id>-<slug>.evidence.md`.

The draft frontmatter must contain:

```yaml
source_id: src-NNN
candidate_id: CAND-NNN
design_task_id: <core-task-id>  # required for published v1 candidates
status: draft | published | raw-only | out-of-scope | rejected
published_card: cards/card-id.md  # required only for published
decision_reason: <required for raw-only, out-of-scope, and rejected>
```

The pair is permanent local provenance. Do not delete it after publication or
after a candidate is withheld.

The sidecar maps each Option, Tradeoff row, application rule, and Anti-Pattern to ledger claims:

```markdown
# Evidence Binding: <candidate-id>

- source_id: src-NNN
- candidate_id: CAND-NNN

- Option A: CLM-001, CLM-004
- Tradeoff A advantage: CLM-004
- Tradeoff A cost: CLM-006
- Apply rule 1: CLM-007
- Anti-pattern 1: CLM-009
```

Options require `supported` claims. Inferred claims may support derived rules only when their `inference_chain` is complete. A sidecar is required for every lifecycle status but is not copied into `cards/`. `published` drafts must point to an active card; all other statuses must not set `published_card`.

For `development-agent-v1`, the sidecar must additionally bind all six labels:

```markdown
- Procedure Trigger: CLM-001
- Procedure Decision Inputs: CLM-002
- Procedure Option Relationship: CLM-003
- Procedure Selection Rules: CLM-004
- Procedure Required Artifacts: CLM-005
- Procedure Verification: CLM-006
```

Use supported claims for direct source facts. A development-Agent action derived
from those facts uses an inferred claim with a complete `inference_chain`.

For a published v1 candidate, bind the chosen design task, copied design goal,
required artifact types, and failure risks in the draft frontmatter. The
sidecar continues to bind the Procedure to source claims; map alignment and
proposal evidence remain in `derived/`, not in public cards.
