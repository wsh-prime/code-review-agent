# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 4
- Changed entities: 4
- Risk signals: 2
- Findings: 2
- Needs human review: 0
- Discarded: 0
- Agent runs: 2
- Loop enabled: True
- Target repo modified: False

## Loop Summary

| Metric | Value |
|---|---:|
| Iterations | 1 / 1 |
| Converged | True |
| Fallback | False |
| Retry count | 0 |
| Total latency | 10024 ms |
| Token in | 7540 |
| Token out | 390 |

- Iteration 0: 2 candidates, 2 verified, 0 uncertain, 2 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `risk_first_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 6468 |
| Selected evidence | 4 |
| Omitted evidence | 200 |
| Context truncated | True |
| Review shards | 1 |
| Context requests | 0 |
| Refills | 0 |

## Findings

- `functionality` medium at `ghost/core/core/shared/config/env/config.development.json:26` (0.80)
  - Removing the 'useRpcPing' privacy config option disables the ability to control XML-RPC ping behavior via configuration, which may affect site discoverability for users who relied on this setting.
  - Suggestion: If the XML-RPC service is intentionally removed, ensure the config removal is coordinated with the service deletion. If the service is kept, preserve the config option.
  - Evidence: `diff_hunk:ghost/core/core/shared/config/env/config.development.json:23`

- `functionality` medium at `ghost/core/core/boot.js:313` (0.90)
  - The XML-RPC service module is removed from the service initialization in boot.js, but the corresponding config option 'useRpcPing' is also removed from the development config. This is consistent with removing the XML-RPC ping feature entirely, but the change removes a feature that previously notified external services (e.g., Ping-o-Matic) about new posts.
  - Suggestion: If the XML-RPC ping feature is intentionally being removed, ensure this is documented and communicated. If the feature is still needed, restore the service initialization and config option.
  - Evidence: `diff_hunk:ghost/core/core/boot.js:310`, `diff_hunk:ghost/core/core/shared/config/env/config.development.json:23`

## Needs Human Review

None.

## Changed Files

- `ghost/core/core/boot.js` (modified)
- `ghost/core/core/server/services/xmlrpc.js` (deleted)
- `ghost/core/core/shared/config/env/config.development.json` (modified)
- `ghost/core/test/unit/server/services/xmlrpc.test.js` (deleted)

## Changed Entities

- `ghost/core/core/boot.js:313-318` module `ghost.core.core.boot`
- `ghost/core/core/server/services/xmlrpc.js:1-134` module `ghost.core.core.server.services.xmlrpc`
- `ghost/core/core/shared/config/env/config.development.json:26-26` module `ghost.core.core.shared.config.env.config.development`
- `ghost/core/test/unit/server/services/xmlrpc.test.js:1-277` module `ghost.core.test.unit.server.services.xmlrpc.test`

## Risk Signals

- `security_sensitive` (0.74): Security-sensitive keywords changed in ghost/core/core/server/services/xmlrpc.js.
- `security_sensitive` (0.74): Security-sensitive keywords changed in ghost/core/test/unit/server/services/xmlrpc.test.js.

## Evidence Index

- `diff:ghost/core/core/boot.js:313` [diff]: ghost/core/core/boot.js:313
- `diff:ghost/core/core/boot.js:318` [diff]: ghost/core/core/boot.js:318
- `diff:ghost/core/core/boot.js:350` [diff]: ghost/core/core/boot.js:350
- `diff:ghost/core/core/boot.js:352` [diff]: ghost/core/core/boot.js:352
- `diff:ghost/core/core/boot.js:364` [diff]: ghost/core/core/boot.js:364
- `diff:ghost/core/core/boot.js:365` [diff]: ghost/core/core/boot.js:365
- `diff:ghost/core/core/boot.js:368` [diff]: ghost/core/core/boot.js:368
- `diff:ghost/core/core/boot.js:370` [diff]: ghost/core/core/boot.js:370
- `diff:ghost/core/core/boot.js:371` [diff]: ghost/core/core/boot.js:371
- `diff:ghost/core/core/boot.js:372` [diff]: ghost/core/core/boot.js:372
- `diff:ghost/core/core/server/services/xmlrpc.js:1` [diff]: ghost/core/core/server/services/xmlrpc.js:1
- `diff:ghost/core/core/server/services/xmlrpc.js:10` [diff]: ghost/core/core/server/services/xmlrpc.js:10
- `diff:ghost/core/core/server/services/xmlrpc.js:100` [diff]: ghost/core/core/server/services/xmlrpc.js:100
- `diff:ghost/core/core/server/services/xmlrpc.js:101` [diff]: ghost/core/core/server/services/xmlrpc.js:101
- `diff:ghost/core/core/server/services/xmlrpc.js:102` [diff]: ghost/core/core/server/services/xmlrpc.js:102
- `diff:ghost/core/core/server/services/xmlrpc.js:103` [diff]: ghost/core/core/server/services/xmlrpc.js:103
- `diff:ghost/core/core/server/services/xmlrpc.js:104` [diff]: ghost/core/core/server/services/xmlrpc.js:104
- `diff:ghost/core/core/server/services/xmlrpc.js:105` [diff]: ghost/core/core/server/services/xmlrpc.js:105
- `diff:ghost/core/core/server/services/xmlrpc.js:106` [diff]: ghost/core/core/server/services/xmlrpc.js:106
- `diff:ghost/core/core/server/services/xmlrpc.js:107` [diff]: ghost/core/core/server/services/xmlrpc.js:107
- `diff:ghost/core/core/server/services/xmlrpc.js:108` [diff]: ghost/core/core/server/services/xmlrpc.js:108
- `diff:ghost/core/core/server/services/xmlrpc.js:109` [diff]: ghost/core/core/server/services/xmlrpc.js:109
- `diff:ghost/core/core/server/services/xmlrpc.js:11` [diff]: ghost/core/core/server/services/xmlrpc.js:11
- `diff:ghost/core/core/server/services/xmlrpc.js:110` [diff]: ghost/core/core/server/services/xmlrpc.js:110
- `diff:ghost/core/core/server/services/xmlrpc.js:111` [diff]: ghost/core/core/server/services/xmlrpc.js:111
- `diff:ghost/core/core/server/services/xmlrpc.js:112` [diff]: ghost/core/core/server/services/xmlrpc.js:112
- `diff:ghost/core/core/server/services/xmlrpc.js:113` [diff]: ghost/core/core/server/services/xmlrpc.js:113
- `diff:ghost/core/core/server/services/xmlrpc.js:114` [diff]: ghost/core/core/server/services/xmlrpc.js:114
- `diff:ghost/core/core/server/services/xmlrpc.js:115` [diff]: ghost/core/core/server/services/xmlrpc.js:115
- `diff:ghost/core/core/server/services/xmlrpc.js:116` [diff]: ghost/core/core/server/services/xmlrpc.js:116
- ... 404 more evidence items omitted.
