# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 23
- Changed entities: 23
- Risk signals: 9
- Findings: 2
- Needs human review: 5
- Discarded: 4
- Agent runs: 7
- Loop enabled: True
- Target repo modified: False

## Loop Summary

| Metric | Value |
|---|---:|
| Iterations | 1 / 1 |
| Converged | False |
| Fallback | False |
| Retry count | 3 |
| Total latency | 230677 ms |
| Token in | 39063 |
| Token out | 2137 |

- Iteration 0: 11 candidates, 7 verified, 5 uncertain, 2 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `file_risk_shards_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 33720 |
| Selected evidence | 26 |
| Omitted evidence | 680 |
| Context truncated | True |
| Review shards | 6 |
| Context requests | 0 |
| Refills | 0 |

## Findings

- `naming_convention` high at `packages/features/bookings/repositories/PrismaBookingAttendeeRepository.ts:1` (0.90)
  - Repository class name 'PrismaBookingAttendeeRepository' does not follow the required 'Prisma<Entity>Repository' pattern where Entity should be a single entity name (e.g., PrismaAttendeeRepository). The filename also uses a compound name 'PrismaBookingAttendeeRepository.ts' which deviates from the expected pattern.
  - Suggestion: Rename the file to 'PrismaAttendeeRepository.ts' and the class to 'PrismaAttendeeRepository' to match the naming convention.
  - Evidence: `diff_hunk:packages/features/bookings/repositories/PrismaBookingAttendeeRepository.ts:1`

- `circular_dependency` high at `packages/features/bookings/repositories/BookingRepository.ts:10` (0.85)
  - Import from '@calcom/lib/server/repository/dto/IBookingRepository' violates the rule that 'lib' package must not import from 'features' package. The import path indicates a dependency from the 'lib' package into the 'features' package, which is a restricted cross-package import.
  - Suggestion: Move the IBookingRepository interface to a shared package (e.g., @calcom/types) or restructure to avoid the lib->features dependency.
  - Evidence: `diff_hunk:packages/features/bookings/repositories/BookingRepository.ts:10`

## Needs Human Review

- `naming_convention` medium at `apps/api/v2/src/lib/repositories/prisma-booking-attendee.repository.ts:6` (0.50)
  - Repository class name 'PrismaBookingAttendeeRepository' does not follow the required naming pattern 'Prisma<Entity>Repository' because the entity name 'BookingAttendee' is not a single PascalCase entity name; the file is named 'prisma-booking-attendee.repository.ts' which uses kebab-case and a dot-suffix, violating the guideline that filenames must match class names exactly in PascalCase.
  - Suggestion: Rename the file to 'PrismaBookingAttendeeRepository.ts' and ensure the class name matches exactly.
  - Evidence: `diff_hunk:apps/api/v2/src/lib/repositories/prisma-booking-attendee.repository.ts:1`

- `naming_convention` medium at `apps/api/v2/src/lib/repositories/prisma-booking-reference.repository.ts:6` (0.50)
  - Repository class name 'PrismaBookingReferenceRepository' does not follow the required naming pattern 'Prisma<Entity>Repository' because the entity name 'BookingReference' is not a single PascalCase entity name; the file is named 'prisma-booking-reference.repository.ts' which uses kebab-case and a dot-suffix, violating the guideline that filenames must match class names exactly in PascalCase.
  - Suggestion: Rename the file to 'PrismaBookingReferenceRepository.ts' and ensure the class name matches exactly.
  - Evidence: `diff_hunk:apps/api/v2/src/lib/repositories/prisma-booking-reference.repository.ts:1`

- `naming_convention` medium at `apps/api/v2/src/lib/repositories/prisma-profile.repository.ts:6` (0.50)
  - Repository class name 'PrismaProfileRepository' does not follow the required naming pattern 'Prisma<Entity>Repository' because the entity name 'Profile' is a single PascalCase entity name, but the file is named 'prisma-profile.repository.ts' which uses kebab-case and a dot-suffix, violating the guideline that filenames must match class names exactly in PascalCase.
  - Suggestion: Rename the file to 'PrismaProfileRepository.ts' and ensure the class name matches exactly.
  - Evidence: `diff_hunk:apps/api/v2/src/lib/repositories/prisma-profile.repository.ts:1`

- `architecture` error at `packages/features/bookings/lib/handleCancelBooking.ts:18` (0.50)
  - Violation of 'Prevent Circular Dependencies Between Core Packages': packages/features/bookings/lib/handleCancelBooking.ts imports from @calcom/features/profile/repositories/ProfileRepository and @calcom/features/users/repositories/UserRepository, which are within the 'features' package. The 'lib' package must not import from 'features'.
  - Suggestion: Move ProfileRepository and UserRepository to a shared package that both lib and features can depend on, or inject these dependencies via the handler's parameters instead of importing them directly.
  - Evidence: `diff_hunk:packages/features/bookings/lib/handleCancelBooking.ts:18`

- `maintainability` warning at `packages/features/bookings/lib/handleCancelBooking.ts:136` (0.50)
  - The handler function now accepts an optional dependencies parameter but falls back to constructing repository instances directly inside the function body when dependencies are not provided. This creates a hidden dependency on concrete repository classes and bypasses the DI container, making the code harder to test and maintain.
  - Suggestion: Remove the fallback construction inside the handler and require callers to always provide dependencies, or use the DI container to resolve dependencies consistently.
  - Evidence: `diff_hunk:packages/features/bookings/lib/handleCancelBooking.ts:136`

## Changed Files

- `apps/api/v2/src/lib/modules/booking-cancel.module.ts` (modified)
- `apps/api/v2/src/lib/repositories/prisma-booking-attendee.repository.ts` (added)
- `apps/api/v2/src/lib/repositories/prisma-booking-reference.repository.ts` (added)
- `apps/api/v2/src/lib/repositories/prisma-profile.repository.ts` (added)
- `apps/api/v2/src/lib/services/booking-cancel.service.ts` (modified)
- `packages/features/bookingReference/repositories/BookingReferenceRepository.ts` (modified)
- `packages/features/bookings/di/BookingAttendeeRepository.module.ts` (added)
- `packages/features/bookings/di/BookingCancelService.module.ts` (modified)
- `packages/features/bookings/di/BookingReferenceRepository.module.ts` (added)
- `packages/features/bookings/di/tokens.ts` (modified)
- `packages/features/bookings/lib/dto/IBookingAttendeeRepository.ts` (added)
- `packages/features/bookings/lib/handleCancelBooking.ts` (modified)
- `packages/features/bookings/lib/handleCancelBooking/test/handleCancelBooking.test.ts` (modified)
- `packages/features/bookings/repositories/BookingRepository.ts` (modified)
- `packages/features/bookings/repositories/PrismaBookingAttendeeRepository.ts` (added)
- `packages/features/di/tokens.ts` (modified)
- `packages/features/profile/repositories/ProfileRepository.ts` (modified)
- `packages/features/users/di/Profile.module.ts` (added)
- `packages/features/users/repositories/UserRepository.ts` (modified)
- `packages/lib/server/repository/dto/IBookingReferenceRepository.ts` (added)
- `packages/lib/server/repository/dto/IBookingRepository.ts` (added)
- `packages/lib/server/repository/dto/IProfileRepository.ts` (added)
- `packages/platform/libraries/repositories.ts` (modified)

## Changed Entities

- `apps/api/v2/src/lib/modules/booking-cancel.module.ts:1-19` module `apps.api.v2.src.lib.modules.booking-cancel.module`
- `apps/api/v2/src/lib/repositories/prisma-booking-attendee.repository.ts:1-11` module `apps.api.v2.src.lib.repositories.prisma-booking-attendee.repository`
- `apps/api/v2/src/lib/repositories/prisma-booking-reference.repository.ts:1-11` module `apps.api.v2.src.lib.repositories.prisma-booking-reference.repository`
- `apps/api/v2/src/lib/repositories/prisma-profile.repository.ts:1-11` module `apps.api.v2.src.lib.repositories.prisma-profile.repository`
- `apps/api/v2/src/lib/services/booking-cancel.service.ts:1-24` module `apps.api.v2.src.lib.services.booking-cancel.service`
- `packages/features/bookingReference/repositories/BookingReferenceRepository.ts:2-6` module `packages.features.bookingReference.repositories.BookingReferenceRepository`
- `packages/features/bookings/di/BookingAttendeeRepository.module.ts:1-20` module `packages.features.bookings.di.BookingAttendeeRepository.module`
- `packages/features/bookings/di/BookingCancelService.module.ts:1-8` module `packages.features.bookings.di.BookingCancelService.module`
- `packages/features/bookings/di/BookingReferenceRepository.module.ts:1-22` module `packages.features.bookings.di.BookingReferenceRepository.module`
- `packages/features/bookings/di/tokens.ts:10-13` module `packages.features.bookings.di.tokens`
- `packages/features/bookings/lib/dto/IBookingAttendeeRepository.ts:1-3` module `packages.features.bookings.lib.dto.IBookingAttendeeRepository`
- `packages/features/bookings/lib/handleCancelBooking.ts:21-22` module `packages.features.bookings.lib.handleCancelBooking`
- `packages/features/bookings/lib/handleCancelBooking/test/handleCancelBooking.test.ts:1056-1516` module `packages.features.bookings.lib.handleCancelBooking.test.handleCancelBooking.test`
- `packages/features/bookings/repositories/BookingRepository.ts:13-32` module `packages.features.bookings.repositories.BookingRepository`
- `packages/features/bookings/repositories/PrismaBookingAttendeeRepository.ts:1-15` module `packages.features.bookings.repositories.PrismaBookingAttendeeRepository`
- `packages/features/di/tokens.ts:65-66` module `packages.features.di.tokens`
- `packages/features/profile/repositories/ProfileRepository.ts:10-18` module `packages.features.profile.repositories.ProfileRepository`
- `packages/features/users/di/Profile.module.ts:1-22` module `packages.features.users.di.Profile.module`
- `packages/features/users/repositories/UserRepository.ts:101-101` module `packages.features.users.repositories.UserRepository`
- `packages/lib/server/repository/dto/IBookingReferenceRepository.ts:1-16` module `packages.lib.server.repository.dto.IBookingReferenceRepository`
- `packages/lib/server/repository/dto/IBookingRepository.ts:1-55` module `packages.lib.server.repository.dto.IBookingRepository`
- `packages/lib/server/repository/dto/IProfileRepository.ts:1-13` module `packages.lib.server.repository.dto.IProfileRepository`
- `packages/platform/libraries/repositories.ts:14-16` module `packages.platform.libraries.repositories`

## Risk Signals

- `security_sensitive` (0.74): Security-sensitive keywords changed in packages/features/bookings/di/BookingAttendeeRepository.module.ts.
- `security_sensitive` (0.74): Security-sensitive keywords changed in packages/features/bookings/di/BookingCancelService.module.ts.
- `security_sensitive` (0.74): Security-sensitive keywords changed in packages/features/bookings/di/BookingReferenceRepository.module.ts.
- `security_sensitive` (0.74): Security-sensitive keywords changed in packages/features/bookings/lib/handleCancelBooking.ts.
- `security_sensitive` (0.74): Security-sensitive keywords changed in packages/features/bookings/lib/handleCancelBooking/test/handleCancelBooking.test.ts.
- `security_sensitive` (0.74): Security-sensitive keywords changed in packages/features/bookings/repositories/BookingRepository.ts.
- `security_sensitive` (0.74): Security-sensitive keywords changed in packages/features/bookings/repositories/PrismaBookingAttendeeRepository.ts.
- `security_sensitive` (0.74): Security-sensitive keywords changed in packages/features/users/di/Profile.module.ts.
- `security_sensitive` (0.74): Security-sensitive keywords changed in packages/lib/server/repository/dto/IBookingRepository.ts.

## Evidence Index

- `diff:apps/api/v2/src/lib/modules/booking-cancel.module.ts:1` [diff]: apps/api/v2/src/lib/modules/booking-cancel.module.ts:1
- `diff:apps/api/v2/src/lib/modules/booking-cancel.module.ts:12` [diff]: apps/api/v2/src/lib/modules/booking-cancel.module.ts:12
- `diff:apps/api/v2/src/lib/modules/booking-cancel.module.ts:13` [diff]: apps/api/v2/src/lib/modules/booking-cancel.module.ts:13
- `diff:apps/api/v2/src/lib/modules/booking-cancel.module.ts:14` [diff]: apps/api/v2/src/lib/modules/booking-cancel.module.ts:14
- `diff:apps/api/v2/src/lib/modules/booking-cancel.module.ts:15` [diff]: apps/api/v2/src/lib/modules/booking-cancel.module.ts:15
- `diff:apps/api/v2/src/lib/modules/booking-cancel.module.ts:16` [diff]: apps/api/v2/src/lib/modules/booking-cancel.module.ts:16
- `diff:apps/api/v2/src/lib/modules/booking-cancel.module.ts:17` [diff]: apps/api/v2/src/lib/modules/booking-cancel.module.ts:17
- `diff:apps/api/v2/src/lib/modules/booking-cancel.module.ts:18` [diff]: apps/api/v2/src/lib/modules/booking-cancel.module.ts:18
- `diff:apps/api/v2/src/lib/modules/booking-cancel.module.ts:19` [diff]: apps/api/v2/src/lib/modules/booking-cancel.module.ts:19
- `diff:apps/api/v2/src/lib/modules/booking-cancel.module.ts:2` [diff]: apps/api/v2/src/lib/modules/booking-cancel.module.ts:2
- `diff:apps/api/v2/src/lib/modules/booking-cancel.module.ts:3` [diff]: apps/api/v2/src/lib/modules/booking-cancel.module.ts:3
- `diff:apps/api/v2/src/lib/modules/booking-cancel.module.ts:4` [diff]: apps/api/v2/src/lib/modules/booking-cancel.module.ts:4
- `diff:apps/api/v2/src/lib/modules/booking-cancel.module.ts:5` [diff]: apps/api/v2/src/lib/modules/booking-cancel.module.ts:5
- `diff:apps/api/v2/src/lib/modules/booking-cancel.module.ts:7` [diff]: apps/api/v2/src/lib/modules/booking-cancel.module.ts:7
- `diff:apps/api/v2/src/lib/repositories/prisma-booking-attendee.repository.ts:1` [diff]: apps/api/v2/src/lib/repositories/prisma-booking-attendee.repository.ts:1
- `diff:apps/api/v2/src/lib/repositories/prisma-booking-attendee.repository.ts:10` [diff]: apps/api/v2/src/lib/repositories/prisma-booking-attendee.repository.ts:10
- `diff:apps/api/v2/src/lib/repositories/prisma-booking-attendee.repository.ts:11` [diff]: apps/api/v2/src/lib/repositories/prisma-booking-attendee.repository.ts:11
- `diff:apps/api/v2/src/lib/repositories/prisma-booking-attendee.repository.ts:2` [diff]: apps/api/v2/src/lib/repositories/prisma-booking-attendee.repository.ts:2
- `diff:apps/api/v2/src/lib/repositories/prisma-booking-attendee.repository.ts:3` [diff]: apps/api/v2/src/lib/repositories/prisma-booking-attendee.repository.ts:3
- `diff:apps/api/v2/src/lib/repositories/prisma-booking-attendee.repository.ts:4` [diff]: apps/api/v2/src/lib/repositories/prisma-booking-attendee.repository.ts:4
- `diff:apps/api/v2/src/lib/repositories/prisma-booking-attendee.repository.ts:5` [diff]: apps/api/v2/src/lib/repositories/prisma-booking-attendee.repository.ts:5
- `diff:apps/api/v2/src/lib/repositories/prisma-booking-attendee.repository.ts:6` [diff]: apps/api/v2/src/lib/repositories/prisma-booking-attendee.repository.ts:6
- `diff:apps/api/v2/src/lib/repositories/prisma-booking-attendee.repository.ts:7` [diff]: apps/api/v2/src/lib/repositories/prisma-booking-attendee.repository.ts:7
- `diff:apps/api/v2/src/lib/repositories/prisma-booking-attendee.repository.ts:8` [diff]: apps/api/v2/src/lib/repositories/prisma-booking-attendee.repository.ts:8
- `diff:apps/api/v2/src/lib/repositories/prisma-booking-attendee.repository.ts:9` [diff]: apps/api/v2/src/lib/repositories/prisma-booking-attendee.repository.ts:9
- `diff:apps/api/v2/src/lib/repositories/prisma-booking-reference.repository.ts:1` [diff]: apps/api/v2/src/lib/repositories/prisma-booking-reference.repository.ts:1
- `diff:apps/api/v2/src/lib/repositories/prisma-booking-reference.repository.ts:10` [diff]: apps/api/v2/src/lib/repositories/prisma-booking-reference.repository.ts:10
- `diff:apps/api/v2/src/lib/repositories/prisma-booking-reference.repository.ts:11` [diff]: apps/api/v2/src/lib/repositories/prisma-booking-reference.repository.ts:11
- `diff:apps/api/v2/src/lib/repositories/prisma-booking-reference.repository.ts:2` [diff]: apps/api/v2/src/lib/repositories/prisma-booking-reference.repository.ts:2
- `diff:apps/api/v2/src/lib/repositories/prisma-booking-reference.repository.ts:3` [diff]: apps/api/v2/src/lib/repositories/prisma-booking-reference.repository.ts:3
- ... 1051 more evidence items omitted.
