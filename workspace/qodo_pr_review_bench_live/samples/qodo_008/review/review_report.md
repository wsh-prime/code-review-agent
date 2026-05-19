# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 3
- Changed entities: 3
- Risk signals: 0
- Findings: 0
- Needs human review: 3
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
| Retry count | 0 |
| Total latency | 63292 ms |
| Token in | 6992 |
| Token out | 934 |

- Iteration 0: 3 candidates, 3 verified, 3 uncertain, 0 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `file_risk_shards_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 5317 |
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

- `correctness` high at `ghost/core/core/server/services/email-service/DomainWarmingService.ts:15` (0.50)
  - The patch replaces a detailed warmup scaling table with a simple linear interpolation formula (start * (end/start)^(day/(totalDays-1))) but the provided evidence does not show the actual calculation logic. The integration test asserts a hardcoded value of 237 for day 1, which is derived from the formula, but the formula itself is not visible in the evidence. This could lead to incorrect volume calculations if the formula is misimplemented or if edge cases (e.g., totalDays=0, start=0) are not handled.
  - Suggestion: Ensure the time-based warmup formula is correctly implemented and handles edge cases such as zero or negative values for start, end, or totalDays. Add unit tests for the formula directly.
  - Evidence: `diff_hunk:ghost/core/core/server/services/email-service/DomainWarmingService.ts:15`, `diff_hunk:ghost/core/test/integration/services/email-service/domain-warming.test.js:195`

- `correctness` medium at `ghost/core/test/integration/services/email-service/domain-warming.test.js:195` (0.50)
  - The integration test asserts a hardcoded expected limit of 237 for day 2, which is derived from the time-based warmup formula. This value is brittle and will break if the default warmup options (start=200, end=200000, totalDays=42) change. The test does not verify the formula itself, only a specific numeric output.
  - Suggestion: Instead of hardcoding the expected value, compute it dynamically using the same formula as the production code, or add a separate unit test for the formula to avoid brittle integration tests.
  - Evidence: `diff_hunk:ghost/core/test/integration/services/email-service/domain-warming.test.js:195`

- `potential_bug` high at `ghost/core/core/server/services/email-service/DomainWarmingService.ts:61` (0.50)
  - The new warmup limit calculation uses exponential growth formula that may produce unexpectedly high limits for early days, potentially exceeding intended warmup constraints.
  - Suggestion: Verify the exponential formula produces correct limits for all days, especially day 0 and day 1. Consider adding unit tests with edge cases.
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
