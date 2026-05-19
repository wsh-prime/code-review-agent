# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 3
- Changed entities: 3
- Risk signals: 1
- Findings: 2
- Needs human review: 0
- Discarded: 1
- Agent runs: 3
- Loop enabled: True
- Target repo modified: False

## Loop Summary

| Metric | Value |
|---|---:|
| Iterations | 1 / 1 |
| Converged | True |
| Fallback | False |
| Retry count | 1 |
| Total latency | 87009 ms |
| Token in | 9058 |
| Token out | 627 |

- Iteration 0: 3 candidates, 2 verified, 0 uncertain, 2 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `file_risk_shards_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 8084 |
| Selected evidence | 5 |
| Omitted evidence | 85 |
| Context truncated | True |
| Review shards | 1 |
| Context requests | 2 |
| Refills | 1 |

## Findings

- `maintainability` low at `src/Shared/CertificateGeneration/CertificateManager.cs:969` (0.90)
  - Removed the XML documentation comment from CertificateManagerEventSource class without adding a replacement comment, reducing API documentation.
  - Suggestion: Restore or update the XML doc comment to describe the event source's purpose.
  - Evidence: `diff_hunk:src/Shared/CertificateGeneration/CertificateManager.cs:966`

- `correctness` medium at `src/Shared/CertificateGeneration/UnixCertificateManager.cs:358` (0.60)
  - The variable 'hasValidSslCertDir' is set to false in all branches except when SSL_CERT_DIR already includes certDir; however, the 'sawTrustFailure' assignment at line 408 uses '!hasValidSslCertDir', which may incorrectly report trust failure when SSL_CERT_DIR is unset but OpenSSL directory is valid.
  - Suggestion: Ensure that when TryGetOpenSslDirectory succeeds, hasValidSslCertDir is set to true if the OpenSSL directory is valid, or adjust the logic to avoid false trust failures.
  - Evidence: `diff_hunk:src/Shared/CertificateGeneration/UnixCertificateManager.cs:355`

## Needs Human Review

None.

## Changed Files

- `src/Shared/CertificateGeneration/CertificateManager.cs` (modified)
- `src/Shared/CertificateGeneration/UnixCertificateManager.cs` (modified)
- `src/Tools/dotnet-dev-certs/src/Program.cs` (modified)

## Changed Entities

- `src/Shared/CertificateGeneration/CertificateManager.cs:969-971` module `src.Shared.CertificateGeneration.CertificateManager`
- `src/Shared/CertificateGeneration/UnixCertificateManager.cs:358-408` module `src.Shared.CertificateGeneration.UnixCertificateManager`
- `src/Tools/dotnet-dev-certs/src/Program.cs:127-140` module `src.Tools.dotnet-dev-certs.src.Program`

## Risk Signals

- `security_sensitive` (0.74): Security-sensitive keywords changed in src/Tools/dotnet-dev-certs/src/Program.cs.

## Evidence Index

- `diff:src/Shared/CertificateGeneration/CertificateManager.cs:1303` [diff]: src/Shared/CertificateGeneration/CertificateManager.cs:1303
- `diff:src/Shared/CertificateGeneration/CertificateManager.cs:1306` [diff]: src/Shared/CertificateGeneration/CertificateManager.cs:1306
- `diff:src/Shared/CertificateGeneration/CertificateManager.cs:1313` [diff]: src/Shared/CertificateGeneration/CertificateManager.cs:1313
- `diff:src/Shared/CertificateGeneration/CertificateManager.cs:1314` [diff]: src/Shared/CertificateGeneration/CertificateManager.cs:1314
- `diff:src/Shared/CertificateGeneration/CertificateManager.cs:1315` [diff]: src/Shared/CertificateGeneration/CertificateManager.cs:1315
- `diff:src/Shared/CertificateGeneration/CertificateManager.cs:1316` [diff]: src/Shared/CertificateGeneration/CertificateManager.cs:1316
- `diff:src/Shared/CertificateGeneration/CertificateManager.cs:1317` [diff]: src/Shared/CertificateGeneration/CertificateManager.cs:1317
- `diff:src/Shared/CertificateGeneration/CertificateManager.cs:1318` [diff]: src/Shared/CertificateGeneration/CertificateManager.cs:1318
- `diff:src/Shared/CertificateGeneration/CertificateManager.cs:1319` [diff]: src/Shared/CertificateGeneration/CertificateManager.cs:1319
- `diff:src/Shared/CertificateGeneration/CertificateManager.cs:1320` [diff]: src/Shared/CertificateGeneration/CertificateManager.cs:1320
- `diff:src/Shared/CertificateGeneration/CertificateManager.cs:969` [diff]: src/Shared/CertificateGeneration/CertificateManager.cs:969
- `diff:src/Shared/CertificateGeneration/CertificateManager.cs:970` [diff]: src/Shared/CertificateGeneration/CertificateManager.cs:970
- `diff:src/Shared/CertificateGeneration/CertificateManager.cs:971` [diff]: src/Shared/CertificateGeneration/CertificateManager.cs:971
- `diff:src/Shared/CertificateGeneration/UnixCertificateManager.cs:1000` [diff]: src/Shared/CertificateGeneration/UnixCertificateManager.cs:1000
- `diff:src/Shared/CertificateGeneration/UnixCertificateManager.cs:1001` [diff]: src/Shared/CertificateGeneration/UnixCertificateManager.cs:1001
- `diff:src/Shared/CertificateGeneration/UnixCertificateManager.cs:1002` [diff]: src/Shared/CertificateGeneration/UnixCertificateManager.cs:1002
- `diff:src/Shared/CertificateGeneration/UnixCertificateManager.cs:1003` [diff]: src/Shared/CertificateGeneration/UnixCertificateManager.cs:1003
- `diff:src/Shared/CertificateGeneration/UnixCertificateManager.cs:1004` [diff]: src/Shared/CertificateGeneration/UnixCertificateManager.cs:1004
- `diff:src/Shared/CertificateGeneration/UnixCertificateManager.cs:1005` [diff]: src/Shared/CertificateGeneration/UnixCertificateManager.cs:1005
- `diff:src/Shared/CertificateGeneration/UnixCertificateManager.cs:1006` [diff]: src/Shared/CertificateGeneration/UnixCertificateManager.cs:1006
- `diff:src/Shared/CertificateGeneration/UnixCertificateManager.cs:358` [diff]: src/Shared/CertificateGeneration/UnixCertificateManager.cs:358
- `diff:src/Shared/CertificateGeneration/UnixCertificateManager.cs:359` [diff]: src/Shared/CertificateGeneration/UnixCertificateManager.cs:359
- `diff:src/Shared/CertificateGeneration/UnixCertificateManager.cs:360` [diff]: src/Shared/CertificateGeneration/UnixCertificateManager.cs:360
- `diff:src/Shared/CertificateGeneration/UnixCertificateManager.cs:361` [diff]: src/Shared/CertificateGeneration/UnixCertificateManager.cs:361
- `diff:src/Shared/CertificateGeneration/UnixCertificateManager.cs:362` [diff]: src/Shared/CertificateGeneration/UnixCertificateManager.cs:362
- `diff:src/Shared/CertificateGeneration/UnixCertificateManager.cs:363` [diff]: src/Shared/CertificateGeneration/UnixCertificateManager.cs:363
- `diff:src/Shared/CertificateGeneration/UnixCertificateManager.cs:364` [diff]: src/Shared/CertificateGeneration/UnixCertificateManager.cs:364
- `diff:src/Shared/CertificateGeneration/UnixCertificateManager.cs:365` [diff]: src/Shared/CertificateGeneration/UnixCertificateManager.cs:365
- `diff:src/Shared/CertificateGeneration/UnixCertificateManager.cs:366` [diff]: src/Shared/CertificateGeneration/UnixCertificateManager.cs:366
- `diff:src/Shared/CertificateGeneration/UnixCertificateManager.cs:367` [diff]: src/Shared/CertificateGeneration/UnixCertificateManager.cs:367
- ... 60 more evidence items omitted.
