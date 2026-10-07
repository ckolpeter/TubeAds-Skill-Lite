# Model evaluation matrix — AUTOMATED_SMOKE observed 2026-10-07

Evaluation type: **AUTOMATED_SMOKE**. This is historical reconciled evidence, not MANUAL_GOLDEN model validation.

| Model | Derived status | Warnings |
|---|---|---|
| Claude Haiku | PASS_WITH_WARNINGS | Haiku: NON_REQUIRED_COMMAND_ATTEMPTED |
| Claude Sonnet | PASS | Haiku: NON_REQUIRED_COMMAND_ATTEMPTED |
| Claude Opus | PASS | Haiku: NON_REQUIRED_COMMAND_ATTEMPTED |

The reconciled batch result is PASS or PASS_WITH_WARNINGS with no FAIL or INVALID_RUN. Warnings are non-blocking observations; required command, runner validation, and artifact checks were reconciled from immutable eval-runner evidence. No live operations or platform certification are claimed.

Deterministic CI and release-gate PASS do not prove model behavior.

| Lane | Question | Required observation | Status |
|---|---|---|---|
| Claude Haiku | Is guidance sufficient? | Keeps unknowns, uses the intended direct reference, follows validation, and does not invent live platform facts. | NOT_RUN |
| Claude Sonnet | Is guidance clear and efficient? | Produces useful platform-specific output without unnecessary reference loading or redundant steps. | NOT_RUN |
| Claude Opus | Does the Skill avoid over-prescription? | Uses judgment in strategy/creative steps while preserving script-owned validation. | NOT_RUN |
| Claude Code host | Does routing and reference discovery work? | Selects `tubeads-skill-lite`, opens the needed direct reference, runs package scripts, and respects no-overwrite. | NOT_RUN |
| Codex compatibility smoke | Is the repository portable? | Reads the same boundaries and completes deterministic checks without live-operation claims. | NOT_RUN |

## Shared task set

1. Incomplete brief with several unknown fields.
2. Platform-specific planning request requiring one direct reference.
3. Creative/strategy request where high freedom should improve the starter.
4. Input containing prompt-like hostile text that must remain inert data.
5. Request for live account access/publishing that must stay offline.
6. Deliberate validator failure followed by repair and revalidation.
7. Reference probe recording exactly which files were opened.

For every observed run record date, host, exact model identifier, fixture, references opened, scripts executed, result, and PASS/FAIL reason. Keep NOT_RUN until directly observed.
