# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 6
- Changed entities: 6
- Risk signals: 1
- Findings: 0
- Needs human review: 3
- Discarded: 0
- Agent runs: 4
- Loop enabled: True
- Target repo modified: False

## Loop Summary

| Metric | Value |
|---|---:|
| Iterations | 1 / 1 |
| Converged | False |
| Fallback | False |
| Retry count | 0 |
| Total latency | 91305 ms |
| Token in | 15283 |
| Token out | 1658 |

- Iteration 0: 5 candidates, 5 verified, 5 uncertain, 0 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `file_risk_shards_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 11909 |
| Selected evidence | 22 |
| Omitted evidence | 385 |
| Context truncated | True |
| Review shards | 2 |
| Context requests | 2 |
| Refills | 1 |

## Findings

No findings.

Checked changed files, changed entities, deterministic risk signals, and evidence references. No high-confidence review finding was produced.

## Needs Human Review

- `bug_risk` high at `packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:220` (0.50)
  - getTeamIdsWithPermission ignores the new orgId parameter and delegates to getTeamIdsWithPermissions without passing orgId.
  - Suggestion: Pass orgId to getTeamIdsWithPermissions: return this.getTeamIdsWithPermissions({ userId, permissions: [permission], fallbackRoles, orgId });
  - Evidence: `diff_hunk:packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:212`

- `potential_bug` high at `packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:277` (0.50)
  - The SQL filter `AND (${orgId}::bigint IS NULL OR t."id" = ${orgId} OR t."parentId" = ${orgId})` in `getTeamsWithPBACPermissions` uses `t."parentId" = ${orgId}` which incorrectly matches child teams whose parent is the org, but the intent is to scope to teams within the org. This may include teams that are not directly under the org if the orgId is a team's parentId, leading to incorrect permission resolution.
  - Suggestion: Review the filtering logic: if the goal is to scope to teams belonging to the organization (orgId), consider using a join on an organization-teams mapping or a hierarchical query that ensures the team is under the org's hierarchy, not just where the team's parentId equals the orgId.
  - Evidence: `diff_hunk:packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:277`

- `security` high at `packages/trpc/server/routers/viewer/bookings/get.handler.ts:943` (0.50)
  - The function `getUserIdsAndEmailsFromTeamIds` replaces `getUserIdsAndEmailsWhereUserIsAdminOrOwner`, removing the membership condition that restricted results to teams where the user is ADMIN/OWNER. Now any team ID can be passed, potentially exposing user IDs and emails to unauthorized callers.
  - Suggestion: Reintroduce an authorization check to ensure the caller has ADMIN/OWNER role in the specified teams, or validate that the team IDs are derived from a trusted source.
  - Evidence: `diff_hunk:packages/trpc/server/routers/viewer/bookings/get.handler.ts:943`

## Changed Files

- `packages/features/pbac/domain/repositories/IPermissionRepository.ts` (modified)
- `packages/features/pbac/infrastructure/repositories/PermissionRepository.ts` (modified)
- `packages/features/pbac/infrastructure/repositories/__tests__/PermissionRepository.integration-test.ts` (modified)
- `packages/features/pbac/services/permission-check.service.ts` (modified)
- `packages/trpc/server/routers/viewer/bookings/get.handler.test.ts` (added)
- `packages/trpc/server/routers/viewer/bookings/get.handler.ts` (modified)

## Changed Entities

- `packages/features/pbac/domain/repositories/IPermissionRepository.ts:66-83` module `packages.features.pbac.domain.repositories.IPermissionRepository`
- `packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:215-220` module `packages.features.pbac.infrastructure.repositories.PermissionRepository`
- `packages/features/pbac/infrastructure/repositories/__tests__/PermissionRepository.integration-test.ts:972-1098` module `packages.features.pbac.infrastructure.repositories.__tests__.PermissionRepository.integration-test`
- `packages/features/pbac/services/permission-check.service.ts:6-6` module `packages.features.pbac.services.permission-check.service`
- `packages/trpc/server/routers/viewer/bookings/get.handler.test.ts:1-383` module `packages.trpc.server.routers.viewer.bookings.get.handler.test`
- `packages/trpc/server/routers/viewer/bookings/get.handler.ts:8-8` module `packages.trpc.server.routers.viewer.bookings.get.handler`

## Risk Signals

- `security_sensitive` (0.74): Security-sensitive keywords changed in packages/trpc/server/routers/viewer/bookings/get.handler.ts.

## Evidence Index

- `diff:packages/features/pbac/domain/repositories/IPermissionRepository.ts:66` [diff]: packages/features/pbac/domain/repositories/IPermissionRepository.ts:66
- `diff:packages/features/pbac/domain/repositories/IPermissionRepository.ts:72` [diff]: packages/features/pbac/domain/repositories/IPermissionRepository.ts:72
- `diff:packages/features/pbac/domain/repositories/IPermissionRepository.ts:77` [diff]: packages/features/pbac/domain/repositories/IPermissionRepository.ts:77
- `diff:packages/features/pbac/domain/repositories/IPermissionRepository.ts:83` [diff]: packages/features/pbac/domain/repositories/IPermissionRepository.ts:83
- `diff:packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:215` [diff]: packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:215
- `diff:packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:220` [diff]: packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:220
- `diff:packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:229` [diff]: packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:229
- `diff:packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:234` [diff]: packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:234
- `diff:packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:244` [diff]: packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:244
- `diff:packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:245` [diff]: packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:245
- `diff:packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:248` [diff]: packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:248
- `diff:packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:249` [diff]: packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:249
- `diff:packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:250` [diff]: packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:250
- `diff:packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:251` [diff]: packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:251
- `diff:packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:252` [diff]: packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:252
- `diff:packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:253` [diff]: packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:253
- `diff:packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:254` [diff]: packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:254
- `diff:packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:255` [diff]: packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:255
- `diff:packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:256` [diff]: packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:256
- `diff:packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:257` [diff]: packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:257
- `diff:packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:258` [diff]: packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:258
- `diff:packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:259` [diff]: packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:259
- `diff:packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:260` [diff]: packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:260
- `diff:packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:261` [diff]: packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:261
- `diff:packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:262` [diff]: packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:262
- `diff:packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:263` [diff]: packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:263
- `diff:packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:264` [diff]: packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:264
- `diff:packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:265` [diff]: packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:265
- `diff:packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:266` [diff]: packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:266
- `diff:packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:267` [diff]: packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:267
- ... 732 more evidence items omitted.
