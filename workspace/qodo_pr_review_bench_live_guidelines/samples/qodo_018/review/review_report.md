# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 20
- Changed entities: 20
- Risk signals: 7
- Findings: 10
- Needs human review: 2
- Discarded: 4
- Agent runs: 8
- Loop enabled: True
- Target repo modified: False

## Loop Summary

| Metric | Value |
|---|---:|
| Iterations | 1 / 1 |
| Converged | False |
| Fallback | False |
| Retry count | 1 |
| Total latency | 236858 ms |
| Token in | 45320 |
| Token out | 3088 |

- Iteration 0: 17 candidates, 13 verified, 2 uncertain, 11 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `file_risk_shards_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 44139 |
| Selected evidence | 26 |
| Omitted evidence | 479 |
| Context truncated | True |
| Review shards | 5 |
| Context requests | 4 |
| Refills | 2 |

## Findings

- `correctness` medium at `src/Components/WebAssembly/WebAssembly.Authentication/src/RemoteAuthenticatorViewCore.cs:106` (0.70)
  - Removal of SignOutSessionStateManager injection without verifying that all usages are removed may cause runtime failures if the component still references it.
  - Suggestion: Ensure all references to SignOutManager in the class are removed or replaced with the new implementation before deleting the injection.
  - Evidence: `diff_hunk:src/Components/WebAssembly/WebAssembly.Authentication/src/RemoteAuthenticatorViewCore.cs:106`

- `api_compatibility` medium at `src/Components/WebAssembly/WebAssembly.Authentication/src/PublicAPI.Unshipped.txt:1` (0.90)
  - Multiple public API symbols are being removed, including AccessTokenResult constructor, RemoteAuthenticationService constructor, and SignOutSessionStateManager. This is a breaking change for consumers.
  - Suggestion: Ensure these removals are intentional and documented as breaking changes. Consider obsoleting before removal if not already done.
  - Evidence: `diff_hunk:src/Components/WebAssembly/WebAssembly.Authentication/src/PublicAPI.Unshipped.txt:1`

- `api_compatibility` low at `src/Components/Web/src/WebRenderer.cs:55` (0.60)
  - Removal of the Obsolete init setter for RendererId may break derived classes that were setting the property via init, even though it was marked obsolete.
  - Suggestion: Confirm that no derived classes rely on the init setter, or keep the setter with a more targeted deprecation message.
  - Evidence: `diff_hunk:src/Components/Web/src/WebRenderer.cs:52`

- `api_compatibility` low at `src/Components/WebAssembly/JSInterop/src/InternalCalls.cs:4` (0.70)
  - Removal of the obsolete InvokeJS<T0,T1,T2,TRes> method may break backward compatibility for callers that still depend on it, even though it was marked obsolete.
  - Suggestion: Ensure that no internal or external consumers still rely on this method before removal.
  - Evidence: `diff_hunk:src/Components/WebAssembly/JSInterop/src/InternalCalls.cs:1`

- `backward_compatibility` medium at `src/Components/WebAssembly/WebAssembly.Authentication/src/RemoteAuthenticatorViewCore.cs:106` (0.70)
  - Removal of the obsolete SignOutSessionStateManager injection without a replacement may break consumers that depend on the SignOutManager property.
  - Suggestion: If SignOutManager is no longer needed, ensure all internal usage has been migrated and consider adding an [Obsolete] property stub that throws or returns null to ease migration.
  - Evidence: `diff_hunk:src/Components/WebAssembly/WebAssembly.Authentication/src/RemoteAuthenticatorViewCore.cs:106`, `diff:src/Components/WebAssembly/WebAssembly.Authentication/src/RemoteAuthenticatorViewCore.cs:110`

- `correctness` high at `src/Components/WebAssembly/WebAssembly.Authentication/src/Services/AccessTokenNotAvailableException.cs:38` (0.90)
  - Removing the null check for `_tokenResult.InteractiveRequestUrl` before passing it to `_navigation.NavigateToLogin` can cause a NullReferenceException when `InteractiveRequestUrl` is null.
  - Suggestion: Restore the null check for `_tokenResult.InteractiveRequestUrl` or add a guard before calling `NavigateToLogin`.
  - Evidence: `diff_hunk:src/Components/WebAssembly/WebAssembly.Authentication/src/Services/AccessTokenNotAvailableException.cs:35`

- `maintainability` info at `src/Components/WebAssembly/WebAssembly.Authentication/src/Services/SignOutSessionStateManager.cs:1` (0.80)
  - The entire file is deleted, which is a breaking change for any consumers still using the obsolete `SignOutSessionStateManager` class. Ensure that all references have been migrated to the recommended `NavigateToLogout` method.
  - Suggestion: Verify that no remaining code references `SignOutSessionStateManager` and that the migration path is documented.
  - Evidence: `diff_hunk:src/Components/WebAssembly/WebAssembly.Authentication/src/Services/SignOutSessionStateManager.cs:1`

- `correctness` medium at `src/Components/WebAssembly/WebAssembly.Authentication/src/WebAssemblyAuthenticationServiceCollectionExtensions.cs:74` (0.80)
  - Removal of SignOutSessionStateManager registration without removing all dependent code may cause runtime failures for consumers relying on this service.
  - Suggestion: Ensure that all references to SignOutSessionStateManager are removed or replaced, and that the service is no longer required by any component.
  - Evidence: `diff_hunk:src/Components/WebAssembly/WebAssembly.Authentication/src/WebAssemblyAuthenticationServiceCollectionExtensions.cs:71`

- `correctness` medium at `src/Components/WebAssembly/WebAssembly.Authentication/test/RemoteAuthenticatorCoreTests.cs:370` (0.70)
  - Removal of test 'AuthenticationManager_Logout_RedirectsToFailureOnInvalidSignOutState' reduces test coverage for the logout failure scenario when SignOutSessionStateManager returns invalid state.
  - Suggestion: If the SignOutSessionStateManager is removed, consider adding a new test that validates the expected behavior when sign-out state is invalid, or update the existing test to reflect the new design.
  - Evidence: `diff_hunk:src/Components/WebAssembly/WebAssembly.Authentication/test/RemoteAuthenticatorCoreTests.cs:370`

- `maintainability` low at `src/Components/WebAssembly/WebAssembly/src/Infrastructure/JSInteropMethods.cs:17` (0.60)
  - Removal of the obsolete NotifyLocationChanged method may break external consumers that still reference it, even though it is marked obsolete.
  - Suggestion: If the method is no longer used internally, ensure that no external consumers depend on it, or provide a migration path.
  - Evidence: `diff_hunk:src/Components/WebAssembly/WebAssembly/src/Infrastructure/JSInteropMethods.cs:14`

## Needs Human Review

- `style` error at `src/Components/Components/src/Routing/Router.cs:101` (0.50)
  - File is missing the required MIT license header.
  - Suggestion: Add the following two-line comment at the very beginning of the file: '// Licensed to the .NET Foundation under one or more agreements.' followed by '// The .NET Foundation licenses this file to you under the MIT license.'
  - Evidence: `entity:src/Components/Components/src/Routing/Router.cs:src.Components.Components.src.Routing.Router`

- `style` error at `src/Components/Forms/src/EditContextDataAnnotationsExtensions.cs:23` (0.50)
  - File is missing the required MIT license header.
  - Suggestion: Add the following two-line comment at the very beginning of the file: '// Licensed to the .NET Foundation under one or more agreements.' followed by '// The .NET Foundation licenses this file to you under the MIT license.'
  - Evidence: `entity:src/Components/Forms/src/EditContextDataAnnotationsExtensions.cs:src.Components.Forms.src.EditContextDataAnnotationsExtensions`

## Changed Files

- `src/Components/Components/src/PublicAPI.Unshipped.txt` (modified)
- `src/Components/Components/src/Routing/Router.cs` (modified)
- `src/Components/Forms/src/EditContextDataAnnotationsExtensions.cs` (modified)
- `src/Components/Forms/src/PublicAPI.Unshipped.txt` (modified)
- `src/Components/Forms/test/EditContextDataAnnotationsExtensionsTest.cs` (modified)
- `src/Components/Web/src/Forms/InputFile/RemoteBrowserFileStreamOptions.cs` (deleted)
- `src/Components/Web/src/PublicAPI.Unshipped.txt` (modified)
- `src/Components/Web/src/Web/WebEventCallbackFactoryEventArgsExtensions.cs` (deleted)
- `src/Components/Web/src/WebRenderer.cs` (modified)
- `src/Components/WebAssembly/JSInterop/src/InternalCalls.cs` (modified)
- `src/Components/WebAssembly/WebAssembly.Authentication/src/PublicAPI.Unshipped.txt` (modified)
- `src/Components/WebAssembly/WebAssembly.Authentication/src/RemoteAuthenticatorViewCore.cs` (modified)
- `src/Components/WebAssembly/WebAssembly.Authentication/src/Services/AccessTokenNotAvailableException.cs` (modified)
- `src/Components/WebAssembly/WebAssembly.Authentication/src/Services/AccessTokenResult.cs` (modified)
- `src/Components/WebAssembly/WebAssembly.Authentication/src/Services/RemoteAuthenticationService.cs` (modified)
- `src/Components/WebAssembly/WebAssembly.Authentication/src/Services/SignOutSessionStateManager.cs` (deleted)
- `src/Components/WebAssembly/WebAssembly.Authentication/src/WebAssemblyAuthenticationServiceCollectionExtensions.cs` (modified)
- `src/Components/WebAssembly/WebAssembly.Authentication/test/RemoteAuthenticatorCoreTests.cs` (modified)
- `src/Components/WebAssembly/WebAssembly/src/Infrastructure/JSInteropMethods.cs` (modified)
- `src/Components/WebAssembly/WebAssembly/src/PublicAPI.Unshipped.txt` (modified)

## Changed Entities

- `src/Components/Components/src/PublicAPI.Unshipped.txt:2-4` module `src.Components.Components.src.PublicAPI.Unshipped`
- `src/Components/Components/src/Routing/Router.cs:101-108` module `src.Components.Components.src.Routing.Router`
- `src/Components/Forms/src/EditContextDataAnnotationsExtensions.cs:23-43` module `src.Components.Forms.src.EditContextDataAnnotationsExtensions`
- `src/Components/Forms/src/PublicAPI.Unshipped.txt:2-3` module `src.Components.Forms.src.PublicAPI.Unshipped`
- `src/Components/Forms/test/EditContextDataAnnotationsExtensionsTest.cs:21-30` module `src.Components.Forms.test.EditContextDataAnnotationsExtensionsTest`
- `src/Components/Web/src/Forms/InputFile/RemoteBrowserFileStreamOptions.cs:1-39` module `src.Components.Web.src.Forms.InputFile.RemoteBrowserFileStreamOptions`
- `src/Components/Web/src/PublicAPI.Unshipped.txt:2-31` module `src.Components.Web.src.PublicAPI.Unshipped`
- `src/Components/Web/src/Web/WebEventCallbackFactoryEventArgsExtensions.cs:1-329` module `src.Components.Web.src.Web.WebEventCallbackFactoryEventArgsExtensions`
- `src/Components/Web/src/WebRenderer.cs:55-57` module `src.Components.Web.src.WebRenderer`
- `src/Components/WebAssembly/JSInterop/src/InternalCalls.cs:4-19` module `src.Components.WebAssembly.JSInterop.src.InternalCalls`
- `src/Components/WebAssembly/WebAssembly.Authentication/src/PublicAPI.Unshipped.txt:2-8` module `src.Components.WebAssembly.WebAssembly.Authentication.src.PublicAPI.Unshipped`
- `src/Components/WebAssembly/WebAssembly.Authentication/src/RemoteAuthenticatorViewCore.cs:109-112` module `src.Components.WebAssembly.WebAssembly.Authentication.src.RemoteAuthenticatorViewCore`
- `src/Components/WebAssembly/WebAssembly.Authentication/src/Services/AccessTokenNotAvailableException.cs:38-46` module `src.Components.WebAssembly.WebAssembly.Authentication.src.Services.AccessTokenNotAvailableException`
- `src/Components/WebAssembly/WebAssembly.Authentication/src/Services/AccessTokenResult.cs:15-28` module `src.Components.WebAssembly.WebAssembly.Authentication.src.Services.AccessTokenResult`
- `src/Components/WebAssembly/WebAssembly.Authentication/src/Services/RemoteAuthenticationService.cs:60-76` module `src.Components.WebAssembly.WebAssembly.Authentication.src.Services.RemoteAuthenticationService`
- `src/Components/WebAssembly/WebAssembly.Authentication/src/Services/SignOutSessionStateManager.cs:1-88` module `src.Components.WebAssembly.WebAssembly.Authentication.src.Services.SignOutSessionStateManager`
- `src/Components/WebAssembly/WebAssembly.Authentication/src/WebAssemblyAuthenticationServiceCollectionExtensions.cs:74-76` module `src.Components.WebAssembly.WebAssembly.Authentication.src.WebAssemblyAuthenticationServiceCollectionExtensions`
- `src/Components/WebAssembly/WebAssembly.Authentication/test/RemoteAuthenticatorCoreTests.cs:373-403` module `src.Components.WebAssembly.WebAssembly.Authentication.test.RemoteAuthenticatorCoreTests`
- `src/Components/WebAssembly/WebAssembly/src/Infrastructure/JSInteropMethods.cs:17-23` module `src.Components.WebAssembly.WebAssembly.src.Infrastructure.JSInteropMethods`
- `src/Components/WebAssembly/WebAssembly/src/PublicAPI.Unshipped.txt:2-3` module `src.Components.WebAssembly.WebAssembly.src.PublicAPI.Unshipped`

## Risk Signals

- `security_sensitive` (0.74): Security-sensitive keywords changed in src/Components/WebAssembly/WebAssembly.Authentication/src/PublicAPI.Unshipped.txt.
- `security_sensitive` (0.74): Security-sensitive keywords changed in src/Components/WebAssembly/WebAssembly.Authentication/src/RemoteAuthenticatorViewCore.cs.
- `security_sensitive` (0.74): Security-sensitive keywords changed in src/Components/WebAssembly/WebAssembly.Authentication/src/Services/AccessTokenNotAvailableException.cs.
- `security_sensitive` (0.74): Security-sensitive keywords changed in src/Components/WebAssembly/WebAssembly.Authentication/src/Services/AccessTokenResult.cs.
- `security_sensitive` (0.74): Security-sensitive keywords changed in src/Components/WebAssembly/WebAssembly.Authentication/src/Services/RemoteAuthenticationService.cs.
- `security_sensitive` (0.74): Security-sensitive keywords changed in src/Components/WebAssembly/WebAssembly.Authentication/src/Services/SignOutSessionStateManager.cs.
- `security_sensitive` (0.74): Security-sensitive keywords changed in src/Components/WebAssembly/WebAssembly.Authentication/test/RemoteAuthenticatorCoreTests.cs.

## Evidence Index

- `diff:src/Components/Components/src/PublicAPI.Unshipped.txt:2` [diff]: src/Components/Components/src/PublicAPI.Unshipped.txt:2
- `diff:src/Components/Components/src/PublicAPI.Unshipped.txt:3` [diff]: src/Components/Components/src/PublicAPI.Unshipped.txt:3
- `diff:src/Components/Components/src/PublicAPI.Unshipped.txt:4` [diff]: src/Components/Components/src/PublicAPI.Unshipped.txt:4
- `diff:src/Components/Components/src/Routing/Router.cs:101` [diff]: src/Components/Components/src/Routing/Router.cs:101
- `diff:src/Components/Components/src/Routing/Router.cs:102` [diff]: src/Components/Components/src/Routing/Router.cs:102
- `diff:src/Components/Components/src/Routing/Router.cs:103` [diff]: src/Components/Components/src/Routing/Router.cs:103
- `diff:src/Components/Components/src/Routing/Router.cs:104` [diff]: src/Components/Components/src/Routing/Router.cs:104
- `diff:src/Components/Components/src/Routing/Router.cs:105` [diff]: src/Components/Components/src/Routing/Router.cs:105
- `diff:src/Components/Components/src/Routing/Router.cs:106` [diff]: src/Components/Components/src/Routing/Router.cs:106
- `diff:src/Components/Components/src/Routing/Router.cs:107` [diff]: src/Components/Components/src/Routing/Router.cs:107
- `diff:src/Components/Components/src/Routing/Router.cs:108` [diff]: src/Components/Components/src/Routing/Router.cs:108
- `diff:src/Components/Forms/src/EditContextDataAnnotationsExtensions.cs:23` [diff]: src/Components/Forms/src/EditContextDataAnnotationsExtensions.cs:23
- `diff:src/Components/Forms/src/EditContextDataAnnotationsExtensions.cs:24` [diff]: src/Components/Forms/src/EditContextDataAnnotationsExtensions.cs:24
- `diff:src/Components/Forms/src/EditContextDataAnnotationsExtensions.cs:25` [diff]: src/Components/Forms/src/EditContextDataAnnotationsExtensions.cs:25
- `diff:src/Components/Forms/src/EditContextDataAnnotationsExtensions.cs:26` [diff]: src/Components/Forms/src/EditContextDataAnnotationsExtensions.cs:26
- `diff:src/Components/Forms/src/EditContextDataAnnotationsExtensions.cs:27` [diff]: src/Components/Forms/src/EditContextDataAnnotationsExtensions.cs:27
- `diff:src/Components/Forms/src/EditContextDataAnnotationsExtensions.cs:28` [diff]: src/Components/Forms/src/EditContextDataAnnotationsExtensions.cs:28
- `diff:src/Components/Forms/src/EditContextDataAnnotationsExtensions.cs:29` [diff]: src/Components/Forms/src/EditContextDataAnnotationsExtensions.cs:29
- `diff:src/Components/Forms/src/EditContextDataAnnotationsExtensions.cs:30` [diff]: src/Components/Forms/src/EditContextDataAnnotationsExtensions.cs:30
- `diff:src/Components/Forms/src/EditContextDataAnnotationsExtensions.cs:31` [diff]: src/Components/Forms/src/EditContextDataAnnotationsExtensions.cs:31
- `diff:src/Components/Forms/src/EditContextDataAnnotationsExtensions.cs:32` [diff]: src/Components/Forms/src/EditContextDataAnnotationsExtensions.cs:32
- `diff:src/Components/Forms/src/EditContextDataAnnotationsExtensions.cs:33` [diff]: src/Components/Forms/src/EditContextDataAnnotationsExtensions.cs:33
- `diff:src/Components/Forms/src/EditContextDataAnnotationsExtensions.cs:34` [diff]: src/Components/Forms/src/EditContextDataAnnotationsExtensions.cs:34
- `diff:src/Components/Forms/src/EditContextDataAnnotationsExtensions.cs:35` [diff]: src/Components/Forms/src/EditContextDataAnnotationsExtensions.cs:35
- `diff:src/Components/Forms/src/EditContextDataAnnotationsExtensions.cs:36` [diff]: src/Components/Forms/src/EditContextDataAnnotationsExtensions.cs:36
- `diff:src/Components/Forms/src/EditContextDataAnnotationsExtensions.cs:37` [diff]: src/Components/Forms/src/EditContextDataAnnotationsExtensions.cs:37
- `diff:src/Components/Forms/src/EditContextDataAnnotationsExtensions.cs:38` [diff]: src/Components/Forms/src/EditContextDataAnnotationsExtensions.cs:38
- `diff:src/Components/Forms/src/EditContextDataAnnotationsExtensions.cs:39` [diff]: src/Components/Forms/src/EditContextDataAnnotationsExtensions.cs:39
- `diff:src/Components/Forms/src/EditContextDataAnnotationsExtensions.cs:40` [diff]: src/Components/Forms/src/EditContextDataAnnotationsExtensions.cs:40
- `diff:src/Components/Forms/src/EditContextDataAnnotationsExtensions.cs:41` [diff]: src/Components/Forms/src/EditContextDataAnnotationsExtensions.cs:41
- ... 687 more evidence items omitted.
