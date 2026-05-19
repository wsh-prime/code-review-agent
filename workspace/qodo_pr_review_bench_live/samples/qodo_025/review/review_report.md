# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 23
- Changed entities: 23
- Risk signals: 9
- Findings: 3
- Needs human review: 2
- Discarded: 0
- Agent runs: 8
- Loop enabled: True
- Target repo modified: False

## Loop Summary

| Metric | Value |
|---|---:|
| Iterations | 1 / 1 |
| Converged | False |
| Fallback | False |
| Retry count | 0 |
| Total latency | 30814 ms |
| Token in | 30498 |
| Token out | 1648 |

- Iteration 0: 8 candidates, 8 verified, 5 uncertain, 3 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `file_risk_shards_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 23597 |
| Selected evidence | 27 |
| Omitted evidence | 679 |
| Context truncated | True |
| Review shards | 6 |
| Context requests | 2 |
| Refills | 1 |

## Findings

- `correctness` high at `packages/features/bookings/di/BookingCancelService.module.ts:17` (0.70)
  - The DI module for BookingCancelService now injects five repository dependencies (userRepository, bookingRepository, profileRepository, bookingReferenceRepository, attendeeRepository) but the constructor signature of BookingCancelService in the base class is not visible in the provided evidence. If the base class constructor expects a single prismaClient argument, this change will cause a runtime instantiation error due to mismatched dependency injection.
  - Suggestion: Verify that the base BookingCancelService class constructor accepts these five named dependencies. If it still expects a single prismaClient, update the base class or adjust the depsMap accordingly.
  - Evidence: `diff_hunk:packages/features/bookings/di/BookingCancelService.module.ts:17`, `diff_hunk:packages/features/bookings/di/BookingCancelService.module.ts:1`

- `correctness` high at `apps/api/v2/src/lib/services/booking-cancel.service.ts:1` (0.70)
  - The API v2 BookingCancelService now extends BaseBookingCancelService and passes five repository instances to super(), but the base class constructor signature is not shown. If the base class still expects a single prismaClient object, this change will cause a runtime error because the spread of named properties will not match the expected constructor parameter.
  - Suggestion: Confirm that the base BookingCancelService constructor accepts an object with these five repository keys. If not, update the base class or revert the change.
  - Evidence: `diff_hunk:apps/api/v2/src/lib/services/booking-cancel.service.ts:1`

- `security` high at `packages/features/bookings/lib/handleCancelBooking.ts:136` (0.70)
  - The handler function now accepts an optional `dependencies` parameter that allows callers to inject arbitrary repository implementations. If this function is exposed to untrusted callers (e.g., via an API route or event handler), an attacker could supply a malicious `bookingReferenceRepository` or `attendeeRepository` that deletes or modifies bookings without authorization.
  - Suggestion: Ensure that the `dependencies` parameter is only used in trusted internal contexts (e.g., dependency injection containers) and that the public API surface of `handler` does not accept user-controlled dependencies. Consider removing the optional parameter or validating that the provided dependencies are from a trusted source.
  - Evidence: `diff_hunk:packages/features/bookings/lib/handleCancelBooking.ts:136`

## Needs Human Review

- `security` high at `packages/features/bookings/repositories/BookingRepository.ts:1502` (0.50)
  - The new `updateMany` method accepts a `BookingWhereInput` filter without any authorization check, allowing bulk updates to any booking record in the database.
  - Suggestion: Add an authorization guard that verifies the caller has permission to update the targeted bookings, e.g., by ensuring the `where` clause includes the organizer's userId or a team membership check.
  - Evidence: `diff_hunk:packages/features/bookings/repositories/BookingRepository.ts:1499`

- `security` high at `packages/features/bookings/repositories/PrismaBookingAttendeeRepository.ts:8` (0.50)
  - The new `deleteManyByBookingId` method deletes all attendees for a given bookingId without any authorization check, allowing an attacker to delete attendees from any booking.
  - Suggestion: Add an authorization check that verifies the caller has permission to modify the booking's attendees, e.g., by checking the booking's organizer or team membership.
  - Evidence: `diff_hunk:packages/features/bookings/repositories/PrismaBookingAttendeeRepository.ts:1`

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
