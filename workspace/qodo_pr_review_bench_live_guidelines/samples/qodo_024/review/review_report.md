# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 4
- Changed entities: 4
- Risk signals: 1
- Findings: 0
- Needs human review: 0
- Discarded: 1
- Agent runs: 2
- Loop enabled: True
- Target repo modified: False

## Loop Summary

| Metric | Value |
|---|---:|
| Iterations | 1 / 1 |
| Converged | True |
| Fallback | False |
| Retry count | 0 |
| Total latency | 12196 ms |
| Token in | 7021 |
| Token out | 164 |

- Iteration 0: 1 candidates, 0 verified, 0 uncertain, 0 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `risk_first_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 5982 |
| Selected evidence | 5 |
| Omitted evidence | 200 |
| Context truncated | True |
| Review shards | 1 |
| Context requests | 0 |
| Refills | 0 |

## Findings

No findings.

Checked changed files, changed entities, deterministic risk signals, and evidence references. No high-confidence review finding was produced.

## Needs Human Review

None.

## Changed Files

- `apps/web/app/(use-page-wrapper)/onboarding/getting-started/page.tsx` (modified)
- `packages/features/auth/lib/onboardingUtils.ts` (modified)
- `packages/features/membership/repositories/MembershipRepository.integration-test.ts` (added)
- `packages/features/membership/repositories/MembershipRepository.ts` (modified)

## Changed Entities

- `apps/web/app/(use-page-wrapper)/onboarding/getting-started/page.tsx:1-7` module `apps.web.app.(use-page-wrapper).onboarding.getting-started.page`
- `packages/features/auth/lib/onboardingUtils.ts:3-3` module `packages.features.auth.lib.onboardingUtils`
- `packages/features/membership/repositories/MembershipRepository.integration-test.ts:1-164` module `packages.features.membership.repositories.MembershipRepository.integration-test`
- `packages/features/membership/repositories/MembershipRepository.ts:6-7` module `packages.features.membership.repositories.MembershipRepository`

## Risk Signals

- `security_sensitive` (0.74): Security-sensitive keywords changed in apps/web/app/(use-page-wrapper)/onboarding/getting-started/page.tsx.

## Evidence Index

- `diff:apps/web/app/(use-page-wrapper)/onboarding/getting-started/page.tsx:1` [diff]: apps/web/app/(use-page-wrapper)/onboarding/getting-started/page.tsx:1
- `diff:apps/web/app/(use-page-wrapper)/onboarding/getting-started/page.tsx:2` [diff]: apps/web/app/(use-page-wrapper)/onboarding/getting-started/page.tsx:2
- `diff:apps/web/app/(use-page-wrapper)/onboarding/getting-started/page.tsx:28` [diff]: apps/web/app/(use-page-wrapper)/onboarding/getting-started/page.tsx:28
- `diff:apps/web/app/(use-page-wrapper)/onboarding/getting-started/page.tsx:29` [diff]: apps/web/app/(use-page-wrapper)/onboarding/getting-started/page.tsx:29
- `diff:apps/web/app/(use-page-wrapper)/onboarding/getting-started/page.tsx:3` [diff]: apps/web/app/(use-page-wrapper)/onboarding/getting-started/page.tsx:3
- `diff:apps/web/app/(use-page-wrapper)/onboarding/getting-started/page.tsx:30` [diff]: apps/web/app/(use-page-wrapper)/onboarding/getting-started/page.tsx:30
- `diff:apps/web/app/(use-page-wrapper)/onboarding/getting-started/page.tsx:31` [diff]: apps/web/app/(use-page-wrapper)/onboarding/getting-started/page.tsx:31
- `diff:apps/web/app/(use-page-wrapper)/onboarding/getting-started/page.tsx:32` [diff]: apps/web/app/(use-page-wrapper)/onboarding/getting-started/page.tsx:32
- `diff:apps/web/app/(use-page-wrapper)/onboarding/getting-started/page.tsx:33` [diff]: apps/web/app/(use-page-wrapper)/onboarding/getting-started/page.tsx:33
- `diff:apps/web/app/(use-page-wrapper)/onboarding/getting-started/page.tsx:34` [diff]: apps/web/app/(use-page-wrapper)/onboarding/getting-started/page.tsx:34
- `diff:apps/web/app/(use-page-wrapper)/onboarding/getting-started/page.tsx:35` [diff]: apps/web/app/(use-page-wrapper)/onboarding/getting-started/page.tsx:35
- `diff:apps/web/app/(use-page-wrapper)/onboarding/getting-started/page.tsx:4` [diff]: apps/web/app/(use-page-wrapper)/onboarding/getting-started/page.tsx:4
- `diff:apps/web/app/(use-page-wrapper)/onboarding/getting-started/page.tsx:5` [diff]: apps/web/app/(use-page-wrapper)/onboarding/getting-started/page.tsx:5
- `diff:apps/web/app/(use-page-wrapper)/onboarding/getting-started/page.tsx:6` [diff]: apps/web/app/(use-page-wrapper)/onboarding/getting-started/page.tsx:6
- `diff:apps/web/app/(use-page-wrapper)/onboarding/getting-started/page.tsx:7` [diff]: apps/web/app/(use-page-wrapper)/onboarding/getting-started/page.tsx:7
- `diff:packages/features/auth/lib/onboardingUtils.ts:3` [diff]: packages/features/auth/lib/onboardingUtils.ts:3
- `diff:packages/features/auth/lib/onboardingUtils.ts:54` [diff]: packages/features/auth/lib/onboardingUtils.ts:54
- `diff:packages/features/auth/lib/onboardingUtils.ts:55` [diff]: packages/features/auth/lib/onboardingUtils.ts:55
- `diff:packages/features/auth/lib/onboardingUtils.ts:56` [diff]: packages/features/auth/lib/onboardingUtils.ts:56
- `diff:packages/features/auth/lib/onboardingUtils.ts:67` [diff]: packages/features/auth/lib/onboardingUtils.ts:67
- `diff:packages/features/auth/lib/onboardingUtils.ts:68` [diff]: packages/features/auth/lib/onboardingUtils.ts:68
- `diff:packages/features/auth/lib/onboardingUtils.ts:69` [diff]: packages/features/auth/lib/onboardingUtils.ts:69
- `diff:packages/features/auth/lib/onboardingUtils.ts:70` [diff]: packages/features/auth/lib/onboardingUtils.ts:70
- `diff:packages/features/auth/lib/onboardingUtils.ts:71` [diff]: packages/features/auth/lib/onboardingUtils.ts:71
- `diff:packages/features/auth/lib/onboardingUtils.ts:72` [diff]: packages/features/auth/lib/onboardingUtils.ts:72
- `diff:packages/features/auth/lib/onboardingUtils.ts:73` [diff]: packages/features/auth/lib/onboardingUtils.ts:73
- `diff:packages/features/auth/lib/onboardingUtils.ts:74` [diff]: packages/features/auth/lib/onboardingUtils.ts:74
- `diff:packages/features/auth/lib/onboardingUtils.ts:75` [diff]: packages/features/auth/lib/onboardingUtils.ts:75
- `diff:packages/features/auth/lib/onboardingUtils.ts:77` [diff]: packages/features/auth/lib/onboardingUtils.ts:77
- `diff:packages/features/membership/repositories/MembershipRepository.integration-test.ts:1` [diff]: packages/features/membership/repositories/MembershipRepository.integration-test.ts:1
- ... 199 more evidence items omitted.
