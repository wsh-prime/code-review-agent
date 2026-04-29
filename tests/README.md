# Tests

## Responsibility

This directory contains automated tests that protect the CLI, shared models, and subsystem behavior.

## Current Status

Phase 1 tests are present for the CLI, shared dataclass models, and Project Hygiene Review scanner/classifier/planner behavior.

## Files

| File | Responsibility |
|---|---|
| `test_cli.py` | Verifies CLI help and the Phase 1 `review` command output behavior. |
| `test_models.py` | Verifies shared dataclass construction and `to_dict()` output. |
| `test_hygiene_scanner.py` | Validates scanner ignore rules and text sample metadata. |
| `test_hygiene_classifier.py` | Validates file classification rules and mainline import protection. |
| `test_hygiene_planner.py` | Validates move suggestions, target conflict handling, and read-only behavior. |
| `test_diff_parser.py` | Planned: validate unified diff parsing. |
| `test_repo_map.py` | Planned: validate Python symbol and import extraction. |

## Inputs

- Source modules under `src/code_review_agent/`.
- Demo fixtures under `examples/`.
- Temporary directories created by pytest fixtures.

## Outputs

- pytest pass/fail results.
- Regression coverage for public behavior.

## Not Responsible For

- Manual demo scripts.
- Benchmark datasets or metrics.
- Production report output.

## Next Changes

- Update CLI tests for `summary`, `hygiene`, and `review` command routing.
- Add `summary` tests once the summary module is introduced.
- Keep tests read-only unless a test uses an isolated temporary directory.
