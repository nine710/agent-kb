---
name: agent-kb-distill
description: Distill a human-selected project, document set, paper, PDF, HTML archive, or Markdown source into agent-kb decision cards. Use when a new source must be registered, analyzed, evidence-tracked, deduplicated against existing cards, and automatically published only after the repository's distillation gates pass.
---

# Agent KB Distill

Use this Skill only inside an `agent-kb` repository. Read `SCHEMA.md`, `raw/sources.md`, existing `cards/`, and the references below before creating or changing cards.

## Boundaries

- Accept a source selected by a human. Do not autonomously add a new external source.
- Keep upstream files unchanged in `raw/src-NNN-<slug>/source/`.
- Do not run Git commands. Git is project workflow, not Skill behavior.
- Do not publish a card that fails any gate. Retain its draft and evidence sidecar with status `raw-only`, `out-of-scope`, or `rejected`; use `published` for a card that passes all gates. A candidate merged into an existing card still gets a `published` archive record pointing to that card.
- Never delete a draft or evidence sidecar after a status transition. `drafts/` is a permanent local audit archive and remains Git-ignored.

## Workflow

1. Read [source intake rules](references/source-intake-rules.md). Register or reuse a `src-NNN`; create `source/`, `derived/`, and `excerpts/`, then create `drafts/<source_id>/` for the source's permanent archive.
2. Create `derived/manifest.md`, `inventory.md`, and `progress.md` from the templates. Inventory every source unit and assign an extraction reliability rating.
3. Follow [extraction and locator rules](references/extraction-and-locator-rules.md). Preserve source locations; do not let low-reliability text independently support publication.
4. Read all inventoried, in-scope units. Write one claim per row in `derived/evidence-ledger.md` using [the ledger schema](references/evidence-ledger-schema.md).
5. Create `derived/candidate-problems.md` using [the candidate schema](references/candidate-problem-schema.md). Compare every candidate against existing cards semantically.
6. For every candidate, create `drafts/<source_id>/<candidate-id>-<slug>.md` and its matching `.evidence.md` sidecar using [draft binding rules](references/draft-evidence-binding.md). Set the lifecycle status to `draft` while analysis is incomplete; use `raw-only`, `out-of-scope`, or `rejected` with a decision reason when a candidate is withheld.
7. Apply [publication gates](references/publication-gates.md). Only a `published` draft may produce or update a file in `cards/`; set its `published_card` link after the active card exists. Run both validation commands before treating the source as complete:

   ```text
   python scripts/validate_distillation.py <source-package> --drafts drafts --cards cards
   python scripts/validate_card.py --all
   ```

8. Write `derived/distillation-report.md`. Include coverage, published cards, all withheld candidates, archive paths, conflicts, reliability issues, and source suggestions.

## Archive lifecycle

Every candidate has exactly one draft and one evidence sidecar under
`drafts/<source_id>/`. Draft frontmatter must include `source_id`,
`candidate_id`, and one of these statuses:

| Status | Use |
|---|---|
| `draft` | Still being analyzed or reviewed |
| `published` | Passed gates and points to an active `cards/` file via `published_card` |
| `raw-only` | Fails the genuine-three-options threshold; record the concrete reason |
| `out-of-scope` | Does not belong in this knowledge base; record the scope reason |
| `rejected` | Fails another quality or provenance rule; record the rejection reason |

The validator checks the candidate/archive one-to-one relationship, sidecar
bindings, lifecycle-specific fields, and active-card links. Failed validation
retains all artifacts and reports the source, candidate, file, and rule.

## Resume

Read `derived/progress.md` before work. Resume from `last_locator`; do not silently replace claim IDs or completed work. Re-run downstream stages only when the recorded source fingerprint changes.

## Resources

- [Source intake](references/source-intake-rules.md)
- [Extraction and locators](references/extraction-and-locator-rules.md)
- [Evidence ledger](references/evidence-ledger-schema.md)
- [Candidate problems](references/candidate-problem-schema.md)
- [Draft evidence binding](references/draft-evidence-binding.md)
- [Publication gates](references/publication-gates.md)
