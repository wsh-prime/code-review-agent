# Qodo PR-Review-Bench Live Summary

## Aggregate

- total: 1
- ok: 1
- errors: 0
- fallbacks: 0
- ground_truth_issues: 4
- findings: 1
- findings_plus_nhr: 1
- finding_recall_exact: 0.0
- broad_recall_exact: 0.0
- finding_recall_line10: 0.0
- broad_recall_line10: 0.0
- finding_recall_file: 0.0
- broad_recall_file: 0.0
- finding_precision_line10: 0.0
- broad_precision_line10: 0.0
- total_token_in: 6626
- total_token_out: 179

## Samples

| id | repo | gt | F | NHR | recall F@10 | recall broad@10 | precision F@10 | fallback | tokens |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| qodo_000 | Ghost | 4 | 1 | 0 | 0.0 | 0.0 | 0.0 | False | 6626/179 |

## Metric Notes

- Exact recall requires same file and predicted line inside the ground-truth issue range.
- Line10 recall allows the predicted line to be within +/-10 lines of the ground-truth range.
- Broad metrics count both findings and needs_human_review as detections.
- Precision here is location-based and deterministic; it does not judge semantic equivalence.
