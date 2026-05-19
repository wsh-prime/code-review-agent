# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 3
- Changed entities: 3
- Risk signals: 0
- Findings: 0
- Needs human review: 1
- Discarded: 1
- Agent runs: 3
- Loop enabled: True
- Target repo modified: False

## Loop Summary

| Metric | Value |
|---|---:|
| Iterations | 1 / 1 |
| Converged | False |
| Fallback | False |
| Retry count | 1 |
| Total latency | 140740 ms |
| Token in | 12517 |
| Token out | 1326 |

- Iteration 0: 4 candidates, 3 verified, 3 uncertain, 0 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `file_risk_shards_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 10684 |
| Selected evidence | 14 |
| Omitted evidence | 167 |
| Context truncated | True |
| Review shards | 1 |
| Context requests | 2 |
| Refills | 1 |

## Findings

No findings.

Checked changed files, changed entities, deterministic risk signals, and evidence references. No high-confidence review finding was produced.

## Needs Human Review

- `correctness` high at `ghost/core/core/server/services/email-service/DomainWarmingService.ts:3` (0.50)
  - Changing the EmailModel type from findOne to findPage changes the return type from a single nullable record to an object with a data array. Any existing callers that destructure or expect a single record will break at runtime.
  - Suggestion: Verify all callers of EmailModel are updated to handle the new findPage signature and return shape, or add a compatibility wrapper.
  - Evidence: `diff_hunk:ghost/core/core/server/services/email-service/DomainWarmingService.ts:3`

## Changed Files

- `ghost/core/core/server/services/email-service/DomainWarmingService.ts` (modified)
- `ghost/core/test/integration/services/email-service/domain-warming.test.js` (modified)
- `ghost/core/test/unit/server/services/email-service/domain-warming-service.test.ts` (modified)

## Changed Entities

- `ghost/core/core/server/services/email-service/DomainWarmingService.ts:6-6` module `ghost.core.core.server.services.email-service.DomainWarmingService`
- `ghost/core/test/integration/services/email-service/domain-warming.test.js:53-66` module `ghost.core.test.integration.services.email-service.domain-warming.test`
- `ghost/core/test/unit/server/services/email-service/domain-warming-service.test.ts:11-11` module `ghost.core.test.unit.server.services.email-service.domain-warming-service.test`

## Risk Signals

None.

## Evidence Index

- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:101` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:101
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:102` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:102
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:103` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:103
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:104` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:104
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:107` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:107
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:111` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:111
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:112` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:112
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:124` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:124
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:125` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:125
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:126` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:126
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:127` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:127
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:128` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:128
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:129` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:129
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:130` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:130
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:132` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:132
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:137` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:137
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:138` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:138
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:23` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:23
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:24` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:24
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:25` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:25
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:26` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:26
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:27` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:27
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:30` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:30
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:31` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:31
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:32` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:32
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:33` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:33
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:34` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:34
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:35` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:35
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:36` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:36
- `diff:ghost/core/core/server/services/email-service/DomainWarmingService.ts:37` [diff]: ghost/core/core/server/services/email-service/DomainWarmingService.ts:37
- ... 151 more evidence items omitted.
