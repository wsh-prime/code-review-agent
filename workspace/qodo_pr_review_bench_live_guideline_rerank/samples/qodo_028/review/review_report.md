# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 6
- Changed entities: 6
- Risk signals: 4
- Findings: 2
- Needs human review: 0
- Discarded: 0
- Agent runs: 3
- Loop enabled: True
- Target repo modified: False

## Loop Summary

| Metric | Value |
|---|---:|
| Iterations | 1 / 1 |
| Converged | True |
| Fallback | False |
| Retry count | 2 |
| Total latency | 186033 ms |
| Token in | 4841 |
| Token out | 314 |

- Iteration 0: 2 candidates, 2 verified, 0 uncertain, 2 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `file_risk_shards_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 11000 |
| Selected evidence | 8 |
| Omitted evidence | 218 |
| Context truncated | True |
| Review shards | 2 |
| Context requests | 0 |
| Refills | 0 |

## Findings

- `bug_risk` high at `packages/features/ee/teams/services/teamService.ts:99` (0.95)
  - The condition for buildInviteLink is inverted, causing org context to return the generic invite link instead of the getting-started path.
  - Suggestion: Revert the condition back to `if (!isOrgContext)` to preserve original behavior where non-org contexts get the generic link and org contexts get the getting-started path.
  - Evidence: `diff_hunk:packages/features/ee/teams/services/teamService.ts:96`

- `security` medium at `packages/features/ee/teams/services/teamService.ts:99` (0.85)
  - The returned token is now `newToken.identifier` instead of the original `token` variable, but `buildInviteLink` still uses the original `token` parameter, creating a mismatch between the returned token and the one embedded in the invite link.
  - Suggestion: Either pass `newToken.identifier` to `buildInviteLink` or return the original `token` to ensure consistency between the returned token and the link.
  - Evidence: `diff_hunk:packages/features/ee/teams/services/teamService.ts:85`, `diff_hunk:packages/features/ee/teams/services/teamService.ts:96`

## Needs Human Review

None.

## Changed Files

- `apps/api/v2/src/ee/platform-endpoints-module.ts` (modified)
- `apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts` (added)
- `apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.ts` (added)
- `apps/api/v2/src/modules/teams/invite/outputs/invite.output.ts` (added)
- `apps/api/v2/src/modules/teams/invite/teams-invite.module.ts` (added)
- `packages/features/ee/teams/services/teamService.ts` (modified)

## Changed Entities

- `apps/api/v2/src/ee/platform-endpoints-module.ts:16-16` module `apps.api.v2.src.ee.platform-endpoints-module`
- `apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:1-209` module `apps.api.v2.src.modules.teams.invite.controllers.teams-invite.controller.e2e-spec`
- `apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.ts:1-41` module `apps.api.v2.src.modules.teams.invite.controllers.teams-invite.controller`
- `apps/api/v2/src/modules/teams/invite/outputs/invite.output.ts:1-38` module `apps.api.v2.src.modules.teams.invite.outputs.invite.output`
- `apps/api/v2/src/modules/teams/invite/teams-invite.module.ts:1-11` module `apps.api.v2.src.modules.teams.invite.teams-invite.module`
- `packages/features/ee/teams/services/teamService.ts:88-88` module `packages.features.ee.teams.services.teamService`

## Risk Signals

- `security_sensitive` (0.74): Security-sensitive keywords changed in apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts.
- `security_sensitive` (0.74): Security-sensitive keywords changed in apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.ts.
- `security_sensitive` (0.74): Security-sensitive keywords changed in apps/api/v2/src/modules/teams/invite/outputs/invite.output.ts.
- `security_sensitive` (0.74): Security-sensitive keywords changed in packages/features/ee/teams/services/teamService.ts.

## Evidence Index

- `diff:apps/api/v2/src/ee/platform-endpoints-module.ts:16` [diff]: apps/api/v2/src/ee/platform-endpoints-module.ts:16
- `diff:apps/api/v2/src/ee/platform-endpoints-module.ts:36` [diff]: apps/api/v2/src/ee/platform-endpoints-module.ts:36
- `diff:apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:1` [diff]: apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:1
- `diff:apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:10` [diff]: apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:10
- `diff:apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:100` [diff]: apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:100
- `diff:apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:101` [diff]: apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:101
- `diff:apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:102` [diff]: apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:102
- `diff:apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:103` [diff]: apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:103
- `diff:apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:104` [diff]: apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:104
- `diff:apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:105` [diff]: apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:105
- `diff:apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:106` [diff]: apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:106
- `diff:apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:107` [diff]: apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:107
- `diff:apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:108` [diff]: apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:108
- `diff:apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:109` [diff]: apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:109
- `diff:apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:11` [diff]: apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:11
- `diff:apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:110` [diff]: apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:110
- `diff:apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:111` [diff]: apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:111
- `diff:apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:112` [diff]: apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:112
- `diff:apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:113` [diff]: apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:113
- `diff:apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:114` [diff]: apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:114
- `diff:apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:115` [diff]: apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:115
- `diff:apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:116` [diff]: apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:116
- `diff:apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:117` [diff]: apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:117
- `diff:apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:118` [diff]: apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:118
- `diff:apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:119` [diff]: apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:119
- `diff:apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:12` [diff]: apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:12
- `diff:apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:120` [diff]: apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:120
- `diff:apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:121` [diff]: apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:121
- `diff:apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:122` [diff]: apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:122
- `diff:apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:123` [diff]: apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:123
- ... 294 more evidence items omitted.
