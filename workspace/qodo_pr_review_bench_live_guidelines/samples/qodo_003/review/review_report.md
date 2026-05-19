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
| Total latency | 9697 ms |
| Token in | 12370 |
| Token out | 352 |

- Iteration 0: 2 candidates, 2 verified, 0 uncertain, 2 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `file_risk_shards_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 10646 |
| Selected evidence | 6 |
| Omitted evidence | 234 |
| Context truncated | True |
| Review shards | 2 |
| Context requests | 0 |
| Refills | 0 |

## Findings

- `security` high at `apps/posts/src/views/comments/components/comments-list.tsx:59` (0.95)
  - The new CommentContent component uses dangerouslySetInnerHTML to render comment HTML content without sanitization, introducing a stored XSS vulnerability. User-generated comment HTML is rendered directly into the DOM, allowing arbitrary script execution.
  - Suggestion: Sanitize the HTML content before passing it to dangerouslySetInnerHTML using a library like DOMPurify, or render the content as plain text if HTML is not required.
  - Evidence: `diff_hunk:apps/posts/src/views/comments/components/comments-list.tsx:59`

- `best_practice` medium at `apps/posts/src/views/comments/components/comments-list.tsx:59` (0.90)
  - The new <Button> element in ExpandButton lacks an explicit type attribute. Without type="button", the button defaults to type="submit" inside a form, which can cause unintended form submissions.
  - Suggestion: Add type="button" to the <Button> component to prevent accidental form submission behavior.
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
