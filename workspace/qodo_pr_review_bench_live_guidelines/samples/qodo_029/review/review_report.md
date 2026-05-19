# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 6
- Changed entities: 6
- Risk signals: 0
- Findings: 0
- Needs human review: 0
- Discarded: 3
- Agent runs: 4
- Loop enabled: True
- Target repo modified: False

## Loop Summary

| Metric | Value |
|---|---:|
| Iterations | 1 / 1 |
| Converged | True |
| Fallback | False |
| Retry count | 1 |
| Total latency | 80792 ms |
| Token in | 13493 |
| Token out | 983 |

- Iteration 0: 3 candidates, 0 verified, 0 uncertain, 0 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `file_risk_shards_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 12204 |
| Selected evidence | 14 |
| Omitted evidence | 116 |
| Context truncated | True |
| Review shards | 2 |
| Context requests | 1 |
| Refills | 1 |

## Findings

No findings.

Checked changed files, changed entities, deterministic risk signals, and evidence references. No high-confidence review finding was produced.

## Needs Human Review

None.

## Changed Files

- `packages/features/calendar-subscription/adapters/AdaptersFactory.ts` (modified)
- `packages/features/calendar-subscription/lib/CalendarSubscriptionService.ts` (modified)
- `packages/features/calendar-subscription/lib/__tests__/CalendarSubscriptionService.test.ts` (modified)
- `packages/features/selectedCalendar/repositories/SelectedCalendarRepository.interface.ts` (modified)
- `packages/features/selectedCalendar/repositories/SelectedCalendarRepository.test.ts` (modified)
- `packages/features/selectedCalendar/repositories/SelectedCalendarRepository.ts` (modified)

## Changed Entities

- `packages/features/calendar-subscription/adapters/AdaptersFactory.ts:7-25` module `packages.features.calendar-subscription.adapters.AdaptersFactory`
- `packages/features/calendar-subscription/lib/CalendarSubscriptionService.ts:395-395` module `packages.features.calendar-subscription.lib.CalendarSubscriptionService`
- `packages/features/calendar-subscription/lib/__tests__/CalendarSubscriptionService.test.ts:115-120` module `packages.features.calendar-subscription.lib.__tests__.CalendarSubscriptionService.test`
- `packages/features/selectedCalendar/repositories/SelectedCalendarRepository.interface.ts:24-35` module `packages.features.selectedCalendar.repositories.SelectedCalendarRepository.interface`
- `packages/features/selectedCalendar/repositories/SelectedCalendarRepository.test.ts:134-134` module `packages.features.selectedCalendar.repositories.SelectedCalendarRepository.test`
- `packages/features/selectedCalendar/repositories/SelectedCalendarRepository.ts:5-5` module `packages.features.selectedCalendar.repositories.SelectedCalendarRepository`

## Risk Signals

None.

## Evidence Index

- `diff:packages/features/calendar-subscription/adapters/AdaptersFactory.ts:10` [diff]: packages/features/calendar-subscription/adapters/AdaptersFactory.ts:10
- `diff:packages/features/calendar-subscription/adapters/AdaptersFactory.ts:11` [diff]: packages/features/calendar-subscription/adapters/AdaptersFactory.ts:11
- `diff:packages/features/calendar-subscription/adapters/AdaptersFactory.ts:12` [diff]: packages/features/calendar-subscription/adapters/AdaptersFactory.ts:12
- `diff:packages/features/calendar-subscription/adapters/AdaptersFactory.ts:13` [diff]: packages/features/calendar-subscription/adapters/AdaptersFactory.ts:13
- `diff:packages/features/calendar-subscription/adapters/AdaptersFactory.ts:14` [diff]: packages/features/calendar-subscription/adapters/AdaptersFactory.ts:14
- `diff:packages/features/calendar-subscription/adapters/AdaptersFactory.ts:15` [diff]: packages/features/calendar-subscription/adapters/AdaptersFactory.ts:15
- `diff:packages/features/calendar-subscription/adapters/AdaptersFactory.ts:16` [diff]: packages/features/calendar-subscription/adapters/AdaptersFactory.ts:16
- `diff:packages/features/calendar-subscription/adapters/AdaptersFactory.ts:17` [diff]: packages/features/calendar-subscription/adapters/AdaptersFactory.ts:17
- `diff:packages/features/calendar-subscription/adapters/AdaptersFactory.ts:18` [diff]: packages/features/calendar-subscription/adapters/AdaptersFactory.ts:18
- `diff:packages/features/calendar-subscription/adapters/AdaptersFactory.ts:19` [diff]: packages/features/calendar-subscription/adapters/AdaptersFactory.ts:19
- `diff:packages/features/calendar-subscription/adapters/AdaptersFactory.ts:20` [diff]: packages/features/calendar-subscription/adapters/AdaptersFactory.ts:20
- `diff:packages/features/calendar-subscription/adapters/AdaptersFactory.ts:21` [diff]: packages/features/calendar-subscription/adapters/AdaptersFactory.ts:21
- `diff:packages/features/calendar-subscription/adapters/AdaptersFactory.ts:25` [diff]: packages/features/calendar-subscription/adapters/AdaptersFactory.ts:25
- `diff:packages/features/calendar-subscription/adapters/AdaptersFactory.ts:60` [diff]: packages/features/calendar-subscription/adapters/AdaptersFactory.ts:60
- `diff:packages/features/calendar-subscription/adapters/AdaptersFactory.ts:61` [diff]: packages/features/calendar-subscription/adapters/AdaptersFactory.ts:61
- `diff:packages/features/calendar-subscription/adapters/AdaptersFactory.ts:62` [diff]: packages/features/calendar-subscription/adapters/AdaptersFactory.ts:62
- `diff:packages/features/calendar-subscription/adapters/AdaptersFactory.ts:63` [diff]: packages/features/calendar-subscription/adapters/AdaptersFactory.ts:63
- `diff:packages/features/calendar-subscription/adapters/AdaptersFactory.ts:64` [diff]: packages/features/calendar-subscription/adapters/AdaptersFactory.ts:64
- `diff:packages/features/calendar-subscription/adapters/AdaptersFactory.ts:65` [diff]: packages/features/calendar-subscription/adapters/AdaptersFactory.ts:65
- `diff:packages/features/calendar-subscription/adapters/AdaptersFactory.ts:66` [diff]: packages/features/calendar-subscription/adapters/AdaptersFactory.ts:66
- `diff:packages/features/calendar-subscription/adapters/AdaptersFactory.ts:67` [diff]: packages/features/calendar-subscription/adapters/AdaptersFactory.ts:67
- `diff:packages/features/calendar-subscription/adapters/AdaptersFactory.ts:68` [diff]: packages/features/calendar-subscription/adapters/AdaptersFactory.ts:68
- `diff:packages/features/calendar-subscription/adapters/AdaptersFactory.ts:69` [diff]: packages/features/calendar-subscription/adapters/AdaptersFactory.ts:69
- `diff:packages/features/calendar-subscription/adapters/AdaptersFactory.ts:7` [diff]: packages/features/calendar-subscription/adapters/AdaptersFactory.ts:7
- `diff:packages/features/calendar-subscription/adapters/AdaptersFactory.ts:70` [diff]: packages/features/calendar-subscription/adapters/AdaptersFactory.ts:70
- `diff:packages/features/calendar-subscription/adapters/AdaptersFactory.ts:71` [diff]: packages/features/calendar-subscription/adapters/AdaptersFactory.ts:71
- `diff:packages/features/calendar-subscription/adapters/AdaptersFactory.ts:8` [diff]: packages/features/calendar-subscription/adapters/AdaptersFactory.ts:8
- `diff:packages/features/calendar-subscription/adapters/AdaptersFactory.ts:9` [diff]: packages/features/calendar-subscription/adapters/AdaptersFactory.ts:9
- `diff:packages/features/calendar-subscription/lib/CalendarSubscriptionService.ts:395` [diff]: packages/features/calendar-subscription/lib/CalendarSubscriptionService.ts:395
- `diff:packages/features/calendar-subscription/lib/__tests__/CalendarSubscriptionService.test.ts:115` [diff]: packages/features/calendar-subscription/lib/__tests__/CalendarSubscriptionService.test.ts:115
- ... 100 more evidence items omitted.
