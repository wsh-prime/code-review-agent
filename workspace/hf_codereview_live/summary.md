# HF CodeReview Live Benchmark

## Aggregate

- total: 24
- ok: 24
- errors: 0
- fallbacks: 0
- negative false positives: 4 / 6
- token in/out: 58426 / 6819

## Samples

| id | type | negative | status | findings | nhr | fallback | tokens | file |
|---|---|---:|---|---:|---:|---:|---:|---|
| sample_000 | refactor | False | ok | 0 | 0 | False | 3221/154 | mlx_audio/tts/generate.py |
| sample_001 | bug | False | ok | 1 | 1 | False | 3661/613 | gpt_engineer/db.py |
| sample_002 | suggestion | False | ok | 0 | 0 | False | 1614/164 | gpt_engineer/main.py |
| sample_003 | question | False | ok | 0 | 0 | False | 2563/228 | gpt_engineer/main.py |
| sample_004 | suggestion | False | ok | 0 | 0 | False | 1726/189 | gpt_engineer/steps.py |
| sample_005 | question | False | ok | 1 | 0 | False | 1976/268 | gpt_engineer/steps.py |
| sample_006 | question | False | ok | 0 | 0 | False | 1482/172 | gpt_engineer/ai.py |
| sample_007 | suggestion | False | ok | 0 | 0 | False | 1452/12 | gpt_engineer/steps.py |
| sample_008 | suggestion | False | ok | 1 | 0 | False | 1716/202 | scripts/benchmark.py |
| sample_009 | question | False | ok | 1 | 0 | False | 2922/417 | scripts/clean_benchmarks.py |
| sample_010 | suggestion | False | ok | 0 | 2 | False | 3444/437 | gpt_engineer/steps.py |
| sample_011 | question | False | ok | 0 | 0 | False | 2439/243 | gpt_engineer/db.py |
| sample_012 | suggestion | False | ok | 0 | 1 | False | 1315/176 | gpt_engineer/main.py |
| sample_013 | suggestion | False | ok | 0 | 0 | False | 2450/161 | gpt_engineer/steps.py |
| sample_014 | suggestion | False | ok | 0 | 0 | False | 4406/300 | gpt_engineer/ai.py |
| sample_015 | suggestion | False | ok | 0 | 1 | False | 3761/1272 | gpt_engineer/main.py |
| sample_016 | suggestion | False | ok | 0 | 2 | False | 2344/463 | gpt_engineer/steps.py |
| sample_017 | suggestion | False | ok | 0 | 0 | False | 2328/185 | scripts/benchmark.py |
| sample_018 | none | True | ok | 0 | 1 | False | 2081/174 | gpt_engineer/db.py |
| sample_019 | none | True | ok | 0 | 0 | False | 2019/103 | tests/test_db.py |
| sample_020 | none | True | ok | 1 | 0 | False | 1587/261 | gpt_engineer/db.py |
| sample_021 | none | True | ok | 0 | 1 | False | 1829/297 | gpt_engineer/db.py |
| sample_022 | none | True | ok | 1 | 0 | False | 2175/235 | tests/test_collect.py |
| sample_023 | none | True | ok | 0 | 0 | False | 3915/93 | tests/steps/test_archive.py |
