# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 20
- Changed entities: 20
- Risk signals: 7
- Findings: 5
- Needs human review: 4
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
| Retry count | 4 |
| Total latency | 337671 ms |
| Token in | 45396 |
| Token out | 2845 |

- Iteration 0: 13 candidates, 10 verified, 4 uncertain, 6 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `file_risk_shards_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 41603 |
| Selected evidence | 29 |
| Omitted evidence | 476 |
| Context truncated | True |
| Review shards | 5 |
| Context requests | 6 |
| Refills | 3 |

## Findings

- `api_breaking_change` medium at `src/Components/WebAssembly/WebAssembly.Authentication/src/PublicAPI.Unshipped.txt:2` (0.90)
  - Multiple public API entries are being removed, including AccessTokenResult constructor, RemoteAuthenticationService constructor, and the entire SignOutSessionStateManager class. This is a breaking change for consumers.
  - Suggestion: If these removals are intentional, ensure they are documented in a migration guide and that consumers have a clear upgrade path.
  - Evidence: `diff_hunk:src/Components/WebAssembly/WebAssembly.Authentication/src/PublicAPI.Unshipped.txt:1`

- `api_breaking_change` low at `src/Components/Web/src/WebRenderer.cs:55` (0.70)
  - Removal of the obsolete init setter for RendererId may break derived classes that were using the init accessor to set the renderer ID.
  - Suggestion: If the init setter is no longer needed, ensure that derived classes have an alternative way to set the renderer ID (e.g., via GetWebRendererId override).
  - Evidence: `diff_hunk:src/Components/Web/src/WebRenderer.cs:52`

- `api_breaking_change` medium at `src/Components/WebAssembly/JSInterop/src/InternalCalls.cs:12` (0.80)
  - Removal of the obsolete InvokeJS<T0,T1,T2,TRes> method may break consumers that still depend on this backward-compatibility shim.
  - Suggestion: Ensure that all consumers have migrated to the new InvokeJSJson method before removing the obsolete method.
  - Evidence: `diff_hunk:src/Components/WebAssembly/JSInterop/src/InternalCalls.cs:1`

- `security` high at `src/Components/WebAssembly/WebAssembly.Authentication/src/RemoteAuthenticatorViewCore.cs:278` (0.85)
  - Removal of fallback sign-out state validation may allow externally initiated logouts to bypass state validation when HistoryEntryState is null.
  - Suggestion: Restore the fallback check for SignOutManager.ValidateSignOutState() when Navigation.HistoryEntryState is null, or ensure that ValidateSignOutRequestState() covers both cases.
  - Evidence: `diff_hunk:src/Components/WebAssembly/WebAssembly.Authentication/src/RemoteAuthenticatorViewCore.cs:278`

- `correctness` high at `src/Components/WebAssembly/WebAssembly.Authentication/src/Services/AccessTokenNotAvailableException.cs:38` (0.90)
  - Removing the null check for _tokenResult.InteractiveRequestUrl can cause a NullReferenceException when _tokenResult.InteractiveRequestUrl is null but InteractionOptions is not null.
  - Suggestion: Restore the null check for _tokenResult.InteractiveRequestUrl before passing it to _navigation.NavigateToLogin, or ensure InteractiveRequestUrl is always non-null when InteractionOptions is set.
  - Evidence: `diff:src/Components/WebAssembly/WebAssembly.Authentication/src/Services/AccessTokenNotAvailableException.cs:44`, `diff_hunk:src/Components/WebAssembly/WebAssembly.Authentication/src/Services/AccessTokenNotAvailableException.cs:35`

## Needs Human Review

- `correctness` medium at `src/Components/Forms/test/EditContextDataAnnotationsExtensionsTest.cs:18` (0.50)
  - Removal of test 'ObsoleteApiReturnsEditContextForChaining' without verifying that the obsolete API it tested is still functional or that its removal is covered elsewhere.
  - Suggestion: Ensure the obsolete API 'AddDataAnnotationsValidation' is either removed or its behavior is covered by another test.
  - Evidence: `diff_hunk:src/Components/Forms/test/EditContextDataAnnotationsExtensionsTest.cs:18`

- `test_quality` medium at `src/Components/WebAssembly/WebAssembly.Authentication/test/RemoteAuthenticatorCoreTests.cs:370` (0.50)
  - Removed test 'AuthenticationManager_Logout_RedirectsToFailureOnInvalidSignOutState' without replacement, reducing coverage for the SignOutSessionStateManager flow. The test validated that an invalid sign-out state redirects to the logout-failed page with the correct error message.
  - Suggestion: Ensure the removed scenario is covered by an existing or new test, or add a test that validates the behavior when SignOutSessionStateManager returns false for sign-out state.
  - Evidence: `diff_hunk:src/Components/WebAssembly/WebAssembly.Authentication/test/RemoteAuthenticatorCoreTests.cs:370`

- `backward_compatibility` medium at `src/Components/WebAssembly/WebAssembly.Authentication/src/WebAssemblyAuthenticationServiceCollectionExtensions.cs:74` (0.50)
  - Removed registration of 'SignOutSessionStateManager' (marked obsolete) from DI. This is a breaking change for any consumer that depends on this service being available via DI, even if the type is obsolete.
  - Suggestion: If the service is no longer needed, ensure all internal consumers have been migrated. If external consumers may still rely on it, consider keeping the registration with an extended obsoletion message or providing a shim.
  - Evidence: `diff_hunk:src/Components/WebAssembly/WebAssembly.Authentication/src/WebAssemblyAuthenticationServiceCollectionExtensions.cs:71`

- `backward_compatibility` medium at `src/Components/WebAssembly/WebAssembly/src/Infrastructure/JSInteropMethods.cs:17` (0.50)
  - Removed public method 'NotifyLocationChanged' which was marked obsolete but still part of the public API surface. This is a breaking change for any external caller that may still reference it.
  - Suggestion: If the method is no longer used internally and safe to remove, ensure no external consumers depend on it. Otherwise, keep the method with an updated obsoletion message.
  - Evidence: `diff_hunk:src/Components/WebAssembly/WebAssembly/src/Infrastructure/JSInteropMethods.cs:14`

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
