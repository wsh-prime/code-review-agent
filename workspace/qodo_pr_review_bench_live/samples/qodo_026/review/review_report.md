# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 14
- Changed entities: 14
- Risk signals: 0
- Findings: 0
- Needs human review: 0
- Discarded: 1
- Agent runs: 5
- Loop enabled: True
- Target repo modified: False

## Loop Summary

| Metric | Value |
|---|---:|
| Iterations | 1 / 1 |
| Converged | True |
| Fallback | False |
| Retry count | 2 |
| Total latency | 138561 ms |
| Token in | 21186 |
| Token out | 284 |

- Iteration 0: 1 candidates, 0 verified, 0 uncertain, 0 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `file_risk_shards_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 14259 |
| Selected evidence | 14 |
| Omitted evidence | 304 |
| Context truncated | True |
| Review shards | 4 |
| Context requests | 0 |
| Refills | 0 |

## Findings

No findings.

Checked changed files, changed entities, deterministic risk signals, and evidence references. No high-confidence review finding was produced.

## Needs Human Review

None.

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
