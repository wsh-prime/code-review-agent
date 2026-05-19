# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 22
- Changed entities: 22
- Risk signals: 9
- Findings: 4
- Needs human review: 5
- Discarded: 10
- Agent runs: 11
- Loop enabled: True
- Target repo modified: False

## Loop Summary

| Metric | Value |
|---|---:|
| Iterations | 1 / 1 |
| Converged | False |
| Fallback | False |
| Retry count | 3 |
| Total latency | 379818 ms |
| Token in | 42037 |
| Token out | 5359 |

- Iteration 0: 18 candidates, 8 verified, 4 uncertain, 4 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `file_risk_shards_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 32659 |
| Selected evidence | 36 |
| Omitted evidence | 77 |
| Context truncated | True |
| Review shards | 6 |
| Context requests | 6 |
| Refills | 4 |

## Findings

- `best_practice` medium at `apps/signup-form/src/components/frame.tsx:1` (0.99)
  - React Button Elements Must Have Explicit Type Attribute: The patch does not introduce any <button> elements, so no violation of this rule.
  - Suggestion: No action required.
  - Evidence: `diff_hunk:apps/signup-form/src/components/frame.tsx:1`

- `correctness` medium at `apps/signup-form/src/components/pages/form-page.tsx:30` (0.85)
  - Removing `setLoading(false)` in the minimal branch leaves the loading state stuck as `true` when the form submission succeeds in minimal mode, causing the UI to remain in a loading state indefinitely.
  - Suggestion: Restore `setLoading(false)` in the minimal branch, or ensure loading state is reset elsewhere after success.
  - Evidence: `diff_hunk:apps/signup-form/src/components/pages/form-page.tsx:27`

- `best_practice` low at `apps/signup-form/src/components/pages/form-view.tsx:56` (0.90)
  - Review guideline violation: 'React Button Elements Must Have Explicit Type Attribute'. The `<button>` element in this file does not have an explicit `type` attribute, which defaults to `submit` and can cause unintended form submissions.
  - Suggestion: Add `type="button"` to buttons that are not meant to submit the form, or `type="submit"` for the submit button.
  - Evidence: `diff_hunk:apps/signup-form/src/components/pages/form-view.tsx:53`

- `best_practice` medium at `apps/signup-form/src/components/pages/success-page.tsx:2` (0.95)
  - File renamed to kebab-case but import path uses kebab-case, which is correct; however, the file is in apps/signup-form/ which is not an admin app (apps/admin-x-*), so the kebab-case naming guideline does not apply. No issue.
  - Suggestion: 
  - Evidence: `diff_hunk:apps/signup-form/src/components/pages/success-page.tsx:1`

## Needs Human Review

- `dependency_change` low at `apps/signup-form/package.json:3` (0.75)
  - Dependency declarations changed and should be reviewed with install/test impact in mind.
  - Suggestion: Confirm lock files, compatibility, and test coverage for the dependency change.
  - Evidence: `diff:apps/signup-form/package.json:3`, `risk:dependency_change:apps/signup-form/package.json`

- `correctness` medium at `apps/signup-form/src/components/pages/form-view.tsx:56` (0.50)
  - React List Rendering Must Not Use Array Index as Key: The patch does not introduce a list rendering issue, but the review guideline prohibits array index keys. No evidence of list rendering in this hunk.
  - Suggestion: Ensure any list rendering in this file uses stable unique identifiers (e.g., item.id) instead of array indices.
  - Evidence: `diff_hunk:apps/signup-form/src/components/pages/form-view.tsx:53`

- `correctness` medium at `apps/signup-form/src/components/pages/success-page.tsx:3` (0.50)
  - Import path changed from './SuccessView' to './success-view' but the file was renamed from SuccessView.tsx to success-view.tsx. The import path must match the actual file name exactly.
  - Suggestion: Verify that the import path './success-view' matches the renamed file 'success-view.tsx' in the same directory.
  - Evidence: `diff_hunk:apps/signup-form/src/components/pages/success-page.tsx:1`

- `code_style` minor at `apps/signup-form/src/utils/helpers.tsx:20` (0.50)
  - String literal uses double quotes instead of single quotes, violating the 'Code Must Use Single Quotes for Strings' guideline.
  - Suggestion: Replace double quotes with single quotes: const STORAGE_KEY = 'ghost-history';
  - Evidence: `diff_hunk:apps/signup-form/src/utils/helpers.tsx:17`

- `bug_risk` medium at `apps/signup-form/src/utils/helpers.tsx:45` (0.50)
  - Removing the null check on getDefaultUrlHistory() return value may cause downstream code to receive undefined when sessionStorage is empty or throws, potentially leading to runtime errors.
  - Suggestion: Restore the null check or ensure callers handle undefined history values.
  - Evidence: `diff_hunk:apps/signup-form/src/utils/helpers.tsx:42`

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
