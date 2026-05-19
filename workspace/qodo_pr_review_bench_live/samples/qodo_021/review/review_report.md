# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 13
- Changed entities: 13
- Risk signals: 7
- Findings: 0
- Needs human review: 2
- Discarded: 2
- Agent runs: 7
- Loop enabled: True
- Target repo modified: False

## Loop Summary

| Metric | Value |
|---|---:|
| Iterations | 1 / 1 |
| Converged | False |
| Fallback | False |
| Retry count | 0 |
| Total latency | 62649 ms |
| Token in | 29074 |
| Token out | 1059 |

- Iteration 0: 4 candidates, 2 verified, 2 uncertain, 0 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `file_risk_shards_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 21197 |
| Selected evidence | 27 |
| Omitted evidence | 443 |
| Context truncated | True |
| Review shards | 4 |
| Context requests | 3 |
| Refills | 2 |

## Findings

No findings.

Checked changed files, changed entities, deterministic risk signals, and evidence references. No high-confidence review finding was produced.

## Needs Human Review

- `correctness` medium at `eng/Versions.props:14` (0.50)
  - ValidateBaseline changed from true to false, which disables baseline validation. This may allow regressions in package version consistency to go undetected.
  - Suggestion: Ensure that disabling ValidateBaseline is intentional and that alternative validation mechanisms are in place.
  - Evidence: `diff_hunk:eng/Versions.props:9`

- `test_quality` medium at `src/Components/test/E2ETest/ServerExecutionTests/WebSocketCompressionTests.cs:101` (0.50)
  - The test 'EmbeddingServerAppInsideIframe_WithCompressionEnabled_Fails' is quarantined due to a known issue, but the patch does not include any fix or workaround for the underlying problem. The test will be skipped, potentially masking regressions.
  - Suggestion: Either fix the underlying issue referenced in the quarantine link, or add a comment explaining why the test is quarantined and what conditions would allow it to be unquarantined.
  - Evidence: `diff_hunk:src/Components/test/E2ETest/ServerExecutionTests/WebSocketCompressionTests.cs:98`

## Changed Files

- `.azure/pipelines/jobs/default-build.yml` (modified)
- `NuGet.config` (modified)
- `eng/PackageOverrides.txt` (added)
- `eng/PlatformManifest.txt` (added)
- `eng/Version.Details.props` (modified)
- `eng/Version.Details.xml` (modified)
- `eng/Versions.props` (modified)
- `eng/common/SetupNugetSources.ps1` (modified)
- `eng/common/SetupNugetSources.sh` (modified)
- `eng/common/core-templates/steps/install-microbuild.yml` (modified)
- `eng/targets/ResolveReferences.targets` (modified)
- `global.json` (modified)
- `src/Components/test/E2ETest/ServerExecutionTests/WebSocketCompressionTests.cs` (modified)

## Changed Entities

- `.azure/pipelines/jobs/default-build.yml:106-106` module `.azure.pipelines.jobs.default-build`
- `NuGet.config:7-7` module `NuGet`
- `eng/PackageOverrides.txt:1-140` module `eng.PackageOverrides`
- `eng/PlatformManifest.txt:1-143` module `eng.PlatformManifest`
- `eng/Version.Details.props:9-100` module `eng.Version.Details`
- `eng/Version.Details.xml:11-337` module `eng.Version.Details`
- `eng/Versions.props:12-14` module `eng.Versions`
- `eng/common/SetupNugetSources.ps1:2-4` module `eng.common.SetupNugetSources`
- `eng/common/SetupNugetSources.sh:4-6` module `eng.common.SetupNugetSources`
- `eng/common/core-templates/steps/install-microbuild.yml:14-30` module `eng.common.core-templates.steps.install-microbuild`
- `eng/targets/ResolveReferences.targets:211-211` module `eng.targets.ResolveReferences`
- `global.json:3-6` module `global`
- `src/Components/test/E2ETest/ServerExecutionTests/WebSocketCompressionTests.cs:10-17` module `src.Components.test.E2ETest.ServerExecutionTests.WebSocketCompressionTests`

## Risk Signals

- `config_change` (0.86): Configuration file changed: .azure/pipelines/jobs/default-build.yml.
- `config_change` (0.86): Configuration file changed: eng/common/core-templates/steps/install-microbuild.yml.
- `security_sensitive` (0.74): Security-sensitive keywords changed in eng/PackageOverrides.txt.
- `security_sensitive` (0.74): Security-sensitive keywords changed in eng/PlatformManifest.txt.
- `security_sensitive` (0.74): Security-sensitive keywords changed in eng/Version.Details.props.
- `security_sensitive` (0.74): Security-sensitive keywords changed in eng/Version.Details.xml.
- `security_sensitive` (0.74): Security-sensitive keywords changed in eng/common/SetupNugetSources.ps1.

## Evidence Index

- `diff:.azure/pipelines/jobs/default-build.yml:106` [diff]: .azure/pipelines/jobs/default-build.yml:106
- `diff:.azure/pipelines/jobs/default-build.yml:167` [diff]: .azure/pipelines/jobs/default-build.yml:167
- `diff:.azure/pipelines/jobs/default-build.yml:322` [diff]: .azure/pipelines/jobs/default-build.yml:322
- `diff:.azure/pipelines/jobs/default-build.yml:393` [diff]: .azure/pipelines/jobs/default-build.yml:393
- `diff:NuGet.config:7` [diff]: NuGet.config:7
- `diff:eng/PackageOverrides.txt:1` [diff]: eng/PackageOverrides.txt:1
- `diff:eng/PackageOverrides.txt:10` [diff]: eng/PackageOverrides.txt:10
- `diff:eng/PackageOverrides.txt:100` [diff]: eng/PackageOverrides.txt:100
- `diff:eng/PackageOverrides.txt:101` [diff]: eng/PackageOverrides.txt:101
- `diff:eng/PackageOverrides.txt:102` [diff]: eng/PackageOverrides.txt:102
- `diff:eng/PackageOverrides.txt:103` [diff]: eng/PackageOverrides.txt:103
- `diff:eng/PackageOverrides.txt:104` [diff]: eng/PackageOverrides.txt:104
- `diff:eng/PackageOverrides.txt:105` [diff]: eng/PackageOverrides.txt:105
- `diff:eng/PackageOverrides.txt:106` [diff]: eng/PackageOverrides.txt:106
- `diff:eng/PackageOverrides.txt:107` [diff]: eng/PackageOverrides.txt:107
- `diff:eng/PackageOverrides.txt:108` [diff]: eng/PackageOverrides.txt:108
- `diff:eng/PackageOverrides.txt:109` [diff]: eng/PackageOverrides.txt:109
- `diff:eng/PackageOverrides.txt:11` [diff]: eng/PackageOverrides.txt:11
- `diff:eng/PackageOverrides.txt:110` [diff]: eng/PackageOverrides.txt:110
- `diff:eng/PackageOverrides.txt:111` [diff]: eng/PackageOverrides.txt:111
- `diff:eng/PackageOverrides.txt:112` [diff]: eng/PackageOverrides.txt:112
- `diff:eng/PackageOverrides.txt:113` [diff]: eng/PackageOverrides.txt:113
- `diff:eng/PackageOverrides.txt:114` [diff]: eng/PackageOverrides.txt:114
- `diff:eng/PackageOverrides.txt:115` [diff]: eng/PackageOverrides.txt:115
- `diff:eng/PackageOverrides.txt:116` [diff]: eng/PackageOverrides.txt:116
- `diff:eng/PackageOverrides.txt:117` [diff]: eng/PackageOverrides.txt:117
- `diff:eng/PackageOverrides.txt:118` [diff]: eng/PackageOverrides.txt:118
- `diff:eng/PackageOverrides.txt:119` [diff]: eng/PackageOverrides.txt:119
- `diff:eng/PackageOverrides.txt:12` [diff]: eng/PackageOverrides.txt:12
- `diff:eng/PackageOverrides.txt:120` [diff]: eng/PackageOverrides.txt:120
- ... 645 more evidence items omitted.
