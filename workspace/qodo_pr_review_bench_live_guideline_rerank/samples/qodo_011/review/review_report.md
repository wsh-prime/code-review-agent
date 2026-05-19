# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 14
- Changed entities: 14
- Risk signals: 10
- Findings: 0
- Needs human review: 1
- Discarded: 2
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
| Total latency | 92941 ms |
| Token in | 31649 |
| Token out | 637 |

- Iteration 0: 3 candidates, 1 verified, 1 uncertain, 0 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `file_risk_shards_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 24756 |
| Selected evidence | 23 |
| Omitted evidence | 409 |
| Context truncated | True |
| Review shards | 4 |
| Context requests | 0 |
| Refills | 0 |

## Findings

No findings.

Checked changed files, changed entities, deterministic risk signals, and evidence references. No high-confidence review finding was produced.

## Needs Human Review

- `security` high at `ghost/core/core/server/services/tinybird/TinybirdService.js:147` (0.50)
  - Removing `noTimestamp: true` from JWT signing options causes the token to include an `iat` (issued at) claim, which may break token validation on the Tinybird side if it expects tokens without timestamps.
  - Suggestion: Verify that Tinybird accepts JWT tokens with an `iat` claim. If not, restore `{noTimestamp: true}` or add explicit `iat` handling.
  - Evidence: `diff_hunk:ghost/core/core/server/services/tinybird/TinybirdService.js:144`

## Changed Files

- `ghost/core/core/server/data/tinybird/endpoints/api_kpis.pipe` (modified)
- `ghost/core/core/server/data/tinybird/endpoints/api_top_locations.pipe` (modified)
- `ghost/core/core/server/data/tinybird/endpoints/api_top_pages.pipe` (modified)
- `ghost/core/core/server/data/tinybird/pipes/filtered_sessions.pipe` (modified)
- `ghost/core/core/server/data/tinybird/tests/api_kpis.yaml` (modified)
- `ghost/core/core/server/data/tinybird/tests/api_top_locations.yaml` (modified)
- `ghost/core/core/server/data/tinybird/tests/api_top_pages.yaml` (modified)
- `ghost/core/core/server/data/tinybird/tests/api_top_sources.yaml` (modified)
- `ghost/core/core/server/data/tinybird/tests/api_top_utm_campaigns.yaml` (modified)
- `ghost/core/core/server/data/tinybird/tests/api_top_utm_contents.yaml` (modified)
- `ghost/core/core/server/data/tinybird/tests/api_top_utm_mediums.yaml` (modified)
- `ghost/core/core/server/data/tinybird/tests/api_top_utm_sources.yaml` (modified)
- `ghost/core/core/server/data/tinybird/tests/api_top_utm_terms.yaml` (modified)
- `ghost/core/core/server/services/tinybird/TinybirdService.js` (modified)

## Changed Entities

- `ghost/core/core/server/data/tinybird/endpoints/api_kpis.pipe:143-145` module `ghost.core.core.server.data.tinybird.endpoints.api_kpis`
- `ghost/core/core/server/data/tinybird/endpoints/api_top_locations.pipe:42-44` module `ghost.core.core.server.data.tinybird.endpoints.api_top_locations`
- `ghost/core/core/server/data/tinybird/endpoints/api_top_pages.pipe:43-47` module `ghost.core.core.server.data.tinybird.endpoints.api_top_pages`
- `ghost/core/core/server/data/tinybird/pipes/filtered_sessions.pipe:23-25` module `ghost.core.core.server.data.tinybird.pipes.filtered_sessions`
- `ghost/core/core/server/data/tinybird/tests/api_kpis.yaml:14-37` module `ghost.core.core.server.data.tinybird.tests.api_kpis`
- `ghost/core/core/server/data/tinybird/tests/api_top_locations.yaml:12-45` module `ghost.core.core.server.data.tinybird.tests.api_top_locations`
- `ghost/core/core/server/data/tinybird/tests/api_top_pages.yaml:11-27` module `ghost.core.core.server.data.tinybird.tests.api_top_pages`
- `ghost/core/core/server/data/tinybird/tests/api_top_sources.yaml:16-37` module `ghost.core.core.server.data.tinybird.tests.api_top_sources`
- `ghost/core/core/server/data/tinybird/tests/api_top_utm_campaigns.yaml:13-31` module `ghost.core.core.server.data.tinybird.tests.api_top_utm_campaigns`
- `ghost/core/core/server/data/tinybird/tests/api_top_utm_contents.yaml:15-36` module `ghost.core.core.server.data.tinybird.tests.api_top_utm_contents`
- `ghost/core/core/server/data/tinybird/tests/api_top_utm_mediums.yaml:13-32` module `ghost.core.core.server.data.tinybird.tests.api_top_utm_mediums`
- `ghost/core/core/server/data/tinybird/tests/api_top_utm_sources.yaml:16-39` module `ghost.core.core.server.data.tinybird.tests.api_top_utm_sources`
- `ghost/core/core/server/data/tinybird/tests/api_top_utm_terms.yaml:14-33` module `ghost.core.core.server.data.tinybird.tests.api_top_utm_terms`
- `ghost/core/core/server/services/tinybird/TinybirdService.js:51-54` module `ghost.core.core.server.services.tinybird.TinybirdService`

## Risk Signals

- `config_change` (0.86): Configuration file changed: ghost/core/core/server/data/tinybird/tests/api_kpis.yaml.
- `config_change` (0.86): Configuration file changed: ghost/core/core/server/data/tinybird/tests/api_top_locations.yaml.
- `config_change` (0.86): Configuration file changed: ghost/core/core/server/data/tinybird/tests/api_top_pages.yaml.
- `config_change` (0.86): Configuration file changed: ghost/core/core/server/data/tinybird/tests/api_top_sources.yaml.
- `config_change` (0.86): Configuration file changed: ghost/core/core/server/data/tinybird/tests/api_top_utm_campaigns.yaml.
- `config_change` (0.86): Configuration file changed: ghost/core/core/server/data/tinybird/tests/api_top_utm_contents.yaml.
- `config_change` (0.86): Configuration file changed: ghost/core/core/server/data/tinybird/tests/api_top_utm_mediums.yaml.
- `config_change` (0.86): Configuration file changed: ghost/core/core/server/data/tinybird/tests/api_top_utm_sources.yaml.
- `config_change` (0.86): Configuration file changed: ghost/core/core/server/data/tinybird/tests/api_top_utm_terms.yaml.
- `security_sensitive` (0.74): Security-sensitive keywords changed in ghost/core/core/server/services/tinybird/TinybirdService.js.

## Evidence Index

- `diff:ghost/core/core/server/data/tinybird/endpoints/api_kpis.pipe:143` [diff]: ghost/core/core/server/data/tinybird/endpoints/api_kpis.pipe:143
- `diff:ghost/core/core/server/data/tinybird/endpoints/api_kpis.pipe:144` [diff]: ghost/core/core/server/data/tinybird/endpoints/api_kpis.pipe:144
- `diff:ghost/core/core/server/data/tinybird/endpoints/api_kpis.pipe:145` [diff]: ghost/core/core/server/data/tinybird/endpoints/api_kpis.pipe:145
- `diff:ghost/core/core/server/data/tinybird/endpoints/api_top_locations.pipe:42` [diff]: ghost/core/core/server/data/tinybird/endpoints/api_top_locations.pipe:42
- `diff:ghost/core/core/server/data/tinybird/endpoints/api_top_locations.pipe:43` [diff]: ghost/core/core/server/data/tinybird/endpoints/api_top_locations.pipe:43
- `diff:ghost/core/core/server/data/tinybird/endpoints/api_top_locations.pipe:44` [diff]: ghost/core/core/server/data/tinybird/endpoints/api_top_locations.pipe:44
- `diff:ghost/core/core/server/data/tinybird/endpoints/api_top_pages.pipe:43` [diff]: ghost/core/core/server/data/tinybird/endpoints/api_top_pages.pipe:43
- `diff:ghost/core/core/server/data/tinybird/endpoints/api_top_pages.pipe:44` [diff]: ghost/core/core/server/data/tinybird/endpoints/api_top_pages.pipe:44
- `diff:ghost/core/core/server/data/tinybird/endpoints/api_top_pages.pipe:45` [diff]: ghost/core/core/server/data/tinybird/endpoints/api_top_pages.pipe:45
- `diff:ghost/core/core/server/data/tinybird/endpoints/api_top_pages.pipe:46` [diff]: ghost/core/core/server/data/tinybird/endpoints/api_top_pages.pipe:46
- `diff:ghost/core/core/server/data/tinybird/endpoints/api_top_pages.pipe:47` [diff]: ghost/core/core/server/data/tinybird/endpoints/api_top_pages.pipe:47
- `diff:ghost/core/core/server/data/tinybird/pipes/filtered_sessions.pipe:23` [diff]: ghost/core/core/server/data/tinybird/pipes/filtered_sessions.pipe:23
- `diff:ghost/core/core/server/data/tinybird/pipes/filtered_sessions.pipe:24` [diff]: ghost/core/core/server/data/tinybird/pipes/filtered_sessions.pipe:24
- `diff:ghost/core/core/server/data/tinybird/pipes/filtered_sessions.pipe:25` [diff]: ghost/core/core/server/data/tinybird/pipes/filtered_sessions.pipe:25
- `diff:ghost/core/core/server/data/tinybird/tests/api_kpis.yaml:14` [diff]: ghost/core/core/server/data/tinybird/tests/api_kpis.yaml:14
- `diff:ghost/core/core/server/data/tinybird/tests/api_kpis.yaml:15` [diff]: ghost/core/core/server/data/tinybird/tests/api_kpis.yaml:15
- `diff:ghost/core/core/server/data/tinybird/tests/api_kpis.yaml:16` [diff]: ghost/core/core/server/data/tinybird/tests/api_kpis.yaml:16
- `diff:ghost/core/core/server/data/tinybird/tests/api_kpis.yaml:17` [diff]: ghost/core/core/server/data/tinybird/tests/api_kpis.yaml:17
- `diff:ghost/core/core/server/data/tinybird/tests/api_kpis.yaml:18` [diff]: ghost/core/core/server/data/tinybird/tests/api_kpis.yaml:18
- `diff:ghost/core/core/server/data/tinybird/tests/api_kpis.yaml:19` [diff]: ghost/core/core/server/data/tinybird/tests/api_kpis.yaml:19
- `diff:ghost/core/core/server/data/tinybird/tests/api_kpis.yaml:20` [diff]: ghost/core/core/server/data/tinybird/tests/api_kpis.yaml:20
- `diff:ghost/core/core/server/data/tinybird/tests/api_kpis.yaml:21` [diff]: ghost/core/core/server/data/tinybird/tests/api_kpis.yaml:21
- `diff:ghost/core/core/server/data/tinybird/tests/api_kpis.yaml:22` [diff]: ghost/core/core/server/data/tinybird/tests/api_kpis.yaml:22
- `diff:ghost/core/core/server/data/tinybird/tests/api_kpis.yaml:23` [diff]: ghost/core/core/server/data/tinybird/tests/api_kpis.yaml:23
- `diff:ghost/core/core/server/data/tinybird/tests/api_kpis.yaml:24` [diff]: ghost/core/core/server/data/tinybird/tests/api_kpis.yaml:24
- `diff:ghost/core/core/server/data/tinybird/tests/api_kpis.yaml:25` [diff]: ghost/core/core/server/data/tinybird/tests/api_kpis.yaml:25
- `diff:ghost/core/core/server/data/tinybird/tests/api_kpis.yaml:26` [diff]: ghost/core/core/server/data/tinybird/tests/api_kpis.yaml:26
- `diff:ghost/core/core/server/data/tinybird/tests/api_kpis.yaml:27` [diff]: ghost/core/core/server/data/tinybird/tests/api_kpis.yaml:27
- `diff:ghost/core/core/server/data/tinybird/tests/api_kpis.yaml:28` [diff]: ghost/core/core/server/data/tinybird/tests/api_kpis.yaml:28
- `diff:ghost/core/core/server/data/tinybird/tests/api_kpis.yaml:29` [diff]: ghost/core/core/server/data/tinybird/tests/api_kpis.yaml:29
- ... 402 more evidence items omitted.
