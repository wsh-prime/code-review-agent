# Qodo PR-Review-Bench Live Summary

## Aggregate

- total: 30
- ok: 30
- errors: 0
- fallbacks: 0
- ground_truth_issues: 183
- findings: 38
- findings_plus_nhr: 100
- finding_recall_exact: 0.0383
- broad_recall_exact: 0.1093
- finding_recall_line10: 0.0437
- broad_recall_line10: 0.1694
- finding_recall_file: 0.0874
- broad_recall_file: 0.2623
- finding_precision_line10: 0.2105
- broad_precision_line10: 0.31
- total_token_in: 964916
- total_token_out: 35680

## Samples

| id | repo | gt | F | NHR | recall F@10 | recall broad@10 | precision F@10 | fallback | tokens |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| qodo_000 | Ghost | 4 | 2 | 0 | 0.25 | 0.25 | 0.5 | False | 7536/374 |
| qodo_001 | Ghost | 4 | 0 | 0 | 0.0 | 0.0 | None | False | 6455/12 |
| qodo_002 | Ghost | 4 | 0 | 2 | 0.0 | 0.25 | None | False | 10673/908 |
| qodo_003 | Ghost | 6 | 2 | 0 | 0.0 | 0.0 | 0.0 | False | 12370/352 |
| qodo_004 | Ghost | 5 | 3 | 6 | 0.0 | 0.6 | 0.0 | False | 40444/2226 |
| qodo_005 | Ghost | 3 | 2 | 0 | 0.6667 | 0.6667 | 1.0 | False | 9044/326 |
| qodo_006 | Ghost | 4 | 7 | 5 | 0.0 | 0.25 | 0.0 | False | 333617/7470 |
| qodo_007 | Ghost | 7 | 0 | 1 | 0.0 | 0.0 | None | False | 6722/160 |
| qodo_008 | Ghost | 5 | 0 | 1 | 0.0 | 0.2 | None | False | 11240/305 |
| qodo_009 | Ghost | 6 | 1 | 3 | 0.0 | 0.3333 | 0.0 | False | 19176/1098 |
| qodo_010 | Ghost | 6 | 0 | 0 | 0.0 | 0.0 | None | False | 5827/146 |
| qodo_011 | Ghost | 5 | 2 | 0 | 0.2 | 0.2 | 0.5 | False | 34299/740 |
| qodo_012 | Ghost | 4 | 0 | 1 | 0.0 | 0.25 | None | False | 94598/1046 |
| qodo_013 | aspnetcore | 7 | 0 | 2 | 0.0 | 0.2857 | None | False | 15730/958 |
| qodo_014 | aspnetcore | 9 | 0 | 2 | 0.0 | 0.2222 | None | False | 17859/777 |
| qodo_015 | aspnetcore | 5 | 0 | 3 | 0.0 | 0.4 | None | False | 6215/517 |
| qodo_016 | aspnetcore | 15 | 2 | 1 | 0.0 | 0.0667 | 0.0 | False | 20826/1020 |
| qodo_017 | aspnetcore | 8 | 0 | 2 | 0.0 | 0.125 | None | False | 6451/535 |
| qodo_018 | aspnetcore | 3 | 10 | 2 | 0.3333 | 0.3333 | 0.1 | False | 45320/3088 |
| qodo_019 | aspnetcore | 4 | 0 | 2 | 0.0 | 0.25 | None | False | 14992/911 |
| qodo_020 | aspnetcore | 9 | 1 | 1 | 0.1111 | 0.2222 | 1.0 | False | 27439/215 |
| qodo_021 | aspnetcore | 6 | 0 | 2 | 0.0 | 0.3333 | None | False | 29972/1006 |
| qodo_022 | aspnetcore | 5 | 0 | 10 | 0.0 | 0.0 | None | False | 23606/1639 |
| qodo_023 | cal.com | 8 | 2 | 1 | 0.0 | 0.125 | 0.0 | False | 12907/585 |
| qodo_024 | cal.com | 5 | 0 | 0 | 0.0 | 0.0 | None | False | 7021/164 |
| qodo_025 | cal.com | 12 | 0 | 7 | 0.0 | 0.0833 | None | False | 34684/1963 |
| qodo_026 | cal.com | 7 | 0 | 1 | 0.0 | 0.0 | None | False | 34754/1667 |
| qodo_027 | cal.com | 5 | 0 | 7 | 0.0 | 0.0 | None | False | 39243/2461 |
| qodo_028 | cal.com | 8 | 4 | 0 | 0.25 | 0.25 | 0.5 | False | 22403/2028 |
| qodo_029 | cal.com | 4 | 0 | 0 | 0.0 | 0.0 | None | False | 13493/983 |

## Metric Notes

- Exact recall requires same file and predicted line inside the ground-truth issue range.
- Line10 recall allows the predicted line to be within +/-10 lines of the ground-truth range.
- Broad metrics count both findings and needs_human_review as detections.
- Precision here is location-based and deterministic; it does not judge semantic equivalence.
