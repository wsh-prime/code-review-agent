# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 3
- Changed entities: 3
- Risk signals: 0
- Findings: 0
- Needs human review: 2
- Discarded: 0
- Agent runs: 2
- Loop enabled: True
- Target repo modified: False

## Loop Summary

| Metric | Value |
|---|---:|
| Iterations | 1 / 1 |
| Converged | False |
| Fallback | False |
| Retry count | 0 |
| Total latency | 10421 ms |
| Token in | 6451 |
| Token out | 535 |

- Iteration 0: 2 candidates, 2 verified, 2 uncertain, 0 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `risk_first_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 6186 |
| Selected evidence | 3 |
| Omitted evidence | 200 |
| Context truncated | True |
| Review shards | 1 |
| Context requests | 0 |
| Refills | 0 |

## Findings

No findings.

Checked changed files, changed entities, deterministic risk signals, and evidence references. No high-confidence review finding was produced.

## Needs Human Review

- `style` error at `src/Components/Endpoints/test/TestComponents/GenericComponent.razor:1` (0.50)
  - ReviewGuideline violation: 'Use Curly Braces for All Control Flow Statements' - The Razor file uses an inline expression `@(Value?.ToString() ?? "(null)")` which is not a control flow statement, but the file does not contain any control flow statements. No violation.
  - Suggestion: 
  - Evidence: `diff_hunk:src/Components/Endpoints/test/TestComponents/GenericComponent.razor:1`

- `style` error at `src/Components/Server/test/Circuits/ServerComponentDeserializerTest.cs:1` (0.50)
  - ReviewGuideline violation: 'Use File-Scoped Namespace Declarations' - The file changed from file-scoped namespace (`namespace Microsoft.AspNetCore.Components.Server.Circuits;`) to block-scoped namespace (`namespace Microsoft.AspNetCore.Components.Server.Circuits { ... }`), violating the guideline that requires file-scoped namespace declarations.
  - Suggestion: Revert to file-scoped namespace: `namespace Microsoft.AspNetCore.Components.Server.Circuits;` and remove the opening/closing braces.
  - Evidence: `diff_hunk:src/Components/Server/test/Circuits/ServerComponentDeserializerTest.cs:1`

## Changed Files

- `src/Components/Endpoints/test/EndpointHtmlRendererTest.cs` (modified)
- `src/Components/Endpoints/test/TestComponents/GenericComponent.razor` (added)
- `src/Components/Server/test/Circuits/ServerComponentDeserializerTest.cs` (modified)

## Changed Entities

- `src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:721-847` module `src.Components.Endpoints.test.EndpointHtmlRendererTest`
- `src/Components/Endpoints/test/TestComponents/GenericComponent.razor:1-6` module `src.Components.Endpoints.test.TestComponents.GenericComponent`
- `src/Components/Server/test/Circuits/ServerComponentDeserializerTest.cs:4-13` module `src.Components.Server.test.Circuits.ServerComponentDeserializerTest`

## Risk Signals

None.

## Evidence Index

- `diff:src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:721` [diff]: src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:721
- `diff:src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:722` [diff]: src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:722
- `diff:src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:723` [diff]: src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:723
- `diff:src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:724` [diff]: src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:724
- `diff:src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:725` [diff]: src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:725
- `diff:src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:726` [diff]: src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:726
- `diff:src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:727` [diff]: src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:727
- `diff:src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:728` [diff]: src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:728
- `diff:src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:729` [diff]: src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:729
- `diff:src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:730` [diff]: src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:730
- `diff:src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:731` [diff]: src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:731
- `diff:src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:732` [diff]: src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:732
- `diff:src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:733` [diff]: src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:733
- `diff:src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:734` [diff]: src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:734
- `diff:src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:735` [diff]: src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:735
- `diff:src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:736` [diff]: src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:736
- `diff:src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:737` [diff]: src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:737
- `diff:src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:738` [diff]: src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:738
- `diff:src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:739` [diff]: src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:739
- `diff:src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:740` [diff]: src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:740
- `diff:src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:741` [diff]: src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:741
- `diff:src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:742` [diff]: src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:742
- `diff:src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:743` [diff]: src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:743
- `diff:src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:744` [diff]: src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:744
- `diff:src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:745` [diff]: src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:745
- `diff:src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:746` [diff]: src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:746
- `diff:src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:747` [diff]: src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:747
- `diff:src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:748` [diff]: src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:748
- `diff:src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:749` [diff]: src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:749
- `diff:src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:750` [diff]: src/Components/Endpoints/test/EndpointHtmlRendererTest.cs:750
- ... 194 more evidence items omitted.
