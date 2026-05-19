# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 3
- Changed entities: 3
- Risk signals: 1
- Findings: 0
- Needs human review: 3
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
| Total latency | 27015 ms |
| Token in | 6215 |
| Token out | 517 |

- Iteration 0: 3 candidates, 3 verified, 3 uncertain, 0 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `risk_first_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 5989 |
| Selected evidence | 3 |
| Omitted evidence | 87 |
| Context truncated | True |
| Review shards | 1 |
| Context requests | 0 |
| Refills | 0 |

## Findings

No findings.

Checked changed files, changed entities, deterministic risk signals, and evidence references. No high-confidence review finding was produced.

## Needs Human Review

- `style` minor at `src/Shared/CertificateGeneration/CertificateManager.cs:969` (0.50)
  - Review guideline violation: 'All C# Source Files Must Include MIT License Header' - The file is missing the required MIT license header at the top.
  - Suggestion: Add the standard .NET Foundation MIT license header at the beginning of the file: '// Licensed to the .NET Foundation under one or more agreements.' followed by '// The .NET Foundation licenses this file to you under the MIT license.'
  - Evidence: `diff_hunk:src/Shared/CertificateGeneration/CertificateManager.cs:966`

- `style` minor at `src/Shared/CertificateGeneration/UnixCertificateManager.cs:358` (0.50)
  - Review guideline violation: 'All C# Source Files Must Include MIT License Header' - The file is missing the required MIT license header at the top.
  - Suggestion: Add the standard .NET Foundation MIT license header at the beginning of the file: '// Licensed to the .NET Foundation under one or more agreements.' followed by '// The .NET Foundation licenses this file to you under the MIT license.'
  - Evidence: `diff_hunk:src/Shared/CertificateGeneration/UnixCertificateManager.cs:355`

- `style` minor at `src/Tools/dotnet-dev-certs/src/Program.cs:127` (0.50)
  - Review guideline violation: 'All C# Source Files Must Include MIT License Header' - The file is missing the required MIT license header at the top.
  - Suggestion: Add the standard .NET Foundation MIT license header at the beginning of the file: '// Licensed to the .NET Foundation under one or more agreements.' followed by '// The .NET Foundation licenses this file to you under the MIT license.'
  - Evidence: `diff_hunk:src/Tools/dotnet-dev-certs/src/Program.cs:124`

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
