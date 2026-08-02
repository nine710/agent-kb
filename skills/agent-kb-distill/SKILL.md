---
name: agent-kb-distill
description: Distill a human-selected project, document set, paper, PDF, HTML archive, or Markdown source into agent-kb decision cards. Use when a new source must be registered, analyzed, evidence-tracked, deduplicated against existing cards, and automatically published only after the repository's distillation gates pass.
---

# Agent KB Distill

Use this Skill only inside an `agent-kb` repository. Read `DECISION-MAP.md`, `SCHEMA.md`, `raw/sources.md`, existing `cards/`, `eval/benchmarks/development-agent/`, and the references below before creating or changing cards.

## Skill source and runtime mirror

- The canonical development source is `skills/agent-kb-distill/`.
- Codex discovers the project-scoped runtime mirror at `.agents/skills/agent-kb-distill/`.
- Edit and review the canonical source first. Do not edit the runtime mirror directly.
- After the source is confirmed, run `python scripts/sync_project_skill.py check`, then `python scripts/sync_project_skill.py sync`, and run `check` again before using the refreshed Skill.

## Boundaries

- Accept a source selected by a human. Do not autonomously add a new external source.
- Keep upstream files unchanged in `raw/src-NNN-<slug>/source/`.
- Do not run Git commands. Git is project workflow, not Skill behavior.
- Do not publish a card that fails any gate. Retain its draft and evidence sidecar with status `raw-only`, `out-of-scope`, or `rejected`; use `published` for a card that passes all gates. A candidate merged into an existing card still gets a `published` archive record pointing to that card.
- Never delete a draft or evidence sidecar after a status transition. `drafts/` is a permanent local audit archive and remains Git-ignored.
- Every distillation run must read and analyze the entire selected source boundary again. This applies to a first distillation, re-distillation, card refresh, Skill/schema change, and benchmark change. Previous cards, drafts, evidence ledgers, reports, and source fingerprints never substitute for the current run's full reading.
- Inventory every item in the selected material package before reading. Read every readable in-scope item from first to last; record any excluded auxiliary or duplicate format, its reason, and any cross-check performed in the manifest and report.

## Workflow

1. Read [source intake rules](references/source-intake-rules.md). Register or reuse a `src-NNN`; create `source/`, `derived/`, and `excerpts/`, then create `drafts/<source_id>/` for the source's permanent archive. Start a new distillation run record even when the source ID and input fingerprint are unchanged.
2. Create or revalidate `derived/manifest.md`, `inventory.md`, and `progress.md` from the templates. Inventory every source unit and assign an extraction reliability rating before reading; do not inherit prior completion as proof of current-run reading.
3. Follow [extraction and locator rules](references/extraction-and-locator-rules.md). Preserve source locations; do not let low-reliability text independently support publication.
4. In this run, read all inventoried, in-scope units from first to last. Write or refresh one claim per row in `derived/evidence-ledger.md` using [the ledger schema](references/evidence-ledger-schema.md). Prior ledgers may be used for continuity comparison only, never as the sole evidence of current-run reading.
5. Align all in-scope claim groups to `DECISION-MAP.md` before discovering candidates. Create `derived/decision-map-alignment.md`; source chapters never determine cards by themselves.
6. Read applicable tasks in `eval/benchmarks/development-agent/` and identify decisions, required artifacts, and failure risks that current cards do not cover. Treat these tasks as the demand signal; do not invent a candidate only because a chapter has a named concept.
7. Create `derived/map-change-proposals.md` and `derived/card-review.md`. Claims that cannot fit a Core task need an add/split/merge/exclude proposal; reassess every affected active card as keep, update, split, merge, or deprecate.
8. Create `derived/candidate-problems.md` using [the candidate schema](references/candidate-problem-schema.md). Every candidate identifies its Core design task or an explicit emerging/excluded mapping reason, its `card_type` (`atomic-decision` or `composition-strategy`), and applicable independent benchmark task IDs. Compare every candidate against existing cards semantically.
9. For every candidate, create `drafts/<source_id>/<candidate-id>-<slug>.md` and its matching `.evidence.md` sidecar using [draft binding rules](references/draft-evidence-binding.md). Set the lifecycle status to `draft` while analysis is incomplete; use `raw-only`, `out-of-scope`, or `rejected` with a decision reason when a candidate is withheld.
10. For a candidate targeting `development-agent-v1`, perform the Development-Agent adaptation stage: define consumer, card type, decision scope, option relationship, design-task binding, all six Procedure fields, and evidence bindings. Create one public `typical`, `boundary`, and `anti-pattern` evaluation task under `eval/development-agent/<card-id>/`. A reviewer must record a real development-Agent answer against every task rubric before `review_status: pass` is valid; these tasks do not prove independent utility.
11. Apply [publication gates](references/publication-gates.md). Only a `published` draft may produce or update a file in `cards/`; set its `published_card` link after the active card exists. A published v1 card starts with `utility_status: unverified` unless at least three applicable independent benchmark tasks have a recorded baseline-versus-card comparison. Run both validation commands before treating the source as complete:

   ```text
   python scripts/validate_distillation.py <source-package> --drafts drafts --cards cards
   python scripts/validate_card.py --all
   ```

