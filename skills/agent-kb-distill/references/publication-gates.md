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

When a gate fails, keep the result out of `cards/` and record its status and reason in the candidate queue and report.
