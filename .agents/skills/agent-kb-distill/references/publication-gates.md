# Publication Gates

Publish only after all gates pass:

1. The card passes `scripts/validate_card.py`.
2. The source package and draft sidecars pass `scripts/validate_distillation.py`.
3. The problem is reusable and non-summary.
4. The card has at least three genuinely different options.
5. Every Option has direct `supported` evidence.
6. Derived Tradeoffs, application rules, and Anti-Patterns have a complete inference chain.
7. No published field relies on `unsupported`, unresolved `conflict`, or a low-reliability claim.
8. The candidate has a completed semantic deduplication decision.
9. The card contains no personal project experience.
10. Sources expose stable, human-readable locations.
11. A `development-agent-v1` card has consumer metadata, all six Procedure fields, six Procedure evidence bindings, and exactly three reviewed public evaluation tasks.
12. Every v1 evaluation task has a real reviewed Agent response; critical rubric items do not fail and at most one non-critical item is partial.
13. The source package contains decision-map alignment, map-change proposal, and existing-card review archives.
14. Every publishable v1 candidate and card binds a Core design task, allowed artifacts, and allowed failure risks.
15. A new or split Core task has complete independent-responsibility evidence; otherwise it remains Emerging or Excluded.
16. A `material_contract_version: v1` package has a valid material profile, finite boundary, reproducible snapshot, provenance, material state, profile references, and input fingerprint.
17. Every included v1 inventory unit has the required profile, role, version-aware locator, read method, quality check, reliability, and completion/blocking status.
18. A v1 published binding has a permitted content role and non-auxiliary source position; it cannot rely on `unresolved` conflict status.
19. A `github-repository` v1 package records a human-provided repository URL and commit and is `upstream-clean`; a local overlay must be outside the source boundary.
20. PDF/DOCX claims that depend on tables, diagrams, code samples, or layout include a recorded visual cross-check. Low-reliability material cannot independently support publication.
21. A v1 candidate using more than one source declares all `source_ids` and matching `cross_source_review_refs`. Every qualified claim resolves to a sibling source package and ledger claim.
22. A published v1 binding cannot rely on a missing, unreviewed, or `unresolved` cross-source claim; `distinct-scope` requires scope conditions and `superseded` requires a superseding claim reference.

When a gate fails, keep the result out of `cards/`, retain the draft and evidence sidecar, and record `raw-only`, `out-of-scope`, or `rejected` plus a concrete `decision_reason` in the archive, candidate queue, and report. A candidate already covered by an existing active card is archived as `published` with a `published_card` link.
