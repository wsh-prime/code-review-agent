# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 14
- Changed entities: 14
- Risk signals: 0
- Findings: 0
- Needs human review: 1
- Discarded: 3
- Agent runs: 7
- Loop enabled: True
- Target repo modified: False

## Loop Summary

| Metric | Value |
|---|---:|
| Iterations | 1 / 1 |
| Converged | False |
| Fallback | False |
| Retry count | 1 |
| Total latency | 141878 ms |
| Token in | 34754 |
| Token out | 1667 |

- Iteration 0: 4 candidates, 1 verified, 1 uncertain, 0 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `file_risk_shards_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 27293 |
| Selected evidence | 27 |
| Omitted evidence | 291 |
| Context truncated | True |
| Review shards | 4 |
| Context requests | 3 |
| Refills | 2 |

## Findings

No findings.

Checked changed files, changed entities, deterministic risk signals, and evidence references. No high-confidence review finding was produced.

## Needs Human Review

- `correctness` medium at `apps/api/v2/src/ee/bookings/2024-08-13/services/output.service.ts:96` (0.50)
  - The regex in getDisplayEmail only strips a plus sign followed by exactly 25 alphanumeric characters, but email sub-addressing (plus addressing) can have variable-length tags. This will fail to strip tags of different lengths, causing displayEmail to still contain the sub-address suffix.
  - Suggestion: Use a more flexible regex like /\+[a-zA-Z0-9]+/ to match any length of sub-addressing tag, or use email.split('@')[0].split('+')[0] + '@' + email.split('@')[1] to reliably extract the base email.
  - Evidence: `diff_hunk:apps/api/v2/src/ee/bookings/2024-08-13/services/output.service.ts:93`

## Changed Files

- `.github/oasdiff-err-ignore.txt` (modified)
- `apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/api-key-bookings.e2e-spec.ts` (modified)
- `apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/managed-user-bookings.e2e-spec.ts` (modified)
- `apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/reassign-bookings.e2e-spec.ts` (modified)
- `apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/recurring-bookings.e2e-spec.ts` (modified)
- `apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/seated-bookings.e2e-spec.ts` (modified)
- `apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/team-bookings.e2e-spec.ts` (modified)
- `apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/user-bookings.e2e-spec.ts` (modified)
- `apps/api/v2/src/ee/bookings/2024-08-13/services/output.service.ts` (modified)
- `apps/api/v2/src/modules/organizations/bookings/organizations-bookings.controller.e2e-spec.ts` (modified)
- `apps/api/v2/src/modules/organizations/teams/bookings/organizations-teams-bookings.controller.e2e-spec.ts` (modified)
- `apps/api/v2/src/modules/organizations/users/bookings/controllers/organizations-users-bookings.e2e-spec.ts` (modified)
- `docs/api-reference/v2/openapi.json` (modified)
- `packages/platform/types/bookings/2024-08-13/outputs/booking.output.ts` (modified)

## Changed Entities

- `.github/oasdiff-err-ignore.txt:5-10` module `.github.oasdiff-err-ignore`
- `apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/api-key-bookings.e2e-spec.ts:180-180` module `apps.api.v2.src.ee.bookings.2024-08-13.controllers.e2e.api-key-bookings.e2e-spec`
- `apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/managed-user-bookings.e2e-spec.ts:627-711` module `apps.api.v2.src.ee.bookings.2024-08-13.controllers.e2e.managed-user-bookings.e2e-spec`
- `apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/reassign-bookings.e2e-spec.ts:495-495` module `apps.api.v2.src.ee.bookings.2024-08-13.controllers.e2e.reassign-bookings.e2e-spec`
- `apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/recurring-bookings.e2e-spec.ts:188-188` module `apps.api.v2.src.ee.bookings.2024-08-13.controllers.e2e.recurring-bookings.e2e-spec`
- `apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/seated-bookings.e2e-spec.ts:204-204` module `apps.api.v2.src.ee.bookings.2024-08-13.controllers.e2e.seated-bookings.e2e-spec`
- `apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/team-bookings.e2e-spec.ts:522-522` module `apps.api.v2.src.ee.bookings.2024-08-13.controllers.e2e.team-bookings.e2e-spec`
- `apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/user-bookings.e2e-spec.ts:486-486` module `apps.api.v2.src.ee.bookings.2024-08-13.controllers.e2e.user-bookings.e2e-spec`
- `apps/api/v2/src/ee/bookings/2024-08-13/services/output.service.ts:96-99` module `apps.api.v2.src.ee.bookings.2024-08-13.services.output.service`
- `apps/api/v2/src/modules/organizations/bookings/organizations-bookings.controller.e2e-spec.ts:338-338` module `apps.api.v2.src.modules.organizations.bookings.organizations-bookings.controller.e2e-spec`
- `apps/api/v2/src/modules/organizations/teams/bookings/organizations-teams-bookings.controller.e2e-spec.ts:253-253` module `apps.api.v2.src.modules.organizations.teams.bookings.organizations-teams-bookings.controller.e2e-spec`
- `apps/api/v2/src/modules/organizations/users/bookings/controllers/organizations-users-bookings.e2e-spec.ts:236-236` module `apps.api.v2.src.modules.organizations.users.bookings.controllers.organizations-users-bookings.e2e-spec`
- `docs/api-reference/v2/openapi.json:31715-31719` module `docs.api-reference.v2.openapi`
- `packages/platform/types/bookings/2024-08-13/outputs/booking.output.ts:32-36` module `packages.platform.types.bookings.2024-08-13.outputs.booking.output`

## Risk Signals

None.

## Evidence Index

- `diff:.github/oasdiff-err-ignore.txt:10` [diff]: .github/oasdiff-err-ignore.txt:10
- `diff:.github/oasdiff-err-ignore.txt:5` [diff]: .github/oasdiff-err-ignore.txt:5
- `diff:.github/oasdiff-err-ignore.txt:6` [diff]: .github/oasdiff-err-ignore.txt:6
- `diff:.github/oasdiff-err-ignore.txt:7` [diff]: .github/oasdiff-err-ignore.txt:7
- `diff:.github/oasdiff-err-ignore.txt:8` [diff]: .github/oasdiff-err-ignore.txt:8
- `diff:.github/oasdiff-err-ignore.txt:9` [diff]: .github/oasdiff-err-ignore.txt:9
- `diff:apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/api-key-bookings.e2e-spec.ts:180` [diff]: apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/api-key-bookings.e2e-spec.ts:180
- `diff:apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/managed-user-bookings.e2e-spec.ts:627` [diff]: apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/managed-user-bookings.e2e-spec.ts:627
- `diff:apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/managed-user-bookings.e2e-spec.ts:628` [diff]: apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/managed-user-bookings.e2e-spec.ts:628
- `diff:apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/managed-user-bookings.e2e-spec.ts:629` [diff]: apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/managed-user-bookings.e2e-spec.ts:629
- `diff:apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/managed-user-bookings.e2e-spec.ts:630` [diff]: apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/managed-user-bookings.e2e-spec.ts:630
- `diff:apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/managed-user-bookings.e2e-spec.ts:631` [diff]: apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/managed-user-bookings.e2e-spec.ts:631
- `diff:apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/managed-user-bookings.e2e-spec.ts:632` [diff]: apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/managed-user-bookings.e2e-spec.ts:632
- `diff:apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/managed-user-bookings.e2e-spec.ts:633` [diff]: apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/managed-user-bookings.e2e-spec.ts:633
- `diff:apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/managed-user-bookings.e2e-spec.ts:634` [diff]: apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/managed-user-bookings.e2e-spec.ts:634
- `diff:apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/managed-user-bookings.e2e-spec.ts:635` [diff]: apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/managed-user-bookings.e2e-spec.ts:635
- `diff:apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/managed-user-bookings.e2e-spec.ts:636` [diff]: apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/managed-user-bookings.e2e-spec.ts:636
- `diff:apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/managed-user-bookings.e2e-spec.ts:637` [diff]: apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/managed-user-bookings.e2e-spec.ts:637
- `diff:apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/managed-user-bookings.e2e-spec.ts:638` [diff]: apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/managed-user-bookings.e2e-spec.ts:638
- `diff:apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/managed-user-bookings.e2e-spec.ts:639` [diff]: apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/managed-user-bookings.e2e-spec.ts:639
- `diff:apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/managed-user-bookings.e2e-spec.ts:640` [diff]: apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/managed-user-bookings.e2e-spec.ts:640
- `diff:apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/managed-user-bookings.e2e-spec.ts:641` [diff]: apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/managed-user-bookings.e2e-spec.ts:641
- `diff:apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/managed-user-bookings.e2e-spec.ts:642` [diff]: apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/managed-user-bookings.e2e-spec.ts:642
- `diff:apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/managed-user-bookings.e2e-spec.ts:643` [diff]: apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/managed-user-bookings.e2e-spec.ts:643
- `diff:apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/managed-user-bookings.e2e-spec.ts:644` [diff]: apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/managed-user-bookings.e2e-spec.ts:644
- `diff:apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/managed-user-bookings.e2e-spec.ts:645` [diff]: apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/managed-user-bookings.e2e-spec.ts:645
- `diff:apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/managed-user-bookings.e2e-spec.ts:646` [diff]: apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/managed-user-bookings.e2e-spec.ts:646
- `diff:apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/managed-user-bookings.e2e-spec.ts:647` [diff]: apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/managed-user-bookings.e2e-spec.ts:647
- `diff:apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/managed-user-bookings.e2e-spec.ts:648` [diff]: apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/managed-user-bookings.e2e-spec.ts:648
- `diff:apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/managed-user-bookings.e2e-spec.ts:649` [diff]: apps/api/v2/src/ee/bookings/2024-08-13/controllers/e2e/managed-user-bookings.e2e-spec.ts:649
- ... 288 more evidence items omitted.
