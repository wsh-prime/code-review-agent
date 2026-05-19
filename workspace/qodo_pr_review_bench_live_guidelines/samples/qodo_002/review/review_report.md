# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 3
- Changed entities: 3
- Risk signals: 0
- Findings: 0
- Needs human review: 2
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
| Retry count | 0 |
| Total latency | 49428 ms |
| Token in | 10673 |
| Token out | 908 |

- Iteration 0: 3 candidates, 2 verified, 2 uncertain, 0 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `file_risk_shards_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 9757 |
| Selected evidence | 6 |
| Omitted evidence | 175 |
| Context truncated | True |
| Review shards | 1 |
| Context requests | 1 |
| Refills | 1 |

## Findings

No findings.

Checked changed files, changed entities, deterministic risk signals, and evidence references. No high-confidence review finding was produced.

## Needs Human Review

- `api_breaking_change` high at `ghost/core/core/server/services/email-service/DomainWarmingService.ts:3` (0.50)
  - The EmailModel type changed from `findOne` to `findPage`, altering the return type from a single record to a paginated result set. This breaks all existing callers that depend on the old interface.
  - Suggestion: Ensure all callers of EmailModel are updated to handle the new paginated response (e.g., accessing `result.data` instead of a single record).
  - Evidence: `diff_hunk:ghost/core/core/server/services/email-service/DomainWarmingService.ts:3`

- `correctness` medium at `ghost/core/core/server/services/email-service/DomainWarmingService.ts:98` (0.50)
  - The `#getHighestCount` method now uses `findPage` with `created_at:<=` (including today) instead of the previous `created_at:<` (excluding today). This changes the semantics: the method is documented to return 'the highest number of messages sent from the CSD in a single email (excluding today)', but the new filter includes today's emails. This could cause the domain warming service to consider today's partially sent email count when calculating the next batch, potentially leading to incorrect scaling decisions.
  - Suggestion: Revert the filter to `created_at:<` to exclude today's emails, or update the documentation to reflect the new behavior if including today is intentional.
  - Evidence: `diff_hunk:ghost/core/core/server/services/email-service/DomainWarmingService.ts:98`

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
