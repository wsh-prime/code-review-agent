# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 11
- Changed entities: 11
- Risk signals: 2
- Findings: 1
- Needs human review: 4
- Discarded: 0
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
| Total latency | 111357 ms |
| Token in | 18188 |
| Token out | 869 |

- Iteration 0: 4 candidates, 4 verified, 4 uncertain, 0 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `file_risk_shards_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 16448 |
| Selected evidence | 11 |
| Omitted evidence | 278 |
| Context truncated | True |
| Review shards | 3 |
| Context requests | 0 |
| Refills | 0 |

## Findings

- `experiment_artifact` medium at `src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/snapshots/OperationTests.SupportsRouteParametersFromControllers#OpenApiXmlCommentSupport.generated.verified.cs:1` (0.78)
  - A process or experiment artifact appears to have been added to mainline code.
  - Suggestion: Move the artifact under a dedicated experiments, scripts, or docs area before merging.
  - Evidence: `diff:src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/snapshots/OperationTests.SupportsRouteParametersFromControllers#OpenApiXmlCommentSupport.generated.verified.cs:1`, `diff:src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/snapshots/OperationTests.SupportsRouteParametersFromControllers#OpenApiXmlCommentSupport.generated.verified.cs:10`, `diff:src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/snapshots/OperationTests.SupportsRouteParametersFromControllers#OpenApiXmlCommentSupport.generated.verified.cs:100`, `diff:src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/snapshots/OperationTests.SupportsRouteParametersFromControllers#OpenApiXmlCommentSupport.generated.verified.cs:101`, `diff:src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/snapshots/OperationTests.SupportsRouteParametersFromControllers#OpenApiXmlCommentSupport.generated.verified.cs:102`, `diff:src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/snapshots/OperationTests.SupportsRouteParametersFromControllers#OpenApiXmlCommentSupport.generated.verified.cs:103`, `diff:src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/snapshots/OperationTests.SupportsRouteParametersFromControllers#OpenApiXmlCommentSupport.generated.verified.cs:104`, `diff:src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/snapshots/OperationTests.SupportsRouteParametersFromControllers#OpenApiXmlCommentSupport.generated.verified.cs:105`, `diff:src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/snapshots/OperationTests.SupportsRouteParametersFromControllers#OpenApiXmlCommentSupport.generated.verified.cs:106`, `diff:src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/snapshots/OperationTests.SupportsRouteParametersFromControllers#OpenApiXmlCommentSupport.generated.verified.cs:107`, ... 3 more

## Needs Human Review

- `maintainability` low at `src/OpenApi/gen/XmlCommentGenerator.Emitter.cs:1` (0.50)
  - Removal of the MIT license header from the source file may cause licensing compliance issues if the project requires a license notice in every file.
  - Suggestion: Restore the license header or ensure the project's licensing policy allows omission of per-file headers.
  - Evidence: `diff_hunk:src/OpenApi/gen/XmlCommentGenerator.Emitter.cs:1`

- `correctness` medium at `src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/snapshots/CompletenessTests.SupportsAllXmlTagsOnSchemas#OpenApiXmlCommentSupport.generated.verified.cs:556` (0.50)
  - Adding a null check for `metadata` before accessing `MetadataKind` may change behavior when `metadata` is null. Previously, a null reference exception would occur; now the condition silently skips the parameter, potentially omitting XML comments for parameters with null metadata.
  - Suggestion: Ensure that skipping parameters with null metadata is the intended behavior and does not lead to missing XML documentation for valid parameters.
  - Evidence: `diff_hunk:src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/snapshots/CompletenessTests.SupportsAllXmlTagsOnSchemas#OpenApiXmlCommentSupport.generated.verified.cs:553`