12. Write `derived/distillation-report.md`. Include decision-map coverage and changes, benchmark task gaps, existing-card review decisions, published cards, consumer contract/readiness, utility status, all withheld candidates, archive paths, conflicts, reliability issues, and source suggestions.

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

## Development-Agent adaptation

`decision-card-v0` is a valid transitional decision card. A
`development-agent-v1` card is a direct execution reference for a programming
Agent and must include:

1. `consumer: development-agent`, a valid decision scope, `card_type` set to
   `atomic-decision` or `composition-strategy`, `utility_status`, and an
   explicit option relationship;
2. Development Agent Procedure fields: Trigger, Decision Inputs, Option
   Relationship, Selection Rules, Required Artifacts, and Verification;
3. six matching `Procedure ...` labels in the local evidence sidecar;
4. three reviewed public tasks under `eval/development-agent/<card-id>/`.

Direct procedure facts require supported claims. An engineering action that is
derived from source facts must bind to an inferred claim with a complete
`inference_chain`; do not present it as a direct source conclusion. Do not mark
a v1 task as passed merely because it exists: the Review Record must reflect a
development Agent's actual answer and reviewer scoring. Conversely, a passing
card-specific task is not an independent utility result. Set
`utility_status: validated` only after at least three applicable independent
benchmark tasks compare a no-card baseline with the card-enabled result and
show a documented, non-trivial improvement without a critical regression.

## Decision-map discipline

- Start from a development responsibility in `DECISION-MAP.md`, then ask which source claims support reusable problems below it. Do not turn a chapter title, model term, or algorithm name into a card merely because it appears in the material.
- A candidate must state its trigger, design goal, required artifacts, independent failure risks, true options, and deduplication conclusion.
- A new long-lived responsibility is a map proposal, not an automatic Core task. It needs source claims, an explanation of why it cannot fit an existing task, independent artifacts and risks, at least two child-problem candidates, and a maturity statement.
- Keep `emerging` and `excluded` discoveries in local archives. Only a Core task may be referenced by a formal v1 card.

## Resume

Read `derived/progress.md` before work. `last_locator` may resume an interrupted read only within the same explicitly identified run; it does not waive the full-material rule for a new run. A new run reads from the first unit through the last even when the source fingerprint is unchanged. Fingerprints identify the input version only; they do not prove that the current run read or analyzed the material. Do not silently replace claim IDs; append the run ID and record claims as confirmed, changed, or withdrawn.

## Resources

- [Source intake](references/source-intake-rules.md)
- [Extraction and locators](references/extraction-and-locator-rules.md)
- [Evidence ledger](references/evidence-ledger-schema.md)
- [Candidate problems](references/candidate-problem-schema.md)
- [Draft evidence binding](references/draft-evidence-binding.md)
- [Publication gates](references/publication-gates.md)
