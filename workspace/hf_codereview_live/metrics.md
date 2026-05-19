# HF CodeReview Metrics

## Headline

- total: 24
- ok: 24
- success_rate: 100.00%
- fallback_rate: 0.00%
- positive_any_issue_rate: 44.44%
- positive_finding_rate: 22.22%
- negative_silence_rate_any_issue: 33.33%
- negative_silence_rate_findings_only: 66.67%
- high_signal_positive_any_issue_rate: 50.00%
- positive_line_within_3_rate: 25.00%
- positive_line_within_10_rate: 87.50%
- avg_token_in: 2434.42
- avg_token_out: 284.12
- p50_latency_ms: 24907
- p95_latency_ms: 135808
- avg_findings_per_ok_sample: 0.25
- avg_needs_human_review_per_ok_sample: 0.38
- avg_discarded_per_ok_sample: 0.21

## Counts

- positive: `18`
- negative: `6`
- high_signal_positive: `2`
- issue_categories: `{"error_handling_change": 1, "security": 1, "error_handling": 1, "correctness": 2, "test_quality": 1}`
- needs_human_review_categories: `{"behavior_change": 5, "api_change": 2, "correctness": 2}`
- risk_tags: `{"api_change": 6, "security_sensitive": 3, "behavior_change": 11, "error_handling_change": 2}`
- discard_reasons: `{"low_signal_suggestion": 4, "style_preference": 1}`

## By Comment Type

| type | total | any issue | finding | NHR | line +/-3 | line +/-10 |
|---|---:|---:|---:|---:|---:|---:|
| bug | 1 | 100.00% | 100.00% | 100.00% | 0.00% | 100.00% |
| none | 6 | 66.67% | 33.33% | 33.33% | 0.00% | 0.00% |
| question | 5 | 40.00% | 40.00% | 0.00% | 40.00% | 40.00% |
| refactor | 1 | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| suggestion | 11 | 45.45% | 9.09% | 36.36% | 0.00% | 36.36% |

## Samples

| id | type | neg | status | F | NHR | D | line +/-10 | tokens | file |
|---|---|---:|---|---:|---:|---:|---:|---:|---|
| sample_000 | refactor | False | ok | 0 | 0 | 0 | False | 3221/154 | mlx_audio/tts/generate.py |
| sample_001 | bug | False | ok | 1 | 1 | 0 | True | 3661/613 | gpt_engineer/db.py |
| sample_002 | suggestion | False | ok | 0 | 0 | 1 | False | 1614/164 | gpt_engineer/main.py |
| sample_003 | question | False | ok | 0 | 0 | 0 | False | 2563/228 | gpt_engineer/main.py |
| sample_004 | suggestion | False | ok | 0 | 0 | 1 | False | 1726/189 | gpt_engineer/steps.py |
| sample_005 | question | False | ok | 1 | 0 | 0 | True | 1976/268 | gpt_engineer/steps.py |
| sample_006 | question | False | ok | 0 | 0 | 1 | False | 1482/172 | gpt_engineer/ai.py |
| sample_007 | suggestion | False | ok | 0 | 0 | 0 | False | 1452/12 | gpt_engineer/steps.py |
| sample_008 | suggestion | False | ok | 1 | 0 | 0 | True | 1716/202 | scripts/benchmark.py |
| sample_009 | question | False | ok | 1 | 0 | 0 | True | 2922/417 | scripts/clean_benchmarks.py |
| sample_010 | suggestion | False | ok | 0 | 2 | 0 | True | 3444/437 | gpt_engineer/steps.py |
| sample_011 | question | False | ok | 0 | 0 | 1 | False | 2439/243 | gpt_engineer/db.py |
| sample_012 | suggestion | False | ok | 0 | 1 | 0 | True | 1315/176 | gpt_engineer/main.py |
| sample_013 | suggestion | False | ok | 0 | 0 | 0 | False | 2450/161 | gpt_engineer/steps.py |
| sample_014 | suggestion | False | ok | 0 | 0 | 1 | False | 4406/300 | gpt_engineer/ai.py |
| sample_015 | suggestion | False | ok | 0 | 1 | 0 | False | 3761/1272 | gpt_engineer/main.py |
| sample_016 | suggestion | False | ok | 0 | 2 | 0 | True | 2344/463 | gpt_engineer/steps.py |
| sample_017 | suggestion | False | ok | 0 | 0 | 0 | False | 2328/185 | scripts/benchmark.py |
| sample_018 | none | True | ok | 0 | 1 | 0 | False | 2081/174 | gpt_engineer/db.py |
| sample_019 | none | True | ok | 0 | 0 | 0 | False | 2019/103 | tests/test_db.py |
| sample_020 | none | True | ok | 1 | 0 | 0 | False | 1587/261 | gpt_engineer/db.py |
| sample_021 | none | True | ok | 0 | 1 | 0 | False | 1829/297 | gpt_engineer/db.py |
| sample_022 | none | True | ok | 1 | 0 | 0 | False | 2175/235 | tests/test_collect.py |
| sample_023 | none | True | ok | 0 | 0 | 0 | False | 3915/93 | tests/steps/test_archive.py |

## Notes

- `positive_*` treats human-commented chunks as weak positives.
- `negative_*` treats no-comment chunks as weak negatives; these are not guaranteed to be bug-free.
- Line proximity compares emitted issue line against the dataset's human `comment_line` for positive samples.
