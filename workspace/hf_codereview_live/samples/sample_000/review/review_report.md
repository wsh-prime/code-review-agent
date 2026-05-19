# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 1
- Changed entities: 1
- Risk signals: 2
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
| Retry count | 3 |
| Total latency | 271372 ms |
| Token in | 3221 |
| Token out | 154 |

- Iteration 0: 0 candidates, 0 verified, 0 uncertain, 0 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `file_risk_shards_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 3604 |
| Selected evidence | 3 |
| Omitted evidence | 51 |
| Context truncated | True |
| Review shards | 1 |
| Context requests | 1 |
| Refills | 1 |

## Findings

No findings.

Checked changed files, changed entities, deterministic risk signals, and evidence references. No high-confidence review finding was produced.

## Needs Human Review

None.

## Changed Files

- `mlx_audio/tts/generate.py` (modified)

## Changed Entities

- `mlx_audio/tts/generate.py:1-51` module `mlx_audio.tts.generate`

## Risk Signals

- `api_change` (0.82): Public function or class signature changed in mlx_audio/tts/generate.py.
- `security_sensitive` (0.74): Security-sensitive keywords changed in mlx_audio/tts/generate.py.

## Evidence Index

- `diff:mlx_audio/tts/generate.py:1` [diff]: mlx_audio/tts/generate.py:1
- `diff:mlx_audio/tts/generate.py:10` [diff]: mlx_audio/tts/generate.py:10
- `diff:mlx_audio/tts/generate.py:11` [diff]: mlx_audio/tts/generate.py:11
- `diff:mlx_audio/tts/generate.py:12` [diff]: mlx_audio/tts/generate.py:12
- `diff:mlx_audio/tts/generate.py:13` [diff]: mlx_audio/tts/generate.py:13
- `diff:mlx_audio/tts/generate.py:14` [diff]: mlx_audio/tts/generate.py:14
- `diff:mlx_audio/tts/generate.py:15` [diff]: mlx_audio/tts/generate.py:15
- `diff:mlx_audio/tts/generate.py:16` [diff]: mlx_audio/tts/generate.py:16
- `diff:mlx_audio/tts/generate.py:17` [diff]: mlx_audio/tts/generate.py:17
- `diff:mlx_audio/tts/generate.py:18` [diff]: mlx_audio/tts/generate.py:18
- `diff:mlx_audio/tts/generate.py:19` [diff]: mlx_audio/tts/generate.py:19
- `diff:mlx_audio/tts/generate.py:2` [diff]: mlx_audio/tts/generate.py:2
- `diff:mlx_audio/tts/generate.py:20` [diff]: mlx_audio/tts/generate.py:20
- `diff:mlx_audio/tts/generate.py:21` [diff]: mlx_audio/tts/generate.py:21
- `diff:mlx_audio/tts/generate.py:22` [diff]: mlx_audio/tts/generate.py:22
- `diff:mlx_audio/tts/generate.py:23` [diff]: mlx_audio/tts/generate.py:23
- `diff:mlx_audio/tts/generate.py:24` [diff]: mlx_audio/tts/generate.py:24
- `diff:mlx_audio/tts/generate.py:25` [diff]: mlx_audio/tts/generate.py:25
- `diff:mlx_audio/tts/generate.py:26` [diff]: mlx_audio/tts/generate.py:26
- `diff:mlx_audio/tts/generate.py:27` [diff]: mlx_audio/tts/generate.py:27
- `diff:mlx_audio/tts/generate.py:28` [diff]: mlx_audio/tts/generate.py:28
- `diff:mlx_audio/tts/generate.py:29` [diff]: mlx_audio/tts/generate.py:29
- `diff:mlx_audio/tts/generate.py:3` [diff]: mlx_audio/tts/generate.py:3
- `diff:mlx_audio/tts/generate.py:30` [diff]: mlx_audio/tts/generate.py:30
- `diff:mlx_audio/tts/generate.py:31` [diff]: mlx_audio/tts/generate.py:31
- `diff:mlx_audio/tts/generate.py:32` [diff]: mlx_audio/tts/generate.py:32
- `diff:mlx_audio/tts/generate.py:33` [diff]: mlx_audio/tts/generate.py:33
- `diff:mlx_audio/tts/generate.py:34` [diff]: mlx_audio/tts/generate.py:34
- `diff:mlx_audio/tts/generate.py:35` [diff]: mlx_audio/tts/generate.py:35
- `diff:mlx_audio/tts/generate.py:36` [diff]: mlx_audio/tts/generate.py:36
- ... 24 more evidence items omitted.
