# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 6
- Changed entities: 6
- Risk signals: 1
- Findings: 1
- Needs human review: 1
- Discarded: 1
- Agent runs: 5
- Loop enabled: True
- Target repo modified: False

## Loop Summary

| Metric | Value |
|---|---:|
| Iterations | 1 / 1 |
| Converged | False |
| Fallback | False |
| Retry count | 2 |
| Total latency | 248557 ms |
| Token in | 24670 |
| Token out | 2387 |

- Iteration 0: 6 candidates, 5 verified, 4 uncertain, 1 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `file_risk_shards_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 20882 |
| Selected evidence | 26 |
| Omitted evidence | 381 |
| Context truncated | True |
| Review shards | 2 |
| Context requests | 3 |
| Refills | 2 |

## Findings

- `maintainability` medium at `packages/trpc/server/routers/viewer/bookings/get.handler.ts:5` (0.80)
  - The import of `PermissionCheckService` from `@calcom/features/pbac/services/permission-check.service` may introduce a circular dependency between `trpc` and `features` packages, violating the guideline 'Prevent Circular Dependencies Between Core Packages' which states that `trpc` should not import from `features`.
  - Suggestion: Move the permission check logic to a shared package that both `trpc` and `features` can depend on, or refactor to avoid the cross-package import.
  - Evidence: `diff_hunk:packages/trpc/server/routers/viewer/bookings/get.handler.ts:5`

## Needs Human Review

- `bug_risk` high at `packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:215` (0.50)
  - getTeamIdsWithPermission does not pass orgId to getTeamIdsWithPermissions, so the orgId parameter is silently ignored.
  - Suggestion: Pass orgId to getTeamIdsWithPermissions: return this.getTeamIdsWithPermissions({ userId, permissions: [permission], fallbackRoles, orgId });
  - Evidence: `diff_hunk:packages/features/pbac/infrastructure/repositories/PermissionRepository.ts:212`

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
