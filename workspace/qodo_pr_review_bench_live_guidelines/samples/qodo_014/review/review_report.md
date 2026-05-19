# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 11
- Changed entities: 11
- Risk signals: 4
- Findings: 0
- Needs human review: 2
- Discarded: 2
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
| Total latency | 163433 ms |
| Token in | 17859 |
| Token out | 777 |

- Iteration 0: 4 candidates, 2 verified, 2 uncertain, 0 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `file_risk_shards_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 15867 |
| Selected evidence | 11 |
| Omitted evidence | 75 |
| Context truncated | True |
| Review shards | 3 |
| Context requests | 0 |
| Refills | 0 |

## Findings

No findings.

Checked changed files, changed entities, deterministic risk signals, and evidence references. No high-confidence review finding was produced.

## Needs Human Review

- `maintainability` medium at `src/Components/test/E2ETest/ServerExecutionTests/WebSocketCompressionTests.cs:107` (0.50)
  - Test method EmbeddingServerAppInsideIframe_WithCompressionEnabled_Fails lacks explicit // Arrange, // Act, and // Assert comments as required by the 'Test Methods Must Use Arrange-Act-Assert Pattern with Comments' guideline.
  - Suggestion: Add // Arrange, // Act, and // Assert comments to clearly delineate the three phases of the test.
  - Evidence: `diff_hunk:src/Components/test/E2ETest/ServerExecutionTests/WebSocketCompressionTests.cs:104`

- `maintainability` medium at `src/SignalR/server/StackExchangeRedis/test/RedisEndToEnd.cs:92` (0.50)
  - Test method CanSendAndReceiveUserMessagesFromMultipleConnectionsWithSameUser lacks explicit // Arrange, // Act, and // Assert comments as required by the 'Test Methods Must Use Arrange-Act-Assert Pattern with Comments' guideline.
  - Suggestion: Add // Arrange, // Act, and // Assert comments to clearly delineate the three phases of the test.
  - Evidence: `diff_hunk:src/SignalR/server/StackExchangeRedis/test/RedisEndToEnd.cs:89`

## Changed Files

- `eng/Version.Details.xml` (modified)
- `eng/Versions.props` (modified)
- `eng/common/core-templates/job/source-build.yml` (modified)
- `eng/common/core-templates/job/source-index-stage1.yml` (modified)
- `eng/common/core-templates/steps/source-build.yml` (modified)
- `eng/common/internal-feed-operations.ps1` (modified)
- `eng/common/post-build/nuget-verification.ps1` (modified)
- `eng/common/tools.ps1` (modified)
- `global.json` (modified)
- `src/Components/test/E2ETest/ServerExecutionTests/WebSocketCompressionTests.cs` (modified)
- `src/SignalR/server/StackExchangeRedis/test/RedisEndToEnd.cs` (modified)

## Changed Entities

- `eng/Version.Details.xml:391-415` module `eng.Version.Details`
- `eng/Versions.props:169-172` module `eng.Versions`
- `eng/common/core-templates/job/source-build.yml:68-68` module `eng.common.core-templates.job.source-build`
- `eng/common/core-templates/job/source-index-stage1.yml:9-9` module `eng.common.core-templates.job.source-index-stage1`
- `eng/common/core-templates/steps/source-build.yml:44-44` module `eng.common.core-templates.steps.source-build`
- `eng/common/internal-feed-operations.ps1:29-29` module `eng.common.internal-feed-operations`
- `eng/common/post-build/nuget-verification.ps1:68-68` module `eng.common.post-build.nuget-verification`
- `eng/common/tools.ps1:269-269` module `eng.common.tools`
- `global.json:30-31` module `global`
- `src/Components/test/E2ETest/ServerExecutionTests/WebSocketCompressionTests.cs:107-117` module `src.Components.test.E2ETest.ServerExecutionTests.WebSocketCompressionTests`
- `src/SignalR/server/StackExchangeRedis/test/RedisEndToEnd.cs:92-92` module `src.SignalR.server.StackExchangeRedis.test.RedisEndToEnd`

## Risk Signals

- `config_change` (0.86): Configuration file changed: eng/common/core-templates/job/source-build.yml.
- `config_change` (0.86): Configuration file changed: eng/common/core-templates/job/source-index-stage1.yml.
- `config_change` (0.86): Configuration file changed: eng/common/core-templates/steps/source-build.yml.
- `security_sensitive` (0.74): Security-sensitive keywords changed in eng/common/core-templates/steps/source-build.yml.

## Evidence Index

- `diff:eng/Version.Details.xml:391` [diff]: eng/Version.Details.xml:391
- `diff:eng/Version.Details.xml:393` [diff]: eng/Version.Details.xml:393
- `diff:eng/Version.Details.xml:396` [diff]: eng/Version.Details.xml:396
- `diff:eng/Version.Details.xml:398` [diff]: eng/Version.Details.xml:398
- `diff:eng/Version.Details.xml:401` [diff]: eng/Version.Details.xml:401
- `diff:eng/Version.Details.xml:403` [diff]: eng/Version.Details.xml:403
- `diff:eng/Version.Details.xml:405` [diff]: eng/Version.Details.xml:405
- `diff:eng/Version.Details.xml:407` [diff]: eng/Version.Details.xml:407
- `diff:eng/Version.Details.xml:409` [diff]: eng/Version.Details.xml:409
- `diff:eng/Version.Details.xml:411` [diff]: eng/Version.Details.xml:411
- `diff:eng/Version.Details.xml:413` [diff]: eng/Version.Details.xml:413
- `diff:eng/Version.Details.xml:415` [diff]: eng/Version.Details.xml:415
- `diff:eng/Versions.props:169` [diff]: eng/Versions.props:169
- `diff:eng/Versions.props:170` [diff]: eng/Versions.props:170
- `diff:eng/Versions.props:171` [diff]: eng/Versions.props:171
- `diff:eng/Versions.props:172` [diff]: eng/Versions.props:172
- `diff:eng/common/core-templates/job/source-build.yml:68` [diff]: eng/common/core-templates/job/source-build.yml:68
- `diff:eng/common/core-templates/job/source-index-stage1.yml:9` [diff]: eng/common/core-templates/job/source-index-stage1.yml:9
- `diff:eng/common/core-templates/steps/source-build.yml:44` [diff]: eng/common/core-templates/steps/source-build.yml:44
- `diff:eng/common/internal-feed-operations.ps1:29` [diff]: eng/common/internal-feed-operations.ps1:29
- `diff:eng/common/post-build/nuget-verification.ps1:68` [diff]: eng/common/post-build/nuget-verification.ps1:68
- `diff:eng/common/tools.ps1:269` [diff]: eng/common/tools.ps1:269
- `diff:eng/common/tools.ps1:502` [diff]: eng/common/tools.ps1:502
- `diff:eng/common/tools.ps1:546` [diff]: eng/common/tools.ps1:546
- `diff:eng/common/tools.ps1:550` [diff]: eng/common/tools.ps1:550
- `diff:eng/common/tools.ps1:551` [diff]: eng/common/tools.ps1:551
- `diff:eng/common/tools.ps1:552` [diff]: eng/common/tools.ps1:552
- `diff:eng/common/tools.ps1:553` [diff]: eng/common/tools.ps1:553
- `diff:eng/common/tools.ps1:554` [diff]: eng/common/tools.ps1:554
- `diff:eng/common/tools.ps1:555` [diff]: eng/common/tools.ps1:555
- ... 56 more evidence items omitted.
