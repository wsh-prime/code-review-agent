# Qodo PR-Review-Bench Live Summary

## Aggregate

- total: 30
- ok: 30
- errors: 0
- fallbacks: 0
- ground_truth_issues: 183
- findings: 41
- findings_plus_nhr: 107
- finding_recall_exact: 0.0328
- broad_recall_exact: 0.1093
- finding_recall_line10: 0.0656
- broad_recall_line10: 0.1858
- finding_recall_file: 0.0984
- broad_recall_file: 0.2678
- finding_precision_line10: 0.2927
- broad_precision_line10: 0.3178
- total_token_in: 916534
- total_token_out: 43094

## Samples

| id | repo | gt | F | NHR | recall F@10 | recall broad@10 | precision F@10 | fallback | tokens |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| qodo_000 | Ghost | 4 | 0 | 0 | 0.0 | 0.0 | None | False | 7029/12 |
| qodo_001 | Ghost | 4 | 0 | 1 | 0.0 | 0.25 | None | False | 9613/903 |
| qodo_002 | Ghost | 4 | 0 | 1 | 0.0 | 0.0 | None | False | 12517/1326 |
| qodo_003 | Ghost | 6 | 2 | 0 | 0.0 | 0.0 | 0.0 | False | 11230/378 |
| qodo_004 | Ghost | 5 | 4 | 5 | 0.4 | 0.8 | 0.5 | False | 42037/5359 |
| qodo_005 | Ghost | 3 | 0 | 4 | 0.0 | 1.0 | None | False | 8463/830 |
| qodo_006 | Ghost | 4 | 4 | 0 | 0.0 | 0.0 | 0.0 | False | 297893/5917 |
| qodo_007 | Ghost | 7 | 0 | 0 | 0.0 | 0.0 | None | False | 6042/12 |
| qodo_008 | Ghost | 5 | 0 | 2 | 0.0 | 0.0 | None | False | 10125/936 |
| qodo_009 | Ghost | 6 | 0 | 3 | 0.0 | 0.1667 | None | False | 15379/1315 |
| qodo_010 | Ghost | 6 | 0 | 0 | 0.0 | 0.0 | None | False | 5171/134 |
| qodo_011 | Ghost | 5 | 0 | 1 | 0.0 | 0.2 | None | False | 31649/637 |
| qodo_012 | Ghost | 4 | 3 | 1 | 0.0 | 0.0 | 0.0 | False | 92143/2002 |
| qodo_013 | aspnetcore | 7 | 0 | 3 | 0.0 | 0.4286 | None | False | 13781/969 |
| qodo_014 | aspnetcore | 9 | 5 | 1 | 0.0 | 0.1111 | 0.0 | False | 19637/1350 |
| qodo_015 | aspnetcore | 5 | 2 | 0 | 0.2 | 0.2 | 0.5 | False | 9058/627 |
| qodo_016 | aspnetcore | 15 | 0 | 4 | 0.0 | 0.0667 | None | False | 41990/2610 |
| qodo_017 | aspnetcore | 8 | 0 | 1 | 0.0 | 0.0 | None | False | 6065/436 |
| qodo_018 | aspnetcore | 3 | 5 | 4 | 0.6667 | 0.6667 | 0.4 | False | 45396/2845 |
| qodo_019 | aspnetcore | 4 | 0 | 1 | 0.0 | 0.0 | None | False | 10359/654 |
| qodo_020 | aspnetcore | 9 | 1 | 1 | 0.1111 | 0.2222 | 1.0 | False | 23186/203 |
| qodo_021 | aspnetcore | 6 | 1 | 2 | 0.1667 | 0.3333 | 1.0 | False | 28029/1075 |
| qodo_022 | aspnetcore | 5 | 1 | 6 | 0.0 | 0.2 | 0.0 | False | 18954/1218 |
| qodo_023 | cal.com | 8 | 1 | 1 | 0.0 | 0.125 | 0.0 | False | 24670/2387 |
| qodo_024 | cal.com | 5 | 2 | 0 | 0.2 | 0.2 | 0.5 | False | 7339/447 |
| qodo_025 | cal.com | 12 | 8 | 3 | 0.1667 | 0.4167 | 0.25 | False | 43545/3344 |
| qodo_026 | cal.com | 7 | 0 | 0 | 0.0 | 0.0 | None | False | 20687/36 |
| qodo_027 | cal.com | 5 | 0 | 20 | 0.0 | 0.4 | None | False | 39047/4361 |
| qodo_028 | cal.com | 8 | 2 | 0 | 0.25 | 0.25 | 1.0 | False | 4841/314 |
| qodo_029 | cal.com | 4 | 0 | 1 | 0.0 | 0.0 | None | False | 10659/457 |

## Metric Notes

- Exact recall requires same file and predicted line inside the ground-truth issue range.
- Line10 recall allows the predicted line to be within +/-10 lines of the ground-truth range.
- Broad metrics count both findings and needs_human_review as detections.
- Precision here is location-based and deterministic; it does not judge semantic equivalence.
