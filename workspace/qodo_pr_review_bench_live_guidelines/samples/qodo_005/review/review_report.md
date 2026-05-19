# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 4
- Changed entities: 4
- Risk signals: 4
- Findings: 2
- Needs human review: 0
- Discarded: 0
- Agent runs: 2
- Loop enabled: True
- Target repo modified: False

## Loop Summary

| Metric | Value |
|---|---:|
| Iterations | 1 / 1 |
| Converged | True |
| Fallback | False |
| Retry count | 1 |
| Total latency | 64386 ms |
| Token in | 9044 |
| Token out | 326 |

- Iteration 0: 2 candidates, 2 verified, 0 uncertain, 2 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `risk_first_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 8481 |
| Selected evidence | 9 |
| Omitted evidence | 68 |
| Context truncated | True |
| Review shards | 1 |
| Context requests | 0 |
| Refills | 0 |

## Findings

- `logic_error` high at `ghost/core/core/server/services/member-welcome-emails/jobs/index.js:15` (0.95)
  - Negated condition on hasScheduled.processOutbox was removed, causing the job to be scheduled only when already true, which prevents the job from ever being added.
  - Suggestion: Restore the negation: change `if (hasScheduled.processOutbox && ...)` back to `if (!hasScheduled.processOutbox && ...)`.
  - Evidence: `diff_hunk:ghost/core/core/server/services/member-welcome-emails/jobs/index.js:8`

- `code_style` medium at `ghost/core/core/server/services/members/members-api/repositories/MemberRepository.js:340` (1.00)
  - Variable declaration changed from `let` to `var` for `member`, violating the guideline 'Code Must Use let or const Instead of var'.
  - Suggestion: Use `let member;` instead of `var member;`.
  - Evidence: `diff_hunk:ghost/core/core/server/services/members/members-api/repositories/MemberRepository.js:337`

## Needs Human Review

None.

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
