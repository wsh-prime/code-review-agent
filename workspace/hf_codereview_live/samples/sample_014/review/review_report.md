# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 1
- Changed entities: 1
- Risk signals: 2
- Findings: 0
- Needs human review: 0
- Discarded: 1
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
| Total latency | 24887 ms |
| Token in | 4406 |
| Token out | 300 |

- Iteration 0: 1 candidates, 0 verified, 0 uncertain, 0 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `file_risk_shards_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 2455 |
| Selected evidence | 2 |
| Omitted evidence | 46 |
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

- `gpt_engineer/ai.py` (modified)

## Changed Entities

- `gpt_engineer/ai.py:1-51` module `gpt_engineer.ai`

## Risk Signals

- `api_change` (0.82): Public function or class signature changed in gpt_engineer/ai.py.
- `security_sensitive` (0.74): Security-sensitive keywords changed in gpt_engineer/ai.py.

## Evidence Index

- `diff:gpt_engineer/ai.py:1` [diff]: gpt_engineer/ai.py:1
- `diff:gpt_engineer/ai.py:10` [diff]: gpt_engineer/ai.py:10
- `diff:gpt_engineer/ai.py:11` [diff]: gpt_engineer/ai.py:11
- `diff:gpt_engineer/ai.py:12` [diff]: gpt_engineer/ai.py:12
- `diff:gpt_engineer/ai.py:13` [diff]: gpt_engineer/ai.py:13
- `diff:gpt_engineer/ai.py:14` [diff]: gpt_engineer/ai.py:14
- `diff:gpt_engineer/ai.py:15` [diff]: gpt_engineer/ai.py:15
- `diff:gpt_engineer/ai.py:16` [diff]: gpt_engineer/ai.py:16
- `diff:gpt_engineer/ai.py:19` [diff]: gpt_engineer/ai.py:19
- `diff:gpt_engineer/ai.py:2` [diff]: gpt_engineer/ai.py:2
- `diff:gpt_engineer/ai.py:25` [diff]: gpt_engineer/ai.py:25
- `diff:gpt_engineer/ai.py:26` [diff]: gpt_engineer/ai.py:26
- `diff:gpt_engineer/ai.py:27` [diff]: gpt_engineer/ai.py:27
- `diff:gpt_engineer/ai.py:28` [diff]: gpt_engineer/ai.py:28
- `diff:gpt_engineer/ai.py:29` [diff]: gpt_engineer/ai.py:29
- `diff:gpt_engineer/ai.py:3` [diff]: gpt_engineer/ai.py:3
- `diff:gpt_engineer/ai.py:30` [diff]: gpt_engineer/ai.py:30
- `diff:gpt_engineer/ai.py:31` [diff]: gpt_engineer/ai.py:31
- `diff:gpt_engineer/ai.py:32` [diff]: gpt_engineer/ai.py:32
- `diff:gpt_engineer/ai.py:33` [diff]: gpt_engineer/ai.py:33
- `diff:gpt_engineer/ai.py:34` [diff]: gpt_engineer/ai.py:34
- `diff:gpt_engineer/ai.py:35` [diff]: gpt_engineer/ai.py:35
- `diff:gpt_engineer/ai.py:36` [diff]: gpt_engineer/ai.py:36
- `diff:gpt_engineer/ai.py:37` [diff]: gpt_engineer/ai.py:37
- `diff:gpt_engineer/ai.py:38` [diff]: gpt_engineer/ai.py:38
- `diff:gpt_engineer/ai.py:39` [diff]: gpt_engineer/ai.py:39
- `diff:gpt_engineer/ai.py:4` [diff]: gpt_engineer/ai.py:4
- `diff:gpt_engineer/ai.py:40` [diff]: gpt_engineer/ai.py:40
- `diff:gpt_engineer/ai.py:41` [diff]: gpt_engineer/ai.py:41
- `diff:gpt_engineer/ai.py:42` [diff]: gpt_engineer/ai.py:42
- ... 18 more evidence items omitted.
