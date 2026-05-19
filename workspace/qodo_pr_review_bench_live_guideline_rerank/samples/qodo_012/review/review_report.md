# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 36
- Changed entities: 36
- Risk signals: 27
- Findings: 3
- Needs human review: 1
- Discarded: 2
- Agent runs: 13
- Loop enabled: True
- Target repo modified: False

## Loop Summary

| Metric | Value |
|---|---:|
| Iterations | 1 / 1 |
| Converged | False |
| Fallback | False |
| Retry count | 3 |
| Total latency | 380110 ms |
| Token in | 92143 |
| Token out | 2002 |

- Iteration 0: 6 candidates, 4 verified, 1 uncertain, 3 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `file_risk_shards_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 70989 |
| Selected evidence | 49 |
| Omitted evidence | 1475 |
| Context truncated | True |
| Review shards | 10 |
| Context requests | 4 |
| Refills | 2 |

## Findings

- `correctness` high at `ghost/core/core/server/services/tinybird/TinybirdService.js:59` (0.80)
  - The test expects the URL to contain 'test_pipe_v2.json' but the pipe name in the config is 'api_kpis_v2'. The buildRequest method likely appends the version to the pipe name, but the test uses 'test_pipe' as the pipe name and expects 'test_pipe_v2.json'. This mismatch suggests the version is being appended to the pipe name, which would produce 'test_pipe_v2.json' for pipe 'test_pipe' and version 'v2'. However, the actual pipe names in the config already include '_v2' suffix (e.g., 'api_kpis_v2'). If buildRequest appends the version to the pipe name, it would produce 'api_kpis_v2_v2' for those pipes, which is incorrect.
  - Suggestion: Verify that the buildRequest method does not append the version suffix to pipe names that already contain '_v2'. If it does, either remove the '_v2' suffix from the pipe names in the config or modify buildRequest to avoid double-suffixing.
  - Evidence: `diff_hunk:ghost/core/core/server/services/tinybird/TinybirdService.js:56`, `diff_hunk:ghost/core/test/unit/server/services/stats/utils/tinybird.test.js:70`

- `test_quality` medium at `ghost/core/test/unit/server/services/stats/utils/tinybird.test.js:110` (0.70)
  - The test 'ignores tbVersion when local is enabled' was removed. This test verified that when local mode is enabled, the tbVersion parameter is ignored and the URL does not contain '__v2'. The removal of this test reduces coverage for the local mode behavior, which could mask a regression where tbVersion is incorrectly applied in local mode.
  - Suggestion: Consider adding a test that verifies the version from config is ignored when local mode is enabled, similar to the removed test but adapted for the new version config approach.
  - Evidence: `diff_hunk:ghost/core/test/unit/server/services/stats/utils/tinybird.test.js:110`

- `test_coverage` medium at `ghost/core/test/unit/server/services/stats/utils/tinybird.test.js:110` (0.80)
  - Removed test 'ignores tbVersion when local is enabled' without adding equivalent coverage for the new v2 pipes.
  - Suggestion: Add a test that verifies tbVersion is ignored when local is enabled, covering the new v2 pipe names to ensure the materialized view optimization does not break local mode behavior.
  - Evidence: `diff_hunk:ghost/core/test/unit/server/services/stats/utils/tinybird.test.js:110`, `diff_hunk:ghost/core/core/server/services/tinybird/TinybirdService.js:56`

## Needs Human Review

- `maintainability` low at `apps/admin-x-framework/src/providers/framework-provider.tsx:13` (0.50)
  - The new 'version' property in StatsConfig interface is optional but its usage in stats-config.ts does not handle the case where version is an empty string, which would produce an endpoint name like '_api_kpis'.
  - Suggestion: Consider treating an empty string version the same as undefined, or add validation to reject empty strings.
  - Evidence: `diff_hunk:apps/admin-x-framework/src/providers/framework-provider.tsx:10`, `diff_hunk:apps/admin-x-framework/src/utils/stats-config.ts:13`

## Changed Files

- `apps/admin-x-framework/src/providers/framework-provider.tsx` (modified)
- `apps/admin-x-framework/src/utils/stats-config.ts` (modified)
- `ghost/core/core/server/api/endpoints/stats.js` (modified)
- `ghost/core/core/server/data/tinybird/README.md` (modified)
- `ghost/core/core/server/data/tinybird/datasources/_mv_session_data_v2.datasource` (added)
- `ghost/core/core/server/data/tinybird/endpoints/README.md` (modified)
- `ghost/core/core/server/data/tinybird/endpoints/api_active_visitors_v2.pipe` (added)
- `ghost/core/core/server/data/tinybird/endpoints/api_kpis_v2.pipe` (added)
- `ghost/core/core/server/data/tinybird/endpoints/api_post_visitor_counts_v2.pipe` (added)
- `ghost/core/core/server/data/tinybird/endpoints/api_top_devices_v2.pipe` (added)
- `ghost/core/core/server/data/tinybird/endpoints/api_top_locations_v2.pipe` (added)
- `ghost/core/core/server/data/tinybird/endpoints/api_top_pages_v2.pipe` (added)
- `ghost/core/core/server/data/tinybird/endpoints/api_top_sources_v2.pipe` (added)
- `ghost/core/core/server/data/tinybird/endpoints/api_top_utm_campaigns_v2.pipe` (added)
- `ghost/core/core/server/data/tinybird/endpoints/api_top_utm_contents_v2.pipe` (added)
- `ghost/core/core/server/data/tinybird/endpoints/api_top_utm_mediums_v2.pipe` (added)
- `ghost/core/core/server/data/tinybird/endpoints/api_top_utm_sources_v2.pipe` (added)
- `ghost/core/core/server/data/tinybird/endpoints/api_top_utm_terms_v2.pipe` (added)
- `ghost/core/core/server/data/tinybird/pipes/filtered_sessions_v2.pipe` (added)
- `ghost/core/core/server/data/tinybird/pipes/mv_session_data_v2.pipe` (added)
- `ghost/core/core/server/data/tinybird/tests/api_active_visitors_v2.yaml` (added)
- `ghost/core/core/server/data/tinybird/tests/api_kpis_v2.yaml` (added)
- `ghost/core/core/server/data/tinybird/tests/api_post_visitor_counts_v2.yaml` (added)
- `ghost/core/core/server/data/tinybird/tests/api_top_devices_v2.yaml` (added)
- `ghost/core/core/server/data/tinybird/tests/api_top_locations_v2.yaml` (added)
- `ghost/core/core/server/data/tinybird/tests/api_top_pages_v2.yaml` (added)
- `ghost/core/core/server/data/tinybird/tests/api_top_sources_v2.yaml` (added)
- `ghost/core/core/server/data/tinybird/tests/api_top_utm_campaigns_v2.yaml` (added)
- `ghost/core/core/server/data/tinybird/tests/api_top_utm_contents_v2.yaml` (added)
- `ghost/core/core/server/data/tinybird/tests/api_top_utm_mediums_v2.yaml` (added)
- `ghost/core/core/server/data/tinybird/tests/api_top_utm_sources_v2.yaml` (added)
- `ghost/core/core/server/data/tinybird/tests/api_top_utm_terms_v2.yaml` (added)
- `ghost/core/core/server/services/stats/ContentStatsService.js` (modified)
- `ghost/core/core/server/services/stats/utils/tinybird.js` (modified)
- `ghost/core/core/server/services/tinybird/TinybirdService.js` (modified)
- `ghost/core/test/unit/server/services/stats/utils/tinybird.test.js` (modified)

## Changed Entities

- `apps/admin-x-framework/src/providers/framework-provider.tsx:13-13` module `apps.admin-x-framework.src.providers.framework-provider`
- `apps/admin-x-framework/src/utils/stats-config.ts:16-20` module `apps.admin-x-framework.src.utils.stats-config`
- `ghost/core/core/server/api/endpoints/stats.js:128-128` module `ghost.core.core.server.api.endpoints.stats`
- `ghost/core/core/server/data/tinybird/README.md:81-82` module `ghost.core.core.server.data.tinybird.README`
- `ghost/core/core/server/data/tinybird/datasources/_mv_session_data_v2.datasource:1-16` module `ghost.core.core.server.data.tinybird.datasources._mv_session_data_v2`
- `ghost/core/core/server/data/tinybird/endpoints/README.md:10-10` module `ghost.core.core.server.data.tinybird.endpoints.README`
- `ghost/core/core/server/data/tinybird/endpoints/api_active_visitors_v2.pipe:1-15` module `ghost.core.core.server.data.tinybird.endpoints.api_active_visitors_v2`
- `ghost/core/core/server/data/tinybird/endpoints/api_kpis_v2.pipe:1-162` module `ghost.core.core.server.data.tinybird.endpoints.api_kpis_v2`
- `ghost/core/core/server/data/tinybird/endpoints/api_post_visitor_counts_v2.pipe:1-17` module `ghost.core.core.server.data.tinybird.endpoints.api_post_visitor_counts_v2`
- `ghost/core/core/server/data/tinybird/endpoints/api_top_devices_v2.pipe:1-28` module `ghost.core.core.server.data.tinybird.endpoints.api_top_devices_v2`
- `ghost/core/core/server/data/tinybird/endpoints/api_top_locations_v2.pipe:1-31` module `ghost.core.core.server.data.tinybird.endpoints.api_top_locations_v2`
- `ghost/core/core/server/data/tinybird/endpoints/api_top_pages_v2.pipe:1-39` module `ghost.core.core.server.data.tinybird.endpoints.api_top_pages_v2`
- `ghost/core/core/server/data/tinybird/endpoints/api_top_sources_v2.pipe:1-28` module `ghost.core.core.server.data.tinybird.endpoints.api_top_sources_v2`
- `ghost/core/core/server/data/tinybird/endpoints/api_top_utm_campaigns_v2.pipe:1-30` module `ghost.core.core.server.data.tinybird.endpoints.api_top_utm_campaigns_v2`
- `ghost/core/core/server/data/tinybird/endpoints/api_top_utm_contents_v2.pipe:1-30` module `ghost.core.core.server.data.tinybird.endpoints.api_top_utm_contents_v2`
- `ghost/core/core/server/data/tinybird/endpoints/api_top_utm_mediums_v2.pipe:1-30` module `ghost.core.core.server.data.tinybird.endpoints.api_top_utm_mediums_v2`
- `ghost/core/core/server/data/tinybird/endpoints/api_top_utm_sources_v2.pipe:1-30` module `ghost.core.core.server.data.tinybird.endpoints.api_top_utm_sources_v2`
- `ghost/core/core/server/data/tinybird/endpoints/api_top_utm_terms_v2.pipe:1-30` module `ghost.core.core.server.data.tinybird.endpoints.api_top_utm_terms_v2`
- `ghost/core/core/server/data/tinybird/pipes/filtered_sessions_v2.pipe:1-85` module `ghost.core.core.server.data.tinybird.pipes.filtered_sessions_v2`
- `ghost/core/core/server/data/tinybird/pipes/mv_session_data_v2.pipe:1-22` module `ghost.core.core.server.data.tinybird.pipes.mv_session_data_v2`
- `ghost/core/core/server/data/tinybird/tests/api_active_visitors_v2.yaml:1-24` module `ghost.core.core.server.data.tinybird.tests.api_active_visitors_v2`
- `ghost/core/core/server/data/tinybird/tests/api_kpis_v2.yaml:1-267` module `ghost.core.core.server.data.tinybird.tests.api_kpis_v2`
- `ghost/core/core/server/data/tinybird/tests/api_post_visitor_counts_v2.yaml:1-19` module `ghost.core.core.server.data.tinybird.tests.api_post_visitor_counts_v2`
- `ghost/core/core/server/data/tinybird/tests/api_top_devices_v2.yaml:1-62` module `ghost.core.core.server.data.tinybird.tests.api_top_devices_v2`
- `ghost/core/core/server/data/tinybird/tests/api_top_locations_v2.yaml:1-86` module `ghost.core.core.server.data.tinybird.tests.api_top_locations_v2`
- `ghost/core/core/server/data/tinybird/tests/api_top_pages_v2.yaml:1-135` module `ghost.core.core.server.data.tinybird.tests.api_top_pages_v2`
- `ghost/core/core/server/data/tinybird/tests/api_top_sources_v2.yaml:1-131` module `ghost.core.core.server.data.tinybird.tests.api_top_sources_v2`
- `ghost/core/core/server/data/tinybird/tests/api_top_utm_campaigns_v2.yaml:1-79` module `ghost.core.core.server.data.tinybird.tests.api_top_utm_campaigns_v2`
- `ghost/core/core/server/data/tinybird/tests/api_top_utm_contents_v2.yaml:1-81` module `ghost.core.core.server.data.tinybird.tests.api_top_utm_contents_v2`
- `ghost/core/core/server/data/tinybird/tests/api_top_utm_mediums_v2.yaml:1-79` module `ghost.core.core.server.data.tinybird.tests.api_top_utm_mediums_v2`
- `ghost/core/core/server/data/tinybird/tests/api_top_utm_sources_v2.yaml:1-88` module `ghost.core.core.server.data.tinybird.tests.api_top_utm_sources_v2`
- `ghost/core/core/server/data/tinybird/tests/api_top_utm_terms_v2.yaml:1-82` module `ghost.core.core.server.data.tinybird.tests.api_top_utm_terms_v2`
- `ghost/core/core/server/services/stats/ContentStatsService.js:33-33` module `ghost.core.core.server.services.stats.ContentStatsService`
- `ghost/core/core/server/services/stats/utils/tinybird.js:22-22` module `ghost.core.core.server.services.stats.utils.tinybird`
- `ghost/core/core/server/services/tinybird/TinybirdService.js:59-72` module `ghost.core.core.server.services.tinybird.TinybirdService`
- `ghost/core/test/unit/server/services/stats/utils/tinybird.test.js:73-86` module `ghost.core.test.unit.server.services.stats.utils.tinybird.test`

## Risk Signals

- `config_change` (0.86): Configuration file changed: ghost/core/core/server/data/tinybird/tests/api_active_visitors_v2.yaml.
- `config_change` (0.86): Configuration file changed: ghost/core/core/server/data/tinybird/tests/api_kpis_v2.yaml.
- `config_change` (0.86): Configuration file changed: ghost/core/core/server/data/tinybird/tests/api_post_visitor_counts_v2.yaml.
- `config_change` (0.86): Configuration file changed: ghost/core/core/server/data/tinybird/tests/api_top_devices_v2.yaml.
- `config_change` (0.86): Configuration file changed: ghost/core/core/server/data/tinybird/tests/api_top_locations_v2.yaml.
- `config_change` (0.86): Configuration file changed: ghost/core/core/server/data/tinybird/tests/api_top_pages_v2.yaml.
- `config_change` (0.86): Configuration file changed: ghost/core/core/server/data/tinybird/tests/api_top_sources_v2.yaml.
- `config_change` (0.86): Configuration file changed: ghost/core/core/server/data/tinybird/tests/api_top_utm_campaigns_v2.yaml.
- `config_change` (0.86): Configuration file changed: ghost/core/core/server/data/tinybird/tests/api_top_utm_contents_v2.yaml.
- `config_change` (0.86): Configuration file changed: ghost/core/core/server/data/tinybird/tests/api_top_utm_mediums_v2.yaml.
- `config_change` (0.86): Configuration file changed: ghost/core/core/server/data/tinybird/tests/api_top_utm_sources_v2.yaml.
- `config_change` (0.86): Configuration file changed: ghost/core/core/server/data/tinybird/tests/api_top_utm_terms_v2.yaml.
- `security_sensitive` (0.74): Security-sensitive keywords changed in ghost/core/core/server/data/tinybird/endpoints/api_active_visitors_v2.pipe.
- `security_sensitive` (0.74): Security-sensitive keywords changed in ghost/core/core/server/data/tinybird/endpoints/api_kpis_v2.pipe.
- `security_sensitive` (0.74): Security-sensitive keywords changed in ghost/core/core/server/data/tinybird/endpoints/api_post_visitor_counts_v2.pipe.
- `security_sensitive` (0.74): Security-sensitive keywords changed in ghost/core/core/server/data/tinybird/endpoints/api_top_devices_v2.pipe.
- `security_sensitive` (0.74): Security-sensitive keywords changed in ghost/core/core/server/data/tinybird/endpoints/api_top_locations_v2.pipe.
- `security_sensitive` (0.74): Security-sensitive keywords changed in ghost/core/core/server/data/tinybird/endpoints/api_top_pages_v2.pipe.
- `security_sensitive` (0.74): Security-sensitive keywords changed in ghost/core/core/server/data/tinybird/endpoints/api_top_sources_v2.pipe.
- `security_sensitive` (0.74): Security-sensitive keywords changed in ghost/core/core/server/data/tinybird/endpoints/api_top_utm_campaigns_v2.pipe.
- `security_sensitive` (0.74): Security-sensitive keywords changed in ghost/core/core/server/data/tinybird/endpoints/api_top_utm_contents_v2.pipe.
- `security_sensitive` (0.74): Security-sensitive keywords changed in ghost/core/core/server/data/tinybird/endpoints/api_top_utm_mediums_v2.pipe.
- `security_sensitive` (0.74): Security-sensitive keywords changed in ghost/core/core/server/data/tinybird/endpoints/api_top_utm_sources_v2.pipe.
- `security_sensitive` (0.74): Security-sensitive keywords changed in ghost/core/core/server/data/tinybird/endpoints/api_top_utm_terms_v2.pipe.
- `security_sensitive` (0.74): Security-sensitive keywords changed in ghost/core/core/server/data/tinybird/pipes/filtered_sessions_v2.pipe.
- `security_sensitive` (0.74): Security-sensitive keywords changed in ghost/core/core/server/data/tinybird/pipes/mv_session_data_v2.pipe.
- `security_sensitive` (0.74): Security-sensitive keywords changed in ghost/core/test/unit/server/services/stats/utils/tinybird.test.js.

## Evidence Index

- `diff:apps/admin-x-framework/src/providers/framework-provider.tsx:13` [diff]: apps/admin-x-framework/src/providers/framework-provider.tsx:13
- `diff:apps/admin-x-framework/src/providers/framework-provider.tsx:89` [diff]: apps/admin-x-framework/src/providers/framework-provider.tsx:89
- `diff:apps/admin-x-framework/src/providers/framework-provider.tsx:90` [diff]: apps/admin-x-framework/src/providers/framework-provider.tsx:90
- `diff:apps/admin-x-framework/src/providers/framework-provider.tsx:91` [diff]: apps/admin-x-framework/src/providers/framework-provider.tsx:91
- `diff:apps/admin-x-framework/src/utils/stats-config.ts:16` [diff]: apps/admin-x-framework/src/utils/stats-config.ts:16
- `diff:apps/admin-x-framework/src/utils/stats-config.ts:17` [diff]: apps/admin-x-framework/src/utils/stats-config.ts:17
- `diff:apps/admin-x-framework/src/utils/stats-config.ts:18` [diff]: apps/admin-x-framework/src/utils/stats-config.ts:18
- `diff:apps/admin-x-framework/src/utils/stats-config.ts:19` [diff]: apps/admin-x-framework/src/utils/stats-config.ts:19
- `diff:apps/admin-x-framework/src/utils/stats-config.ts:20` [diff]: apps/admin-x-framework/src/utils/stats-config.ts:20
- `diff:ghost/core/core/server/api/endpoints/stats.js:128` [diff]: ghost/core/core/server/api/endpoints/stats.js:128
- `diff:ghost/core/core/server/data/tinybird/README.md:81` [diff]: ghost/core/core/server/data/tinybird/README.md:81
- `diff:ghost/core/core/server/data/tinybird/README.md:82` [diff]: ghost/core/core/server/data/tinybird/README.md:82
- `diff:ghost/core/core/server/data/tinybird/datasources/_mv_session_data_v2.datasource:1` [diff]: ghost/core/core/server/data/tinybird/datasources/_mv_session_data_v2.datasource:1
- `diff:ghost/core/core/server/data/tinybird/datasources/_mv_session_data_v2.datasource:10` [diff]: ghost/core/core/server/data/tinybird/datasources/_mv_session_data_v2.datasource:10
- `diff:ghost/core/core/server/data/tinybird/datasources/_mv_session_data_v2.datasource:11` [diff]: ghost/core/core/server/data/tinybird/datasources/_mv_session_data_v2.datasource:11
- `diff:ghost/core/core/server/data/tinybird/datasources/_mv_session_data_v2.datasource:12` [diff]: ghost/core/core/server/data/tinybird/datasources/_mv_session_data_v2.datasource:12
- `diff:ghost/core/core/server/data/tinybird/datasources/_mv_session_data_v2.datasource:13` [diff]: ghost/core/core/server/data/tinybird/datasources/_mv_session_data_v2.datasource:13
- `diff:ghost/core/core/server/data/tinybird/datasources/_mv_session_data_v2.datasource:14` [diff]: ghost/core/core/server/data/tinybird/datasources/_mv_session_data_v2.datasource:14
- `diff:ghost/core/core/server/data/tinybird/datasources/_mv_session_data_v2.datasource:15` [diff]: ghost/core/core/server/data/tinybird/datasources/_mv_session_data_v2.datasource:15
- `diff:ghost/core/core/server/data/tinybird/datasources/_mv_session_data_v2.datasource:16` [diff]: ghost/core/core/server/data/tinybird/datasources/_mv_session_data_v2.datasource:16
- `diff:ghost/core/core/server/data/tinybird/datasources/_mv_session_data_v2.datasource:2` [diff]: ghost/core/core/server/data/tinybird/datasources/_mv_session_data_v2.datasource:2
- `diff:ghost/core/core/server/data/tinybird/datasources/_mv_session_data_v2.datasource:3` [diff]: ghost/core/core/server/data/tinybird/datasources/_mv_session_data_v2.datasource:3
- `diff:ghost/core/core/server/data/tinybird/datasources/_mv_session_data_v2.datasource:4` [diff]: ghost/core/core/server/data/tinybird/datasources/_mv_session_data_v2.datasource:4
- `diff:ghost/core/core/server/data/tinybird/datasources/_mv_session_data_v2.datasource:5` [diff]: ghost/core/core/server/data/tinybird/datasources/_mv_session_data_v2.datasource:5
- `diff:ghost/core/core/server/data/tinybird/datasources/_mv_session_data_v2.datasource:6` [diff]: ghost/core/core/server/data/tinybird/datasources/_mv_session_data_v2.datasource:6
- `diff:ghost/core/core/server/data/tinybird/datasources/_mv_session_data_v2.datasource:7` [diff]: ghost/core/core/server/data/tinybird/datasources/_mv_session_data_v2.datasource:7
- `diff:ghost/core/core/server/data/tinybird/datasources/_mv_session_data_v2.datasource:8` [diff]: ghost/core/core/server/data/tinybird/datasources/_mv_session_data_v2.datasource:8
- `diff:ghost/core/core/server/data/tinybird/datasources/_mv_session_data_v2.datasource:9` [diff]: ghost/core/core/server/data/tinybird/datasources/_mv_session_data_v2.datasource:9
- `diff:ghost/core/core/server/data/tinybird/endpoints/README.md:10` [diff]: ghost/core/core/server/data/tinybird/endpoints/README.md:10
- `diff:ghost/core/core/server/data/tinybird/endpoints/README.md:42` [diff]: ghost/core/core/server/data/tinybird/endpoints/README.md:42
- ... 1879 more evidence items omitted.
