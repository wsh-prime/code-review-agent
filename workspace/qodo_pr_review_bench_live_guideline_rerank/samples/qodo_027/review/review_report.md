# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 21
- Changed entities: 21
- Risk signals: 0
- Findings: 0
- Needs human review: 20
- Discarded: 1
- Agent runs: 9
- Loop enabled: True
- Target repo modified: False

## Loop Summary

| Metric | Value |
|---|---:|
| Iterations | 1 / 1 |
| Converged | False |
| Fallback | False |
| Retry count | 0 |
| Total latency | 225918 ms |
| Token in | 39047 |
| Token out | 4361 |

- Iteration 0: 23 candidates, 22 verified, 22 uncertain, 0 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `file_risk_shards_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 31912 |
| Selected evidence | 32 |
| Omitted evidence | 340 |
| Context truncated | True |
| Review shards | 6 |
| Context requests | 5 |
| Refills | 2 |

## Findings

No findings.

Checked changed files, changed entities, deterministic risk signals, and evidence references. No high-confidence review finding was produced.

## Needs Human Review

- `best_practice` medium at `companion/app/(tabs)/(availability)/availability-detail.tsx:91` (0.50)
  - Default export used in non-Next.js page/layout file, violating the 'Default Exports Allowed Only in Next.js Page and Layout Files' rule.
  - Suggestion: Replace 'export default function AvailabilityDetail()' with a named export (e.g., 'export function AvailabilityDetail()') and update all imports accordingly.
  - Evidence: `diff_hunk:companion/app/(tabs)/(availability)/availability-detail.tsx:88`

- `best_practice` medium at `companion/app/(tabs)/(bookings)/index.ios.tsx:65` (0.50)
  - Default export used in non-Next.js page/layout file, violating the 'Default Exports Allowed Only in Next.js Page and Layout Files' rule.
  - Suggestion: Replace 'export default function Bookings()' with a named export (e.g., 'export function Bookings()') and update all imports accordingly.
  - Evidence: `diff_hunk:companion/app/(tabs)/(bookings)/index.ios.tsx:62`

- `best_practice` medium at `companion/app/(tabs)/(bookings)/index.tsx:65` (0.50)
  - Default export used in non-Next.js page/layout file, violating the 'Default Exports Allowed Only in Next.js Page and Layout Files' rule.
  - Suggestion: Replace 'export default function Bookings()' with a named export (e.g., 'export function Bookings()') and update all imports accordingly.
  - Evidence: `diff_hunk:companion/app/(tabs)/(bookings)/index.tsx:62`

- `best_practice` medium at `companion/app/(tabs)/(event-types)/event-type-detail.tsx:180` (0.50)
  - Default export used in non-Next.js page/layout file, violating the 'Default Exports Allowed Only in Next.js Page and Layout Files' rule.
  - Suggestion: Replace 'export default function EventTypeDetail()' with a named export (e.g., 'export function EventTypeDetail()') and update all imports accordingly.
  - Evidence: `diff_hunk:companion/app/(tabs)/(event-types)/event-type-detail.tsx:177`

- `correctness` warning at `companion/app/(tabs)/(event-types)/index.ios.tsx:1` (0.50)
  - Removed import of ContextMenu and HStack from @expo/ui/swift-ui without verifying they are unused elsewhere in the file. If these components are still referenced, the removal will cause a runtime error.
  - Suggestion: Ensure that ContextMenu and HStack are not used anywhere in the file before removing their imports. If they are used, restore the imports.
  - Evidence: `diff_hunk:companion/app/(tabs)/(event-types)/index.ios.tsx:1`

- `correctness` warning at `companion/app/(tabs)/(event-types)/index.tsx:37` (0.50)
  - Removed import of CalComAPIService from @/services/calcom. If this service is still used elsewhere in the file (e.g., for API calls), the removal will cause a runtime error.
  - Suggestion: Verify that CalComAPIService is not used anywhere in the file. If it is used, restore the import.
  - Evidence: `diff_hunk:companion/app/(tabs)/(event-types)/index.tsx:37`

- `visual` info at `companion/app/profile-sheet.ios.tsx:150` (0.50)
  - Removed border-b and border-gray-200 classes from the profile header View. This may change the visual appearance by removing the bottom border separator.
  - Suggestion: Confirm that the removal of the bottom border is intentional and does not negatively affect the UI layout or visual hierarchy.
  - Evidence: `diff_hunk:companion/app/profile-sheet.ios.tsx:147`

- `visual` info at `companion/app/profile-sheet.tsx:127` (0.50)
  - Removed border-b and border-gray-200 classes from the profile header View. This may change the visual appearance by removing the bottom border separator.
  - Suggestion: Confirm that the removal of the bottom border is intentional and does not negatively affect the UI layout or visual hierarchy.
  - Evidence: `diff_hunk:companion/app/profile-sheet.tsx:124`

- `best-practice` minor at `companion/app/(tabs)/(event-types)/index.ios.tsx:1` (0.50)
  - File uses a default export (export default function EventTypesIOS) but does not match the Next.js page/layout exception pattern (apps/web/app/**/page.tsx, apps/web/app/**/layout.tsx). Review guidelines require named exports for non-page/layout files.
  - Suggestion: Convert to a named export: export function EventTypesIOS() { ... } and update imports accordingly.
  - Evidence: `diff_hunk:companion/app/(tabs)/(event-types)/index.ios.tsx:111`

- `best-practice` minor at `companion/app/(tabs)/(event-types)/index.tsx:40` (0.50)
  - File uses a default export (export default function EventTypes) but does not match the Next.js page/layout exception pattern (apps/web/app/**/page.tsx, apps/web/app/**/layout.tsx). Review guidelines require named exports for non-page/layout files.
  - Suggestion: Convert to a named export: export function EventTypes() { ... } and update imports accordingly.
  - Evidence: `diff_hunk:companion/app/(tabs)/(event-types)/index.tsx:133`

- `best_practice` minor at `companion/components/Header.tsx:106` (0.50)
  - Review guideline violation: 'React Components Must Use react-hook-form with Zod Schema Validation' - The Header component is a form-related component (contains filter dropdown and pressable elements) but does not use react-hook-form with Zod schema validation as required by the repository guidelines.
  - Suggestion: If this component handles form-like input (e.g., filter selection), wrap it with react-hook-form and a Zod schema. Otherwise, confirm it is not a form component and consider adding a comment to clarify.
  - Evidence: `diff_hunk:companion/components/Header.tsx:103`

- `best_practice` minor at `companion/components/event-type-detail/tabs/AdvancedTab.tsx:141` (0.50)
  - Review guideline violation: 'React Components Must Use react-hook-form with Zod Schema Validation' - The AdvancedTab component is a form tab but does not use react-hook-form with Zod schema validation as required.
  - Suggestion: Integrate react-hook-form with zodResolver and define Zod schemas for form fields in this tab.
  - Evidence: `diff_hunk:companion/components/event-type-detail/tabs/AdvancedTab.tsx:138`

- `best_practice` minor at `companion/components/event-type-detail/tabs/BasicsTab.tsx:40` (0.50)
  - Review guideline violation: 'React Components Must Use react-hook-form with Zod Schema Validation' - The BasicsTab component is a form tab but does not use react-hook-form with Zod schema validation as required.
  - Suggestion: Integrate react-hook-form with zodResolver and define Zod schemas for form fields in this tab.
  - Evidence: `diff_hunk:companion/components/event-type-detail/tabs/BasicsTab.tsx:37`

- `best_practice` minor at `companion/components/event-type-detail/tabs/LimitsTab.tsx:127` (0.50)
  - Review guideline violation: 'React Components Must Use react-hook-form with Zod Schema Validation' - The LimitsTab component is a form tab but does not use react-hook-form with Zod schema validation as required.
  - Suggestion: Integrate react-hook-form with zodResolver and define Zod schemas for form fields in this tab.
  - Evidence: `diff_hunk:companion/components/event-type-detail/tabs/LimitsTab.tsx:124`

- `correctness` medium at `companion/components/event-type-list-item/EventTypeListItemParts.tsx:7` (0.50)
  - getDisplayUrl function may produce an incorrect URL path when username is undefined but slug is defined, returning '/undefined/slug' instead of '/slug'.
  - Suggestion: Change the fallback to `return slug ? `/${slug}` : '';` to avoid 'undefined' in the URL path.
  - Evidence: `diff_hunk:companion/components/event-type-list-item/EventTypeListItemParts.tsx:4`

- `functionality` medium at `companion/services/calcom.ts:318` (0.50)
  - Removal of `getUsername()` and `buildEventTypeLink()` functions may break callers that depend on building shareable event type links.
  - Suggestion: Verify that all callers of `getUsername()` and `buildEventTypeLink()` have been updated to use the new `bookingUrl` field or an alternative mechanism before removing these functions.
  - Evidence: `diff_hunk:companion/services/calcom.ts:318`

- `maintainability` low at `companion/extension/lib/linkedin.ts:118` (0.50)
  - New optional field `bookingUrl` is added to the EventType interface but no corresponding usage or population logic is visible in the provided evidence.
  - Suggestion: Ensure that `bookingUrl` is populated and consumed correctly in the LinkedIn integration logic.
  - Evidence: `diff_hunk:companion/extension/lib/linkedin.ts:115`

- `correctness` medium at `companion/services/calcom.ts:1651` (0.50)
  - The new `getUsername` helper catches errors from `getUserProfile` and throws a generic 'Failed to get username' error, discarding the original error context. This makes debugging harder and violates the guideline requiring custom error classes with typed codes and structured context.
  - Suggestion: Either let the error propagate naturally or use a custom error class (e.g., extending ErrorWithCode) that preserves the original error cause and includes a typed error code.
  - Evidence: `diff_hunk:companion/services/calcom.ts:1651`

- `maintainability` low at `companion/services/calcom.ts:1671` (0.50)
  - The export `buildEventTypeLink` is removed from `CalComAPIService` but no evidence shows it is still used elsewhere or that a replacement is provided. This could break callers that depend on this export.
  - Suggestion: Verify that all consumers of `buildEventTypeLink` have been updated to use an alternative, or keep the export if it is still needed.
  - Evidence: `diff_hunk:companion/services/calcom.ts:1671`

- `maintainability` medium at `companion/services/types/event-types.types.ts:282` (0.50)
  - The new `bookingUrl` property is added to the `EventType` interface without a corresponding Zod schema export in a separate `.schema.ts` file, violating the guideline that schema definitions must be in separate `.schema.ts` files with both TypeScript types and Zod schemas.
  - Suggestion: Move the `bookingUrl` property definition to a dedicated `.schema.ts` file (e.g., `event-types.schema.ts`) and export both the TypeScript type and a corresponding Zod schema for validation.
  - Evidence: `diff_hunk:companion/services/types/event-types.types.ts:278`

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
