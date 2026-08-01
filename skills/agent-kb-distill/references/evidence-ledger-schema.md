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

`inferred` claims require at least one supporting claim ID. Preserve `unsupported` and `conflict` rows; they explain why a candidate was withheld.
