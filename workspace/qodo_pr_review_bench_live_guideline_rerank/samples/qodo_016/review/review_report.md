# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 16
- Changed entities: 16
- Risk signals: 4
- Findings: 0
- Needs human review: 4
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
| Retry count | 5 |
| Total latency | 455131 ms |
| Token in | 41990 |
| Token out | 2610 |

- Iteration 0: 8 candidates, 4 verified, 4 uncertain, 0 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `file_risk_shards_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 35609 |
| Selected evidence | 22 |
| Omitted evidence | 349 |
| Context truncated | True |
| Review shards | 5 |
| Context requests | 5 |
| Refills | 2 |

## Findings

No findings.

Checked changed files, changed entities, deterministic risk signals, and evidence references. No high-confidence review finding was produced.

## Needs Human Review

- `best_practice` medium at `src/Components/Web/src/Forms/DisplayName.cs:1` (0.50)
  - Missing XML documentation comments on public API: class DisplayName<TValue> and its public members lack <summary> tags.
  - Suggestion: Add XML doc comments for the class and all public members (For, Attach, SetParametersAsync).
  - Evidence: `diff_hunk:src/Components/Web/src/Forms/DisplayName.cs:1`

- `best_practice` medium at `src/Components/Web/src/Forms/ExpressionMemberAccessor.cs:1` (0.50)
  - Missing XML documentation comments on public API: public method GetDisplayName(MemberInfo) and GetDisplayName<TValue>(Expression<Func<TValue>>) lack <summary> tags.
  - Suggestion: Add XML doc comments for the public methods.
  - Evidence: `diff_hunk:src/Components/Web/src/Forms/ExpressionMemberAccessor.cs:1`

- `code_style` medium at `src/Components/test/testassets/BasicTestApp/TestResources.cs:1` (0.50)
  - New C# file TestResources.cs is missing the required MIT license header. Guideline 'All C# Source Files Must Include MIT License Header' requires the exact two-line comment header at the start of every .cs file.
  - Suggestion: Add the standard license header: '// Licensed to the .NET Foundation under one or more agreements.' followed by '// The .NET Foundation licenses this file to you under the MIT license.' at the top of the file.
  - Evidence: `diff_hunk:src/Components/test/testassets/BasicTestApp/TestResources.cs:1`

- `security` medium at `src/ProjectTemplates/Web.ProjectTemplates/content/BlazorWeb-CSharp/BlazorWebCSharp.1/Components/Account/Pages/ResetPassword.razor:96` (0.50)
  - The patch adds [Display(Name = "Email")] and [Display(Name = "Password")] data annotation attributes to the InputModel properties. While these are used for UI display names, the password field is also decorated with [DataType(DataType.Password)]. The change replaces hardcoded label text with a <DisplayName> component that reads from these annotations. If the DisplayName component or the underlying model binding does not properly handle the DataType.Password attribute, the password field could be rendered as plain text in the UI, exposing the password in the HTML source or on screen.
  - Suggestion: Verify that the <DisplayName> component respects the [DataType(DataType.Password)] attribute and renders the input as a password field (type="password"). If not, ensure the password input retains type="password" explicitly or that the DisplayName component does not override the input type.
  - Evidence: `diff_hunk:src/ProjectTemplates/Web.ProjectTemplates/content/BlazorWeb-CSharp/BlazorWebCSharp.1/Components/Account/Pages/ResetPassword.razor:96`, `diff_hunk:src/ProjectTemplates/Web.ProjectTemplates/content/BlazorWeb-CSharp/BlazorWebCSharp.1/Components/Account/Pages/ResetPassword.razor:24`

## Changed Files

- `src/Components/Web/src/Forms/DisplayName.cs` (added)
- `src/Components/Web/src/Forms/ExpressionMemberAccessor.cs` (added)
- `src/Components/Web/src/PublicAPI.Unshipped.txt` (modified)
- `src/Components/Web/test/Forms/DisplayNameTest.cs` (added)
- `src/Components/test/E2ETest/Tests/FormsTest.cs` (modified)
- `src/Components/test/testassets/BasicTestApp/FormsTest/DisplayNameComponent.razor` (added)
- `src/Components/test/testassets/BasicTestApp/Index.razor` (modified)
- `src/Components/test/testassets/BasicTestApp/Resources.fr.resx` (modified)
- `src/Components/test/testassets/BasicTestApp/Resources.resx` (modified)
- `src/Components/test/testassets/BasicTestApp/TestResources.cs` (added)
- `src/ProjectTemplates/Web.ProjectTemplates/content/BlazorWeb-CSharp/BlazorWebCSharp.1/Components/Account/Pages/ForgotPassword.razor` (modified)
- `src/ProjectTemplates/Web.ProjectTemplates/content/BlazorWeb-CSharp/BlazorWebCSharp.1/Components/Account/Pages/Login.razor` (modified)
- `src/ProjectTemplates/Web.ProjectTemplates/content/BlazorWeb-CSharp/BlazorWebCSharp.1/Components/Account/Pages/Manage/ChangePassword.razor` (modified)
- `src/ProjectTemplates/Web.ProjectTemplates/content/BlazorWeb-CSharp/BlazorWebCSharp.1/Components/Account/Pages/Manage/Email.razor` (modified)
- `src/ProjectTemplates/Web.ProjectTemplates/content/BlazorWeb-CSharp/BlazorWebCSharp.1/Components/Account/Pages/Register.razor` (modified)
- `src/ProjectTemplates/Web.ProjectTemplates/content/BlazorWeb-CSharp/BlazorWebCSharp.1/Components/Account/Pages/ResetPassword.razor` (modified)

## Changed Entities

- `src/Components/Web/src/Forms/DisplayName.cs:1-64` module `src.Components.Web.src.Forms.DisplayName`
- `src/Components/Web/src/Forms/ExpressionMemberAccessor.cs:1-87` module `src.Components.Web.src.Forms.ExpressionMemberAccessor`
- `src/Components/Web/src/PublicAPI.Unshipped.txt:43-46` module `src.Components.Web.src.PublicAPI.Unshipped`
- `src/Components/Web/test/Forms/DisplayNameTest.cs:1-232` module `src.Components.Web.test.Forms.DisplayNameTest`
- `src/Components/test/E2ETest/Tests/FormsTest.cs:558-583` module `src.Components.test.E2ETest.Tests.FormsTest`
- `src/Components/test/testassets/BasicTestApp/FormsTest/DisplayNameComponent.razor:1-35` module `src.Components.test.testassets.BasicTestApp.FormsTest.DisplayNameComponent`
- `src/Components/test/testassets/BasicTestApp/Index.razor:30-30` module `src.Components.test.testassets.BasicTestApp.Index`
- `src/Components/test/testassets/BasicTestApp/Resources.fr.resx:123-125` module `src.Components.test.testassets.BasicTestApp.Resources.fr`
- `src/Components/test/testassets/BasicTestApp/Resources.resx:123-125` module `src.Components.test.testassets.BasicTestApp.Resources`
- `src/Components/test/testassets/BasicTestApp/TestResources.cs:1-11` module `src.Components.test.testassets.BasicTestApp.TestResources`
- `src/ProjectTemplates/Web.ProjectTemplates/content/BlazorWeb-CSharp/BlazorWebCSharp.1/Components/Account/Pages/ForgotPassword.razor:28-30` module `src.ProjectTemplates.Web.ProjectTemplates.content.BlazorWeb-CSharp.BlazorWebCSharp.1.Components.Account.Pages.ForgotPassword`
- `src/ProjectTemplates/Web.ProjectTemplates/content/BlazorWeb-CSharp/BlazorWebCSharp.1/Components/Account/Pages/Login.razor:28-38` module `src.ProjectTemplates.Web.ProjectTemplates.content.BlazorWeb-CSharp.BlazorWebCSharp.1.Components.Account.Pages.Login`
- `src/ProjectTemplates/Web.ProjectTemplates/content/BlazorWeb-CSharp/BlazorWebCSharp.1/Components/Account/Pages/Manage/ChangePassword.razor:23-39` module `src.ProjectTemplates.Web.ProjectTemplates.content.BlazorWeb-CSharp.BlazorWebCSharp.1.Components.Account.Pages.Manage.ChangePassword`
- `src/ProjectTemplates/Web.ProjectTemplates/content/BlazorWeb-CSharp/BlazorWebCSharp.1/Components/Account/Pages/Manage/Email.razor:48-50` module `src.ProjectTemplates.Web.ProjectTemplates.content.BlazorWeb-CSharp.BlazorWebCSharp.1.Components.Account.Pages.Manage.Email`
- `src/ProjectTemplates/Web.ProjectTemplates/content/BlazorWeb-CSharp/BlazorWebCSharp.1/Components/Account/Pages/Register.razor:32-48` module `src.ProjectTemplates.Web.ProjectTemplates.content.BlazorWeb-CSharp.BlazorWebCSharp.1.Components.Account.Pages.Register`
- `src/ProjectTemplates/Web.ProjectTemplates/content/BlazorWeb-CSharp/BlazorWebCSharp.1/Components/Account/Pages/ResetPassword.razor:27-43` module `src.ProjectTemplates.Web.ProjectTemplates.content.BlazorWeb-CSharp.BlazorWebCSharp.1.Components.Account.Pages.ResetPassword`

## Risk Signals

- `security_sensitive` (0.74): Security-sensitive keywords changed in src/ProjectTemplates/Web.ProjectTemplates/content/BlazorWeb-CSharp/BlazorWebCSharp.1/Components/Account/Pages/Login.razor.
- `security_sensitive` (0.74): Security-sensitive keywords changed in src/ProjectTemplates/Web.ProjectTemplates/content/BlazorWeb-CSharp/BlazorWebCSharp.1/Components/Account/Pages/Manage/ChangePassword.razor.
- `security_sensitive` (0.74): Security-sensitive keywords changed in src/ProjectTemplates/Web.ProjectTemplates/content/BlazorWeb-CSharp/BlazorWebCSharp.1/Components/Account/Pages/Register.razor.
- `security_sensitive` (0.74): Security-sensitive keywords changed in src/ProjectTemplates/Web.ProjectTemplates/content/BlazorWeb-CSharp/BlazorWebCSharp.1/Components/Account/Pages/ResetPassword.razor.

## Evidence Index

- `diff:src/Components/Web/src/Forms/DisplayName.cs:1` [diff]: src/Components/Web/src/Forms/DisplayName.cs:1
- `diff:src/Components/Web/src/Forms/DisplayName.cs:10` [diff]: src/Components/Web/src/Forms/DisplayName.cs:10
- `diff:src/Components/Web/src/Forms/DisplayName.cs:11` [diff]: src/Components/Web/src/Forms/DisplayName.cs:11
- `diff:src/Components/Web/src/Forms/DisplayName.cs:12` [diff]: src/Components/Web/src/Forms/DisplayName.cs:12
- `diff:src/Components/Web/src/Forms/DisplayName.cs:13` [diff]: src/Components/Web/src/Forms/DisplayName.cs:13
- `diff:src/Components/Web/src/Forms/DisplayName.cs:14` [diff]: src/Components/Web/src/Forms/DisplayName.cs:14
- `diff:src/Components/Web/src/Forms/DisplayName.cs:15` [diff]: src/Components/Web/src/Forms/DisplayName.cs:15
- `diff:src/Components/Web/src/Forms/DisplayName.cs:16` [diff]: src/Components/Web/src/Forms/DisplayName.cs:16
- `diff:src/Components/Web/src/Forms/DisplayName.cs:17` [diff]: src/Components/Web/src/Forms/DisplayName.cs:17
- `diff:src/Components/Web/src/Forms/DisplayName.cs:18` [diff]: src/Components/Web/src/Forms/DisplayName.cs:18
- `diff:src/Components/Web/src/Forms/DisplayName.cs:19` [diff]: src/Components/Web/src/Forms/DisplayName.cs:19
- `diff:src/Components/Web/src/Forms/DisplayName.cs:2` [diff]: src/Components/Web/src/Forms/DisplayName.cs:2
- `diff:src/Components/Web/src/Forms/DisplayName.cs:20` [diff]: src/Components/Web/src/Forms/DisplayName.cs:20
- `diff:src/Components/Web/src/Forms/DisplayName.cs:21` [diff]: src/Components/Web/src/Forms/DisplayName.cs:21
- `diff:src/Components/Web/src/Forms/DisplayName.cs:22` [diff]: src/Components/Web/src/Forms/DisplayName.cs:22
- `diff:src/Components/Web/src/Forms/DisplayName.cs:23` [diff]: src/Components/Web/src/Forms/DisplayName.cs:23
- `diff:src/Components/Web/src/Forms/DisplayName.cs:24` [diff]: src/Components/Web/src/Forms/DisplayName.cs:24
- `diff:src/Components/Web/src/Forms/DisplayName.cs:25` [diff]: src/Components/Web/src/Forms/DisplayName.cs:25
- `diff:src/Components/Web/src/Forms/DisplayName.cs:26` [diff]: src/Components/Web/src/Forms/DisplayName.cs:26
- `diff:src/Components/Web/src/Forms/DisplayName.cs:27` [diff]: src/Components/Web/src/Forms/DisplayName.cs:27
- `diff:src/Components/Web/src/Forms/DisplayName.cs:28` [diff]: src/Components/Web/src/Forms/DisplayName.cs:28
- `diff:src/Components/Web/src/Forms/DisplayName.cs:29` [diff]: src/Components/Web/src/Forms/DisplayName.cs:29
- `diff:src/Components/Web/src/Forms/DisplayName.cs:3` [diff]: src/Components/Web/src/Forms/DisplayName.cs:3
- `diff:src/Components/Web/src/Forms/DisplayName.cs:30` [diff]: src/Components/Web/src/Forms/DisplayName.cs:30
- `diff:src/Components/Web/src/Forms/DisplayName.cs:31` [diff]: src/Components/Web/src/Forms/DisplayName.cs:31
- `diff:src/Components/Web/src/Forms/DisplayName.cs:32` [diff]: src/Components/Web/src/Forms/DisplayName.cs:32
- `diff:src/Components/Web/src/Forms/DisplayName.cs:33` [diff]: src/Components/Web/src/Forms/DisplayName.cs:33
- `diff:src/Components/Web/src/Forms/DisplayName.cs:34` [diff]: src/Components/Web/src/Forms/DisplayName.cs:34
- `diff:src/Components/Web/src/Forms/DisplayName.cs:35` [diff]: src/Components/Web/src/Forms/DisplayName.cs:35
- `diff:src/Components/Web/src/Forms/DisplayName.cs:36` [diff]: src/Components/Web/src/Forms/DisplayName.cs:36
- ... 532 more evidence items omitted.
