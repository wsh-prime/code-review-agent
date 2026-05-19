# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 6
- Changed entities: 6
- Risk signals: 0
- Findings: 0
- Needs human review: 1
- Discarded: 3
- Agent runs: 4
- Loop enabled: True
- Target repo modified: False

## Loop Summary

| Metric | Value |
|---|---:|
| Iterations | 1 / 1 |
| Converged | False |
| Fallback | False |
| Retry count | 1 |
| Total latency | 130365 ms |
| Token in | 14326 |
| Token out | 972 |

- Iteration 0: 4 candidates, 1 verified, 1 uncertain, 0 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `file_risk_shards_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 12283 |
| Selected evidence | 8 |
| Omitted evidence | 95 |
| Context truncated | True |
| Review shards | 2 |
| Context requests | 2 |
| Refills | 1 |

## Findings

No findings.

Checked changed files, changed entities, deterministic risk signals, and evidence references. No high-confidence review finding was produced.

## Needs Human Review

- `correctness` high at `src/Components/test/E2ETest/Tests/StatePersistanceJSRootTest.cs:1` (0.50)
  - Test class 'StatePersistanceJSRootTest' is deleted but its test logic is moved to 'StatePersistenceTest' without verifying that the new test method covers the same scenarios. The deleted test used a server fixture with '--RegisterDynamicJSRootComponent' argument, which is not present in the new test.
  - Suggestion: Ensure the new test method 'PersistentStateIsSupportedInDynamicJSRoots' in 'StatePersistenceTest.cs' includes the necessary server fixture configuration (e.g., '--RegisterDynamicJSRootComponent') to replicate the original test's setup.
  - Evidence: `diff_hunk:src/Components/test/E2ETest/Tests/StatePersistanceJSRootTest.cs:1`, `diff_hunk:src/Components/test/E2ETest/Tests/StatePersistenceTest.cs:276`

## Changed Files

- `src/Components/Web.JS/src/Rendering/JSRootComponents.ts` (modified)
- `src/Components/Web.JS/src/Rendering/WebRendererInteropMethods.ts` (modified)
- `src/Components/test/E2ETest/Tests/StatePersistanceJSRootTest.cs` (deleted)
- `src/Components/test/E2ETest/Tests/StatePersistenceTest.cs` (modified)
- `src/Components/test/testassets/Components.TestServer/Program.cs` (modified)
- `src/Components/test/testassets/Components.TestServer/RazorComponentEndpointsStartup.cs` (modified)

## Changed Entities

- `src/Components/Web.JS/src/Rendering/JSRootComponents.ts:13-15` module `src.Components.Web.JS.src.Rendering.JSRootComponents`
- `src/Components/Web.JS/src/Rendering/WebRendererInteropMethods.ts:34-34` module `src.Components.Web.JS.src.Rendering.WebRendererInteropMethods`
- `src/Components/test/E2ETest/Tests/StatePersistanceJSRootTest.cs:1-42` module `src.Components.test.E2ETest.Tests.StatePersistanceJSRootTest`
- `src/Components/test/E2ETest/Tests/StatePersistenceTest.cs:279-292` module `src.Components.test.E2ETest.Tests.StatePersistenceTest`
- `src/Components/test/testassets/Components.TestServer/Program.cs:27-27` module `src.Components.test.testassets.Components.TestServer.Program`
- `src/Components/test/testassets/Components.TestServer/RazorComponentEndpointsStartup.cs:54-57` module `src.Components.test.testassets.Components.TestServer.RazorComponentEndpointsStartup`

## Risk Signals

None.

## Evidence Index

- `diff:src/Components/Web.JS/src/Rendering/JSRootComponents.ts:121` [diff]: src/Components/Web.JS/src/Rendering/JSRootComponents.ts:121
- `diff:src/Components/Web.JS/src/Rendering/JSRootComponents.ts:123` [diff]: src/Components/Web.JS/src/Rendering/JSRootComponents.ts:123
- `diff:src/Components/Web.JS/src/Rendering/JSRootComponents.ts:124` [diff]: src/Components/Web.JS/src/Rendering/JSRootComponents.ts:124
- `diff:src/Components/Web.JS/src/Rendering/JSRootComponents.ts:125` [diff]: src/Components/Web.JS/src/Rendering/JSRootComponents.ts:125
- `diff:src/Components/Web.JS/src/Rendering/JSRootComponents.ts:126` [diff]: src/Components/Web.JS/src/Rendering/JSRootComponents.ts:126
- `diff:src/Components/Web.JS/src/Rendering/JSRootComponents.ts:127` [diff]: src/Components/Web.JS/src/Rendering/JSRootComponents.ts:127
- `diff:src/Components/Web.JS/src/Rendering/JSRootComponents.ts:128` [diff]: src/Components/Web.JS/src/Rendering/JSRootComponents.ts:128
- `diff:src/Components/Web.JS/src/Rendering/JSRootComponents.ts:13` [diff]: src/Components/Web.JS/src/Rendering/JSRootComponents.ts:13
- `diff:src/Components/Web.JS/src/Rendering/JSRootComponents.ts:130` [diff]: src/Components/Web.JS/src/Rendering/JSRootComponents.ts:130
- `diff:src/Components/Web.JS/src/Rendering/JSRootComponents.ts:131` [diff]: src/Components/Web.JS/src/Rendering/JSRootComponents.ts:131
- `diff:src/Components/Web.JS/src/Rendering/JSRootComponents.ts:132` [diff]: src/Components/Web.JS/src/Rendering/JSRootComponents.ts:132
- `diff:src/Components/Web.JS/src/Rendering/JSRootComponents.ts:133` [diff]: src/Components/Web.JS/src/Rendering/JSRootComponents.ts:133
- `diff:src/Components/Web.JS/src/Rendering/JSRootComponents.ts:134` [diff]: src/Components/Web.JS/src/Rendering/JSRootComponents.ts:134
- `diff:src/Components/Web.JS/src/Rendering/JSRootComponents.ts:135` [diff]: src/Components/Web.JS/src/Rendering/JSRootComponents.ts:135
- `diff:src/Components/Web.JS/src/Rendering/JSRootComponents.ts:136` [diff]: src/Components/Web.JS/src/Rendering/JSRootComponents.ts:136
- `diff:src/Components/Web.JS/src/Rendering/JSRootComponents.ts:137` [diff]: src/Components/Web.JS/src/Rendering/JSRootComponents.ts:137
- `diff:src/Components/Web.JS/src/Rendering/JSRootComponents.ts:138` [diff]: src/Components/Web.JS/src/Rendering/JSRootComponents.ts:138
- `diff:src/Components/Web.JS/src/Rendering/JSRootComponents.ts:139` [diff]: src/Components/Web.JS/src/Rendering/JSRootComponents.ts:139
- `diff:src/Components/Web.JS/src/Rendering/JSRootComponents.ts:140` [diff]: src/Components/Web.JS/src/Rendering/JSRootComponents.ts:140
- `diff:src/Components/Web.JS/src/Rendering/JSRootComponents.ts:141` [diff]: src/Components/Web.JS/src/Rendering/JSRootComponents.ts:141
- `diff:src/Components/Web.JS/src/Rendering/JSRootComponents.ts:142` [diff]: src/Components/Web.JS/src/Rendering/JSRootComponents.ts:142
- `diff:src/Components/Web.JS/src/Rendering/JSRootComponents.ts:143` [diff]: src/Components/Web.JS/src/Rendering/JSRootComponents.ts:143
- `diff:src/Components/Web.JS/src/Rendering/JSRootComponents.ts:144` [diff]: src/Components/Web.JS/src/Rendering/JSRootComponents.ts:144
- `diff:src/Components/Web.JS/src/Rendering/JSRootComponents.ts:145` [diff]: src/Components/Web.JS/src/Rendering/JSRootComponents.ts:145
- `diff:src/Components/Web.JS/src/Rendering/JSRootComponents.ts:146` [diff]: src/Components/Web.JS/src/Rendering/JSRootComponents.ts:146
- `diff:src/Components/Web.JS/src/Rendering/JSRootComponents.ts:148` [diff]: src/Components/Web.JS/src/Rendering/JSRootComponents.ts:148
- `diff:src/Components/Web.JS/src/Rendering/JSRootComponents.ts:149` [diff]: src/Components/Web.JS/src/Rendering/JSRootComponents.ts:149
- `diff:src/Components/Web.JS/src/Rendering/JSRootComponents.ts:15` [diff]: src/Components/Web.JS/src/Rendering/JSRootComponents.ts:15
- `diff:src/Components/Web.JS/src/Rendering/WebRendererInteropMethods.ts:34` [diff]: src/Components/Web.JS/src/Rendering/WebRendererInteropMethods.ts:34
- `diff:src/Components/test/E2ETest/Tests/StatePersistanceJSRootTest.cs:1` [diff]: src/Components/test/E2ETest/Tests/StatePersistanceJSRootTest.cs:1
- ... 73 more evidence items omitted.
