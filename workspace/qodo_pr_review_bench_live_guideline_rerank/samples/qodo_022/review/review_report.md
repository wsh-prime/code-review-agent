# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 13
- Changed entities: 13
- Risk signals: 1
- Findings: 1
- Needs human review: 6
- Discarded: 0
- Agent runs: 6
- Loop enabled: True
- Target repo modified: False

## Loop Summary

| Metric | Value |
|---|---:|
| Iterations | 1 / 1 |
| Converged | False |
| Fallback | False |
| Retry count | 5 |
| Total latency | 430113 ms |
| Token in | 18954 |
| Token out | 1218 |

- Iteration 0: 7 candidates, 2 verified, 1 uncertain, 1 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `file_risk_shards_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 22700 |
| Selected evidence | 19 |
| Omitted evidence | 175 |
| Context truncated | True |
| Review shards | 4 |
| Context requests | 1 |
| Refills | 1 |

## Findings

- `correctness` medium at `src/Logging.AzureAppServices/src/BatchingLoggerProvider.cs:124` (0.95)
  - The IntervalAsync method returns Task.Delay without ConfigureAwait(false), which can cause deadlocks in library code when the synchronization context is blocked.
  - Suggestion: Add .ConfigureAwait(false) to the Task.Delay call: return Task.Delay(interval, cancellationToken).ConfigureAwait(false);
  - Evidence: `diff_hunk:src/Logging.AzureAppServices/src/BatchingLoggerProvider.cs:124`

## Needs Human Review

- `license` medium at `src/Logging.AzureAppServices/src/FileLoggerProvider.cs:1` (0.50)
  - File is missing the required MIT license header.
  - Suggestion: Add the two-line comment header '// Licensed to the .NET Foundation under one or more agreements.' followed by '// The .NET Foundation licenses this file to you under the MIT license.' at the start of the file.
  - Evidence: `diff_hunk:src/Logging.AzureAppServices/src/FileLoggerProvider.cs:12`

- `license` medium at `src/Validation/src/IValidatableInfoResolver.cs:1` (0.50)
  - File is missing the required MIT license header.
  - Suggestion: Add the two-line comment header '// Licensed to the .NET Foundation under one or more agreements.' followed by '// The .NET Foundation licenses this file to you under the MIT license.' at the start of the file.
  - Evidence: `diff_hunk:src/Validation/src/IValidatableInfoResolver.cs:18`

- `license` medium at `src/Validation/src/SkipValidationAttribute.cs:1` (0.50)
  - File is missing the required MIT license header.
  - Suggestion: Add the two-line comment header '// Licensed to the .NET Foundation under one or more agreements.' followed by '// The .NET Foundation licenses this file to you under the MIT license.' at the start of the file.
  - Evidence: `diff_hunk:src/Validation/src/SkipValidationAttribute.cs:6`

- `license` medium at `src/Validation/src/ValidateContext.cs:1` (0.50)
  - File is missing the required MIT license header.
  - Suggestion: Add the two-line comment header '// Licensed to the .NET Foundation under one or more agreements.' followed by '// The .NET Foundation licenses this file to you under the MIT license.' at the start of the file.
  - Evidence: `diff_hunk:src/Validation/src/ValidateContext.cs:23`

- `license_header` high at `src/Validation/src/ValidationOptions.cs:1` (0.50)
  - C# source file is missing the required MIT license header.
  - Suggestion: Add the standard .NET Foundation MIT license header at the beginning of the file: '// Licensed to the .NET Foundation under one or more agreements.' followed by '// The .NET Foundation licenses this file to you under the MIT license.'
  - Evidence: `diff_hunk:src/Validation/src/ValidationOptions.cs:7`

- `style` minor at `src/Validation/src/ValidationOptions.cs:60` (0.50)
  - Brace placement inconsistency: the opening brace for TryGetValidatableParameterInfo is on the same line as the method signature, while other methods in the same file use a new line.
  - Suggestion: Consistently place opening braces on a new line to match the existing style in the file.
  - Evidence: `diff_hunk:src/Validation/src/ValidationOptions.cs:60`

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
