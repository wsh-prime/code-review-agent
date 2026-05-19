# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 1
- Changed entities: 4
- Risk signals: 1
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
| Total latency | 1648 ms |
| Token in | 3915 |
| Token out | 93 |

- Iteration 0: 0 candidates, 0 verified, 0 uncertain, 0 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `file_risk_shards_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 2167 |
| Selected evidence | 2 |
| Omitted evidence | 48 |
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

- `tests/steps/test_archive.py` (modified)

## Changed Entities

- `tests/steps/test_archive.py:1-25` module `tests.steps.test_archive`
- `tests/steps/test_archive.py:10-13` function `freeze_at`
- `tests/steps/test_archive.py:16-23` function `setup_dbs`
- `tests/steps/test_archive.py:26-44` function `test_archive`

## Risk Signals

- `api_change` (0.82): Public function or class signature changed in tests/steps/test_archive.py.

## Evidence Index

- `diff:tests/steps/test_archive.py:1` [diff]: tests/steps/test_archive.py:1
- `diff:tests/steps/test_archive.py:10` [diff]: tests/steps/test_archive.py:10
- `diff:tests/steps/test_archive.py:11` [diff]: tests/steps/test_archive.py:11
- `diff:tests/steps/test_archive.py:12` [diff]: tests/steps/test_archive.py:12
- `diff:tests/steps/test_archive.py:13` [diff]: tests/steps/test_archive.py:13
- `diff:tests/steps/test_archive.py:14` [diff]: tests/steps/test_archive.py:14
- `diff:tests/steps/test_archive.py:15` [diff]: tests/steps/test_archive.py:15
- `diff:tests/steps/test_archive.py:16` [diff]: tests/steps/test_archive.py:16
- `diff:tests/steps/test_archive.py:17` [diff]: tests/steps/test_archive.py:17
- `diff:tests/steps/test_archive.py:18` [diff]: tests/steps/test_archive.py:18
- `diff:tests/steps/test_archive.py:19` [diff]: tests/steps/test_archive.py:19
- `diff:tests/steps/test_archive.py:2` [diff]: tests/steps/test_archive.py:2
- `diff:tests/steps/test_archive.py:20` [diff]: tests/steps/test_archive.py:20
- `diff:tests/steps/test_archive.py:21` [diff]: tests/steps/test_archive.py:21
- `diff:tests/steps/test_archive.py:22` [diff]: tests/steps/test_archive.py:22
- `diff:tests/steps/test_archive.py:23` [diff]: tests/steps/test_archive.py:23
- `diff:tests/steps/test_archive.py:24` [diff]: tests/steps/test_archive.py:24
- `diff:tests/steps/test_archive.py:25` [diff]: tests/steps/test_archive.py:25
- `diff:tests/steps/test_archive.py:26` [diff]: tests/steps/test_archive.py:26
- `diff:tests/steps/test_archive.py:27` [diff]: tests/steps/test_archive.py:27
- `diff:tests/steps/test_archive.py:28` [diff]: tests/steps/test_archive.py:28
- `diff:tests/steps/test_archive.py:29` [diff]: tests/steps/test_archive.py:29
- `diff:tests/steps/test_archive.py:3` [diff]: tests/steps/test_archive.py:3
- `diff:tests/steps/test_archive.py:30` [diff]: tests/steps/test_archive.py:30
- `diff:tests/steps/test_archive.py:31` [diff]: tests/steps/test_archive.py:31
- `diff:tests/steps/test_archive.py:32` [diff]: tests/steps/test_archive.py:32
- `diff:tests/steps/test_archive.py:33` [diff]: tests/steps/test_archive.py:33
- `diff:tests/steps/test_archive.py:34` [diff]: tests/steps/test_archive.py:34
- `diff:tests/steps/test_archive.py:35` [diff]: tests/steps/test_archive.py:35
- `diff:tests/steps/test_archive.py:36` [diff]: tests/steps/test_archive.py:36
- ... 20 more evidence items omitted.
