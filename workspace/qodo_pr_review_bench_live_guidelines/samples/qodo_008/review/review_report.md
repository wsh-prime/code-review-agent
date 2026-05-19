# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 3
- Changed entities: 3
- Risk signals: 0
- Findings: 0
- Needs human review: 1
- Discarded: 0
- Agent runs: 3
- Loop enabled: True
- Target repo modified: False

## Loop Summary

| Metric | Value |
|---|---:|
| Iterations | 1 / 1 |
| Converged | False |
| Fallback | False |
| Retry count | 2 |
| Total latency | 163878 ms |
| Token in | 11240 |
| Token out | 305 |

- Iteration 0: 1 candidates, 1 verified, 1 uncertain, 0 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `file_risk_shards_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 10315 |
| Selected evidence | 5 |
| Omitted evidence | 198 |
| Context truncated | True |
| Review shards | 1 |
| Context requests | 1 |
| Refills | 1 |

## Findings

No findings.

Checked changed files, changed entities, deterministic risk signals, and evidence references. No high-confidence review finding was produced.

## Needs Human Review

- `correctness` medium at `ghost/core/core/server/services/email-service/DomainWarmingService.ts:68` (0.50)
  - Division by zero when totalDays is 1 in getWarmupLimit
  - Suggestion: Guard against totalDays <= 1 by returning emailCount or Infinity directly when totalDays <= 1.
  - Evidence: `diff_hunk:ghost/core/core/server/services/email-service/DomainWarmingService.ts:61`

## Changed Files

- `ghost/core/core/server/services/email-service/DomainWarmingService.ts` (modified)
- `ghost/core/test/integration/services/email-service/domain-warming.test.js` (modified)
- `ghost/core/test/unit/server/services/email-service/domain-warming-service.test.ts` (modified)

## Changed Entities

- `ghost/core/core/server/services/email-service/DomainWarmingService.ts:18-68` module `ghost.core.core.server.services.email-service.DomainWarmingService`
- `ghost/core/test/integration/services/email-service/domain-warming.test.js:198-206` module `ghost.core.test.integration.services.email-service.domain-warming.test`
- `ghost/core/test/unit/server/services/email-service/domain-warming-service.test.ts:16-16` module `ghost.core.test.unit.server.services.email-service.domain-warming-service.test`

## Risk Signals

None.

## Evidence Index

- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:102` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:102
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:103` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:103
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:104` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:104
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:105` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:105
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:106` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:106
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:107` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:107
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:108` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:108
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:109` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:109
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:110` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:110
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:111` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:111
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:112` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:112
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:113` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:113
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:114` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:114
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:115` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:115
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:116` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:116
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:117` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:117
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:118` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:118
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:119` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:119
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:123` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:123
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:127` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:127
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:128` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:128
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:132` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:132
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:133` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:133
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:135` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:135
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:136` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:136
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:137` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:137
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:138` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:138
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:139` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:139
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:140` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:140
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:141` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:141
- ... 258 more evidence items omitted.
