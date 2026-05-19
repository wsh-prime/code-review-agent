# Qodo PR-Review-Bench Live Summary

## Aggregate

- total: 30
- ok: 30
- errors: 0
- fallbacks: 1
- ground_truth_issues: 183
- findings: 16
- findings_plus_nhr: 65
- finding_recall_exact: 0.0219
- broad_recall_exact: 0.0765
- finding_recall_line10: 0.0273
- broad_recall_line10: 0.1148
- finding_recall_file: 0.0437
- broad_recall_file: 0.1803
- finding_precision_line10: 0.3125
- broad_precision_line10: 0.3231
- total_token_in: 722716
- total_token_out: 34435

## Samples

| id | repo | gt | F | NHR | recall F@10 | recall broad@10 | precision F@10 | fallback | tokens |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| qodo_000 | Ghost | 4 | 1 | 0 | 0.0 | 0.0 | 0.0 | False | 5412/185 |
| qodo_001 | Ghost | 4 | 2 | 0 | 0.25 | 0.25 | 0.5 | False | 4331/428 |
| qodo_002 | Ghost | 4 | 0 | 0 | 0.0 | 0.0 | None | False | 6425/590 |
| qodo_003 | Ghost | 6 | 1 | 0 | 0.0 | 0.0 | 0.0 | False | 8122/202 |
| qodo_004 | Ghost | 5 | 0 | 1 | 0.0 | 0.0 | None | False | 24287/1003 |
| qodo_005 | Ghost | 3 | 2 | 0 | 0.6667 | 0.6667 | 1.0 | False | 6920/631 |
| qodo_006 | Ghost | 4 | 0 | 2 | 0.0 | 0.0 | None | False | 244477/8062 |
| qodo_007 | Ghost | 7 | 0 | 0 | 0.0 | 0.0 | None | False | 4598/12 |
| qodo_008 | Ghost | 5 | 0 | 3 | 0.0 | 0.0 | None | False | 6992/934 |
| qodo_009 | Ghost | 6 | 0 | 4 | 0.0 | 0.3333 | None | False | 13503/1577 |
| qodo_010 | Ghost | 6 | 0 | 0 | 0.0 | 0.0 | None | False | 3703/163 |
| qodo_011 | Ghost | 5 | 0 | 3 | 0.0 | 0.4 | None | False | 25803/783 |
| qodo_012 | Ghost | 4 | 0 | 2 | 0.0 | 0.0 | None | False | 77802/2641 |
| qodo_013 | aspnetcore | 7 | 0 | 1 | 0.0 | 0.1429 | None | False | 9116/513 |
| qodo_014 | aspnetcore | 9 | 2 | 4 | 0.0 | 0.0 | 0.0 | False | 15226/1692 |
| qodo_015 | aspnetcore | 5 | 1 | 0 | 0.0 | 0.0 | 0.0 | False | 4186/336 |
| qodo_016 | aspnetcore | 15 | 0 | 1 | 0.0 | 0.0 | None | False | 27365/579 |
| qodo_017 | aspnetcore | 8 | 0 | 0 | 0.0 | 0.0 | None | False | 6734/172 |
| qodo_018 | aspnetcore | 3 | 3 | 2 | 0.0 | 0.3333 | 0.0 | False | 33112/2158 |
| qodo_019 | aspnetcore | 4 | 0 | 2 | 0.0 | 0.0 | None | False | 9474/1089 |
| qodo_020 | aspnetcore | 9 | 1 | 4 | 0.1111 | 0.2222 | 1.0 | False | 18188/869 |
| qodo_021 | aspnetcore | 6 | 0 | 2 | 0.0 | 0.1667 | None | False | 29074/1059 |
| qodo_022 | aspnetcore | 5 | 0 | 1 | 0.0 | 0.2 | None | False | 24999/1088 |
| qodo_023 | cal.com | 8 | 0 | 3 | 0.0 | 0.125 | None | False | 15283/1658 |
| qodo_024 | cal.com | 5 | 0 | 1 | 0.0 | 0.2 | None | False | 5647/208 |
| qodo_025 | cal.com | 12 | 3 | 2 | 0.0833 | 0.25 | 0.3333 | False | 30498/1648 |
| qodo_026 | cal.com | 7 | 0 | 0 | 0.0 | 0.0 | None | False | 21186/284 |
| qodo_027 | cal.com | 5 | 0 | 6 | 0.0 | 0.2 | None | False | 28823/2868 |
| qodo_028 | cal.com | 8 | 0 | 4 | 0.0 | 0.125 | None | True | 0/0 |
| qodo_029 | cal.com | 4 | 0 | 1 | 0.0 | 0.25 | None | False | 11430/1003 |

## Metric Notes

- Exact recall requires same file and predicted line inside the ground-truth issue range.
- Line10 recall allows the predicted line to be within +/-10 lines of the ground-truth range.
- Broad metrics count both findings and needs_human_review as detections.
- Precision here is location-based and deterministic; it does not judge semantic equivalence.
