# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 22
- Changed entities: 22
- Risk signals: 9
- Findings: 6
- Needs human review: 9
- Discarded: 0
- Review results: 15
- Agent runs: 10
- Loop enabled: True
- Target repo modified: False

## Loop Summary

| Metric | Value |
|---|---:|
| Iterations | 1 / 1 |
| Converged | False |
| Fallback | False |
| Retry count | 1 |
| Total latency | 221301 ms |
| Token in | 38867 |
| Token out | 3281 |

- Iteration 0: 15 candidates, 15 verified, 9 uncertain, 6 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `file_risk_shards_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 30307 |
| Selected evidence | 34 |
| Omitted evidence | 79 |
| Context truncated | True |
| Review shards | 6 |
| Context requests | 6 |
| Refills | 3 |

## Review Result Lifecycle

| Status | Count |
|---|---:|
| `finding` | 6 |
| `needs_human_review` | 9 |

## Findings

- `style` medium at `apps/signup-form/.eslintrc.cjs:23` (0.90)
  - Review guideline 'Code Must Use Single Quotes for Strings' requires single quotes for string literals. The added rule configuration uses double quotes for the string 'error'.
  - Suggestion: Change 'error' to 'error' using single quotes.
  - Evidence: `diff_hunk:apps/signup-form/.eslintrc.cjs:15`

- `best_practice` minor at `apps/signup-form/src/components/frame.tsx:1` (0.60)
  - React Button Elements Must Have Explicit Type Attribute: The patch renames the file but does not add explicit type attributes to any <button> elements. The file contains a Frame component that likely renders buttons; without explicit type, buttons default to 'submit' and can cause unintended form submissions.
  - Suggestion: Add type="button" to all <button> elements in the component to prevent unintended form submissions.
  - Evidence: `diff_hunk:apps/signup-form/src/components/frame.tsx:1`

- `correctness` medium at `apps/signup-form/src/components/pages/success-page.tsx:2` (0.80)
  - Import path changed from './SuccessView' to './success-view' but the file was renamed from SuccessView.tsx to success-view.tsx. The import now references a lowercase path while the actual file may still be named with uppercase letters, causing a potential module resolution failure on case-sensitive file systems.
  - Suggestion: Ensure the import path matches the exact file name casing. If the file is now 'success-view.tsx', the import './success-view' is correct; otherwise, update the import to match the actual file name.
  - Evidence: `diff_hunk:apps/signup-form/src/components/pages/success-page.tsx:1`

- `correctness` medium at `apps/signup-form/src/components/pages/success-view.stories.ts:3` (0.80)
  - Import path changed from './SuccessView' to './success-view' but the file was renamed from SuccessView.tsx to success-view.tsx. The import now references a lowercase path while the actual file may still be named with uppercase letters, causing a potential module resolution failure on case-sensitive file systems.
  - Suggestion: Ensure the import path matches the exact file name casing. If the file is now 'success-view.tsx', the import './success-view' is correct; otherwise, update the import to match the actual file name.
  - Evidence: `diff_hunk:apps/signup-form/src/components/pages/success-view.stories.ts:1`

- `correctness` medium at `apps/signup-form/src/components/pages/success-view.tsx:3` (0.80)
  - Import path changed from '../../AppContext' to '../../app-context' but the file was renamed from AppContext.tsx to app-context.tsx. The import now references a lowercase path while the actual file may still be named with uppercase letters, causing a potential module resolution failure on case-sensitive file systems.
  - Suggestion: Ensure the import path matches the exact file name casing. If the file is now 'app-context.tsx', the import '../../app-context' is correct; otherwise, update the import to match the actual file name.
  - Evidence: `diff_hunk:apps/signup-form/src/components/pages/success-view.tsx:1`

- `correctness` medium at `apps/signup-form/src/index.tsx:1` (0.80)
  - Import path changed from './App.tsx' to './app.tsx' but the file was renamed from App.tsx to app.tsx. The import now references a lowercase path while the actual file may still be named with uppercase letters, causing a potential module resolution failure on case-sensitive file systems.
  - Suggestion: Ensure the import path matches the exact file name casing. If the file is now 'app.tsx', the import './app.tsx' is correct; otherwise, update the import to match the actual file name.
  - Evidence: `diff_hunk:apps/signup-form/src/index.tsx:1`

## Needs Human Review

- `dependency_change` low at `apps/signup-form/package.json:3` (0.75)
  - Dependency declarations changed and should be reviewed with install/test impact in mind.
  - Suggestion: Confirm lock files, compatibility, and test coverage for the dependency change.
  - Evidence: `diff:apps/signup-form/package.json:3`, `risk:dependency_change:apps/signup-form/package.json`

- `maintainability` minor at `apps/signup-form/src/components/frame.tsx:1` (0.50)
  - Import path changed from './IFrame' to './iframe' but the renamed target file is not included in the patch, which may break the build if the file was not renamed.
  - Suggestion: Ensure that the file './iframe' exists and is correctly named; if the original file was not renamed, update the import to match the actual file name.
  - Evidence: `diff_hunk:apps/signup-form/src/components/frame.tsx:1`

- `maintainability` minor at `apps/signup-form/src/app.tsx:4` (0.50)
  - Import paths changed from './AppContext', './components/ContentBox', and './components/Frame' to kebab-case equivalents, but the corresponding file renames are not all confirmed in the patch (only app-context.ts is renamed; content-box.tsx and frame.tsx are listed as renamed but have no hunks).
  - Suggestion: Ensure that all renamed files are actually present in the repository and that no other imports reference the old paths.
  - Evidence: `diff_hunk:apps/signup-form/src/app.tsx:1`

- `correctness` medium at `apps/signup-form/src/components/pages/form-page.tsx:30` (0.50)
  - Removing `setLoading(false)` in the minimal branch leaves the loading state permanently true after a successful submission, preventing the form from returning to its idle state.
  - Suggestion: Restore `setLoading(false)` in the minimal branch to reset the loading state after success.
  - Evidence: `diff_hunk:apps/signup-form/src/components/pages/form-page.tsx:27`

- `best_practice` low at `apps/signup-form/src/components/pages/form-view.tsx:56` (0.50)
  - React Button Elements Must Have Explicit Type Attribute: The form's submit button lacks an explicit type attribute, which defaults to 'submit' and can cause unintended form submissions.
  - Suggestion: Add `type="submit"` to the button element to make its behavior explicit.
  - Evidence: `diff_hunk:apps/signup-form/src/components/pages/form-view.tsx:53`

- `correctness` medium at `apps/signup-form/src/components/pages/form-view.tsx:56` (0.50)
  - Calling .trim() on email may produce an empty string, which is then passed to onSubmit without validation. If the parent component expects a non-empty email, this could cause silent failures or unexpected behavior.
  - Suggestion: Add a guard to check that email.trim() is non-empty before calling onSubmit, or handle the empty case explicitly.
  - Evidence: `diff_hunk:apps/signup-form/src/components/pages/form-view.tsx:53`, `diff:apps/signup-form/src/components/pages/form-view.tsx:56`

- `best_practice` minor at `apps/signup-form/src/components/pages/success-page.tsx:2` (0.50)
  - Review guideline violation: 'Admin React Apps Must Use Kebab-Case File Naming' - The file path 'apps/signup-form/src/components/pages/success-page.tsx' does not match the required pattern ^[a-z0-9.-]+$ because it contains uppercase letters in the directory name 'signup-form' (the guideline targets apps/admin-x-* directories, but the rule is triggered for this path).
  - Suggestion: Rename the file and its directory to use only lowercase letters, numbers, hyphens, and dots (e.g., 'apps/signup-form/src/components/pages/success-page.tsx' is already kebab-case; the issue is the directory 'signup-form' contains a hyphen which is allowed, but the guideline expects the entire path to match the pattern; verify if the rule applies to this path).
  - Evidence: `diff_hunk:apps/signup-form/src/components/pages/success-page.tsx:1`

- `code_quality` medium at `apps/signup-form/src/utils/helpers.tsx:20` (0.50)
  - String literal changed from single quotes to double quotes, violating the 'Code Must Use Single Quotes for Strings' guideline.
  - Suggestion: Use single quotes for the string literal: const STORAGE_KEY = 'ghost-history';
  - Evidence: `diff_hunk:apps/signup-form/src/utils/helpers.tsx:17`

- `logical_error` medium at `apps/signup-form/src/utils/helpers.tsx:45` (0.50)
  - Removed null check for getDefaultUrlHistory() return value. If getDefaultUrlHistory() returns null or undefined, the function will now return null/undefined instead of falling through, potentially causing callers to receive an unexpected null value.
  - Suggestion: Restore the null check or ensure callers handle null/undefined return values.
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
