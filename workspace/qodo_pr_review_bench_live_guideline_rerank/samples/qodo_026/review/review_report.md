# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 14
- Changed entities: 14
- Risk signals: 0
- Findings: 0
- Needs human review: 2
- Discarded: 2
- Agent runs: 6
- Loop enabled: True
- Target repo modified: False

## Loop Summary

| Metric | Value |
|---|---:|
| Iterations | 1 / 1 |
| Converged | False |
| Fallback | False |
| Retry count | 0 |
| Total latency | 57358 ms |
| Token in | 32620 |
| Token out | 1411 |

- Iteration 0: 4 candidates, 2 verified, 2 uncertain, 0 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `file_risk_shards_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 25426 |
| Selected evidence | 22 |
| Omitted evidence | 296 |
| Context truncated | True |
| Review shards | 4 |
| Context requests | 1 |
| Refills | 1 |

## Findings

No findings.

Checked changed files, changed entities, deterministic risk signals, and evidence references. No high-confidence review finding was produced.

## Needs Human Review

- `correctness` medium at `apps/api/v2/src/ee/bookings/2024-08-13/services/output.service.ts:96` (0.50)
  - The new `getDisplayEmail` method strips a 25-character alphanumeric suffix after a '+' from an email address, but the regex pattern `/\+[a-zA-Z0-9]{25}/` only matches exactly 25 characters. If the plus-suffix is shorter or longer, the replacement silently fails, leaving the full email unchanged. This can cause displayEmail to equal the raw email when it should have been sanitized, or fail to match a valid plus-suffix of a different length.
  - Suggestion: Use a more flexible pattern such as `/\+[a-zA-Z0-9]+/` to match any length of alphanumeric plus-suffix, or validate the expected suffix length against the actual data to ensure the regex matches correctly.
  - Evidence: `diff_hunk:apps/api/v2/src/ee/bookings/2024-08-13/services/output.service.ts:93`

- `maintainability` medium at `apps/api/v2/src/ee/bookings/2024-08-13/services/output.service.ts:131` (0.50)
  - The getDisplayEmail method is called repeatedly with the same attendee email in multiple hunks (lines 131, 154, 216, 275, 299, 383). If getDisplayEmail performs any non-trivial computation or I/O, this could be inefficient.
  - Suggestion: Consider caching the result of getDisplayEmail for a given email within the request scope, or ensure the method is lightweight.
  - Evidence: `diff_hunk:apps/api/v2/src/ee/bookings/2024-08-13/services/output.service.ts:131`, `diff_hunk:apps/api/v2/src/ee/bookings/2024-08-13/services/output.service.ts:154`, `diff_hunk:apps/api/v2/src/ee/bookings/2024-08-13/services/output.service.ts:216`, `diff_hunk:apps/api/v2/src/ee/bookings/2024-08-13/services/output.service.ts:275`, `diff_hunk:apps/api/v2/src/ee/bookings/2024-08-13/services/output.service.ts:299`, `diff_hunk:apps/api/v2/src/ee/bookings/2024-08-13/services/output.service.ts:383`

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
