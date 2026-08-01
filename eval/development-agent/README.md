# Development-Agent Evaluation Tasks

Each `development-agent-v1` card has exactly three public tasks under
`eval/development-agent/<card-id>/`: one `typical`, one `boundary`, and one
`anti-pattern` task. They test whether a programming Agent can use the card to
make and verify a design decision.

Every task requires this frontmatter:

```yaml
card_id: card-id
task_id: card-id-001
difficulty: typical | boundary | anti-pattern
review_status: pass | fail
reviewer: reviewer identity
reviewed_at: YYYY-MM-DD
```

Every task must contain these sections: Project Background, Development Goal,
Known Constraints, Expected Trigger, Acceptable Decision, Required Artifacts,
Required Verification, Failure Conditions, Rubric, and Review Record.

The Rubric and Review Record each contain all seven IDs:

- `trigger-recognition`
- `decision-inputs`
- `option-relationship`
- `selection`
- `artifacts`
- `verification`
- `anti-pattern`

Review results are `pass`, `partial`, or `fail`. A task passes only when
`trigger-recognition`, `option-relationship`, `selection`, and `verification`
are not `fail`, and no more than one of the remaining criteria is `partial`.
`review_status: pass` is written only after a development Agent has answered
the task and a reviewer has recorded the results; task creation alone is not
evidence of card consumption.
