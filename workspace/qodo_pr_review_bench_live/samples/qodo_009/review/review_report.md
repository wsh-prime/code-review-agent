# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 6
- Changed entities: 6
- Risk signals: 3
- Findings: 0
- Needs human review: 4
- Discarded: 2
- Agent runs: 4
- Loop enabled: True
- Target repo modified: False

## Loop Summary

| Metric | Value |
|---|---:|
| Iterations | 1 / 1 |
| Converged | False |
| Fallback | False |
| Retry count | 1 |
| Total latency | 78892 ms |
| Token in | 13503 |
| Token out | 1577 |

- Iteration 0: 5 candidates, 3 verified, 3 uncertain, 0 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `file_risk_shards_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 10116 |
| Selected evidence | 20 |
| Omitted evidence | 322 |
| Context truncated | True |
| Review shards | 2 |
| Context requests | 3 |
| Refills | 1 |

## Findings

No findings.

Checked changed files, changed entities, deterministic risk signals, and evidence references. No high-confidence review finding was produced.

## Needs Human Review

- `dependency_change` low at `apps/activitypub/package.json:3` (0.75)
  - Dependency declarations changed and should be reviewed with install/test impact in mind.
  - Suggestion: Confirm lock files, compatibility, and test coverage for the dependency change.
  - Evidence: `diff:apps/activitypub/package.json:3`, `risk:dependency_change:apps/activitypub/package.json`

- `api_consistency` medium at `apps/activitypub/src/api/activitypub.ts:29` (0.50)
  - The Account interface replaces `blueskyHandle?: string` with `blueskyHandle?: string | null` and adds `blueskyHandleConfirmed?: boolean`. The test mock for the enable endpoint now returns `null` instead of a handle object, but the test does not verify that the new `blueskyHandleConfirmed` field is set correctly after the enable action.
  - Suggestion: Add an assertion in the test to verify that after calling the enable endpoint, the cached profile includes `blueskyHandleConfirmed: true` and `blueskyHandle` is set to the expected handle (not null).
  - Evidence: `diff_hunk:apps/activitypub/src/api/activitypub.test.ts:1607`, `diff_hunk:apps/activitypub/src/api/activitypub.ts:26`

- `api_consistency` medium at `apps/activitypub/src/hooks/use-activity-pub-queries.ts:2725` (0.50)
  - The `updateAccountBlueskyCache` function now accepts a `BlueskyDetails` object and spreads it into the cached profile. However, the test mock for the enable endpoint returns `null` as the response body, and the test does not show that the cache is updated with the correct `blueskyHandleConfirmed` and `blueskyHandle` values after a successful enable.
  - Suggestion: Ensure the test for the enable endpoint verifies that the query cache is updated with `blueskyHandleConfirmed: true` and a non-null `blueskyHandle`. Consider adding a test that calls the enable endpoint and then checks the cached profile.
  - Evidence: `diff_hunk:apps/activitypub/src/hooks/use-activity-pub-queries.ts:2722`, `diff_hunk:apps/activitypub/src/api/activitypub.test.ts:1607`

- `correctness` high at `apps/activitypub/tsconfig.json:18` (0.50)
  - Disabling strict mode removes TypeScript's strict null checks and other type safety guarantees, which can lead to runtime errors from null/undefined access or incorrect type assumptions.
  - Suggestion: Keep strict: true and fix any type errors instead of disabling strict mode.
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
