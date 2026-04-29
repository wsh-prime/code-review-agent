# Examples

## Responsibility

This directory contains demo repositories and sample patches used to show the project end to end.

## Current Status

Phase 0 includes `demo_repo/` as a placeholder repository and `demo.patch` for CLI argument validation.

## Files

| File or Directory | Responsibility |
|---|---|
| `demo_repo/` | Placeholder demo repository for CLI validation now; later a full reviewable fixture. |
| `demo_repo/README.md` | Explains the current placeholder demo repository. |
| `demo_repo/demo.patch` | Minimal patch used by the Phase 0 placeholder review command. |

## Inputs

- Local CLI commands.
- Future sample source files, scripts, docs, and patches.

## Outputs

- Reproducible demo inputs for manual and automated verification.
- Future report examples under `outputs/` when explicitly generated.

## Not Responsible For

- Unit test assertions; those belong in `tests/`.
- Benchmark-grade datasets; those belong in `eval/`.
- Core implementation logic.

## Next Changes

- Expand `demo_repo/` with main code, tests, temporary scripts, prompt experiments, todo docs, design docs, and a reviewable patch.

