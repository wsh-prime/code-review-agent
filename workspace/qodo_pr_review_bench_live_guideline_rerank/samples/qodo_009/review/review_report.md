# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 6
- Changed entities: 6
- Risk signals: 3
- Findings: 1
- Needs human review: 2
- Discarded: 2
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
| Total latency | 23971 ms |
| Token in | 11263 |
| Token out | 617 |

- Iteration 0: 4 candidates, 2 verified, 1 uncertain, 1 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `file_risk_shards_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 9069 |
| Selected evidence | 7 |
| Omitted evidence | 335 |
| Context truncated | True |
| Review shards | 2 |
| Context requests | 0 |
| Refills | 0 |

## Findings

- `correctness` high at `apps/activitypub/src/api/activitypub.test.ts:1610` (0.85)
  - The test mock for the bluesky enable endpoint now returns null response and no longer validates the handle in the response, which may mask regressions in the API response contract.
  - Suggestion: Add a response body that matches the expected API response shape, e.g., { handle: '@foo@bar.baz' } or the new shape if changed.
  - Evidence: `diff_hunk:apps/activitypub/src/api/activitypub.test.ts:1607`

## Needs Human Review

- `dependency_change` low at `apps/activitypub/package.json:3` (0.75)
  - Dependency declarations changed and should be reviewed with install/test impact in mind.
  - Suggestion: Confirm lock files, compatibility, and test coverage for the dependency change.
  - Evidence: `diff:apps/activitypub/package.json:3`, `risk:dependency_change:apps/activitypub/package.json`

- `correctness` error at `apps/activitypub/tsconfig.json:18` (0.50)
  - TypeScript Files Must Enable Strict Type Checking: 'strict' is set to false, which disables strict type checking and can allow potential runtime errors.
  - Suggestion: Set 'strict' back to true to enable full type checking.
  - Evidence: `diff_hunk:apps/activitypub/tsconfig.json:15`

## Changed Files

- `apps/activitypub/package.json` (modified)
- `apps/activitypub/src/api/activitypub.test.ts` (modified)
- `apps/activitypub/src/api/activitypub.ts` (modified)
- `apps/activitypub/src/hooks/use-activity-pub-queries.ts` (modified)
- `apps/activitypub/src/views/Preferences/components/BlueskySharing.tsx` (modified)
- `apps/activitypub/tsconfig.json` (modified)

## Changed Entities

- `apps/activitypub/package.json:3-3` module `apps.activitypub.package`
- `apps/activitypub/src/api/activitypub.test.ts:1610-1614` module `apps.activitypub.src.api.activitypub.test`
- `apps/activitypub/src/api/activitypub.ts:29-30` module `apps.activitypub.src.api.activitypub`
- `apps/activitypub/src/hooks/use-activity-pub-queries.ts:2725-2741` module `apps.activitypub.src.hooks.use-activity-pub-queries`
- `apps/activitypub/src/views/Preferences/components/BlueskySharing.tsx:4-4` module `apps.activitypub.src.views.Preferences.components.BlueskySharing`
- `apps/activitypub/tsconfig.json:18-18` module `apps.activitypub.tsconfig`

## Risk Signals

- `dependency_change` (0.84): Dependency declaration changed: apps/activitypub/package.json.
- `security_sensitive` (0.74): Security-sensitive keywords changed in apps/activitypub/src/api/activitypub.test.ts.
- `security_sensitive` (0.74): Security-sensitive keywords changed in apps/activitypub/src/views/Preferences/components/BlueskySharing.tsx.

## Evidence Index

- `diff:apps/activitypub/package.json:3` [diff]: apps/activitypub/package.json:3
- `diff:apps/activitypub/src/api/activitypub.test.ts:1610` [diff]: apps/activitypub/src/api/activitypub.test.ts:1610
- `diff:apps/activitypub/src/api/activitypub.test.ts:1611` [diff]: apps/activitypub/src/api/activitypub.test.ts:1611
- `diff:apps/activitypub/src/api/activitypub.test.ts:1612` [diff]: apps/activitypub/src/api/activitypub.test.ts:1612
- `diff:apps/activitypub/src/api/activitypub.test.ts:1613` [diff]: apps/activitypub/src/api/activitypub.test.ts:1613
- `diff:apps/activitypub/src/api/activitypub.test.ts:1614` [diff]: apps/activitypub/src/api/activitypub.test.ts:1614
- `diff:apps/activitypub/src/api/activitypub.test.ts:1624` [diff]: apps/activitypub/src/api/activitypub.test.ts:1624
- `diff:apps/activitypub/src/api/activitypub.test.ts:1625` [diff]: apps/activitypub/src/api/activitypub.test.ts:1625
- `diff:apps/activitypub/src/api/activitypub.test.ts:1626` [diff]: apps/activitypub/src/api/activitypub.test.ts:1626
- `diff:apps/activitypub/src/api/activitypub.test.ts:1627` [diff]: apps/activitypub/src/api/activitypub.test.ts:1627
- `diff:apps/activitypub/src/api/activitypub.test.ts:1629` [diff]: apps/activitypub/src/api/activitypub.test.ts:1629
- `diff:apps/activitypub/src/api/activitypub.test.ts:1630` [diff]: apps/activitypub/src/api/activitypub.test.ts:1630
- `diff:apps/activitypub/src/api/activitypub.test.ts:1638` [diff]: apps/activitypub/src/api/activitypub.test.ts:1638
- `diff:apps/activitypub/src/api/activitypub.test.ts:1639` [diff]: apps/activitypub/src/api/activitypub.test.ts:1639
- `diff:apps/activitypub/src/api/activitypub.test.ts:1640` [diff]: apps/activitypub/src/api/activitypub.test.ts:1640
- `diff:apps/activitypub/src/api/activitypub.test.ts:1641` [diff]: apps/activitypub/src/api/activitypub.test.ts:1641
- `diff:apps/activitypub/src/api/activitypub.test.ts:1642` [diff]: apps/activitypub/src/api/activitypub.test.ts:1642
- `diff:apps/activitypub/src/api/activitypub.test.ts:1650` [diff]: apps/activitypub/src/api/activitypub.test.ts:1650
- `diff:apps/activitypub/src/api/activitypub.test.ts:1651` [diff]: apps/activitypub/src/api/activitypub.test.ts:1651
- `diff:apps/activitypub/src/api/activitypub.test.ts:1652` [diff]: apps/activitypub/src/api/activitypub.test.ts:1652
- `diff:apps/activitypub/src/api/activitypub.test.ts:1654` [diff]: apps/activitypub/src/api/activitypub.test.ts:1654
- `diff:apps/activitypub/src/api/activitypub.test.ts:1655` [diff]: apps/activitypub/src/api/activitypub.test.ts:1655
- `diff:apps/activitypub/src/api/activitypub.test.ts:1656` [diff]: apps/activitypub/src/api/activitypub.test.ts:1656
- `diff:apps/activitypub/src/api/activitypub.test.ts:1658` [diff]: apps/activitypub/src/api/activitypub.test.ts:1658
- `diff:apps/activitypub/src/api/activitypub.test.ts:1659` [diff]: apps/activitypub/src/api/activitypub.test.ts:1659
- `diff:apps/activitypub/src/api/activitypub.test.ts:1664` [diff]: apps/activitypub/src/api/activitypub.test.ts:1664
- `diff:apps/activitypub/src/api/activitypub.test.ts:1666` [diff]: apps/activitypub/src/api/activitypub.test.ts:1666
- `diff:apps/activitypub/src/api/activitypub.test.ts:1668` [diff]: apps/activitypub/src/api/activitypub.test.ts:1668
- `diff:apps/activitypub/src/api/activitypub.test.ts:1670` [diff]: apps/activitypub/src/api/activitypub.test.ts:1670
- `diff:apps/activitypub/src/api/activitypub.test.ts:1678` [diff]: apps/activitypub/src/api/activitypub.test.ts:1678
- ... 312 more evidence items omitted.
