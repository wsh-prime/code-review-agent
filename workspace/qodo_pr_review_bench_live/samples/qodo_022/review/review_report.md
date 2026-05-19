# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 13
- Changed entities: 13
- Risk signals: 1
- Findings: 0
- Needs human review: 1
- Discarded: 0
- Agent runs: 9
- Loop enabled: True
- Target repo modified: False

## Loop Summary

| Metric | Value |
|---|---:|
| Iterations | 1 / 1 |
| Converged | False |
| Fallback | False |
| Retry count | 1 |
| Total latency | 153198 ms |
| Token in | 24999 |
| Token out | 1088 |

- Iteration 0: 1 candidates, 1 verified, 1 uncertain, 0 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `file_risk_shards_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 18440 |
| Selected evidence | 33 |
| Omitted evidence | 161 |
| Context truncated | True |
| Review shards | 4 |
| Context requests | 5 |
| Refills | 4 |

## Findings

No findings.

Checked changed files, changed entities, deterministic risk signals, and evidence references. No high-confidence review finding was produced.

## Needs Human Review

- `correctness` medium at `src/Validation/src/ValidationOptions.cs:42` (0.50)
  - In TryGetValidatableTypeInfo, the out parameter validatableTypeInfo is now assigned null before the loop, but the loop may assign a non-null value via resolver.TryGetValidatableTypeInfo. If the loop completes without finding a match, the out parameter will be null (as before). However, the assignment at line 42 is redundant and could mask a bug if a resolver incorrectly returns true without setting the out parameter, because the out parameter would already be null from the initial assignment, making the [NotNullWhen(true)] contract unreliable.
  - Suggestion: Remove the redundant 'validatableTypeInfo = null;' assignment at line 42, as the out parameter is already assigned by the resolver or defaults to null at the end of the method. Alternatively, ensure that each resolver correctly sets the out parameter when returning true.
  - Evidence: `diff_hunk:src/Validation/src/ValidationOptions.cs:38`, `diff_hunk:src/Validation/src/ValidationOptions.cs:52`

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
