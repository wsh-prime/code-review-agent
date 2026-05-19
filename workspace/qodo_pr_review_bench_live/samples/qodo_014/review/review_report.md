# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 11
- Changed entities: 11
- Risk signals: 4
- Findings: 2
- Needs human review: 4
- Discarded: 2
- Agent runs: 6
- Loop enabled: True
- Target repo modified: False

## Loop Summary

| Metric | Value |
|---|---:|
| Iterations | 1 / 1 |
| Converged | False |
| Fallback | False |
| Retry count | 0 |
| Total latency | 71178 ms |
| Token in | 15226 |
| Token out | 1692 |

- Iteration 0: 8 candidates, 6 verified, 4 uncertain, 2 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `file_risk_shards_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 10101 |
| Selected evidence | 15 |
| Omitted evidence | 71 |
| Context truncated | True |
| Review shards | 3 |
| Context requests | 5 |
| Refills | 2 |

## Findings

- `potential_regression` high at `eng/common/core-templates/job/source-index-stage1.yml:9` (0.85)
  - The condition for the source-index-stage1 job is changed from always running (empty string) to only running on the main branch. This will prevent source indexing from running on non-main branches, which may be intentional but could break CI workflows that depend on source indexing for all branches.
  - Suggestion: If source indexing is needed for all branches, revert the condition to empty string. Otherwise, ensure that all dependent pipelines are aware of this change.
  - Evidence: `diff_hunk:eng/common/core-templates/job/source-index-stage1.yml:6`

- `compatibility` medium at `eng/common/core-templates/job/source-build.yml:68` (0.70)
  - The build image is changed from '1es-mariner-2' to '1es-azurelinux-3'. This may introduce breaking changes if the new image has different tooling, dependencies, or environment variables. The patch does not show any corresponding adjustments to the build steps or scripts.
  - Suggestion: Verify that the new image '1es-azurelinux-3' is compatible with all build steps and scripts used in this job. Update any environment-specific commands or paths if necessary.
  - Evidence: `diff_hunk:eng/common/core-templates/job/source-build.yml:65`

## Needs Human Review

- `compatibility` low at `eng/common/internal-feed-operations.ps1:29` (0.50)
  - Adding '-UseBasicParsing' to Invoke-WebRequest may change the response object type (e.g., no HtmlWebResponseObject), which could break downstream code that expects the default parsing behavior.
  - Suggestion: Ensure that no code downstream relies on the Internet Explorer engine's HTML parsing (e.g., accessing .Links, .Images, or .Forms). If not needed, the change is safe.
  - Evidence: `diff_hunk:eng/common/internal-feed-operations.ps1:26`

- `compatibility` low at `eng/common/post-build/nuget-verification.ps1:68` (0.50)
  - Adding '-UseBasicParsing' to Invoke-WebRequest may change the response object type, potentially breaking code that expects the default IE-driven parsing.
  - Suggestion: Confirm that no downstream code depends on the default HTML parsing features. If not, the change is safe.
  - Evidence: `diff_hunk:eng/common/post-build/nuget-verification.ps1:65`

- `compatibility` low at `eng/common/tools.ps1:269` (0.50)
  - Adding '-UseBasicParsing' to Invoke-WebRequest may change the response object type, potentially breaking code that expects the default IE-driven parsing.
  - Suggestion: Ensure that no downstream code relies on the default HTML parsing. If not, the change is safe.
  - Evidence: `diff_hunk:eng/common/tools.ps1:266`

- `security` medium at `eng/common/core-templates/steps/source-build.yml:44` (0.50)
  - The patch changes the internal runtime download source URL from 'https://dotnetbuilds.blob.core.windows.net/internal' to 'https://ci.dot.net/internal' and adds a new '--runtimesourcefeed' argument. This alters the trust boundary for runtime artifact downloads, potentially exposing the build to a different internal endpoint without evidence of equivalent security controls.
  - Suggestion: Verify that the new URL 'https://ci.dot.net/internal' is an authorized internal feed with equivalent or stronger access controls and that the added '--runtimesourcefeed' argument does not bypass existing authentication or introduce a man-in-the-middle risk.
  - Evidence: `diff_hunk:eng/common/core-templates/steps/source-build.yml:41`, `diff:eng/common/core-templates/steps/source-build.yml:44`

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
