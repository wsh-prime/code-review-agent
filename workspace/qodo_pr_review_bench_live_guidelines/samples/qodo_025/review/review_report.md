# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 23
- Changed entities: 23
- Risk signals: 9
- Findings: 0
- Needs human review: 7
- Discarded: 2
- Agent runs: 8
- Loop enabled: True
- Target repo modified: False

## Loop Summary

| Metric | Value |
|---|---:|
| Iterations | 1 / 1 |
| Converged | False |
| Fallback | False |
| Retry count | 4 |
| Total latency | 401759 ms |
| Token in | 34684 |
| Token out | 1963 |

- Iteration 0: 9 candidates, 7 verified, 7 uncertain, 0 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `file_risk_shards_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 34974 |
| Selected evidence | 28 |
| Omitted evidence | 678 |
| Context truncated | True |
| Review shards | 6 |
| Context requests | 1 |
| Refills | 1 |

## Findings

No findings.

Checked changed files, changed entities, deterministic risk signals, and evidence references. No high-confidence review finding was produced.

## Needs Human Review

- `naming_convention` warning at `packages/features/bookings/di/BookingAttendeeRepository.module.ts:1` (0.50)
  - Repository file name 'BookingAttendeeRepository.module.ts' does not follow the required 'Prisma<Entity>Repository' pattern. The file should be named 'PrismaBookingAttendeeRepository.module.ts' to match the class it binds.
  - Suggestion: Rename the file to 'PrismaBookingAttendeeRepository.module.ts' to follow the naming convention.
  - Evidence: `diff_hunk:packages/features/bookings/di/BookingAttendeeRepository.module.ts:1`

- `naming_convention` warning at `packages/features/bookings/di/BookingCancelService.module.ts:1` (0.50)
  - Service file name 'BookingCancelService.module.ts' does not follow the required '<Entity>Service' pattern. The file should be named 'BookingCancelService.module.ts' (this is correct) but the class it binds is 'BookingCancelService' which is correct. However, the file is a DI module, not a service file. The guideline requires service files to be named '<Entity>Service.ts' with matching class names. This file is a DI module, not a service, so it may be acceptable, but the naming is ambiguous.
  - Suggestion: Consider renaming to 'BookingCancelServiceModule.ts' or similar to clearly indicate it is a DI module.
  - Evidence: `diff_hunk:packages/features/bookings/di/BookingCancelService.module.ts:1`

- `naming_convention` medium at `packages/features/bookingReference/repositories/BookingReferenceRepository.ts:17` (0.50)
  - Repository class name 'BookingReferenceRepository' does not follow the required 'Prisma<Entity>Repository' pattern.
  - Suggestion: Rename the class to 'PrismaBookingReferenceRepository' and update the filename accordingly to 'PrismaBookingReferenceRepository.ts'.
  - Evidence: `diff_hunk:packages/features/bookingReference/repositories/BookingReferenceRepository.ts:15`

- `naming_convention` minor at `packages/features/bookings/di/BookingReferenceRepository.module.ts:1` (0.50)
  - Repository file uses generic naming pattern 'BookingReferenceRepository.module.ts' instead of required 'Prisma<Entity>Repository.ts' pattern.
  - Suggestion: Rename the file to 'PrismaBookingReferenceRepository.ts' and update the class name to 'PrismaBookingReferenceRepository' to follow the naming convention.
  - Evidence: `diff_hunk:packages/features/bookings/di/BookingReferenceRepository.module.ts:1`

- `naming_convention` minor at `packages/features/bookings/lib/handleCancelBooking.ts:136` (0.50)
  - Repository class 'BookingReferenceRepository' is instantiated directly but does not follow the 'Prisma<Entity>Repository' naming pattern.
  - Suggestion: Ensure the imported 'BookingReferenceRepository' class is named 'PrismaBookingReferenceRepository' or rename it accordingly.
  - Evidence: `diff_hunk:packages/features/bookings/lib/handleCancelBooking.ts:136`

- `naming_convention` medium at `packages/lib/server/repository/dto/IBookingRepository.ts:1` (0.50)
  - Repository interface file IBookingRepository.ts does not follow the required 'Prisma<Entity>Repository' naming pattern.
  - Suggestion: Rename the file to PrismaBookingRepository.ts and update the exported interface name accordingly to match the naming convention.
  - Evidence: `diff_hunk:packages/lib/server/repository/dto/IBookingRepository.ts:1`

- `naming_convention` medium at `packages/lib/server/repository/dto/IProfileRepository.ts:1` (0.50)
  - Repository interface file IProfileRepository.ts does not follow the required 'Prisma<Entity>Repository' naming pattern.
  - Suggestion: Rename the file to PrismaProfileRepository.ts and update the exported interface name accordingly to match the naming convention.
  - Evidence: `diff_hunk:packages/lib/server/repository/dto/IProfileRepository.ts:1`

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
