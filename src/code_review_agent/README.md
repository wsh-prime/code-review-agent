# Code Review Agent Package

## Responsibility

This package contains the executable Python code for the Code Review Agent Toolkit. It owns the CLI entry point, shared data models, and subsystem packages for summary generation, hygiene scanning, context building, review orchestration, and report output.

## Current Status

Phase 14 is implemented. The package now has `map`, `hygiene`, `review`, and `eval` workflows, including rules-only, hybrid-fake, and optional hybrid-live review modes, full planted-bug eval metrics, stable report output, a formal review filter, and fake agent prompt export.

## Files

| File or Directory | Responsibility |
|---|---|
| `__init__.py` | Exports shared data models as the package-level public API. |
| `__main__.py` | Supports `python -m code_review_agent` by forwarding to the CLI main function. |
| `cli.py` | Defines the command line interface for `map`, `hygiene`, `review`, and `eval`. |
| `models.py` | Defines shared dataclasses used across scanner, planner, RepoMap, review, and report modules. |
| `context/` | Owns RepoMap and diff-aware context construction. |
| `hygiene/` | Owns Project Hygiene Review scanning, classification, and move planning. |
| `review/` | Owns diff parsing, changed entity extraction, risk classification, evidence packaging, rules-only findings, filtering, fake agents, and review orchestration. |
| `output/` | Owns Markdown and JSON report formatting. |
| `eval/` | Owns deterministic eval case loading, benchmark running, and metrics. |

## Inputs

- CLI arguments from users.
- Repository paths and diff paths.
- Optional repo map and hygiene output files.
- Shared model instances passed between subsystems.

## Outputs

- CLI exit codes and human-readable command output.
- Shared model objects for downstream report generation.
- `project_hygiene.json` and `PROJECT_ARTIFACTS.md` from hygiene.
- `repo_map.json` / `repo_map.md` from map.
- `review_report.json` / `review_report.md` from review.
- `metrics.json` / `case_results.json` / `eval_report.md` from eval.
- Optional review prompt exports under `prompts/` when `--export-prompts` is used.

## Not Responsible For

- Benchmark datasets; those belong in `examples/eval_cases`.
- Test fixtures and validation cases; those belong in `tests` and `examples`.
- Project-level roadmap and design documents; those belong in `docs`.

## Next Changes

- Post-MVP integrations such as GitHub PR comments, auto-fix, MCP tools, and multi-language analyzers.
