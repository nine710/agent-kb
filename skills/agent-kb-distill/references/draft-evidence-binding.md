# Draft Evidence Binding

For every `drafts/<card-id>.md`, create `drafts/<card-id>.evidence.md`.

The sidecar maps each Option, Tradeoff row, application rule, and Anti-Pattern to ledger claims:

```markdown
# Evidence Binding: <card-id>

- source_id: src-NNN
- candidate_id: CAND-NNN

- Option A: CLM-001, CLM-004
- Tradeoff A advantage: CLM-004
- Tradeoff A cost: CLM-006
- Apply rule 1: CLM-007
- Anti-pattern 1: CLM-009
```

Options require `supported` claims. Inferred claims may support derived rules only when their `inference_chain` is complete. A sidecar is required for every draft but is not copied into `cards/`.
