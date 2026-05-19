# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 5
- Changed entities: 5
- Risk signals: 1
- Findings: 2
- Needs human review: 0
- Discarded: 1
- Review results: 3
- Agent runs: 4
- Loop enabled: True
- Target repo modified: False

## Loop Summary

| Metric | Value |
|---|---:|
| Iterations | 1 / 1 |
| Converged | True |
| Fallback | False |
| Retry count | 0 |
| Total latency | 87300 ms |
| Token in | 19898 |
| Token out | 857 |

- Iteration 0: 3 candidates, 2 verified, 0 uncertain, 2 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `file_risk_shards_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 16453 |
| Selected evidence | 30 |
| Omitted evidence | 218 |
| Context truncated | True |
| Review shards | 2 |
| Context requests | 2 |
| Refills | 1 |

## Review Result Lifecycle

| Status | Count |
|---|---:|
| `finding` | 2 |
| `discarded` | 1 |

## Findings

- `security` high at `apps/posts/src/views/comments/components/comments-list.tsx:59` (0.85)
  - The new CommentContent component uses dangerouslySetInnerHTML with user-provided comment HTML (item.html) without sanitization. This introduces a cross-site scripting (XSS) vulnerability if the HTML content is not already sanitized upstream.
  - Suggestion: Sanitize item.html using a library like DOMPurify before passing it to dangerouslySetInnerHTML, or use a safer rendering approach that escapes HTML.
  - Evidence: `diff_hunk:apps/posts/src/views/comments/components/comments-list.tsx:59`

- `best-practice` low at `apps/posts/src/views/comments/components/comments-list.tsx:185` (0.60)
  - The review guideline 'React Components Must Sort JSX Props in Standard Order' may be violated: JSX props in the new Button elements (e.g., className before variant, onClick before variant) do not follow the recommended order (reserved, regular alphabetically, callbacks, shorthand).
  - Suggestion: Reorder props to match the standard: key/ref first, then regular props alphabetically, then callbacks, then shorthand.
  - Evidence: `diff_hunk:apps/posts/src/views/comments/components/comments-list.tsx:185`

## Needs Human Review

None.

## Changed Files

- `apps/admin-x-framework/src/api/comments.ts` (modified)
- `apps/posts/src/views/comments/components/comments-list.tsx` (modified)
- `ghost/core/core/server/api/endpoints/utils/serializers/output/mappers/comments.js` (modified)
- `ghost/core/test/e2e-api/admin/__snapshots__/activity-feed.test.js.snap` (modified)
- `ghost/core/test/e2e-api/admin/__snapshots__/comments.test.js.snap` (modified)

## Changed Entities

- `apps/admin-x-framework/src/api/comments.ts:28-28` module `apps.admin-x-framework.src.api.comments`
- `apps/posts/src/views/comments/components/comments-list.tsx:10-14` module `apps.posts.src.views.comments.components.comments-list`
- `ghost/core/core/server/api/endpoints/utils/serializers/output/mappers/comments.js:38-39` module `ghost.core.core.server.api.endpoints.utils.serializers.output.mappers.comments`
- `ghost/core/test/e2e-api/admin/__snapshots__/activity-feed.test.js.snap:22702-22702` module `ghost.core.test.e2e-api.admin.__snapshots__.activity-feed.test.js`
- `ghost/core/test/e2e-api/admin/__snapshots__/comments.test.js.snap:28-28` module `ghost.core.test.e2e-api.admin.__snapshots__.comments.test.js`

## Risk Signals

- `security_sensitive` (0.74): Security-sensitive keywords changed in apps/posts/src/views/comments/components/comments-list.tsx.

## Evidence Index

- `diff:apps/admin-x-framework/src/api/comments.ts:28` [diff]: apps/admin-x-framework/src/api/comments.ts:28
- `diff:apps/posts/src/views/comments/components/comments-list.tsx:10` [diff]: apps/posts/src/views/comments/components/comments-list.tsx:10
- `diff:apps/posts/src/views/comments/components/comments-list.tsx:100` [diff]: apps/posts/src/views/comments/components/comments-list.tsx:100
- `diff:apps/posts/src/views/comments/components/comments-list.tsx:101` [diff]: apps/posts/src/views/comments/components/comments-list.tsx:101
- `diff:apps/posts/src/views/comments/components/comments-list.tsx:102` [diff]: apps/posts/src/views/comments/components/comments-list.tsx:102
- `diff:apps/posts/src/views/comments/components/comments-list.tsx:103` [diff]: apps/posts/src/views/comments/components/comments-list.tsx:103
- `diff:apps/posts/src/views/comments/components/comments-list.tsx:104` [diff]: apps/posts/src/views/comments/components/comments-list.tsx:104
- `diff:apps/posts/src/views/comments/components/comments-list.tsx:105` [diff]: apps/posts/src/views/comments/components/comments-list.tsx:105
- `diff:apps/posts/src/views/comments/components/comments-list.tsx:106` [diff]: apps/posts/src/views/comments/components/comments-list.tsx:106
- `diff:apps/posts/src/views/comments/components/comments-list.tsx:107` [diff]: apps/posts/src/views/comments/components/comments-list.tsx:107
- `diff:apps/posts/src/views/comments/components/comments-list.tsx:108` [diff]: apps/posts/src/views/comments/components/comments-list.tsx:108
- `diff:apps/posts/src/views/comments/components/comments-list.tsx:109` [diff]: apps/posts/src/views/comments/components/comments-list.tsx:109
- `diff:apps/posts/src/views/comments/components/comments-list.tsx:11` [diff]: apps/posts/src/views/comments/components/comments-list.tsx:11
- `diff:apps/posts/src/views/comments/components/comments-list.tsx:110` [diff]: apps/posts/src/views/comments/components/comments-list.tsx:110
- `diff:apps/posts/src/views/comments/components/comments-list.tsx:111` [diff]: apps/posts/src/views/comments/components/comments-list.tsx:111
- `diff:apps/posts/src/views/comments/components/comments-list.tsx:112` [diff]: apps/posts/src/views/comments/components/comments-list.tsx:112
- `diff:apps/posts/src/views/comments/components/comments-list.tsx:113` [diff]: apps/posts/src/views/comments/components/comments-list.tsx:113
- `diff:apps/posts/src/views/comments/components/comments-list.tsx:114` [diff]: apps/posts/src/views/comments/components/comments-list.tsx:114
- `diff:apps/posts/src/views/comments/components/comments-list.tsx:115` [diff]: apps/posts/src/views/comments/components/comments-list.tsx:115
- `diff:apps/posts/src/views/comments/components/comments-list.tsx:116` [diff]: apps/posts/src/views/comments/components/comments-list.tsx:116
- `diff:apps/posts/src/views/comments/components/comments-list.tsx:117` [diff]: apps/posts/src/views/comments/components/comments-list.tsx:117
- `diff:apps/posts/src/views/comments/components/comments-list.tsx:118` [diff]: apps/posts/src/views/comments/components/comments-list.tsx:118
- `diff:apps/posts/src/views/comments/components/comments-list.tsx:119` [diff]: apps/posts/src/views/comments/components/comments-list.tsx:119
- `diff:apps/posts/src/views/comments/components/comments-list.tsx:135` [diff]: apps/posts/src/views/comments/components/comments-list.tsx:135
- `diff:apps/posts/src/views/comments/components/comments-list.tsx:139` [diff]: apps/posts/src/views/comments/components/comments-list.tsx:139
- `diff:apps/posts/src/views/comments/components/comments-list.tsx:14` [diff]: apps/posts/src/views/comments/components/comments-list.tsx:14
- `diff:apps/posts/src/views/comments/components/comments-list.tsx:140` [diff]: apps/posts/src/views/comments/components/comments-list.tsx:140
- `diff:apps/posts/src/views/comments/components/comments-list.tsx:141` [diff]: apps/posts/src/views/comments/components/comments-list.tsx:141
- `diff:apps/posts/src/views/comments/components/comments-list.tsx:142` [diff]: apps/posts/src/views/comments/components/comments-list.tsx:142
- `diff:apps/posts/src/views/comments/components/comments-list.tsx:143` [diff]: apps/posts/src/views/comments/components/comments-list.tsx:143
- ... 306 more evidence items omitted.
