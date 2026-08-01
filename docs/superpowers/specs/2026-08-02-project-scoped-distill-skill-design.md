# Project-Scoped Distillation Skill Design

## Goal

Make `agent-kb-distill` callable by Codex only when the current workspace is
this repository. The skill must not be installed in a user-level skill
directory or become available to unrelated repositories.

## Architecture

`.agents/skills/agent-kb-distill/` is the sole canonical skill directory.
Codex discovers repository skills from `.agents/skills` while working in this
repository. The existing `skills/agent-kb-distill/` directory is moved there;
it is not copied or linked.

This keeps the skill's `SKILL.md`, `agents/`, `references/`, and `templates/`
together as one version-controlled unit. Repository documentation that names
the old path is updated to point to the canonical project-level path.

## Scope And Data Flow

When a Codex task opens in `E:\ai\agent-kb`, discovery reads
`.agents/skills/agent-kb-distill/SKILL.md` and exposes `agent-kb-distill` to
that task. The skill continues to create and validate the same private source
packages, drafts, and public cards described by its current workflow.

No files are created under `C:\Users\lizongke\.agents\skills`,
`C:\Users\lizongke\.codex\skills`, or any other user-level skill location.
No Windows directory junctions or duplicated skill trees are used.

## Migration Steps

1. Move the complete skill directory to `.agents/skills/agent-kb-distill/`.
2. Update repository references from `skills/agent-kb-distill/` to the new
   project-scoped path.
3. Verify no stale source directory or duplicate `SKILL.md` remains.
4. Verify the card and distillation validators still pass.
5. Reload the Codex task or open a new task rooted at this repository, then
   verify that `agent-kb-distill` is listed and can be invoked.

## Error Handling

If a running Codex task does not refresh its skill catalogue after the
migration, the repository files remain correct; reopening the task is the
required discovery refresh. A missing skill after reopening is treated as a
configuration defect and investigated before card regeneration begins.

## Acceptance Criteria

- The only in-repository `agent-kb-distill/SKILL.md` is below
  `.agents/skills/`.
- All repository documentation uses the new path.
- `python scripts/validate_card.py --all` passes.
- `python scripts/validate_distillation.py raw/src-001-ai-agent-book --drafts drafts --cards cards` passes.
- A newly loaded Codex task in this repository exposes `agent-kb-distill`.
- A Codex task in an unrelated repository does not receive this skill through
  a user-level installation.
