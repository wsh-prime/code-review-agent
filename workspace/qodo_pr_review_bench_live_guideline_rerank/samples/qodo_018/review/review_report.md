# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 20
- Changed entities: 20
- Risk signals: 7
- Findings: 2
- Needs human review: 4
- Discarded: 0
- Agent runs: 6
- Loop enabled: True
- Target repo modified: False

## Loop Summary

| Metric | Value |
|---|---:|
| Iterations | 1 / 1 |
| Converged | False |
| Fallback | False |
| Retry count | 2 |
| Total latency | 265605 ms |
| Token in | 28862 |
| Token out | 1138 |

- Iteration 0: 6 candidates, 6 verified, 4 uncertain, 2 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `file_risk_shards_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 33044 |
| Selected evidence | 20 |
| Omitted evidence | 485 |
| Context truncated | True |
| Review shards | 5 |
| Context requests | 0 |
| Refills | 0 |

## Findings

- `correctness` high at `src/Components/WebAssembly/WebAssembly.Authentication/src/Services/AccessTokenNotAvailableException.cs:38` (0.95)
  - Removing the null check for _tokenResult.InteractiveRequestUrl can cause a NullReferenceException when InteractiveRequestUrl is null.
  - Suggestion: Restore the null check for _tokenResult.InteractiveRequestUrl before calling NavigateToLogin or NavigateTo.
  - Evidence: `diff_hunk:src/Components/WebAssembly/WebAssembly.Authentication/src/Services/AccessTokenNotAvailableException.cs:35`

- `maintainability` medium at `src/Components/WebAssembly/WebAssembly.Authentication/src/Services/AccessTokenNotAvailableException.cs:38` (0.80)
  - The patch removes the obsolete RedirectUrl fallback path but replaces it with InteractiveRequestUrl without a null guard, which may break existing callers relying on the fallback.
  - Suggestion: Ensure InteractiveRequestUrl is non-null before using it, or provide a fallback to RedirectUrl if available.
  - Evidence: `diff_hunk:src/Components/WebAssembly/WebAssembly.Authentication/src/Services/AccessTokenNotAvailableException.cs:35`

## Needs Human Review

- `maintainability` medium at `src/Components/Forms/test/EditContextDataAnnotationsExtensionsTest.cs:18` (0.50)
  - Removed test 'ObsoleteApiReturnsEditContextForChaining' without adding a replacement test for the new API behavior, reducing test coverage for the chaining functionality.
  - Suggestion: Add a new test that validates the current (non-obsolete) API returns EditContext for chaining, or ensure the removal is intentional and covered elsewhere.
  - Evidence: `diff_hunk:src/Components/Forms/test/EditContextDataAnnotationsExtensionsTest.cs:18`

- `test_quality` medium at `src/Components/WebAssembly/WebAssembly.Authentication/test/RemoteAuthenticatorCoreTests.cs:370` (0.50)
  - Removed test 'AuthenticationManager_Logout_RedirectsToFailureOnInvalidSignOutState' without replacement. This test validated behavior when SignOutSessionStateManager returns false, which is now untested.
  - Suggestion: Add a new test that covers the scenario where sign-out state is invalid, using the updated service registration (without SignOutSessionStateManager).
  - Evidence: `diff_hunk:src/Components/WebAssembly/WebAssembly.Authentication/test/RemoteAuthenticatorCoreTests.cs:370`, `diff_hunk:src/Components/WebAssembly/WebAssembly.Authentication/src/WebAssemblyAuthenticationServiceCollectionExtensions.cs:71`

- `backward_compatibility` medium at `src/Components/WebAssembly/WebAssembly.Authentication/src/WebAssemblyAuthenticationServiceCollectionExtensions.cs:74` (0.50)
  - Removal of SignOutSessionStateManager registration from DI is a breaking change for any consumer that depends on this service being available. The class is marked obsolete but was previously registered for backward compatibility.
  - Suggestion: If the service is still needed by external consumers, keep the registration with an updated obsoletion message. If removal is intentional, document the breaking change in release notes.
  - Evidence: `diff_hunk:src/Components/WebAssembly/WebAssembly.Authentication/src/WebAssemblyAuthenticationServiceCollectionExtensions.cs:71`

- `backward_compatibility` medium at `src/Components/WebAssembly/WebAssembly/src/Infrastructure/JSInteropMethods.cs:17` (0.50)
  - Removal of public API 'JSInteropMethods.NotifyLocationChanged' is a breaking change. The method was marked obsolete but was still part of the public surface. Consumers using this method will fail to compile.
  - Suggestion: If removal is intentional, ensure consumers are migrated. Consider keeping the method with [Obsolete] and a removal date if needed.
  - Evidence: `diff_hunk:src/Components/WebAssembly/WebAssembly/src/Infrastructure/JSInteropMethods.cs:14`, `diff_hunk:src/Components/WebAssembly/WebAssembly/src/PublicAPI.Unshipped.txt:1`

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
