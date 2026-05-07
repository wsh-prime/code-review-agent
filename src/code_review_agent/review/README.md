# Review Module

## Responsibility

This module will own the AI-facing review pipeline. It will take diff chunks plus RepoMap and Hygiene context, ask for structured review issues, and aggregate the results.

## Current Status

Phase 2, Phase 4, Phase 5, Phase 6, Phase 7, Phase 8, Phase 10, Phase 11, and Phase 12 are implemented. The module can parse unified diffs, map diff hunks to changed Python entities, classify deterministic risk tags, build an evidence index, create rules-only findings, filter misreports, run fake hybrid agents, optionally call an OpenAI-compatible live reviewer, export prompts, and write the review report through the output module.

## Files

| File | Responsibility |
|---|---|
| `__init__.py` | Marks `review` as a Python package. |
| `diff_parser.py` | Parses unified diff / patch files into changed files and hunks. |
| `changed_entity.py` | Maps hunks to module/class/function/method entities using `RepoMap`. |
| `risk.py` | Emits deterministic `RiskSignal` objects from diff, RepoMap, changed entities, and optional hygiene classifications. |
| `evidence.py` | Builds `EvidencePackage` with stable evidence IDs for diff/entity/risk/test_discovery/hygiene signals. |
| `rules.py` | Converts high-signal risks into evidence-backed `ReviewIssue` objects. |
| `filter.py` | Validates evidence, downgrades weak findings, deduplicates issues, and records discarded candidates for JSON. |
| `agents.py` | Defines review/critic protocols, fake reviewer/critic strategies, and prompt export helpers. |
| `prompts/` | Stores fake review and critic prompt templates used by prompt export. |
| `pipeline.py` | Orchestrates rules-only, hybrid-fake, and hybrid-live review flows and delegates report formatting to `output/`. |

## Inputs

- Parsed diff chunks.
- RepoMap context.
- Hygiene classification data.
- Optional prebuilt `repo_map.json`.
- Optional `project_hygiene.json`.
- Optional `--mode hybrid-fake`, `--mode hybrid-live`, and `--export-prompts` settings.

## Outputs

- `DiffFileChange` objects.
- `ChangedEntity` objects.
- `RiskSignal` objects.
- `EvidencePackage` objects.
- `ReviewIssue` findings, `needs_human_review` items, and JSON-only `discarded` records.
- `review_report.json` / `review_report.md`.
- Optional prompt export files under `prompts/`.

## Not Responsible For

- Scanning project files for hygiene categories.
- Rendering Markdown or JSON output.
- Owning provider-specific API keys or secrets.

## Next Changes

- Post-MVP review orchestration such as separate live reviewer / critic models and GitHub PR comment publishing.
