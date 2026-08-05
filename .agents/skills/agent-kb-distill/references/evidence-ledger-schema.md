# Evidence Ledger Schema

Use one table row per verifiable claim.

| Field | Rule |
|---|---|
| `claim_id` | Stable `CLM-NNN` identifier; never reuse an ID for a different claim |
| `claim` | Atomic factual or design claim, not a paragraph summary |
| `locator` | Stable source location from the extraction rules |
| `support_status` | `supported`, `inferred`, `unsupported`, or `conflict` |
| `reliability` | `high`, `medium`, or `low` |
| `candidate_refs` | Candidate IDs that may use the claim |
| `card_refs` | Draft field labels that use the claim |
| `inference_chain` | Supporting claim IDs required for an inferred claim |
| `content_role` | Inventory role: `documentation`, `implementation`, `test`, `example`, `generated`, `binary`, `metadata`, or `auxiliary` |
| `source_position` | `primary`, `corroborating`, or `auxiliary` evidence position |
| `conflict_status` | `none`, `version-drift`, `distinct-scope`, `documentation-defect`, `test-implementation-mismatch`, or `unresolved` |

`inferred` claims require at least one supporting claim ID. Preserve `unsupported` and `conflict` rows; they explain why a candidate was withheld.

For a v1 material package, copy `content_role` from the inventory unit. Documentation supports stated intent and tradeoffs; implementation supports observed behavior; tests support asserted behavior; examples are illustrative only. Generated, binary, metadata, and auxiliary material cannot independently support publication. Preserve source disagreements as separate claims and classify them in `conflict_status`; do not use an `unresolved` claim in a published field. Cross-source references use `src-NNN/CLM-NNN` in candidates and sidecars; their relationship is recorded separately in `derived/cross-source-review.md`.
