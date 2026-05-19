# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 20
- Changed entities: 20
- Risk signals: 7
- Findings: 3
- Needs human review: 2
- Discarded: 3
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
| Total latency | 66478 ms |
| Token in | 33112 |
| Token out | 2158 |

- Iteration 0: 8 candidates, 5 verified, 2 uncertain, 3 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `file_risk_shards_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 27495 |
| Selected evidence | 31 |
| Omitted evidence | 474 |
| Context truncated | True |
| Review shards | 5 |
| Context requests | 9 |
| Refills | 3 |

## Findings

- `api_breaking_change` medium at `src/Components/WebAssembly/WebAssembly.Authentication/src/PublicAPI.Unshipped.txt:2` (0.80)
  - Removal of public API entries for AccessTokenResult, RemoteAuthenticationService, and SignOutSessionStateManager indicates breaking changes that may affect consumers.
  - Suggestion: Verify that these removals are intentional and documented as breaking changes; consider deprecation warnings if not already done.
  - Evidence: `diff_hunk:src/Components/WebAssembly/WebAssembly.Authentication/src/PublicAPI.Unshipped.txt:1`

- `test_coverage` medium at `src/Components/WebAssembly/WebAssembly.Authentication/test/RemoteAuthenticatorCoreTests.cs:370` (0.80)
  - Removing the test 'AuthenticationManager_Logout_RedirectsToFailureOnInvalidSignOutState' reduces coverage for the invalid sign-out state scenario, which may hide regressions.
  - Suggestion: If the sign-out state validation logic is still present, add a new test that covers the same scenario using the updated implementation.
  - Evidence: `diff_hunk:src/Components/WebAssembly/WebAssembly.Authentication/test/RemoteAuthenticatorCoreTests.cs:370`

- `api_removal` medium at `src/Components/WebAssembly/WebAssembly/src/Infrastructure/JSInteropMethods.cs:17` (0.75)
  - Removing the public method NotifyLocationChanged may break external callers that rely on this API, even if it was marked obsolete.
  - Suggestion: If the method is no longer needed, ensure all internal callers have been migrated and consider a longer deprecation period for external consumers.
  - Evidence: `diff_hunk:src/Components/WebAssembly/WebAssembly/src/Infrastructure/JSInteropMethods.cs:14`

## Needs Human Review

- `potential_bug` high at `src/Components/WebAssembly/WebAssembly.Authentication/src/Services/AccessTokenNotAvailableException.cs:44` (0.50)
  - Removed null check for _tokenResult.InteractiveRequestUrl before passing it to NavigateToLogin and NavigateTo. If InteractiveRequestUrl is null, NavigateToLogin may receive null and NavigateTo will throw ArgumentNullException.
  - Suggestion: Restore the null check for _tokenResult.InteractiveRequestUrl or add a guard before calling NavigateToLogin and NavigateTo.
  - Evidence: `diff_hunk:src/Components/WebAssembly/WebAssembly.Authentication/src/Services/AccessTokenNotAvailableException.cs:35`

- `breaking_change` high at `src/Components/WebAssembly/WebAssembly.Authentication/src/WebAssemblyAuthenticationServiceCollectionExtensions.cs:75` (0.50)
  - Removal of SignOutSessionStateManager registration without replacement may break existing consumers that depend on this service via DI.
  - Suggestion: If SignOutSessionStateManager is still needed by consumers, keep the registration but suppress the obsolete warning. If it is fully replaced, ensure a migration guide or alternative registration is provided.
  - Evidence: `diff_hunk:src/Components/WebAssembly/WebAssembly.Authentication/src/WebAssemblyAuthenticationServiceCollectionExtensions.cs:71`, `diff:src/Components/WebAssembly/WebAssembly.Authentication/src/WebAssemblyAuthenticationServiceCollectionExtensions.cs:75`

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
