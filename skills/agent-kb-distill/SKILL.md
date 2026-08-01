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
- Do not publish a card that fails any gate. Record it as `raw-only`, `merge-with-existing`, `evidence-only`, or `out-of-scope` instead.

## Workflow

1. Read [source intake rules](references/source-intake-rules.md). Register or reuse a `src-NNN`; create `source/`, `derived/`, and `excerpts/`.
2. Create `derived/manifest.md`, `inventory.md`, and `progress.md` from the templates. Inventory every source unit and assign an extraction reliability rating.
3. Follow [extraction and locator rules](references/extraction-and-locator-rules.md). Preserve source locations; do not let low-reliability text independently support publication.
4. Read all inventoried, in-scope units. Write one claim per row in `derived/evidence-ledger.md` using [the ledger schema](references/evidence-ledger-schema.md).
5. Create `derived/candidate-problems.md` using [the candidate schema](references/candidate-problem-schema.md). Compare every candidate against existing cards semantically.
6. For a publishable candidate, create `drafts/<card-id>.md` and its required `drafts/<card-id>.evidence.md` sidecar using [draft binding rules](references/draft-evidence-binding.md).
7. Apply [publication gates](references/publication-gates.md). Run both validation commands before moving a draft into `cards/`:

   ```text
   python scripts/validate_distillation.py <source-package> --drafts drafts --cards cards
   python scripts/validate_card.py --all
   ```

8. Write `derived/distillation-report.md`. Include coverage, published cards, withheld candidates, conflicts, reliability issues, and source suggestions.

## Resume

Read `derived/progress.md` before work. Resume from `last_locator`; do not silently replace claim IDs or completed work. Re-run downstream stages only when the recorded source fingerprint changes.

## Resources

- [Source intake](references/source-intake-rules.md)
- [Extraction and locators](references/extraction-and-locator-rules.md)
- [Evidence ledger](references/evidence-ledger-schema.md)
- [Candidate problems](references/candidate-problem-schema.md)
- [Draft evidence binding](references/draft-evidence-binding.md)
- [Publication gates](references/publication-gates.md)
