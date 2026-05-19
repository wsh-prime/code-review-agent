# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 22
- Changed entities: 22
- Risk signals: 9
- Findings: 3
- Needs human review: 6
- Discarded: 2
- Agent runs: 9
- Loop enabled: True
- Target repo modified: False

## Loop Summary

| Metric | Value |
|---|---:|
| Iterations | 1 / 1 |
| Converged | False |
| Fallback | False |
| Retry count | 4 |
| Total latency | 402820 ms |
| Token in | 40444 |
| Token out | 2226 |

- Iteration 0: 11 candidates, 9 verified, 5 uncertain, 4 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `file_risk_shards_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 35206 |
| Selected evidence | 30 |
| Omitted evidence | 83 |
| Context truncated | True |
| Review shards | 6 |
| Context requests | 3 |
| Refills | 2 |

## Findings

- `style` warning at `apps/signup-form/.eslintrc.cjs:24` (0.70)
  - New rule 'ghost/filenames/match-regex' enforces kebab-case filenames, but the import path change in apps/signup-form/.storybook/preview.tsx from '../src/AppContext' to '../src/app-context' suggests a file rename that may violate this rule if the actual file is not renamed.
  - Suggestion: Ensure the file 'apps/signup-form/src/AppContext' is renamed to 'apps/signup-form/src/app-context' to match the new import path and the kebab-case rule.
  - Evidence: `diff_hunk:apps/signup-form/.eslintrc.cjs:15`, `diff_hunk:apps/signup-form/.storybook/preview.tsx:3`

- `code_style` minor at `apps/signup-form/src/components/frame.tsx:1` (0.70)
  - Import path changed from './IFrame' to './iframe' but the file was not renamed in this patch, which may cause a broken import if the target file does not exist at the new path.
  - Suggestion: Ensure that the file './iframe' exists (or is renamed accordingly) to match the updated import path.
  - Evidence: `diff_hunk:apps/signup-form/src/components/frame.tsx:1`

- `code_style` minor at `apps/signup-form/src/app.tsx:4` (0.70)
  - Import paths changed to kebab-case (e.g., './app-context', './components/content-box', './components/frame') but the corresponding files were renamed without text hunks; ensure the renamed files export the same symbols.
  - Suggestion: Verify that the renamed files export 'AppContextProvider', 'AppContextType', 'ContentBox', and 'Frame' as expected.
  - Evidence: `diff_hunk:apps/signup-form/src/app.tsx:1`

## Needs Human Review

- `dependency_change` low at `apps/signup-form/package.json:3` (0.75)
  - Dependency declarations changed and should be reviewed with install/test impact in mind.
  - Suggestion: Confirm lock files, compatibility, and test coverage for the dependency change.
  - Evidence: `diff:apps/signup-form/package.json:3`, `risk:dependency_change:apps/signup-form/package.json`

- `correctness` medium at `apps/signup-form/src/components/pages/form-page.tsx:30` (0.50)
  - Removing `setLoading(false)` in the minimal branch leaves the loading state stuck as `true` when the form submission succeeds in minimal mode, preventing the UI from transitioning to the success state.
  - Suggestion: Restore `setLoading(false)` in the minimal branch to ensure the loading indicator is cleared when the success state is shown.
  - Evidence: `diff_hunk:apps/signup-form/src/components/pages/form-page.tsx:27`

- `best-practice` low at `apps/signup-form/src/components/pages/form-view.tsx:56` (0.50)
  - The `email` value is trimmed before submission, but the local `email` state is not updated with the trimmed value. This can cause a mismatch between the displayed email and the submitted email.
  - Suggestion: Trim the email value when setting the state (e.g., `setEmail(e.target.value.trim())`) or trim consistently before both display and submission.
  - Evidence: `diff_hunk:apps/signup-form/src/components/pages/form-view.tsx:53`

- `correctness` medium at `apps/signup-form/src/components/pages/success-page.tsx:3` (0.50)
  - Import path changed from './SuccessView' to './success-view' but the file was renamed from 'SuccessView.tsx' to 'success-view.tsx'. The new import path matches the renamed file, which is correct.
  - Suggestion: No action needed; the import correctly references the renamed file.
  - Evidence: `diff_hunk:apps/signup-form/src/components/pages/success-page.tsx:1`

- `best_practice` minor at `apps/signup-form/src/components/pages/success-page.tsx:2` (0.50)
  - Review guideline violation: 'Admin React Apps Must Use Kebab-Case File Naming' - The file was renamed from SuccessPage.tsx to success-page.tsx, which now uses kebab-case. However, the import statement on line 2 uses './success-view' which is kebab-case, but the original file was SuccessView.tsx. The rename to success-view.tsx is correct, but the import path must match the new kebab-case file name. The evidence shows the import was changed from './SuccessView' to './success-view', which is correct. No issue.
  - Suggestion: 
  - Evidence: `diff_hunk:apps/signup-form/src/components/pages/success-page.tsx:1`

- `style` minor at `apps/signup-form/src/utils/helpers.tsx:20` (0.50)
  - String literal uses double quotes instead of single quotes, violating the 'Code Must Use Single Quotes for Strings' guideline.
  - Suggestion: Replace double quotes with single quotes: const STORAGE_KEY = 'ghost-history';
  - Evidence: `diff_hunk:apps/signup-form/src/utils/helpers.tsx:17`

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