- `correctness` medium at `src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/snapshots/OperationTests.SupportsXmlCommentsOnOperationsFromControllers#OpenApiXmlCommentSupport.generated.verified.cs:433` (0.50)
  - Adding a null check for `metadata` before accessing `MetadataKind` may change behavior when `metadata` is null. Previously, a null reference exception would occur; now the condition silently skips the parameter, potentially omitting XML comments for parameters with null metadata.
  - Suggestion: Ensure that skipping parameters with null metadata is the intended behavior and does not lead to missing XML documentation for valid parameters.
  - Evidence: `diff_hunk:src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/snapshots/OperationTests.SupportsXmlCommentsOnOperationsFromControllers#OpenApiXmlCommentSupport.generated.verified.cs:430`

- `correctness` medium at `src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/snapshots/OperationTests.SupportsXmlCommentsOnOperationsFromMinimalApis#OpenApiXmlCommentSupport.generated.verified.cs:477` (0.50)
  - Adding a null check for `metadata` before accessing `MetadataKind` may change behavior when `metadata` is null. Previously, a null reference exception would occur; now the condition silently skips the parameter, potentially omitting XML comments for parameters with null metadata.
  - Suggestion: Ensure that skipping parameters with null metadata is the intended behavior and does not lead to missing XML documentation for valid parameters.
  - Evidence: `diff_hunk:src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/snapshots/OperationTests.SupportsXmlCommentsOnOperationsFromMinimalApis#OpenApiXmlCommentSupport.generated.verified.cs:474`

## Changed Files

- `src/OpenApi/gen/XmlCommentGenerator.Emitter.cs` (modified)
- `src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/OperationTests.Controllers.cs` (modified)
- `src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/snapshots/AddOpenApiTests.CanInterceptAddOpenApi#OpenApiXmlCommentSupport.generated.verified.cs` (modified)
- `src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/snapshots/AdditionalTextsTests.CanHandleXmlForSchemasInAdditionalTexts#OpenApiXmlCommentSupport.generated.verified.cs` (modified)
- `src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/snapshots/CompletenessTests.SupportsAllXmlTagsOnSchemas#OpenApiXmlCommentSupport.generated.verified.cs` (modified)
- `src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/snapshots/OperationTests.SupportsRouteParametersFromControllers#OpenApiXmlCommentSupport.generated.verified.cs` (added)
- `src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/snapshots/OperationTests.SupportsXmlCommentsOnOperationsFromControllers#OpenApiXmlCommentSupport.generated.verified.cs` (modified)
- `src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/snapshots/OperationTests.SupportsXmlCommentsOnOperationsFromMinimalApis#OpenApiXmlCommentSupport.generated.verified.cs` (modified)
- `src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/snapshots/SchemaTests.SupportsXmlCommentsOnSchemas#OpenApiXmlCommentSupport.generated.verified.cs` (modified)
- `src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/snapshots/SchemaTests.XmlCommentsOnPropertiesShouldApplyToSchemaReferences#OpenApiXmlCommentSupport.generated.verified.cs` (modified)
- `src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/snapshots/XmlCommentDocumentationIdTests.CanMergeXmlCommentsWithDifferentDocumentationIdFormats#OpenApiXmlCommentSupport.generated.verified.cs` (modified)

## Changed Entities

