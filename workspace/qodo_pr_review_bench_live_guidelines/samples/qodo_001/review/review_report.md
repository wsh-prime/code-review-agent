# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 3
- Changed entities: 3
- Risk signals: 1
- Findings: 0
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
| Retry count | 0 |
| Total latency | 523 ms |
| Token in | 6455 |
| Token out | 12 |

- Iteration 0: 0 candidates, 0 verified, 0 uncertain, 0 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `risk_first_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 5728 |
| Selected evidence | 3 |
| Omitted evidence | 92 |
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

- `apps/comments-ui/src/components/content/forms/form.tsx` (modified)
- `apps/comments-ui/src/components/content/forms/reply-form.tsx` (modified)
- `apps/comments-ui/test/e2e/actions.test.ts` (modified)

## Changed Entities

- `apps/comments-ui/src/components/content/forms/form.tsx:244-244` module `apps.comments-ui.src.components.content.forms.form`
- `apps/comments-ui/src/components/content/forms/reply-form.tsx:30-35` module `apps.comments-ui.src.components.content.forms.reply-form`
- `apps/comments-ui/test/e2e/actions.test.ts:614-681` module `apps.comments-ui.test.e2e.actions.test`

## Risk Signals

- `security_sensitive` (0.74): Security-sensitive keywords changed in apps/comments-ui/test/e2e/actions.test.ts.

## Evidence Index

- `diff:apps/comments-ui/src/components/content/forms/form.tsx:244` [diff]: apps/comments-ui/src/components/content/forms/form.tsx:244
- `diff:apps/comments-ui/src/components/content/forms/form.tsx:264` [diff]: apps/comments-ui/src/components/content/forms/form.tsx:264
- `diff:apps/comments-ui/src/components/content/forms/form.tsx:265` [diff]: apps/comments-ui/src/components/content/forms/form.tsx:265
- `diff:apps/comments-ui/src/components/content/forms/form.tsx:292` [diff]: apps/comments-ui/src/components/content/forms/form.tsx:292
- `diff:apps/comments-ui/src/components/content/forms/form.tsx:301` [diff]: apps/comments-ui/src/components/content/forms/form.tsx:301
- `diff:apps/comments-ui/src/components/content/forms/form.tsx:308` [diff]: apps/comments-ui/src/components/content/forms/form.tsx:308
- `diff:apps/comments-ui/src/components/content/forms/form.tsx:309` [diff]: apps/comments-ui/src/components/content/forms/form.tsx:309
- `diff:apps/comments-ui/src/components/content/forms/form.tsx:310` [diff]: apps/comments-ui/src/components/content/forms/form.tsx:310
- `diff:apps/comments-ui/src/components/content/forms/form.tsx:311` [diff]: apps/comments-ui/src/components/content/forms/form.tsx:311
- `diff:apps/comments-ui/src/components/content/forms/form.tsx:313` [diff]: apps/comments-ui/src/components/content/forms/form.tsx:313
- `diff:apps/comments-ui/src/components/content/forms/form.tsx:315` [diff]: apps/comments-ui/src/components/content/forms/form.tsx:315
- `diff:apps/comments-ui/src/components/content/forms/reply-form.tsx:30` [diff]: apps/comments-ui/src/components/content/forms/reply-form.tsx:30
- `diff:apps/comments-ui/src/components/content/forms/reply-form.tsx:35` [diff]: apps/comments-ui/src/components/content/forms/reply-form.tsx:35
- `diff:apps/comments-ui/src/components/content/forms/reply-form.tsx:47` [diff]: apps/comments-ui/src/components/content/forms/reply-form.tsx:47
- `diff:apps/comments-ui/src/components/content/forms/reply-form.tsx:48` [diff]: apps/comments-ui/src/components/content/forms/reply-form.tsx:48
- `diff:apps/comments-ui/test/e2e/actions.test.ts:614` [diff]: apps/comments-ui/test/e2e/actions.test.ts:614
- `diff:apps/comments-ui/test/e2e/actions.test.ts:615` [diff]: apps/comments-ui/test/e2e/actions.test.ts:615
- `diff:apps/comments-ui/test/e2e/actions.test.ts:616` [diff]: apps/comments-ui/test/e2e/actions.test.ts:616
- `diff:apps/comments-ui/test/e2e/actions.test.ts:617` [diff]: apps/comments-ui/test/e2e/actions.test.ts:617
- `diff:apps/comments-ui/test/e2e/actions.test.ts:618` [diff]: apps/comments-ui/test/e2e/actions.test.ts:618
- `diff:apps/comments-ui/test/e2e/actions.test.ts:619` [diff]: apps/comments-ui/test/e2e/actions.test.ts:619
- `diff:apps/comments-ui/test/e2e/actions.test.ts:620` [diff]: apps/comments-ui/test/e2e/actions.test.ts:620
- `diff:apps/comments-ui/test/e2e/actions.test.ts:621` [diff]: apps/comments-ui/test/e2e/actions.test.ts:621
- `diff:apps/comments-ui/test/e2e/actions.test.ts:622` [diff]: apps/comments-ui/test/e2e/actions.test.ts:622
- `diff:apps/comments-ui/test/e2e/actions.test.ts:623` [diff]: apps/comments-ui/test/e2e/actions.test.ts:623
- `diff:apps/comments-ui/test/e2e/actions.test.ts:624` [diff]: apps/comments-ui/test/e2e/actions.test.ts:624
- `diff:apps/comments-ui/test/e2e/actions.test.ts:625` [diff]: apps/comments-ui/test/e2e/actions.test.ts:625
- `diff:apps/comments-ui/test/e2e/actions.test.ts:626` [diff]: apps/comments-ui/test/e2e/actions.test.ts:626
- `diff:apps/comments-ui/test/e2e/actions.test.ts:627` [diff]: apps/comments-ui/test/e2e/actions.test.ts:627
- `diff:apps/comments-ui/test/e2e/actions.test.ts:628` [diff]: apps/comments-ui/test/e2e/actions.test.ts:628
- ... 65 more evidence items omitted.
