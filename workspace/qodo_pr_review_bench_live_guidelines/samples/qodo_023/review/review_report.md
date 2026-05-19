# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 6
- Changed entities: 6
- Risk signals: 1
- Findings: 2
- Needs human review: 1
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
| Total latency | 20599 ms |
| Token in | 12907 |
| Token out | 585 |

- Iteration 0: 3 candidates, 3 verified, 1 uncertain, 2 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `file_risk_shards_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 10962 |
| Selected evidence | 7 |
| Omitted evidence | 400 |
| Context truncated | True |
| Review shards | 2 |
| Context requests | 0 |
| Refills | 0 |

## Findings

- `security` high at `packages/trpc/server/routers/viewer/bookings/get.handler.ts:943` (0.85)
  - The patch removes the admin/owner membership check (getEventTypeIdsWhereUserIsAdminOrOwner) and replaces it with a function (getUserIdsAndEmailsFromTeamIds) that accepts arbitrary teamIds without verifying the requesting user's role. This allows any authenticated user to enumerate members and emails of any team by providing teamIds, bypassing the previous authorization guard.
  - Suggestion: Reintroduce a membership condition check that ensures the requesting user is an admin or owner of the specified teams before returning member IDs and emails. Alternatively, validate that the provided teamIds are teams where the user has the required role.
  - Evidence: `diff_hunk:packages/trpc/server/routers/viewer/bookings/get.handler.ts:943`

- `architecture` medium at `packages/trpc/server/routers/viewer/bookings/get.handler.ts:5` (0.95)
  - The import of PermissionCheckService from '@calcom/features/pbac/services/permission-check.service' introduces a cross-package dependency from trpc to features, violating the 'Prevent Circular Dependencies Between Core Packages' guideline which states that trpc must not import from features.
  - Suggestion: Move the permission check logic to a shared package that both trpc and features can depend on, or refactor to avoid the dependency.
  - Evidence: `diff_hunk:packages/trpc/server/routers/viewer/bookings/get.handler.ts:5`

## Needs Human Review

- `architecture` error at `packages/features/pbac/services/permission-check.service.ts:3` (0.50)
  - Importing from @trpc/server in a features package violates the 'Prevent Circular Dependencies Between Core Packages' guideline: features must not import from trpc.
  - Suggestion: Remove the TRPCError import and use a features-specific error class or a shared error utility instead.
  - Evidence: `diff_hunk:packages/features/pbac/services/permission-check.service.ts:3`

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