- `src/OpenApi/gen/XmlCommentGenerator.Emitter.cs:1-3` module `src.OpenApi.gen.XmlCommentGenerator.Emitter`
- `src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/OperationTests.Controllers.cs:99-143` module `src.OpenApi.test.Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests.OperationTests.Controllers`
- `src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/snapshots/AddOpenApiTests.CanInterceptAddOpenApi#OpenApiXmlCommentSupport.generated.verified.cs:429-430` module `src.OpenApi.test.Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests.snapshots.AddOpenApiTests.CanInterceptAddOpenApi#OpenApiXmlCommentSupport.generated.verified`
- `src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/snapshots/AdditionalTextsTests.CanHandleXmlForSchemasInAdditionalTexts#OpenApiXmlCommentSupport.generated.verified.cs:458-459` module `src.OpenApi.test.Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests.snapshots.AdditionalTextsTests.CanHandleXmlForSchemasInAdditionalTexts#OpenApiXmlCommentSupport.generated.verified`
- `src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/snapshots/CompletenessTests.SupportsAllXmlTagsOnSchemas#OpenApiXmlCommentSupport.generated.verified.cs:556-557` module `src.OpenApi.test.Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests.snapshots.CompletenessTests.SupportsAllXmlTagsOnSchemas#OpenApiXmlCommentSupport.generated.verified`
- `src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/snapshots/OperationTests.SupportsRouteParametersFromControllers#OpenApiXmlCommentSupport.generated.verified.cs:1-610` module `src.OpenApi.test.Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests.snapshots.OperationTests.SupportsRouteParametersFromControllers#OpenApiXmlCommentSupport.generated.verified`
- `src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/snapshots/OperationTests.SupportsXmlCommentsOnOperationsFromControllers#OpenApiXmlCommentSupport.generated.verified.cs:433-434` module `src.OpenApi.test.Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests.snapshots.OperationTests.SupportsXmlCommentsOnOperationsFromControllers#OpenApiXmlCommentSupport.generated.verified`
- `src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/snapshots/OperationTests.SupportsXmlCommentsOnOperationsFromMinimalApis#OpenApiXmlCommentSupport.generated.verified.cs:477-478` module `src.OpenApi.test.Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests.snapshots.OperationTests.SupportsXmlCommentsOnOperationsFromMinimalApis#OpenApiXmlCommentSupport.generated.verified`
- `src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/snapshots/SchemaTests.SupportsXmlCommentsOnSchemas#OpenApiXmlCommentSupport.generated.verified.cs:459-460` module `src.OpenApi.test.Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests.snapshots.SchemaTests.SupportsXmlCommentsOnSchemas#OpenApiXmlCommentSupport.generated.verified`
- `src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/snapshots/SchemaTests.XmlCommentsOnPropertiesShouldApplyToSchemaReferences#OpenApiXmlCommentSupport.generated.verified.cs:438-439` module `src.OpenApi.test.Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests.snapshots.SchemaTests.XmlCommentsOnPropertiesShouldApplyToSchemaReferences#OpenApiXmlCommentSupport.generated.verified`
- `src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/snapshots/XmlCommentDocumentationIdTests.CanMergeXmlCommentsWithDifferentDocumentationIdFormats#OpenApiXmlCommentSupport.generated.verified.cs:430-431` module `src.OpenApi.test.Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests.snapshots.XmlCommentDocumentationIdTests.CanMergeXmlCommentsWithDifferentDocumentationIdFormats#OpenApiXmlCommentSupport.generated.verified`

## Risk Signals

- `experiment_artifact` (0.78): New file looks like a process or experiment artifact: src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/snapshots/OperationTests.SupportsRouteParametersFromControllers#OpenApiXmlCommentSupport.generated.verified.cs.
- `security_sensitive` (0.74): Security-sensitive keywords changed in src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/snapshots/OperationTests.SupportsRouteParametersFromControllers#OpenApiXmlCommentSupport.generated.verified.cs.

## Evidence Index

