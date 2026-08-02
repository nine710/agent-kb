# Independent Development-Agent Benchmark

This directory contains design tasks that are independent of the public card
tasks under `eval/development-agent/<card-id>/`.

The card-specific tasks check whether an Agent can follow a card's Procedure.
These benchmark tasks check whether a card improves an Agent's design result on
an unfamiliar project brief. They must not name a card, prescribe an option, or
include an `Acceptable Decision` section.

The pilot contains one typical task for each Core responsibility. The next
stage adds one boundary task for each responsibility. A card can receive
`utility_status: validated` only after it has at least three applicable
benchmark tasks and a recorded baseline-versus-card comparison.

Validate the pilot with:

```text
python scripts/validate_benchmark.py eval/benchmarks/development-agent
```
