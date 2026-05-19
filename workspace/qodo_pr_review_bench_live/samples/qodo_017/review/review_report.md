# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 3
- Changed entities: 3
- Risk signals: 0
- Findings: 0
- Needs human review: 0
- Discarded: 0
- Agent runs: 3
- Loop enabled: True
- Target repo modified: False

## Loop Summary

| Metric | Value |
|---|---:|
| Iterations | 1 / 1 |
| Converged | True |
| Fallback | False |
| Retry count | 0 |
| Total latency | 12148 ms |
| Token in | 6734 |
| Token out | 172 |

- Iteration 0: 0 candidates, 0 verified, 0 uncertain, 0 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `file_risk_shards_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 5227 |
| Selected evidence | 5 |
| Omitted evidence | 198 |
| Context truncated | True |
| Review shards | 1 |
| Context requests | 1 |
| Refills | 1 |

## Findings

No findings.

Checked changed files, changed entities, deterministic risk signals, and evidence references. No high-confidence review finding was produced.

## Needs Human Review

None.

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
