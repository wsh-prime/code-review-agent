# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 36
- Changed entities: 36
- Risk signals: 27
- Findings: 0
- Needs human review: 2
- Discarded: 1
- Agent runs: 14
- Loop enabled: True
- Target repo modified: False

## Loop Summary

| Metric | Value |
|---|---:|
| Iterations | 1 / 1 |
| Converged | False |
| Fallback | False |
| Retry count | 5 |
| Total latency | 420278 ms |
| Token in | 77802 |
| Token out | 2641 |

- Iteration 0: 4 candidates, 3 verified, 3 uncertain, 0 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `file_risk_shards_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 54997 |
| Selected evidence | 55 |
| Omitted evidence | 1295 |
| Context truncated | True |
| Review shards | 9 |
| Context requests | 15 |
| Refills | 4 |

## Findings

No findings.

Checked changed files, changed entities, deterministic risk signals, and evidence references. No high-confidence review finding was produced.

## Needs Human Review

- `backward_compatibility` high at `ghost/core/core/server/api/endpoints/stats.js:128` (0.50)
  - Removing 'tb_version' from allowed query parameters will break existing clients that send this parameter, causing requests to fail or be silently ignored.
  - Suggestion: If 'tb_version' is no longer needed, consider deprecating it first or adding a fallback that accepts but ignores the parameter to avoid breaking existing integrations.
  - Evidence: `diff_hunk:ghost/core/core/server/api/endpoints/stats.js:125`

- `bug_risk` high at `ghost/core/core/server/services/stats/utils/tinybird.js:38` (0.50)
  - The patch removes the `localEnabled` guard that previously prevented versioned pipe URLs when local mode was enabled. Now, if `statsConfig.version` is set, the versioned URL is always used, which may break local development or testing where the versioned pipe does not exist.
  - Suggestion: Restore the `localEnabled` check or add a similar condition to ensure versioned URLs are only used when appropriate (e.g., not in local/dev mode).
  - Evidence: `diff_hunk:ghost/core/core/server/services/stats/utils/tinybird.js:32`

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
