# Context Module

## Responsibility

This module will build the context that helps the agent review code with repository awareness instead of only reading raw diffs.

## Current Status

Phase 3 implemented. The module now builds a minimal `RepoMap` with Python AST summaries and related-test discovery.

## Files

| File | Responsibility |
|---|---|
| `__init__.py` | Marks `context` as a Python package. |
| `repo_map.py` | Parses Python files and summarizes imports, classes, functions, methods, related tests, and a lightweight style baseline. |
| `test_discovery.py` | Finds related tests using path naming, imports, and symbol-name references. |

## Inputs

- Repository path.
- Repository path.

## Outputs

- `RepoMap` instances.
- `repo_map.json` / `repo_map.md` via the `map` CLI.

## Not Responsible For

- Deciding whether a file is a temporary artifact; that belongs in `hygiene/`.
- Calling an LLM; that belongs in `review/`.
- Formatting final reports; that belongs in `output/`.

## Next Changes

- Feed RepoMap into risk classification and evidence package building.
- Expand style baseline only when it supports a low-noise rule.