- `diff:src/OpenApi/gen/XmlCommentGenerator.Emitter.cs:1` [diff]: src/OpenApi/gen/XmlCommentGenerator.Emitter.cs:1
- `diff:src/OpenApi/gen/XmlCommentGenerator.Emitter.cs:2` [diff]: src/OpenApi/gen/XmlCommentGenerator.Emitter.cs:2
- `diff:src/OpenApi/gen/XmlCommentGenerator.Emitter.cs:3` [diff]: src/OpenApi/gen/XmlCommentGenerator.Emitter.cs:3
- `diff:src/OpenApi/gen/XmlCommentGenerator.Emitter.cs:382` [diff]: src/OpenApi/gen/XmlCommentGenerator.Emitter.cs:382
- `diff:src/OpenApi/gen/XmlCommentGenerator.Emitter.cs:385` [diff]: src/OpenApi/gen/XmlCommentGenerator.Emitter.cs:385
- `diff:src/OpenApi/gen/XmlCommentGenerator.Emitter.cs:444` [diff]: src/OpenApi/gen/XmlCommentGenerator.Emitter.cs:444
- `diff:src/OpenApi/gen/XmlCommentGenerator.Emitter.cs:445` [diff]: src/OpenApi/gen/XmlCommentGenerator.Emitter.cs:445
- `diff:src/OpenApi/gen/XmlCommentGenerator.Emitter.cs:447` [diff]: src/OpenApi/gen/XmlCommentGenerator.Emitter.cs:447
- `diff:src/OpenApi/gen/XmlCommentGenerator.Emitter.cs:452` [diff]: src/OpenApi/gen/XmlCommentGenerator.Emitter.cs:452
- `diff:src/OpenApi/gen/XmlCommentGenerator.Emitter.cs:454` [diff]: src/OpenApi/gen/XmlCommentGenerator.Emitter.cs:454
- `diff:src/OpenApi/gen/XmlCommentGenerator.Emitter.cs:468` [diff]: src/OpenApi/gen/XmlCommentGenerator.Emitter.cs:468
- `diff:src/OpenApi/gen/XmlCommentGenerator.Emitter.cs:479` [diff]: src/OpenApi/gen/XmlCommentGenerator.Emitter.cs:479
- `diff:src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/OperationTests.Controllers.cs:100` [diff]: src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/OperationTests.Controllers.cs:100
- `diff:src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/OperationTests.Controllers.cs:101` [diff]: src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/OperationTests.Controllers.cs:101
- `diff:src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/OperationTests.Controllers.cs:102` [diff]: src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/OperationTests.Controllers.cs:102
- `diff:src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/OperationTests.Controllers.cs:103` [diff]: src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/OperationTests.Controllers.cs:103
- `diff:src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/OperationTests.Controllers.cs:104` [diff]: src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/OperationTests.Controllers.cs:104
- `diff:src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/OperationTests.Controllers.cs:105` [diff]: src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/OperationTests.Controllers.cs:105
- `diff:src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/OperationTests.Controllers.cs:106` [diff]: src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/OperationTests.Controllers.cs:106
- `diff:src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/OperationTests.Controllers.cs:107` [diff]: src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/OperationTests.Controllers.cs:107
- `diff:src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/OperationTests.Controllers.cs:108` [diff]: src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/OperationTests.Controllers.cs:108
- `diff:src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/OperationTests.Controllers.cs:109` [diff]: src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/OperationTests.Controllers.cs:109
- `diff:src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/OperationTests.Controllers.cs:110` [diff]: src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/OperationTests.Controllers.cs:110
- `diff:src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/OperationTests.Controllers.cs:111` [diff]: src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/OperationTests.Controllers.cs:111
- `diff:src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/OperationTests.Controllers.cs:112` [diff]: src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/OperationTests.Controllers.cs:112
- `diff:src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/OperationTests.Controllers.cs:113` [diff]: src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/OperationTests.Controllers.cs:113
- `diff:src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/OperationTests.Controllers.cs:114` [diff]: src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/OperationTests.Controllers.cs:114
- `diff:src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/OperationTests.Controllers.cs:115` [diff]: src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/OperationTests.Controllers.cs:115
- `diff:src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/OperationTests.Controllers.cs:116` [diff]: src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/OperationTests.Controllers.cs:116
- `diff:src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/OperationTests.Controllers.cs:117` [diff]: src/OpenApi/test/Microsoft.AspNetCore.OpenApi.SourceGenerators.Tests/OperationTests.Controllers.cs:117
- ... 681 more evidence items omitted.
