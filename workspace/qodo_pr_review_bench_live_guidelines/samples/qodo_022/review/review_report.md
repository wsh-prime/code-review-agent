# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 13
- Changed entities: 13
- Risk signals: 1
- Findings: 0
- Needs human review: 10
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
| Retry count | 0 |
| Total latency | 61194 ms |
| Token in | 23606 |
| Token out | 1639 |

- Iteration 0: 10 candidates, 1 verified, 1 uncertain, 0 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `file_risk_shards_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 22209 |
| Selected evidence | 15 |
| Omitted evidence | 179 |
| Context truncated | True |
| Review shards | 4 |
| Context requests | 0 |
| Refills | 0 |

## Findings

No findings.

Checked changed files, changed entities, deterministic risk signals, and evidence references. No high-confidence review finding was produced.

## Needs Human Review

- `code_style` high at `src/Caching/SqlServer/src/SqlServerCacheOptions.cs:1` (0.50)
  - Missing MIT license header. All C# source files must include the standardized .NET Foundation MIT license header at the beginning of the file.
  - Suggestion: Add the following two-line comment at the top of the file: '// Licensed to the .NET Foundation under one or more agreements.' followed by '// The .NET Foundation licenses this file to you under the MIT license.'
  - Evidence: `diff_hunk:src/Caching/SqlServer/src/SqlServerCacheOptions.cs:8`

- `code_style` high at `src/HttpClientFactory/Polly/src/DependencyInjection/PollyHttpClientBuilderExtensions.cs:1` (0.50)
  - Missing MIT license header. All C# source files must include the standardized .NET Foundation MIT license header at the beginning of the file.
  - Suggestion: Add the following two-line comment at the top of the file: '// Licensed to the .NET Foundation under one or more agreements.' followed by '// The .NET Foundation licenses this file to you under the MIT license.'
  - Evidence: `diff_hunk:src/HttpClientFactory/Polly/src/DependencyInjection/PollyHttpClientBuilderExtensions.cs:11`

- `code_style` high at `src/Logging.AzureAppServices/src/AzureAppServicesLoggerFactoryExtensions.cs:1` (0.50)
  - Missing MIT license header. All C# source files must include the standardized .NET Foundation MIT license header at the beginning of the file.
  - Suggestion: Add the following two-line comment at the top of the file: '// Licensed to the .NET Foundation under one or more agreements.' followed by '// The .NET Foundation licenses this file to you under the MIT license.'
  - Evidence: `diff_hunk:src/Logging.AzureAppServices/src/AzureAppServicesLoggerFactoryExtensions.cs:13`

- `code_style` high at `src/Logging.AzureAppServices/src/AzureBlobLoggerContext.cs:1` (0.50)
  - Missing MIT license header. All C# source files must include the standardized .NET Foundation MIT license header at the beginning of the file.
  - Suggestion: Add the following two-line comment at the top of the file: '// Licensed to the .NET Foundation under one or more agreements.' followed by '// The .NET Foundation licenses this file to you under the MIT license.'
  - Evidence: `diff_hunk:src/Logging.AzureAppServices/src/AzureBlobLoggerContext.cs:6`

- `license` high at `src/Logging.AzureAppServices/src/AzureBlobLoggerOptions.cs:1` (0.50)
  - Missing MIT license header. All C# source files must include the exact two-line comment header: '// Licensed to the .NET Foundation under one or more agreements.' followed by '// The .NET Foundation licenses this file to you under the MIT license.'
  - Suggestion: Add the required license header at the top of the file.
  - Evidence: `diff_hunk:src/Logging.AzureAppServices/src/AzureBlobLoggerOptions.cs:7`

- `license` high at `src/Logging.AzureAppServices/src/AzureFileLoggerOptions.cs:1` (0.50)
  - Missing MIT license header. All C# source files must include the exact two-line comment header: '// Licensed to the .NET Foundation under one or more agreements.' followed by '// The .NET Foundation licenses this file to you under the MIT license.'
  - Suggestion: Add the required license header at the top of the file.
  - Evidence: `diff_hunk:src/Logging.AzureAppServices/src/AzureFileLoggerOptions.cs:7`

- `license` high at `src/Logging.AzureAppServices/src/BatchingLoggerOptions.cs:1` (0.50)
  - Missing MIT license header. All C# source files must include the exact two-line comment header: '// Licensed to the .NET Foundation under one or more agreements.' followed by '// The .NET Foundation licenses this file to you under the MIT license.'
  - Suggestion: Add the required license header at the top of the file.
  - Evidence: `diff_hunk:src/Logging.AzureAppServices/src/BatchingLoggerOptions.cs:6`

- `license` high at `src/Logging.AzureAppServices/src/BatchingLoggerProvider.cs:1` (0.50)
  - Missing MIT license header. All C# source files must include the exact two-line comment header: '// Licensed to the .NET Foundation under one or more agreements.' followed by '// The .NET Foundation licenses this file to you under the MIT license.'
  - Suggestion: Add the required license header at the top of the file.
  - Evidence: `diff_hunk:src/Logging.AzureAppServices/src/BatchingLoggerProvider.cs:11`

- `license_header` high at `src/Validation/src/ValidationOptions.cs:1` (0.50)
  - C# source file is missing the required MIT license header.
  - Suggestion: Add the exact two-line comment header at the beginning of the file: '// Licensed to the .NET Foundation under one or more agreements.' followed by '// The .NET Foundation licenses this file to you under the MIT license.'
  - Evidence: `diff_hunk:src/Validation/src/ValidationOptions.cs:7`

- `namespace_style` medium at `src/Validation/src/ValidationOptions.cs:7` (0.50)
  - File uses a block-scoped namespace declaration instead of a file-scoped namespace declaration.
  - Suggestion: Change 'namespace Microsoft.Extensions.Validation;' to a file-scoped namespace declaration (ending with semicolon, no braces).
  - Evidence: `diff_hunk:src/Validation/src/ValidationOptions.cs:7`

## Changed Files

- `src/Caching/SqlServer/src/SqlServerCacheOptions.cs` (modified)
- `src/HttpClientFactory/Polly/src/DependencyInjection/PollyHttpClientBuilderExtensions.cs` (modified)
- `src/Logging.AzureAppServices/src/AzureAppServicesLoggerFactoryExtensions.cs` (modified)
- `src/Logging.AzureAppServices/src/AzureBlobLoggerContext.cs` (modified)
- `src/Logging.AzureAppServices/src/AzureBlobLoggerOptions.cs` (modified)
- `src/Logging.AzureAppServices/src/AzureFileLoggerOptions.cs` (modified)
- `src/Logging.AzureAppServices/src/BatchingLoggerOptions.cs` (modified)
- `src/Logging.AzureAppServices/src/BatchingLoggerProvider.cs` (modified)
- `src/Logging.AzureAppServices/src/FileLoggerProvider.cs` (modified)
- `src/Validation/src/IValidatableInfoResolver.cs` (modified)
- `src/Validation/src/SkipValidationAttribute.cs` (modified)
- `src/Validation/src/ValidateContext.cs` (modified)
- `src/Validation/src/ValidationOptions.cs` (modified)

## Changed Entities

- `src/Caching/SqlServer/src/SqlServerCacheOptions.cs:11-48` module `src.Caching.SqlServer.src.SqlServerCacheOptions`
- `src/HttpClientFactory/Polly/src/DependencyInjection/PollyHttpClientBuilderExtensions.cs:14-20` module `src.HttpClientFactory.Polly.src.DependencyInjection.PollyHttpClientBuilderExtensions`
- `src/Logging.AzureAppServices/src/AzureAppServicesLoggerFactoryExtensions.cs:16-23` module `src.Logging.AzureAppServices.src.AzureAppServicesLoggerFactoryExtensions`
- `src/Logging.AzureAppServices/src/AzureBlobLoggerContext.cs:9-14` module `src.Logging.AzureAppServices.src.AzureBlobLoggerContext`
- `src/Logging.AzureAppServices/src/AzureBlobLoggerOptions.cs:10-10` module `src.Logging.AzureAppServices.src.AzureBlobLoggerOptions`
- `src/Logging.AzureAppServices/src/AzureFileLoggerOptions.cs:10-10` module `src.Logging.AzureAppServices.src.AzureFileLoggerOptions`
- `src/Logging.AzureAppServices/src/BatchingLoggerOptions.cs:9-9` module `src.Logging.AzureAppServices.src.BatchingLoggerOptions`
- `src/Logging.AzureAppServices/src/BatchingLoggerProvider.cs:14-14` module `src.Logging.AzureAppServices.src.BatchingLoggerProvider`
- `src/Logging.AzureAppServices/src/FileLoggerProvider.cs:15-15` module `src.Logging.AzureAppServices.src.FileLoggerProvider`
- `src/Validation/src/IValidatableInfoResolver.cs:21-31` module `src.Validation.src.IValidatableInfoResolver`
- `src/Validation/src/SkipValidationAttribute.cs:9-16` module `src.Validation.src.SkipValidationAttribute`
- `src/Validation/src/ValidateContext.cs:26-26` module `src.Validation.src.ValidateContext`
- `src/Validation/src/ValidationOptions.cs:10-16` module `src.Validation.src.ValidationOptions`

## Risk Signals

- `security_sensitive` (0.74): Security-sensitive keywords changed in src/Logging.AzureAppServices/src/BatchingLoggerProvider.cs.

## Evidence Index

- `diff:src/Caching/SqlServer/src/SqlServerCacheOptions.cs:11` [diff]: src/Caching/SqlServer/src/SqlServerCacheOptions.cs:11
- `diff:src/Caching/SqlServer/src/SqlServerCacheOptions.cs:16` [diff]: src/Caching/SqlServer/src/SqlServerCacheOptions.cs:16
- `diff:src/Caching/SqlServer/src/SqlServerCacheOptions.cs:21` [diff]: src/Caching/SqlServer/src/SqlServerCacheOptions.cs:21
- `diff:src/Caching/SqlServer/src/SqlServerCacheOptions.cs:23` [diff]: src/Caching/SqlServer/src/SqlServerCacheOptions.cs:23
- `diff:src/Caching/SqlServer/src/SqlServerCacheOptions.cs:24` [diff]: src/Caching/SqlServer/src/SqlServerCacheOptions.cs:24
- `diff:src/Caching/SqlServer/src/SqlServerCacheOptions.cs:25` [diff]: src/Caching/SqlServer/src/SqlServerCacheOptions.cs:25
- `diff:src/Caching/SqlServer/src/SqlServerCacheOptions.cs:26` [diff]: src/Caching/SqlServer/src/SqlServerCacheOptions.cs:26
- `diff:src/Caching/SqlServer/src/SqlServerCacheOptions.cs:29` [diff]: src/Caching/SqlServer/src/SqlServerCacheOptions.cs:29
- `diff:src/Caching/SqlServer/src/SqlServerCacheOptions.cs:31` [diff]: src/Caching/SqlServer/src/SqlServerCacheOptions.cs:31
- `diff:src/Caching/SqlServer/src/SqlServerCacheOptions.cs:34` [diff]: src/Caching/SqlServer/src/SqlServerCacheOptions.cs:34
- `diff:src/Caching/SqlServer/src/SqlServerCacheOptions.cs:36` [diff]: src/Caching/SqlServer/src/SqlServerCacheOptions.cs:36
- `diff:src/Caching/SqlServer/src/SqlServerCacheOptions.cs:39` [diff]: src/Caching/SqlServer/src/SqlServerCacheOptions.cs:39
- `diff:src/Caching/SqlServer/src/SqlServerCacheOptions.cs:41` [diff]: src/Caching/SqlServer/src/SqlServerCacheOptions.cs:41
- `diff:src/Caching/SqlServer/src/SqlServerCacheOptions.cs:42` [diff]: src/Caching/SqlServer/src/SqlServerCacheOptions.cs:42
- `diff:src/Caching/SqlServer/src/SqlServerCacheOptions.cs:44` [diff]: src/Caching/SqlServer/src/SqlServerCacheOptions.cs:44
- `diff:src/Caching/SqlServer/src/SqlServerCacheOptions.cs:46` [diff]: src/Caching/SqlServer/src/SqlServerCacheOptions.cs:46
- `diff:src/Caching/SqlServer/src/SqlServerCacheOptions.cs:47` [diff]: src/Caching/SqlServer/src/SqlServerCacheOptions.cs:47
- `diff:src/Caching/SqlServer/src/SqlServerCacheOptions.cs:48` [diff]: src/Caching/SqlServer/src/SqlServerCacheOptions.cs:48
- `diff:src/HttpClientFactory/Polly/src/DependencyInjection/PollyHttpClientBuilderExtensions.cs:115` [diff]: src/HttpClientFactory/Polly/src/DependencyInjection/PollyHttpClientBuilderExtensions.cs:115
- `diff:src/HttpClientFactory/Polly/src/DependencyInjection/PollyHttpClientBuilderExtensions.cs:14` [diff]: src/HttpClientFactory/Polly/src/DependencyInjection/PollyHttpClientBuilderExtensions.cs:14
- `diff:src/HttpClientFactory/Polly/src/DependencyInjection/PollyHttpClientBuilderExtensions.cs:152` [diff]: src/HttpClientFactory/Polly/src/DependencyInjection/PollyHttpClientBuilderExtensions.cs:152
- `diff:src/HttpClientFactory/Polly/src/DependencyInjection/PollyHttpClientBuilderExtensions.cs:188` [diff]: src/HttpClientFactory/Polly/src/DependencyInjection/PollyHttpClientBuilderExtensions.cs:188
- `diff:src/HttpClientFactory/Polly/src/DependencyInjection/PollyHttpClientBuilderExtensions.cs:20` [diff]: src/HttpClientFactory/Polly/src/DependencyInjection/PollyHttpClientBuilderExtensions.cs:20
- `diff:src/HttpClientFactory/Polly/src/DependencyInjection/PollyHttpClientBuilderExtensions.cs:210` [diff]: src/HttpClientFactory/Polly/src/DependencyInjection/PollyHttpClientBuilderExtensions.cs:210
- `diff:src/HttpClientFactory/Polly/src/DependencyInjection/PollyHttpClientBuilderExtensions.cs:211` [diff]: src/HttpClientFactory/Polly/src/DependencyInjection/PollyHttpClientBuilderExtensions.cs:211
- `diff:src/HttpClientFactory/Polly/src/DependencyInjection/PollyHttpClientBuilderExtensions.cs:239` [diff]: src/HttpClientFactory/Polly/src/DependencyInjection/PollyHttpClientBuilderExtensions.cs:239
- `diff:src/HttpClientFactory/Polly/src/DependencyInjection/PollyHttpClientBuilderExtensions.cs:240` [diff]: src/HttpClientFactory/Polly/src/DependencyInjection/PollyHttpClientBuilderExtensions.cs:240
- `diff:src/HttpClientFactory/Polly/src/DependencyInjection/PollyHttpClientBuilderExtensions.cs:48` [diff]: src/HttpClientFactory/Polly/src/DependencyInjection/PollyHttpClientBuilderExtensions.cs:48
- `diff:src/HttpClientFactory/Polly/src/DependencyInjection/PollyHttpClientBuilderExtensions.cs:80` [diff]: src/HttpClientFactory/Polly/src/DependencyInjection/PollyHttpClientBuilderExtensions.cs:80
- `diff:src/Logging.AzureAppServices/src/AzureAppServicesLoggerFactoryExtensions.cs:16` [diff]: src/Logging.AzureAppServices/src/AzureAppServicesLoggerFactoryExtensions.cs:16
- ... 164 more evidence items omitted.
