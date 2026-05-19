# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 1
- Changed entities: 1
- Risk signals: 0
- Findings: 0
- Needs human review: 0
- Discarded: 1
- Agent runs: 2
- Loop enabled: True
- Target repo modified: False

## Loop Summary

| Metric | Value |
|---|---:|
| Iterations | 1 / 1 |
| Converged | True |
| Fallback | False |
| Retry count | 2 |
| Total latency | 124217 ms |
| Token in | 1614 |
| Token out | 164 |

- Iteration 0: 1 candidates, 0 verified, 0 uncertain, 0 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `risk_first_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 790 |
| Selected evidence | 1 |
| Omitted evidence | 10 |
| Context truncated | True |
| Review shards | 1 |
| Context requests | 0 |
| Refills | 0 |

## Findings

No findings.

Checked changed files, changed entities, deterministic risk signals, and evidence references. No high-confidence review finding was produced.

## Needs Human Review

None.

## Changed Files

- `gpt_engineer/main.py` (modified)

## Changed Entities

- `gpt_engineer/main.py:1-35` module `gpt_engineer.main`

## Risk Signals

None.

## Evidence Index

- `diff:gpt_engineer/main.py:1` [diff]: gpt_engineer/main.py:1
- `diff:gpt_engineer/main.py:16` [diff]: gpt_engineer/main.py:16
- `diff:gpt_engineer/main.py:17` [diff]: gpt_engineer/main.py:17
- `diff:gpt_engineer/main.py:24` [diff]: gpt_engineer/main.py:24
- `diff:gpt_engineer/main.py:25` [diff]: gpt_engineer/main.py:25
- `diff:gpt_engineer/main.py:26` [diff]: gpt_engineer/main.py:26
- `diff:gpt_engineer/main.py:27` [diff]: gpt_engineer/main.py:27
- `diff:gpt_engineer/main.py:34` [diff]: gpt_engineer/main.py:34
- `diff:gpt_engineer/main.py:35` [diff]: gpt_engineer/main.py:35
- `diff_hunk:gpt_engineer/main.py:1` [diff_hunk]: gpt_engineer/main.py:1
- `entity:gpt_engineer/main.py:gpt_engineer.main` [entity]: gpt_engineer/main.py:1-35
