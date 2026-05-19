# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 1
- Changed entities: 1
- Risk signals: 0
- Findings: 0
- Needs human review: 0
- Discarded: 0
- Agent runs: 3
- Loop enabled: True
- Target repo modified: False

## Loop Summary

| Metric | Value |
|---|---:|
| Iterations | 1 / 1 |
| Converged | True |
| Fallback | False |
| Retry count | 0 |
| Total latency | 11346 ms |
| Token in | 2563 |
| Token out | 228 |

- Iteration 0: 0 candidates, 0 verified, 0 uncertain, 0 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `file_risk_shards_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 1063 |
| Selected evidence | 4 |
| Omitted evidence | 0 |
| Context truncated | True |
| Review shards | 1 |
| Context requests | 2 |
| Refills | 1 |

## Findings

No findings.

Checked changed files, changed entities, deterministic risk signals, and evidence references. No high-confidence review finding was produced.

## Needs Human Review

None.

## Changed Files

- `gpt_engineer/main.py` (modified)

## Changed Entities

- `gpt_engineer/main.py:1-2` module `gpt_engineer.main`

## Risk Signals

None.

## Evidence Index

- `diff:gpt_engineer/main.py:1` [diff]: gpt_engineer/main.py:1
- `diff:gpt_engineer/main.py:2` [diff]: gpt_engineer/main.py:2
- `diff_hunk:gpt_engineer/main.py:1` [diff_hunk]: gpt_engineer/main.py:1
- `entity:gpt_engineer/main.py:gpt_engineer.main` [entity]: gpt_engineer/main.py:1-2
