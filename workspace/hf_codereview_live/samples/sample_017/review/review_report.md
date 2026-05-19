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
| Total latency | 54670 ms |
| Token in | 2328 |
| Token out | 185 |

- Iteration 0: 0 candidates, 0 verified, 0 uncertain, 0 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `file_risk_shards_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 976 |
| Selected evidence | 3 |
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

- `scripts/benchmark.py` (modified)

## Changed Entities

- `scripts/benchmark.py:26-26` module `scripts.benchmark`

## Risk Signals

None.

## Evidence Index

- `diff:scripts/benchmark.py:26` [diff]: scripts/benchmark.py:26
- `diff_hunk:scripts/benchmark.py:18` [diff_hunk]: scripts/benchmark.py:18
- `entity:scripts/benchmark.py:scripts.benchmark` [entity]: scripts/benchmark.py:26-26
