# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 1
- Changed entities: 1
- Risk signals: 1
- Findings: 1
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
| Retry count | 1 |
| Total latency | 69425 ms |
| Token in | 2922 |
| Token out | 417 |

- Iteration 0: 1 candidates, 1 verified, 0 uncertain, 1 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `file_risk_shards_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 1512 |
| Selected evidence | 3 |
| Omitted evidence | 1 |
| Context truncated | True |
| Review shards | 1 |
| Context requests | 2 |
| Refills | 1 |

## Findings

- `correctness` medium at `scripts/clean_benchmarks.py:19` (0.65)
  - The patch adds 'prompt' to the skip list but the directory may contain other files or directories that are not meant to be deleted, potentially causing unintended data loss.
  - Suggestion: Verify that skipping 'prompt' is correct and that no other files/directories should be excluded. Consider adding a more explicit allowlist or confirmation step.
  - Evidence: `diff:scripts/clean_benchmarks.py:19`, `diff_hunk:scripts/clean_benchmarks.py:11`

## Needs Human Review

None.

## Changed Files

- `scripts/clean_benchmarks.py` (modified)

## Changed Entities

- `scripts/clean_benchmarks.py:12-28` function `main`

## Risk Signals

- `behavior_change` (0.72): Executable logic changed inside main.

## Evidence Index

- `diff:scripts/clean_benchmarks.py:19` [diff]: scripts/clean_benchmarks.py:19
- `diff_hunk:scripts/clean_benchmarks.py:11` [diff_hunk]: scripts/clean_benchmarks.py:11
- `entity:scripts/clean_benchmarks.py:main` [entity]: scripts/clean_benchmarks.py:12-28
- `risk:behavior_change:scripts/clean_benchmarks.py` [risk]: behavior_change
