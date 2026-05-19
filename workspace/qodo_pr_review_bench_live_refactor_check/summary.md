# Qodo PR-Review-Bench Live Summary

## Aggregate

- total: 5
- ok: 5
- errors: 0
- fallbacks: 0
- ground_truth_issues: 23
- findings: 8
- findings_plus_nhr: 19
- finding_recall_exact: 0.0
- broad_recall_exact: 0.2174
- finding_recall_line10: 0.0
- broad_recall_line10: 0.2174
- finding_recall_file: 0.087
- broad_recall_file: 0.3478
- finding_precision_line10: 0.0
- broad_precision_line10: 0.2632
- total_token_in: 87388
- total_token_out: 5718

## Samples

| id | repo | gt | F | NHR | recall F@10 | recall broad@10 | precision F@10 | fallback | tokens |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| qodo_000 | Ghost | 4 | 0 | 0 | 0.0 | 0.0 | None | False | 7357/12 |
| qodo_001 | Ghost | 4 | 0 | 2 | 0.0 | 0.25 | None | False | 6798/864 |
| qodo_002 | Ghost | 4 | 0 | 0 | 0.0 | 0.0 | None | False | 14468/704 |
| qodo_003 | Ghost | 6 | 2 | 0 | 0.0 | 0.0 | 0.0 | False | 19898/857 |
| qodo_004 | Ghost | 5 | 6 | 9 | 0.0 | 0.8 | 0.0 | False | 38867/3281 |

## Metric Notes

- Exact recall requires same file and predicted line inside the ground-truth issue range.
- Line10 recall allows the predicted line to be within +/-10 lines of the ground-truth range.
- Broad metrics count both findings and needs_human_review as detections.
- Precision here is location-based and deterministic; it does not judge semantic equivalence.
