# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 4
- Changed entities: 4
- Risk signals: 4
- Findings: 0
- Needs human review: 4
- Discarded: 0
- Agent runs: 2
- Loop enabled: True
- Target repo modified: False

## Loop Summary

| Metric | Value |
|---|---:|
| Iterations | 1 / 1 |
| Converged | False |
| Fallback | False |
| Retry count | 0 |
| Total latency | 16455 ms |
| Token in | 8463 |
| Token out | 830 |

- Iteration 0: 4 candidates, 4 verified, 4 uncertain, 0 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `risk_first_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 7579 |
| Selected evidence | 9 |
| Omitted evidence | 68 |
| Context truncated | True |
| Review shards | 1 |
| Context requests | 0 |
| Refills | 0 |

## Findings

No findings.

Checked changed files, changed entities, deterministic risk signals, and evidence references. No high-confidence review finding was produced.

## Needs Human Review

- `logic_error` high at `ghost/core/core/server/services/member-welcome-emails/jobs/index.js:14` (0.50)
  - Negated condition in `if (!hasScheduled.processOutbox && ...)` was changed to `if (hasScheduled.processOutbox && ...)`, which inverts the scheduling guard. Previously the job was added only when `processOutbox` was false; now it is added only when `processOutbox` is true, meaning the job will never be scheduled on the first invocation and may be scheduled repeatedly after the first run.
  - Suggestion: Restore the original negation `!hasScheduled.processOutbox` or confirm the intended logic and update the flag reset accordingly.
  - Evidence: `diff_hunk:ghost/core/core/server/services/member-welcome-emails/jobs/index.js:8`

- `behavior_change` medium at `ghost/core/core/server/services/member-welcome-emails/jobs/index.js:11` (0.50)
  - The feature gate check was changed from `labs.isSet('welcomeEmails')` to `config.get('memberWelcomeEmailTestInbox')`. This replaces a boolean labs flag with a config value that is truthy when set. In production, if `memberWelcomeEmailTestInbox` is not configured, the entire welcome email job will be skipped, effectively disabling the feature for all members.
  - Suggestion: Ensure the config value is set appropriately for production or keep the labs flag as a fallback.
  - Evidence: `diff_hunk:ghost/core/core/server/services/member-welcome-emails/jobs/index.js:8`

- `behavior_change` medium at `ghost/core/core/server/services/members/members-api/repositories/MemberRepository.js:340` (0.50)
  - The condition for triggering welcome email outbox creation was changed from `this._labsService.isSet('welcomeEmails') && WELCOME_EMAIL_SOURCES.includes(source)` to `welcomeEmailConfig || WELCOME_EMAIL_SOURCES.includes(source)`. When `welcomeEmailConfig` is truthy, the source check is bypassed, causing outbox entries to be created for any member source (e.g., admin-created, API-created) instead of only the allowed sources.
  - Suggestion: Keep the source filter: `welcomeEmailConfig && WELCOME_EMAIL_SOURCES.includes(source)` or `(welcomeEmailConfig || this._labsService.isSet('welcomeEmails')) && WELCOME_EMAIL_SOURCES.includes(source)`.
  - Evidence: `diff_hunk:ghost/core/core/server/services/members/members-api/repositories/MemberRepository.js:337`

- `code_style` low at `ghost/core/core/server/services/members/members-api/repositories/MemberRepository.js:339` (0.50)
  - Variable declaration changed from `let member` to `var member`. While not a functional issue, it introduces a function-scoped variable in a module where `let` is used elsewhere, reducing consistency.
  - Suggestion: Keep `let member` for block scoping consistency.
  - Evidence: `diff_hunk:ghost/core/core/server/services/members/members-api/repositories/MemberRepository.js:337`

## Changed Files

- `ghost/core/core/server/services/member-welcome-emails/jobs/index.js` (modified)
- `ghost/core/core/server/services/members/members-api/repositories/MemberRepository.js` (modified)
- `ghost/core/test/integration/services/member-welcome-emails.test.js` (modified)
- `ghost/core/test/unit/server/services/members/members-api/repositories/MemberRepository.test.js` (modified)

## Changed Entities

- `ghost/core/core/server/services/member-welcome-emails/jobs/index.js:3-3` module `ghost.core.core.server.services.member-welcome-emails.jobs.index`
- `ghost/core/core/server/services/members/members-api/repositories/MemberRepository.js:11-11` module `ghost.core.core.server.services.members.members-api.repositories.MemberRepository`
- `ghost/core/test/integration/services/member-welcome-emails.test.js:6-7` module `ghost.core.test.integration.services.member-welcome-emails.test`
- `ghost/core/test/unit/server/services/members/members-api/repositories/MemberRepository.test.js:7-7` module `ghost.core.test.unit.server.services.members.members-api.repositories.MemberRepository.test`

## Risk Signals

- `security_sensitive` (0.74): Security-sensitive keywords changed in ghost/core/core/server/services/member-welcome-emails/jobs/index.js.
- `security_sensitive` (0.74): Security-sensitive keywords changed in ghost/core/core/server/services/members/members-api/repositories/MemberRepository.js.
- `security_sensitive` (0.74): Security-sensitive keywords changed in ghost/core/test/integration/services/member-welcome-emails.test.js.
- `security_sensitive` (0.74): Security-sensitive keywords changed in ghost/core/test/unit/server/services/members/members-api/repositories/MemberRepository.test.js.

## Evidence Index

- `diff:ghost/core/core/server/services/member-welcome-emails/jobs/index.js:11` [diff]: ghost/core/core/server/services/member-welcome-emails/jobs/index.js:11
- `diff:ghost/core/core/server/services/member-welcome-emails/jobs/index.js:15` [diff]: ghost/core/core/server/services/member-welcome-emails/jobs/index.js:15
- `diff:ghost/core/core/server/services/member-welcome-emails/jobs/index.js:3` [diff]: ghost/core/core/server/services/member-welcome-emails/jobs/index.js:3
- `diff:ghost/core/core/server/services/members/members-api/repositories/MemberRepository.js:11` [diff]: ghost/core/core/server/services/members/members-api/repositories/MemberRepository.js:11
- `diff:ghost/core/core/server/services/members/members-api/repositories/MemberRepository.js:339` [diff]: ghost/core/core/server/services/members/members-api/repositories/MemberRepository.js:339
- `diff:ghost/core/core/server/services/members/members-api/repositories/MemberRepository.js:340` [diff]: ghost/core/core/server/services/members/members-api/repositories/MemberRepository.js:340
- `diff:ghost/core/core/server/services/members/members-api/repositories/MemberRepository.js:341` [diff]: ghost/core/core/server/services/members/members-api/repositories/MemberRepository.js:341
- `diff:ghost/core/core/server/services/members/members-api/repositories/MemberRepository.js:342` [diff]: ghost/core/core/server/services/members/members-api/repositories/MemberRepository.js:342
- `diff:ghost/core/test/integration/services/member-welcome-emails.test.js:24` [diff]: ghost/core/test/integration/services/member-welcome-emails.test.js:24
- `diff:ghost/core/test/integration/services/member-welcome-emails.test.js:25` [diff]: ghost/core/test/integration/services/member-welcome-emails.test.js:25
- `diff:ghost/core/test/integration/services/member-welcome-emails.test.js:29` [diff]: ghost/core/test/integration/services/member-welcome-emails.test.js:29
- `diff:ghost/core/test/integration/services/member-welcome-emails.test.js:30` [diff]: ghost/core/test/integration/services/member-welcome-emails.test.js:30
- `diff:ghost/core/test/integration/services/member-welcome-emails.test.js:52` [diff]: ghost/core/test/integration/services/member-welcome-emails.test.js:52
- `diff:ghost/core/test/integration/services/member-welcome-emails.test.js:53` [diff]: ghost/core/test/integration/services/member-welcome-emails.test.js:53
- `diff:ghost/core/test/integration/services/member-welcome-emails.test.js:54` [diff]: ghost/core/test/integration/services/member-welcome-emails.test.js:54
- `diff:ghost/core/test/integration/services/member-welcome-emails.test.js:55` [diff]: ghost/core/test/integration/services/member-welcome-emails.test.js:55
- `diff:ghost/core/test/integration/services/member-welcome-emails.test.js:6` [diff]: ghost/core/test/integration/services/member-welcome-emails.test.js:6
- `diff:ghost/core/test/integration/services/member-welcome-emails.test.js:68` [diff]: ghost/core/test/integration/services/member-welcome-emails.test.js:68
- `diff:ghost/core/test/integration/services/member-welcome-emails.test.js:69` [diff]: ghost/core/test/integration/services/member-welcome-emails.test.js:69
- `diff:ghost/core/test/integration/services/member-welcome-emails.test.js:7` [diff]: ghost/core/test/integration/services/member-welcome-emails.test.js:7
- `diff:ghost/core/test/integration/services/member-welcome-emails.test.js:83` [diff]: ghost/core/test/integration/services/member-welcome-emails.test.js:83
- `diff:ghost/core/test/integration/services/member-welcome-emails.test.js:84` [diff]: ghost/core/test/integration/services/member-welcome-emails.test.js:84
- `diff:ghost/core/test/integration/services/member-welcome-emails.test.js:98` [diff]: ghost/core/test/integration/services/member-welcome-emails.test.js:98
- `diff:ghost/core/test/integration/services/member-welcome-emails.test.js:99` [diff]: ghost/core/test/integration/services/member-welcome-emails.test.js:99
- `diff:ghost/core/test/unit/server/services/members/members-api/repositories/MemberRepository.test.js:469` [diff]: ghost/core/test/unit/server/services/members/members-api/repositories/MemberRepository.test.js:469
- `diff:ghost/core/test/unit/server/services/members/members-api/repositories/MemberRepository.test.js:530` [diff]: ghost/core/test/unit/server/services/members/members-api/repositories/MemberRepository.test.js:530
- `diff:ghost/core/test/unit/server/services/members/members-api/repositories/MemberRepository.test.js:531` [diff]: ghost/core/test/unit/server/services/members/members-api/repositories/MemberRepository.test.js:531
- `diff:ghost/core/test/unit/server/services/members/members-api/repositories/MemberRepository.test.js:532` [diff]: ghost/core/test/unit/server/services/members/members-api/repositories/MemberRepository.test.js:532
- `diff:ghost/core/test/unit/server/services/members/members-api/repositories/MemberRepository.test.js:539` [diff]: ghost/core/test/unit/server/services/members/members-api/repositories/MemberRepository.test.js:539
- `diff:ghost/core/test/unit/server/services/members/members-api/repositories/MemberRepository.test.js:554` [diff]: ghost/core/test/unit/server/services/members/members-api/repositories/MemberRepository.test.js:554
- ... 47 more evidence items omitted.
