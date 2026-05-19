# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 5
- Changed entities: 5
- Risk signals: 1
- Findings: 2
- Needs human review: 0
- Discarded: 0
- Agent runs: 3
- Loop enabled: True
- Target repo modified: False

## Loop Summary

| Metric | Value |
|---|---:|
| Iterations | 1 / 1 |
| Converged | True |
| Fallback | False |
| Retry count | 0 |
| Total latency | 40669 ms |
| Token in | 11230 |
| Token out | 378 |

- Iteration 0: 2 candidates, 2 verified, 0 uncertain, 2 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `file_risk_shards_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 8828 |
| Selected evidence | 6 |
| Omitted evidence | 234 |
| Context truncated | True |
| Review shards | 2 |
| Context requests | 0 |
| Refills | 0 |

## Findings

- `security` high at `apps/posts/src/views/comments/components/comments-list.tsx:59` (0.95)
  - The new CommentContent component uses dangerouslySetInnerHTML to render comment HTML content without sanitization. This introduces a cross-site scripting (XSS) vulnerability if the comment HTML contains malicious scripts.
  - Suggestion: Sanitize the HTML content before passing it to dangerouslySetInnerHTML, e.g., using DOMPurify or a similar library. Alternatively, render the content using a safe React component that escapes HTML.
  - Evidence: `diff_hunk:apps/posts/src/views/comments/components/comments-list.tsx:59`

- `best_practice` medium at `apps/posts/src/views/comments/components/comments-list.tsx:59` (0.85)
  - The CommentContent component uses dangerouslySetInnerHTML with user-generated content (item.html). Even if the content is sanitized server-side, this pattern is fragile and should be avoided in favor of safer rendering approaches.
  - Suggestion: Consider using a React component that safely renders HTML (e.g., using a library like react-html-parser with sanitization) or ensure the server-side sanitization is robust and audited.
  - Evidence: `diff_hunk:apps/posts/src/views/comments/components/comments-list.tsx:59`

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
