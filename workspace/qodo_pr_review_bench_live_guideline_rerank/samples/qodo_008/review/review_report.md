# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 3
- Changed entities: 3
- Risk signals: 0
- Findings: 0
- Needs human review: 2
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
| Total latency | 82887 ms |
| Token in | 10125 |
| Token out | 936 |

- Iteration 0: 4 candidates, 4 verified, 4 uncertain, 0 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `file_risk_shards_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 8518 |
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
  - The new time-based warmup formula uses a hardcoded end value of 200000 and totalDays of 42, but the integration test expects a limit of 237 on day 2. The formula `start * (end/start)^(day/(totalDays-1))` with start=200, end=200000, totalDays=42, day=1 gives 200 * (1000)^(1/41) ≈ 200 * 1.182 ≈ 236.4, which rounds to 236, not 237. The test assertion expects 237, indicating a mismatch between the implementation and the test expectation.
  - Suggestion: Verify the exact formula implementation and ensure the test expectation matches. Either adjust the formula to produce 237 or correct the test to expect 236.
  - Evidence: `diff_hunk:ghost/core/core/server/services/email-service/DomainWarmingService.ts:15`, `diff_hunk:ghost/core/test/integration/services/email-service/domain-warming.test.js:195`

- `correctness` medium at `ghost/core/test/integration/services/email-service/domain-warming.test.js:195` (0.50)
  - The integration test hardcodes the expected limit for day 2 as 237, but this value is derived from a specific formula and configuration. If the warmup configuration (start, end, totalDays) changes, this test will silently break without indicating which part of the logic is incorrect. The test should derive the expected value from the configuration rather than hardcoding it.
  - Suggestion: Consider computing the expected limit dynamically from the DefaultWarmupOptions configuration to make the test resilient to configuration changes.
  - Evidence: `diff_hunk:ghost/core/test/integration/services/email-service/domain-warming.test.js:195`

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
