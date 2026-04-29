# Output Module

## Responsibility

This module owns user-facing and machine-readable report generation for review results.

## Current Status

Phase 12 implemented. Stable JSON and Markdown renderers are used by the review pipeline; JSON now includes filter and fake-agent audit fields while Markdown stays concise.

## Files

| File | Responsibility |
|---|---|
| `__init__.py` | Exports report formatting helpers. |
| `json_report.py` | Normalizes and serializes stable `review_report.json` with schema version `1.1`. |
| `review_markdown.py` | Renders `review_report.md` with fixed review sections. |

## Inputs

- Review report dictionaries produced by `review/pipeline.py`.
- Output file path for JSON writing.
- JSON-only filter and fake-agent audit data such as `discarded`, `agent_runs`, and `prompt_exports`.

## Outputs

- `review_report.md`.
- `review_report.json`.
- Stable section order for README-friendly report snippets.
- JSON fields for `discarded`, `agent_runs`, and `prompt_exports`.

## Not Responsible For

- Deciding whether an issue is valid.
- Running LLM calls.
- Scanning or classifying files.
- Mutating the reviewed repository.

## Next Changes

- Keep Markdown concise enough for README snippets and demos.
- Add eval report output when Phase 13 lands.
