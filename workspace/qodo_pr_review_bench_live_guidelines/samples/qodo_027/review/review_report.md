# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 21
- Changed entities: 21
- Risk signals: 0
- Findings: 0
- Needs human review: 7
- Discarded: 0
- Agent runs: 10
- Loop enabled: True
- Target repo modified: False

## Loop Summary

| Metric | Value |
|---|---:|
| Iterations | 1 / 1 |
| Converged | False |
| Fallback | False |
| Retry count | 5 |
| Total latency | 441498 ms |
| Token in | 39243 |
| Token out | 2461 |

- Iteration 0: 11 candidates, 11 verified, 11 uncertain, 0 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `file_risk_shards_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 32521 |
| Selected evidence | 31 |
| Omitted evidence | 341 |
| Context truncated | True |
| Review shards | 6 |
| Context requests | 8 |
| Refills | 3 |

## Findings

No findings.

Checked changed files, changed entities, deterministic risk signals, and evidence references. No high-confidence review finding was produced.

## Needs Human Review

- `maintainability` medium at `companion/app/(tabs)/(event-types)/index.ios.tsx:1` (0.50)
  - Removed import of ContextMenu and fixedSize without verifying they are unused elsewhere in the file. If these are still referenced, this change will cause a build error.
  - Suggestion: Ensure that ContextMenu and fixedSize are not used anywhere else in the file before removing their imports.
  - Evidence: `diff_hunk:companion/app/(tabs)/(event-types)/index.ios.tsx:1`

- `maintainability` medium at `companion/app/(tabs)/(event-types)/index.tsx:37` (0.50)
  - Removed import of CalComAPIService without verifying it is unused elsewhere in the file. If CalComAPIService is still referenced, this will cause a build error.
  - Suggestion: Ensure that CalComAPIService is not used anywhere else in the file before removing its import.
  - Evidence: `diff_hunk:companion/app/(tabs)/(event-types)/index.tsx:37`

- `visual` low at `companion/app/profile-sheet.ios.tsx:150` (0.50)
  - Removed border-b border-gray-200 from the profile header View. This may cause a visual regression by removing the separator line between the header and content.
  - Suggestion: If the border removal is intentional, ensure the visual design still provides adequate separation between sections.
  - Evidence: `diff_hunk:companion/app/profile-sheet.ios.tsx:147`

- `visual` low at `companion/app/profile-sheet.tsx:127` (0.50)
  - Removed border-b border-gray-200 from the profile header View. This may cause a visual regression by removing the separator line between the header and content.
  - Suggestion: If the border removal is intentional, ensure the visual design still provides adequate separation between sections.
  - Evidence: `diff_hunk:companion/app/profile-sheet.tsx:124`

- `correctness` high at `companion/app/(tabs)/(event-types)/index.ios.tsx:111` (0.50)
  - Removed async API call to buildEventTypeLink without verifying that eventType.bookingUrl is always populated upstream, which may cause silent failures or stale data.
  - Suggestion: Ensure that eventType.bookingUrl is reliably set before this change, or keep the fallback to buildEventTypeLink when bookingUrl is missing.
  - Evidence: `diff_hunk:companion/app/(tabs)/(event-types)/index.ios.tsx:111`

- `correctness` high at `companion/app/(tabs)/(event-types)/index.tsx:133` (0.50)
  - Removed async API call to buildEventTypeLink without verifying that eventType.bookingUrl is always populated upstream, which may cause silent failures or stale data.
  - Suggestion: Ensure that eventType.bookingUrl is reliably set before this change, or keep the fallback to buildEventTypeLink when bookingUrl is missing.
  - Evidence: `diff_hunk:companion/app/(tabs)/(event-types)/index.tsx:133`

- `functionality` medium at `companion/services/calcom.ts:318` (0.50)
  - Removal of buildEventTypeLink and getUsername functions may break callers that depend on building shareable event type links.
  - Suggestion: Ensure all callers of buildEventTypeLink and getUsername have been updated to use the new link-building approach before removing these functions.
  - Evidence: `diff_hunk:companion/services/calcom.ts:318`

## Changed Files

- `companion/app/(tabs)/(availability)/availability-detail.tsx` (modified)
- `companion/app/(tabs)/(bookings)/index.ios.tsx` (modified)
- `companion/app/(tabs)/(bookings)/index.tsx` (modified)
- `companion/app/(tabs)/(event-types)/event-type-detail.tsx` (modified)
- `companion/app/(tabs)/(event-types)/index.ios.tsx` (modified)
- `companion/app/(tabs)/(event-types)/index.tsx` (modified)
- `companion/app/profile-sheet.ios.tsx` (modified)
- `companion/app/profile-sheet.tsx` (modified)
- `companion/components/Header.tsx` (modified)
- `companion/components/event-type-detail/tabs/AdvancedTab.tsx` (modified)
- `companion/components/event-type-detail/tabs/BasicsTab.tsx` (modified)
- `companion/components/event-type-detail/tabs/LimitsTab.tsx` (modified)
- `companion/components/event-type-detail/tabs/RecurringTab.tsx` (modified)
- `companion/components/event-type-list-item/EventTypeListItem.ios.tsx` (modified)
- `companion/components/event-type-list-item/EventTypeListItem.tsx` (modified)
- `companion/components/event-type-list-item/EventTypeListItemParts.tsx` (modified)
- `companion/extension/entrypoints/background/index.ts` (modified)
- `companion/extension/entrypoints/content.ts` (modified)
- `companion/extension/lib/linkedin.ts` (modified)
- `companion/services/calcom.ts` (modified)
- `companion/services/types/event-types.types.ts` (modified)

## Changed Entities

- `companion/app/(tabs)/(availability)/availability-detail.tsx:91-91` module `companion.app.(tabs).(availability).availability-detail`
- `companion/app/(tabs)/(bookings)/index.ios.tsx:65-65` module `companion.app.(tabs).(bookings).index.ios`
- `companion/app/(tabs)/(bookings)/index.tsx:65-74` module `companion.app.(tabs).(bookings).index`
- `companion/app/(tabs)/(event-types)/event-type-detail.tsx:180-180` module `companion.app.(tabs).(event-types).event-type-detail`
- `companion/app/(tabs)/(event-types)/index.ios.tsx:1-3` module `companion.app.(tabs).(event-types).index.ios`
- `companion/app/(tabs)/(event-types)/index.tsx:40-40` module `companion.app.(tabs).(event-types).index`
- `companion/app/profile-sheet.ios.tsx:150-150` module `companion.app.profile-sheet.ios`
- `companion/app/profile-sheet.tsx:127-127` module `companion.app.profile-sheet`
- `companion/components/Header.tsx:106-113` module `companion.components.Header`
- `companion/components/event-type-detail/tabs/AdvancedTab.tsx:141-141` module `companion.components.event-type-detail.tabs.AdvancedTab`
- `companion/components/event-type-detail/tabs/BasicsTab.tsx:40-40` module `companion.components.event-type-detail.tabs.BasicsTab`
- `companion/components/event-type-detail/tabs/LimitsTab.tsx:127-127` module `companion.components.event-type-detail.tabs.LimitsTab`
- `companion/components/event-type-detail/tabs/RecurringTab.tsx:92-92` module `companion.components.event-type-detail.tabs.RecurringTab`
- `companion/components/event-type-list-item/EventTypeListItem.ios.tsx:103-103` module `companion.components.event-type-list-item.EventTypeListItem.ios`
- `companion/components/event-type-list-item/EventTypeListItem.tsx:54-54` module `companion.components.event-type-list-item.EventTypeListItem`
- `companion/components/event-type-list-item/EventTypeListItemParts.tsx:7-32` module `companion.components.event-type-list-item.EventTypeListItemParts`
- `companion/extension/entrypoints/background/index.ts:281-281` module `companion.extension.entrypoints.background.index`
- `companion/extension/entrypoints/content.ts:836-836` module `companion.extension.entrypoints.content`
- `companion/extension/lib/linkedin.ts:118-118` module `companion.extension.lib.linkedin`
- `companion/services/calcom.ts:321-332` module `companion.services.calcom`
- `companion/services/types/event-types.types.ts:281-283` module `companion.services.types.event-types.types`

## Risk Signals

None.

## Evidence Index

- `diff:companion/app/(tabs)/(availability)/availability-detail.tsx:91` [diff]: companion/app/(tabs)/(availability)/availability-detail.tsx:91
- `diff:companion/app/(tabs)/(bookings)/index.ios.tsx:126` [diff]: companion/app/(tabs)/(bookings)/index.ios.tsx:126
- `diff:companion/app/(tabs)/(bookings)/index.ios.tsx:65` [diff]: companion/app/(tabs)/(bookings)/index.ios.tsx:65
- `diff:companion/app/(tabs)/(bookings)/index.tsx:65` [diff]: companion/app/(tabs)/(bookings)/index.tsx:65
- `diff:companion/app/(tabs)/(bookings)/index.tsx:66` [diff]: companion/app/(tabs)/(bookings)/index.tsx:66
- `diff:companion/app/(tabs)/(bookings)/index.tsx:67` [diff]: companion/app/(tabs)/(bookings)/index.tsx:67
- `diff:companion/app/(tabs)/(bookings)/index.tsx:68` [diff]: companion/app/(tabs)/(bookings)/index.tsx:68
- `diff:companion/app/(tabs)/(bookings)/index.tsx:69` [diff]: companion/app/(tabs)/(bookings)/index.tsx:69
- `diff:companion/app/(tabs)/(bookings)/index.tsx:70` [diff]: companion/app/(tabs)/(bookings)/index.tsx:70
- `diff:companion/app/(tabs)/(bookings)/index.tsx:74` [diff]: companion/app/(tabs)/(bookings)/index.tsx:74
- `diff:companion/app/(tabs)/(event-types)/event-type-detail.tsx:1273` [diff]: companion/app/(tabs)/(event-types)/event-type-detail.tsx:1273
- `diff:companion/app/(tabs)/(event-types)/event-type-detail.tsx:1274` [diff]: companion/app/(tabs)/(event-types)/event-type-detail.tsx:1274
- `diff:companion/app/(tabs)/(event-types)/event-type-detail.tsx:1275` [diff]: companion/app/(tabs)/(event-types)/event-type-detail.tsx:1275
- `diff:companion/app/(tabs)/(event-types)/event-type-detail.tsx:1276` [diff]: companion/app/(tabs)/(event-types)/event-type-detail.tsx:1276
- `diff:companion/app/(tabs)/(event-types)/event-type-detail.tsx:1282` [diff]: companion/app/(tabs)/(event-types)/event-type-detail.tsx:1282
- `diff:companion/app/(tabs)/(event-types)/event-type-detail.tsx:1430` [diff]: companion/app/(tabs)/(event-types)/event-type-detail.tsx:1430
- `diff:companion/app/(tabs)/(event-types)/event-type-detail.tsx:180` [diff]: companion/app/(tabs)/(event-types)/event-type-detail.tsx:180
- `diff:companion/app/(tabs)/(event-types)/event-type-detail.tsx:2340` [diff]: companion/app/(tabs)/(event-types)/event-type-detail.tsx:2340
- `diff:companion/app/(tabs)/(event-types)/event-type-detail.tsx:2343` [diff]: companion/app/(tabs)/(event-types)/event-type-detail.tsx:2343
- `diff:companion/app/(tabs)/(event-types)/event-type-detail.tsx:2344` [diff]: companion/app/(tabs)/(event-types)/event-type-detail.tsx:2344
- `diff:companion/app/(tabs)/(event-types)/event-type-detail.tsx:2345` [diff]: companion/app/(tabs)/(event-types)/event-type-detail.tsx:2345
- `diff:companion/app/(tabs)/(event-types)/event-type-detail.tsx:2346` [diff]: companion/app/(tabs)/(event-types)/event-type-detail.tsx:2346
- `diff:companion/app/(tabs)/(event-types)/event-type-detail.tsx:2347` [diff]: companion/app/(tabs)/(event-types)/event-type-detail.tsx:2347
- `diff:companion/app/(tabs)/(event-types)/event-type-detail.tsx:2348` [diff]: companion/app/(tabs)/(event-types)/event-type-detail.tsx:2348
- `diff:companion/app/(tabs)/(event-types)/event-type-detail.tsx:2349` [diff]: companion/app/(tabs)/(event-types)/event-type-detail.tsx:2349
- `diff:companion/app/(tabs)/(event-types)/event-type-detail.tsx:2350` [diff]: companion/app/(tabs)/(event-types)/event-type-detail.tsx:2350
- `diff:companion/app/(tabs)/(event-types)/event-type-detail.tsx:2351` [diff]: companion/app/(tabs)/(event-types)/event-type-detail.tsx:2351
- `diff:companion/app/(tabs)/(event-types)/event-type-detail.tsx:2352` [diff]: companion/app/(tabs)/(event-types)/event-type-detail.tsx:2352
- `diff:companion/app/(tabs)/(event-types)/event-type-detail.tsx:2353` [diff]: companion/app/(tabs)/(event-types)/event-type-detail.tsx:2353
- `diff:companion/app/(tabs)/(event-types)/event-type-detail.tsx:948` [diff]: companion/app/(tabs)/(event-types)/event-type-detail.tsx:948
- ... 342 more evidence items omitted.
