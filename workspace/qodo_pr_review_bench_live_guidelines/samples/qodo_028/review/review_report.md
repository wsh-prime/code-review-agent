# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 6
- Changed entities: 6
- Risk signals: 4
- Findings: 4
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
| Retry count | 0 |
| Total latency | 60105 ms |
| Token in | 22403 |
| Token out | 2028 |

- Iteration 0: 5 candidates, 4 verified, 0 uncertain, 4 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `file_risk_shards_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 17710 |
| Selected evidence | 14 |
| Omitted evidence | 213 |
| Context truncated | True |
| Review shards | 2 |
| Context requests | 3 |
| Refills | 2 |

## Findings

- `security` high at `apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.ts:1` (0.70)
  - The controller uses @Roles("TEAM_MEMBER") guard but the endpoint creates a team invite. The evidence shows the test creates an admin membership, but the role check is for TEAM_MEMBER, which may allow non-admin members to create invites, potentially leading to unauthorized invite generation.
  - Suggestion: Verify that TEAM_MEMBER role is the intended authorization level for creating invites. If only admins should create invites, change the role to "ADMIN" or add an additional role check.
  - Evidence: `diff_hunk:apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:1`, `diff_hunk:apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.ts:1`

- `bug_risk` high at `packages/features/ee/teams/services/teamService.ts:99` (0.85)
  - Negated condition in buildInviteLink: the logic now returns the teamInviteLink when isOrgContext is true, which is the opposite of the original behavior. This likely inverts the invite link flow for organization contexts.
  - Suggestion: Verify that the condition negation is intentional. If the original behavior was correct, revert the change from `if (!isOrgContext)` to `if (isOrgContext)`.
  - Evidence: `diff_hunk:packages/features/ee/teams/services/teamService.ts:85`, `diff_hunk:packages/features/ee/teams/services/teamService.ts:96`

- `logic_error` high at `packages/features/ee/teams/services/teamService.ts:106` (0.95)
  - Inverted condition in buildInviteLink: the patch flips the guard from `if (!isOrgContext)` to `if (isOrgContext)`, which now returns the teamInviteLink directly for org contexts instead of the getting-started path. This breaks the intended flow for organization invitations.
  - Suggestion: Revert the condition back to `if (!isOrgContext)` or ensure the logic correctly distinguishes org vs non-org contexts.
  - Evidence: `diff_hunk:packages/features/ee/teams/services/teamService.ts:96`, `diff:packages/features/ee/teams/services/teamService.ts:106`

- `potential_bug` medium at `packages/features/ee/teams/services/teamService.ts:88` (0.80)
  - Return value changed from `token` (the raw random hex) to `newToken.identifier` (the invite-link identifier). The identifier is a static string `invite-link-for-teamId-${teamId}`, which is not a secret and may leak internal team IDs. Callers expecting a secure token may now receive a predictable value.
  - Suggestion: Return the actual token (`newToken.token`) instead of the identifier, or confirm that all callers expect the identifier.
  - Evidence: `diff_hunk:packages/features/ee/teams/services/teamService.ts:85`, `diff:packages/features/ee/teams/services/teamService.ts:88`, `diff:packages/features/ee/teams/services/teamService.ts:99`

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
