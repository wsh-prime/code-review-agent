# Hygiene Module

## Responsibility

This module owns Project Hygiene Review. It scans a repository, classifies files by role, and generates safe organization suggestions without modifying the target repository by default.

## Current Status

Phase 1 is implemented. The module can scan repositories, classify files with deterministic signals, generate safe move suggestions, and render a `PROJECT_ARTIFACTS.md` draft.

## Files

| File | Responsibility |
|---|---|
| `__init__.py` | Exports the Phase 1 hygiene scanner, classifier, and planner helpers. |
| `scanner.py` | Scans repository files while ignoring cache, build, virtualenv, large, and binary-like paths. |
| `classifier.py` | Classifies files as `main_code`, `test_code`, `data_script`, `experiment`, `todo`, and related categories with signals. |
| `planner.py` | Generates safe `MoveSuggestion` entries and a `PROJECT_ARTIFACTS.md` draft. |

## Inputs

- Repository path.
- Ignore rules.
- File metadata and lightweight content snippets.
- Optional changed file list in later phases.

## Outputs

- `FileClassification` objects.
- `MoveSuggestion` objects.
- `PROJECT_ARTIFACTS.md` draft content.

## Not Responsible For

- Moving files automatically in MVP mode.
- Fixing imports after a move.
- Running lint, tests, or type checks.
- Reviewing code correctness with an LLM.

## Next Changes

- Expose this module through a dedicated `hygiene` CLI command.
- Add semantic taxonomy and optional LLM classification after `summary` exists.
- Feed hygiene classifications into future `review` context and risk assembly.
