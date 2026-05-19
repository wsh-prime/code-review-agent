# Qodo PR-Review-Bench Live Summary

## Aggregate

- total: 1
- ok: 1
- errors: 0
- fallbacks: 0
- ground_truth_issues: 4
- findings: 2
- findings_plus_nhr: 2
- finding_recall_exact: 0.25
- broad_recall_exact: 0.25
- finding_recall_line10: 0.25
- broad_recall_line10: 0.25
- finding_recall_file: 0.25
- broad_recall_file: 0.25
- finding_precision_line10: 0.5
- broad_precision_line10: 0.5
- total_token_in: 7540
- total_token_out: 390

## Samples

| id | repo | gt | F | NHR | recall F@10 | recall broad@10 | precision F@10 | fallback | tokens |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| qodo_000 | Ghost | 4 | 2 | 0 | 0.25 | 0.25 | 0.5 | False | 7540/390 |

## Metric Notes

- Exact recall requires same file and predicted line inside the ground-truth issue range.
- Line10 recall allows the predicted line to be within +/-10 lines of the ground-truth range.
- Broad metrics count both findings and needs_human_review as detections.
- Precision here is location-based and deterministic; it does not judge semantic equivalence.
