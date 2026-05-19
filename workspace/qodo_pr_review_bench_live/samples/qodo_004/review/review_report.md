# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 22
- Changed entities: 22
- Risk signals: 9
- Findings: 0
- Needs human review: 1
- Discarded: 2
- Agent runs: 10
- Loop enabled: True
- Target repo modified: False

## Loop Summary

| Metric | Value |
|---|---:|
| Iterations | 1 / 1 |
| Converged | True |
| Fallback | False |
| Retry count | 1 |
| Total latency | 114770 ms |
| Token in | 24287 |
| Token out | 1003 |

- Iteration 0: 2 candidates, 0 verified, 0 uncertain, 0 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `file_risk_shards_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 15519 |
| Selected evidence | 31 |
| Omitted evidence | 82 |
| Context truncated | True |
| Review shards | 6 |
| Context requests | 9 |
| Refills | 3 |

## Findings

No findings.

Checked changed files, changed entities, deterministic risk signals, and evidence references. No high-confidence review finding was produced.

## Needs Human Review

- `dependency_change` low at `apps/signup-form/package.json:3` (0.75)
  - Dependency declarations changed and should be reviewed with install/test impact in mind.
  - Suggestion: Confirm lock files, compatibility, and test coverage for the dependency change.
  - Evidence: `diff:apps/signup-form/package.json:3`, `risk:dependency_change:apps/signup-form/package.json`

## Changed Files

- `apps/signup-form/.eslintrc.cjs` (modified)
- `apps/signup-form/.storybook/preview.tsx` (modified)
- `apps/signup-form/README.md` (modified)
- `apps/signup-form/package.json` (modified)
- `apps/signup-form/src/app-context.ts` (renamed)
- `apps/signup-form/src/app.tsx` (renamed)
- `apps/signup-form/src/components/content-box.tsx` (renamed)
- `apps/signup-form/src/components/frame.tsx` (renamed)
- `apps/signup-form/src/components/iframe.tsx` (renamed)
- `apps/signup-form/src/components/pages/form-page.tsx` (renamed)
- `apps/signup-form/src/components/pages/form-view.stories.ts` (renamed)
- `apps/signup-form/src/components/pages/form-view.tsx` (renamed)
- `apps/signup-form/src/components/pages/success-page.tsx` (renamed)
- `apps/signup-form/src/components/pages/success-view.stories.ts` (renamed)
- `apps/signup-form/src/components/pages/success-view.tsx` (renamed)
- `apps/signup-form/src/index.tsx` (modified)
- `apps/signup-form/src/pages.tsx` (modified)
- `apps/signup-form/src/preview.stories.tsx` (renamed)
- `apps/signup-form/src/utils/helpers.tsx` (modified)
- `apps/signup-form/src/utils/options.tsx` (modified)
- `apps/signup-form/test/utils/is-test-env.js` (renamed)
- `ghost/core/core/shared/config/defaults.json` (modified)

## Changed Entities

- `apps/signup-form/.eslintrc.cjs:18-31` module `apps.signup-form..eslintrc`
- `apps/signup-form/.storybook/preview.tsx:6-6` module `apps.signup-form..storybook.preview`
- `apps/signup-form/README.md:38-38` module `apps.signup-form.README`
- `apps/signup-form/package.json:3-3` module `apps.signup-form.package`
- `apps/signup-form/src/app-context.ts:1-1` module `apps.signup-form.src.app-context`
- `apps/signup-form/src/app.tsx:4-6` module `apps.signup-form.src.app`
- `apps/signup-form/src/components/content-box.tsx:1-1` module `apps.signup-form.src.components.content-box`
- `apps/signup-form/src/components/frame.tsx:1-5` module `apps.signup-form.src.components.frame`
- `apps/signup-form/src/components/iframe.tsx:1-1` module `apps.signup-form.src.components.iframe`
- `apps/signup-form/src/components/pages/form-page.tsx:2-5` module `apps.signup-form.src.components.pages.form-page`
- `apps/signup-form/src/components/pages/form-view.stories.ts:3-3` module `apps.signup-form.src.components.pages.form-view.stories`
- `apps/signup-form/src/components/pages/form-view.tsx:3-3` module `apps.signup-form.src.components.pages.form-view`
- `apps/signup-form/src/components/pages/success-page.tsx:2-3` module `apps.signup-form.src.components.pages.success-page`
- `apps/signup-form/src/components/pages/success-view.stories.ts:3-3` module `apps.signup-form.src.components.pages.success-view.stories`
- `apps/signup-form/src/components/pages/success-view.tsx:3-3` module `apps.signup-form.src.components.pages.success-view`
- `apps/signup-form/src/index.tsx:1-1` module `apps.signup-form.src.index`
- `apps/signup-form/src/pages.tsx:2-3` module `apps.signup-form.src.pages`
- `apps/signup-form/src/preview.stories.tsx:4-5` module `apps.signup-form.src.preview.stories`
- `apps/signup-form/src/utils/helpers.tsx:1-1` module `apps.signup-form.src.utils.helpers`
- `apps/signup-form/src/utils/options.tsx:2-2` module `apps.signup-form.src.utils.options`
- `apps/signup-form/test/utils/is-test-env.js:1-1` module `apps.signup-form.test.utils.is-test-env`
- `ghost/core/core/shared/config/defaults.json:305-305` module `ghost.core.core.shared.config.defaults`

## Risk Signals

- `dependency_change` (0.84): Dependency declaration changed: apps/signup-form/package.json.
- `security_sensitive` (0.74): Security-sensitive keywords changed in apps/signup-form/.storybook/preview.tsx.
- `security_sensitive` (0.74): Security-sensitive keywords changed in apps/signup-form/src/components/frame.tsx.
- `security_sensitive` (0.74): Security-sensitive keywords changed in apps/signup-form/src/components/pages/form-page.tsx.
- `security_sensitive` (0.74): Security-sensitive keywords changed in apps/signup-form/src/components/pages/form-view.tsx.
- `security_sensitive` (0.74): Security-sensitive keywords changed in apps/signup-form/src/components/pages/success-page.tsx.
- `security_sensitive` (0.74): Security-sensitive keywords changed in apps/signup-form/src/components/pages/success-view.tsx.
- `security_sensitive` (0.74): Security-sensitive keywords changed in apps/signup-form/src/utils/helpers.tsx.
- `security_sensitive` (0.74): Security-sensitive keywords changed in apps/signup-form/src/utils/options.tsx.

## Evidence Index

- `diff:apps/signup-form/.eslintrc.cjs:18` [diff]: apps/signup-form/.eslintrc.cjs:18
- `diff:apps/signup-form/.eslintrc.cjs:23` [diff]: apps/signup-form/.eslintrc.cjs:23
- `diff:apps/signup-form/.eslintrc.cjs:24` [diff]: apps/signup-form/.eslintrc.cjs:24
- `diff:apps/signup-form/.eslintrc.cjs:25` [diff]: apps/signup-form/.eslintrc.cjs:25
- `diff:apps/signup-form/.eslintrc.cjs:26` [diff]: apps/signup-form/.eslintrc.cjs:26
- `diff:apps/signup-form/.eslintrc.cjs:28` [diff]: apps/signup-form/.eslintrc.cjs:28
- `diff:apps/signup-form/.eslintrc.cjs:31` [diff]: apps/signup-form/.eslintrc.cjs:31
- `diff:apps/signup-form/.storybook/preview.tsx:6` [diff]: apps/signup-form/.storybook/preview.tsx:6
- `diff:apps/signup-form/README.md:38` [diff]: apps/signup-form/README.md:38
- `diff:apps/signup-form/README.md:45` [diff]: apps/signup-form/README.md:45
- `diff:apps/signup-form/README.md:46` [diff]: apps/signup-form/README.md:46
- `diff:apps/signup-form/README.md:47` [diff]: apps/signup-form/README.md:47
- `diff:apps/signup-form/README.md:48` [diff]: apps/signup-form/README.md:48
- `diff:apps/signup-form/README.md:49` [diff]: apps/signup-form/README.md:49
- `diff:apps/signup-form/README.md:50` [diff]: apps/signup-form/README.md:50
- `diff:apps/signup-form/README.md:51` [diff]: apps/signup-form/README.md:51
- `diff:apps/signup-form/README.md:52` [diff]: apps/signup-form/README.md:52
- `diff:apps/signup-form/README.md:53` [diff]: apps/signup-form/README.md:53
- `diff:apps/signup-form/README.md:54` [diff]: apps/signup-form/README.md:54
- `diff:apps/signup-form/README.md:55` [diff]: apps/signup-form/README.md:55
- `diff:apps/signup-form/README.md:56` [diff]: apps/signup-form/README.md:56
- `diff:apps/signup-form/README.md:57` [diff]: apps/signup-form/README.md:57
- `diff:apps/signup-form/README.md:58` [diff]: apps/signup-form/README.md:58
- `diff:apps/signup-form/README.md:59` [diff]: apps/signup-form/README.md:59
- `diff:apps/signup-form/README.md:60` [diff]: apps/signup-form/README.md:60
- `diff:apps/signup-form/README.md:61` [diff]: apps/signup-form/README.md:61
- `diff:apps/signup-form/README.md:62` [diff]: apps/signup-form/README.md:62
- `diff:apps/signup-form/package.json:3` [diff]: apps/signup-form/package.json:3
- `diff:apps/signup-form/src/app-context.ts:1` [diff]: apps/signup-form/src/app-context.ts:1
- `diff:apps/signup-form/src/app.tsx:4` [diff]: apps/signup-form/src/app.tsx:4
- ... 83 more evidence items omitted.
