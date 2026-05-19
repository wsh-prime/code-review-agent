# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 3
- Changed entities: 3
- Risk signals: 0
- Findings: 0
- Needs human review: 1
- Discarded: 1
- Agent runs: 2
- Loop enabled: True
- Target repo modified: False

## Loop Summary

| Metric | Value |
|---|---:|
| Iterations | 1 / 1 |
| Converged | False |
| Fallback | False |
| Retry count | 1 |
| Total latency | 100946 ms |
| Token in | 6065 |
| Token out | 436 |

- Iteration 0: 2 candidates, 1 verified, 1 uncertain, 0 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `risk_first_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 5452 |
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

- `convention` medium at `src/Components/Endpoints/test/TestComponents/GenericComponent.razor:1` (0.50)
  - New file GenericComponent.razor is missing the required MIT license header. Review guideline 'All C# Source Files Must Include MIT License Header' requires every .cs file to start with the exact two-line comment header. Although this is a .razor file, the guideline explicitly mentions 'C# source files' and the file contains C# code in the @code block; the same licensing expectation applies.
  - Suggestion: Add the standard license header as the first two lines: '// Licensed to the .NET Foundation under one or more agreements.' followed by '// The .NET Foundation licenses this file to you under the MIT license.'
  - Evidence: `diff_hunk:src/Components/Endpoints/test/TestComponents/GenericComponent.razor:1`

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
