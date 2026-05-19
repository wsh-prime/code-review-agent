# Review Report

## Summary

- Mode: `hybrid-live`
- Changed files: 3
- Changed entities: 3
- Risk signals: 0
- Findings: 0
- Needs human review: 0
- Discarded: 1
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
| Total latency | 5973 ms |
| Token in | 5827 |
| Token out | 146 |

- Iteration 0: 1 candidates, 0 verified, 0 uncertain, 0 kept, 0 rejected

## Context Budget Summary

| Metric | Value |
|---|---:|
| Strategy | `risk_first_v1` |
| Max input tokens | 9000 |
| Estimated input tokens | 5107 |
| Selected evidence | 3 |
| Omitted evidence | 106 |
| Context truncated | True |
| Review shards | 1 |
| Context requests | 0 |
| Refills | 0 |

## Findings

No findings.

Checked changed files, changed entities, deterministic risk signals, and evidence references. No high-confidence review finding was produced.

## Needs Human Review

None.

## Changed Files

- `apps/shade/src/components/ui/filters.tsx` (modified)
- `apps/stats/src/views/Stats/components/stats-filter.tsx` (modified)
- `apps/stats/src/views/Stats/layout/stats-header.tsx` (modified)

## Changed Entities

- `apps/shade/src/components/ui/filters.tsx:105-105` module `apps.shade.src.components.ui.filters`
- `apps/stats/src/views/Stats/components/stats-filter.tsx:93-93` module `apps.stats.src.views.Stats.components.stats-filter`
- `apps/stats/src/views/Stats/layout/stats-header.tsx:67-67` module `apps.stats.src.views.Stats.layout.stats-header`

## Risk Signals

None.

## Evidence Index

- `diff:apps/shade/src/components/ui/filters.tsx:105` [diff]: apps/shade/src/components/ui/filters.tsx:105
- `diff:apps/shade/src/components/ui/filters.tsx:1051` [diff]: apps/shade/src/components/ui/filters.tsx:1051
- `diff:apps/shade/src/components/ui/filters.tsx:1122` [diff]: apps/shade/src/components/ui/filters.tsx:1122
- `diff:apps/shade/src/components/ui/filters.tsx:1125` [diff]: apps/shade/src/components/ui/filters.tsx:1125
- `diff:apps/shade/src/components/ui/filters.tsx:1134` [diff]: apps/shade/src/components/ui/filters.tsx:1134
- `diff:apps/shade/src/components/ui/filters.tsx:1135` [diff]: apps/shade/src/components/ui/filters.tsx:1135
- `diff:apps/shade/src/components/ui/filters.tsx:1136` [diff]: apps/shade/src/components/ui/filters.tsx:1136
- `diff:apps/shade/src/components/ui/filters.tsx:1137` [diff]: apps/shade/src/components/ui/filters.tsx:1137
- `diff:apps/shade/src/components/ui/filters.tsx:1194` [diff]: apps/shade/src/components/ui/filters.tsx:1194
- `diff:apps/shade/src/components/ui/filters.tsx:1201` [diff]: apps/shade/src/components/ui/filters.tsx:1201
- `diff:apps/shade/src/components/ui/filters.tsx:1202` [diff]: apps/shade/src/components/ui/filters.tsx:1202
- `diff:apps/shade/src/components/ui/filters.tsx:1203` [diff]: apps/shade/src/components/ui/filters.tsx:1203
- `diff:apps/shade/src/components/ui/filters.tsx:1204` [diff]: apps/shade/src/components/ui/filters.tsx:1204
- `diff:apps/shade/src/components/ui/filters.tsx:1205` [diff]: apps/shade/src/components/ui/filters.tsx:1205
- `diff:apps/shade/src/components/ui/filters.tsx:1206` [diff]: apps/shade/src/components/ui/filters.tsx:1206
- `diff:apps/shade/src/components/ui/filters.tsx:1207` [diff]: apps/shade/src/components/ui/filters.tsx:1207
- `diff:apps/shade/src/components/ui/filters.tsx:122` [diff]: apps/shade/src/components/ui/filters.tsx:122
- `diff:apps/shade/src/components/ui/filters.tsx:1261` [diff]: apps/shade/src/components/ui/filters.tsx:1261
- `diff:apps/shade/src/components/ui/filters.tsx:1271` [diff]: apps/shade/src/components/ui/filters.tsx:1271
- `diff:apps/shade/src/components/ui/filters.tsx:1272` [diff]: apps/shade/src/components/ui/filters.tsx:1272
- `diff:apps/shade/src/components/ui/filters.tsx:1273` [diff]: apps/shade/src/components/ui/filters.tsx:1273
- `diff:apps/shade/src/components/ui/filters.tsx:1274` [diff]: apps/shade/src/components/ui/filters.tsx:1274
- `diff:apps/shade/src/components/ui/filters.tsx:1628` [diff]: apps/shade/src/components/ui/filters.tsx:1628
- `diff:apps/shade/src/components/ui/filters.tsx:1644` [diff]: apps/shade/src/components/ui/filters.tsx:1644
- `diff:apps/shade/src/components/ui/filters.tsx:2062` [diff]: apps/shade/src/components/ui/filters.tsx:2062
- `diff:apps/shade/src/components/ui/filters.tsx:2076` [diff]: apps/shade/src/components/ui/filters.tsx:2076
- `diff:apps/shade/src/components/ui/filters.tsx:2078` [diff]: apps/shade/src/components/ui/filters.tsx:2078
- `diff:apps/shade/src/components/ui/filters.tsx:2079` [diff]: apps/shade/src/components/ui/filters.tsx:2079
- `diff:apps/shade/src/components/ui/filters.tsx:2080` [diff]: apps/shade/src/components/ui/filters.tsx:2080
- `diff:apps/shade/src/components/ui/filters.tsx:2081` [diff]: apps/shade/src/components/ui/filters.tsx:2081
- ... 79 more evidence items omitted.
