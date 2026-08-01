# Draft Evidence Binding

For every candidate, create one archive pair under
`drafts/<source_id>/<candidate-id>-<slug>.md` and
`drafts/<source_id>/<candidate-id>-<slug>.evidence.md`.

The draft frontmatter must contain:

```yaml
source_id: src-NNN
candidate_id: CAND-NNN
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
