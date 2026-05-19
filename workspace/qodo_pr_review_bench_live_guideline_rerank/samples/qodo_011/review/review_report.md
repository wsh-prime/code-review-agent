# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 14
- Changed entities: 14
- Risk signals: 10
- Findings: 2
- Needs human review: 0
- Discarded: 0
- Agent runs: 6
- Loop enabled: True
- Target repo modified: False

## Loop Summary

| Metric | Value |
|---|---:|
| Iterations | 1 / 1 |
| Converged | True |
| Fallback | False |
| Retry count | 1 |
| Total latency | 111095 ms |
| Token in | 34842 |
| Token out | 690 |

- Iteration 0: 3 candidates, 3 verified, 0 uncertain, 3 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `file_risk_shards_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 27299 |
| Selected evidence | 25 |
| Omitted evidence | 407 |
| Context truncated | True |
| Review shards | 4 |
| Context requests | 1 |
| Refills | 1 |

## Findings

- `security` high at `ghost/core/core/server/services/tinybird/TinybirdService.js:146` (0.90)
  - Removing `noTimestamp: true` from JWT signing options exposes the token to timestamp-based attacks (e.g., replay) by including the `iat` claim, which was previously suppressed.
  - Suggestion: Restore `noTimestamp: true` or explicitly set `{noTimestamp: true}` in the jwt.sign options to maintain the original security posture.
  - Evidence: `diff:ghost/core/core/server/services/tinybird/TinybirdService.js:146`, `diff:ghost/core/core/server/services/tinybird/TinybirdService.js:147`, `diff_hunk:ghost/core/core/server/services/tinybird/TinybirdService.js:144`

- `correctness` medium at `ghost/core/core/server/services/tinybird/TinybirdService.js:51` (0.85)
  - Removing 'api_top_browsers', 'api_top_devices', and 'api_top_os' from TINYBIRD_PIPES without corresponding removal of test cases that filter by browser and device will cause test failures for the removed pipes.
  - Suggestion: Either keep the pipes in the list or remove the associated test cases that depend on them.
  - Evidence: `diff_hunk:ghost/core/core/server/services/tinybird/TinybirdService.js:48`, `diff_hunk:ghost/core/core/server/data/tinybird/tests/api_top_utm_terms.yaml:11`

## Needs Human Review

None.

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
