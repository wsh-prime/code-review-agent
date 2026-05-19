# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 11
- Changed entities: 11
- Risk signals: 4
- Findings: 5
- Needs human review: 1
- Discarded: 0
- Agent runs: 5
- Loop enabled: True
- Target repo modified: False

## Loop Summary

| Metric | Value |
|---|---:|
| Iterations | 1 / 1 |
| Converged | False |
| Fallback | False |
| Retry count | 2 |
| Total latency | 218993 ms |
| Token in | 19637 |
| Token out | 1350 |

- Iteration 0: 6 candidates, 6 verified, 1 uncertain, 5 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `file_risk_shards_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 16296 |
| Selected evidence | 13 |
| Omitted evidence | 73 |
| Context truncated | True |
| Review shards | 3 |
| Context requests | 2 |
| Refills | 1 |

## Findings

- `correctness` medium at `eng/common/core-templates/steps/source-build.yml:44` (0.85)
  - The patch changes the internal runtime source feed URL from 'https://dotnetbuilds.blob.core.windows.net/internal' to 'https://ci.dot.net/internal' and adds a new '--runtimesourcefeed' argument. The diff hunk shows the new URL and argument are appended without a space separator before '--runtimesourcefeed', which may cause the shell to interpret the concatenated string incorrectly, leading to a malformed build argument.
  - Suggestion: Add a space before '--runtimesourcefeed' to ensure it is passed as a separate argument: '/p:DotNetRuntimeSourceFeed=https://ci.dot.net/internal /p:DotNetRuntimeSourceFeedKey=$(dotnetbuilds-internal-container-read-token-base64) --runtimesourcefeed http...'
  - Evidence: `diff_hunk:eng/common/core-templates/steps/source-build.yml:41`

- `best_practice` low at `eng/common/internal-feed-operations.ps1:29` (0.95)
  - The patch adds '-UseBasicParsing' to Invoke-WebRequest. While this is a good practice for environments without Internet Explorer, the evidence does not show any concrete failure scenario introduced by the change. The change is safe and improves compatibility.
  - Suggestion: No action needed; the change is acceptable.
  - Evidence: `diff_hunk:eng/common/internal-feed-operations.ps1:26`

- `best_practice` low at `eng/common/post-build/nuget-verification.ps1:68` (0.95)
  - The patch adds '-UseBasicParsing' to Invoke-WebRequest. This is a safe improvement for environments without Internet Explorer. No concrete failure scenario is introduced.
  - Suggestion: No action needed; the change is acceptable.
  - Evidence: `diff_hunk:eng/common/post-build/nuget-verification.ps1:65`

- `best_practice` low at `eng/common/tools.ps1:269` (0.95)
  - The patch adds '-UseBasicParsing' to Invoke-WebRequest. This is a safe improvement for environments without Internet Explorer. No concrete failure scenario is introduced.
  - Suggestion: No action needed; the change is acceptable.
  - Evidence: `diff_hunk:eng/common/tools.ps1:266`

- `security` high at `eng/common/core-templates/steps/source-build.yml:44` (0.74)
  - The patch changes the internal runtime download feed URL from 'https://dotnetbuilds.blob.core.windows.net/internal' to 'https://ci.dot.net/internal' and adds a new '--runtimesourcefeed' argument with an HTTP URL. This introduces a potential security risk if the new feed or the HTTP source feed is untrusted or if the change bypasses existing access controls, as the internal feed key is still passed as a query parameter.
  - Suggestion: Verify that the new feed URL 'https://ci.dot.net/internal' is authorized and that the added '--runtimesourcefeed http...' argument does not expose the internal feed key or allow redirection to an untrusted source. Consider using HTTPS for all runtime source feeds and validate the feed's integrity.
  - Evidence: `diff_hunk:eng/common/core-templates/steps/source-build.yml:41`, `diff:eng/common/core-templates/steps/source-build.yml:44`, `risk:security_sensitive:eng/common/core-templates/steps/source-build.yml`

## Needs Human Review

- `maintainability` medium at `src/Components/test/E2ETest/ServerExecutionTests/WebSocketCompressionTests.cs:107` (0.50)
  - Test class naming does not follow the required convention: class names must end with 'Test' or 'Tests' suffix. The class 'DefaultConfigurationWebSocketCompressionTests' is defined in this file but the changed class 'WebSocketCompressionTests' is not shown in the diff hunk. However, the file is a test file and the class name appears to end with 'Tests', so no violation is present. No issue.
  - Suggestion: 
  - Evidence: `diff_hunk:src/Components/test/E2ETest/ServerExecutionTests/WebSocketCompressionTests.cs:104`

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
