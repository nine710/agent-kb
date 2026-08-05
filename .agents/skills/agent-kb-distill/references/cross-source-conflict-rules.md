# Cross-Source Conflict Rules

## Classify Before Resolving

Compare normalized claims, not source names or recommendations alone.

| Relationship | Use | Card treatment |
|---|---|---|
| `consistent` | Claims support the same conclusion. | Bind both when each adds relevant provenance. |
| `distinct-scope` | Claims differ because observable applicability conditions differ. | Keep conditioned options or rules; never state either as universal. |
| `superseded` | A versioned claim no longer governs. | Bind the current claim and record the superseding reference. |
| `unresolved` | Claims are incompatible in the same scope and no evidence resolves them. | Retain in the archive; withhold the candidate or affected field. |
| `no-overlap` | The candidate uses only its archive owner's claims. | Record the absence of a cross-source comparison. |

Do not call different design philosophies a factual conflict. For example,
“use callbacks when the external service can notify” and “poll when it cannot”
are `distinct-scope`, not competing universal recommendations. Do not resolve
an incompatible factual claim by choosing the more familiar vendor, the newer
file name, or the source that offers more code examples.

## Qualified Claims

- `CLM-NNN` means a claim in the source package currently being validated.
- `src-NNN/CLM-NNN` means a claim in a sibling package whose manifest declares
  that source ID.
- A draft using external claims lists every source in `source_ids` and lists
  the matching `XSR-NNN` records in `cross_source_review_refs`.
- A sidecar binds the exact qualified claim to the Option, Tradeoff, rule, or
  anti-pattern that uses it. Do not cite an entire source as a substitute.

## Review Record

`derived/cross-source-review.md` contains `candidate_id`, `status`,
`claim_refs`, and `resolution_basis` for every record. `distinct-scope` also
requires `scope_conditions`; `superseded` requires
`superseding_claim_ref`. A candidate with no external claim records
`no-overlap`.

The validator resolves external source packages and claims for published v1
drafts. It rejects missing packages or claims, omitted `source_ids`, missing
review records, unresolved reviews, and incomplete scoped or superseded
records. Drafts may remain incomplete while analysis is underway, but the
report must name every withheld candidate and unresolved relationship.
