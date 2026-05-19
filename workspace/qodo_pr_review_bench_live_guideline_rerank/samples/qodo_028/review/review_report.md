# Review Report

## Summary

- Mode: `hybrid-live/fallback-rules`
- Changed files: 6
- Changed entities: 6
- Risk signals: 4
- Findings: 0
- Needs human review: 4
- Discarded: 0
- Agent runs: 1
- Loop enabled: True
- Target repo modified: False

## Loop Summary

| Metric | Value |
|---|---:|
| Iterations | 0 / 1 |
| Converged | False |
| Fallback | True |
| Retry count | 0 |
| Total latency | 6939 ms |
| Token in | 0 |
| Token out | 0 |


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

No findings.

Checked changed files, changed entities, deterministic risk signals, and evidence references. No high-confidence review finding was produced.

## Needs Human Review

- `security_sensitive` medium at `apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:1` (0.74)
  - Live reviewer was unavailable; this deterministic risk needs human review.
  - Suggestion: Inspect the linked evidence and decide whether the change requires follow-up.
  - Evidence: `diff:apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:1`, `diff:apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:10`, `diff:apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:100`, `diff:apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:101`, `diff:apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:102`, `diff:apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:103`, `diff:apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:104`, `diff:apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:105`, `diff:apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:106`, `diff:apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.e2e-spec.ts:107`, ... 3 more

- `security_sensitive` medium at `apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.ts:1` (0.74)
  - Live reviewer was unavailable; this deterministic risk needs human review.
  - Suggestion: Inspect the linked evidence and decide whether the change requires follow-up.
  - Evidence: `diff:apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.ts:1`, `diff:apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.ts:10`, `diff:apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.ts:11`, `diff:apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.ts:12`, `diff:apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.ts:13`, `diff:apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.ts:14`, `diff:apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.ts:15`, `diff:apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.ts:16`, `diff:apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.ts:17`, `diff:apps/api/v2/src/modules/teams/invite/controllers/teams-invite.controller.ts:18`, ... 3 more

- `security_sensitive` medium at `apps/api/v2/src/modules/teams/invite/outputs/invite.output.ts:1` (0.74)
  - Live reviewer was unavailable; this deterministic risk needs human review.
  - Suggestion: Inspect the linked evidence and decide whether the change requires follow-up.
  - Evidence: `diff:apps/api/v2/src/modules/teams/invite/outputs/invite.output.ts:1`, `diff:apps/api/v2/src/modules/teams/invite/outputs/invite.output.ts:10`, `diff:apps/api/v2/src/modules/teams/invite/outputs/invite.output.ts:11`, `diff:apps/api/v2/src/modules/teams/invite/outputs/invite.output.ts:12`, `diff:apps/api/v2/src/modules/teams/invite/outputs/invite.output.ts:13`, `diff:apps/api/v2/src/modules/teams/invite/outputs/invite.output.ts:14`, `diff:apps/api/v2/src/modules/teams/invite/outputs/invite.output.ts:15`, `diff:apps/api/v2/src/modules/teams/invite/outputs/invite.output.ts:16`, `diff:apps/api/v2/src/modules/teams/invite/outputs/invite.output.ts:17`, `diff:apps/api/v2/src/modules/teams/invite/outputs/invite.output.ts:18`, ... 3 more

- `security_sensitive` medium at `packages/features/ee/teams/services/teamService.ts:106` (0.74)
  - Live reviewer was unavailable; this deterministic risk needs human review.
  - Suggestion: Inspect the linked evidence and decide whether the change requires follow-up.
  - Evidence: `diff:packages/features/ee/teams/services/teamService.ts:106`, `diff:packages/features/ee/teams/services/teamService.ts:567`, `diff:packages/features/ee/teams/services/teamService.ts:88`, `diff:packages/features/ee/teams/services/teamService.ts:99`, `risk:security_sensitive:packages/features/ee/teams/services/teamService.ts`

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
