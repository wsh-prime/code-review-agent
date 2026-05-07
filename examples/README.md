# Examples

## Responsibility

This directory contains demo repositories and sample patches used to show the project end to end.

## Current Status

Phase 14 includes a reviewable `demo_repo/` shop project and `eval_cases/` benchmark fixtures for deterministic evaluation.

## Files

| File or Directory | Responsibility |
|---|---|
| `demo_repo/` | Small Python shop project used by map, hygiene, and review demos. |
| `demo_repo/patches/` | Reviewable demo patches covering findings and no-finding cases. |
| `demo_repo/demo.patch` | Compatibility alias for the test-gap demo patch. |
| `eval_cases/` | Full planted-bug benchmark with patches, ground truth, and a shared demo repo. |

## Inputs

- Local CLI commands.
- Demo source files, scripts, docs, and patches.

## Outputs

- Reproducible demo inputs for manual and automated verification.
- Benchmark inputs for `code-review-agent eval`.
- Report examples under `outputs/` only when explicitly generated.

## Not Responsible For

- Unit test assertions; those belong in `tests/`.
- Core eval implementation logic; that belongs in `src/code_review_agent/eval/`.
- Core implementation logic.

## Next Changes

- Keep demo patches aligned with README commands and eval fixtures.
