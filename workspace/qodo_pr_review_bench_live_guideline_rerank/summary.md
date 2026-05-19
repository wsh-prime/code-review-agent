# Qodo PR-Review-Bench Live Summary

## Aggregate

- total: 4
- ok: 4
- errors: 0
- fallbacks: 0
- ground_truth_issues: 18
- findings: 2
- findings_plus_nhr: 4
- finding_recall_exact: 0.0
- broad_recall_exact: 0.0556
- finding_recall_line10: 0.0
- broad_recall_line10: 0.0556
- finding_recall_file: 0.1111
- broad_recall_file: 0.2222
- finding_precision_line10: 0.0
- broad_precision_line10: 0.25
- total_token_in: 40389
- total_token_out: 2619

## Samples

| id | repo | gt | F | NHR | recall F@10 | recall broad@10 | precision F@10 | fallback | tokens |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| qodo_000 | Ghost | 4 | 0 | 0 | 0.0 | 0.0 | None | False | 7029/12 |
| qodo_001 | Ghost | 4 | 0 | 1 | 0.0 | 0.25 | None | False | 9613/903 |
| qodo_002 | Ghost | 4 | 0 | 1 | 0.0 | 0.0 | None | False | 12517/1326 |
| qodo_003 | Ghost | 6 | 2 | 0 | 0.0 | 0.0 | 0.0 | False | 11230/378 |

## Metric Notes

- Exact recall requires same file and predicted line inside the ground-truth issue range.
- Line10 recall allows the predicted line to be within +/-10 lines of the ground-truth range.
- Broad metrics count both findings and needs_human_review as detections.
- Precision here is location-based and deterministic; it does not judge semantic equivalence.
