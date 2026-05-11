# Code Review Agent Harness

Evidence-first local code review harness for AI-generated patches.

## What Is This

`code-review-agent` is a local PR pre-review harness built for AI coding workflows (Codex / Cursor / Claude Code). Instead of piping raw diffs to an LLM and hoping for useful comments, it constructs **traceable evidence** first, then lets constrained agents review under schema and verifier guards.

**Core rule**: every finding must reference verifiable `evidence_ids`. No evidence, no output.

## Why Not Just Call an LLM

| Problem | What happens | Our answer |
|---|---|---|
| **Correlated failure** | Same-family model generates and reviews code — errors echo instead of cancel | Deterministic tools build evidence first; reviewer and critic use cross-strategy |
| **High false positives** | Bare LLM chases recall, floods PR with noise | GroundingVerifier + Filter discard ungrounded, style-only, low-signal issues |
| **Unreproducible eval** | LLM-as-Judge measures prompt artifacts, not real ability | Planted-bug oracle with deterministic file + category + line-range matching |

## Architecture

```
Repository + unified diff
  │
  ├─ Deterministic Tool Layer
  │   diff parser → AST repo map → changed entities
  │   → risk classification (10 tags) → evidence package (6 evidence kinds)
  │
  ├─ Agent Layer (3 modes)
  │   rules:       deterministic baseline, no API needed
  │   hybrid-fake: fake agents, full loop, no API, for testing
  │   hybrid-live: OpenAI-compatible API, real inference
  │
  ├─ Review Loop
  │   ReviewAgent → GroundingVerifier → CriticAgent
  │       ↑              (zero API)         │
  │       └──── PriorFeedback ◄─── uncertain items
  │
  ├─ Quality Control
  │   verifier: evidence exists? file in diff? line in hunk?
  │   critic:   precision-biased, downgrades weak findings
  │   filter:   dedup, discard style-only, route low-confidence to human
  │
  └─ Output
      review_report.json (machine) + review_report.md (human)
      loop_checkpoint.json (resume) + tracing (latency, tokens, retries)
```

## Quick Start

```bash
pip install -e ".[dev]"

# Build repo map (optional, improves accuracy)
code-review-agent map --repo examples/demo_repo --out outputs/demo-map

# Run review on a patch
code-review-agent review \
  --repo examples/demo_repo \
  --diff examples/demo_repo/patches/case_001_test_gap.patch \
  --out outputs/demo-review

# Run with iterative loop (no API needed)
code-review-agent review \
  --repo examples/demo_repo \
  --diff examples/demo_repo/patches/case_001_test_gap.patch \
  --out outputs/demo-loop \
  --mode hybrid-fake --max-iter 2

# Run eval benchmark
code-review-agent eval --cases examples/eval_cases --out outputs/demo-eval --mode all
```

## Commands

| Command | Purpose | Needs API |
|---|---|---|
| `map` | Scan repo, build AST symbol table, imports, related tests, style baseline | No |
| `hygiene` | Identify experiment scripts, temp docs, process artifacts | No |
| `review` | Parse diff, build evidence, run review pipeline, output report | `rules`/`hybrid-fake`: No · `hybrid-live`: Yes |
| `eval` | Run planted-bug benchmark, output precision/recall/no-finding accuracy | No |

## Sample Output

`case_001_test_gap.patch` triggers a high-quality finding:

```
Category : test_gap
File     : src/shop/service.py
Severity : medium
Message  : Business logic changed while related tests exist but were not updated.
Evidence :
  - diff:src/shop/service.py:18
  - test_discovery:tests/test_service.py
```

`case_005_no_finding_doc_only.patch` correctly produces **No Finding** — the system stays silent on doc-only changes.

## Evidence System

Every `ReviewIssue` must reference entries in the `EvidencePackage.evidence_index`:

| Kind | Example ID | Meaning |
|---|---|---|
| `diff` | `diff:src/svc.py:35` | Single changed line |
| `diff_hunk` | `diff_hunk:src/svc.py:30` | Hunk window with context |
| `entity` | `entity:src/svc.py:Svc.run` | Changed AST symbol |
| `risk` | `risk:test_gap:src/svc.py` | Deterministic risk signal |
| `test_discovery` | `test_discovery:tests/test_svc.py` | Related test file |
| `hygiene` | `hygiene:scripts/poc.py` | File hygiene classification |

Issues with missing, invalid, or ungrounded evidence are **automatically discarded** by the GroundingVerifier and Filter layers.

## Review Loop

The iterative harness runs a bounded `Reviewer → Verifier → Critic` loop:

- **GroundingVerifier** (deterministic, zero API cost): filters hallucinated findings before they reach the Critic
- **CriticAgent** (precision-biased): classifies issues as `keep` / `uncertain` / `reject`
- **PriorFeedback**: uncertain items are fed back to the Reviewer as structured feedback
- **Convergence**: stops when no uncertain items remain, issue set stabilizes, or `max_iter` is reached

Supports checkpoint/resume, exponential-backoff retry, and per-shard fallback for `hybrid-live`.

## Context Budget (Large Diffs)

Large diffs are split into token-aware shards (≤ 9000 tokens each). Each shard gets a compact manifest with `diff_hunk` as the primary evidence. Models can request one round of context refill from 4 allowed types (`same_file_more_evidence`, `related_tests`, `related_symbol`, `risk_evidence`).

A single shard failure does not abort the entire review — other shards continue, and the failure is logged as audit info.

## Eval

Built-in 7-case planted-bug benchmark with **deterministic oracle** (no LLM judge):

```
finding.file == ground_truth.file
AND finding.category == ground_truth.category
AND line_range_overlap >= threshold
```

| Variant | Recall | Spurious/PR | Precision | No-finding Acc | Evidence Cov |
|---|---:|---:|---:|---:|---:|
| `rules` | 0.60 | 0.14 | 0.75 | 1.00 | 1.00 |
| `hybrid-fake-iter1` | 1.00 | 0.71 | 0.50 | 1.00 | 1.00 |
| `hybrid-fake-iter2` | 1.00 | 0.71 | 0.50 | 1.00 | 1.00 |

Three threshold profiles (`strict` / `balanced` / `recall`) generate a precision-recall frontier.

## Live Mode

```bash
# Set up credentials
cp scripts/review-live.env.example scripts/review-live.env.local
# Edit: SILICONFLOW_API_KEY / SILICONFLOW_MODEL / SILICONFLOW_BASE_URL

# Run live review
powershell -ExecutionPolicy Bypass -File scripts/review-live.ps1 `
  -Repo examples/demo_repo -Diff examples/demo_repo/demo.patch `
  -Out outputs/demo-live -Mode hybrid-live
```

Latest live run (17 changed files, 97 entities, 82 risk signals):
- 6 primary shards + 6 refill shards, 13 agent runs (all `ok`)
- 87K input tokens, 8.5K output tokens
- 5 findings, 5 needs-human-review, 2 discarded, 0 fallback

## Engineering

- **Zero runtime dependencies** — stdlib only (`ast`, `json`, `pathlib`, `dataclasses`, `urllib`)
- **175 tests**, all passing — 23 test files covering every module
- **mypy clean** — 34 source files, 0 type errors
- **CI** — GitHub Actions: pytest (Python 3.10 + 3.12 matrix) + mypy
- **42 dataclasses** with `slots=True` — type-safe data contracts, no raw dicts between modules

## Development

```bash
pip install -e ".[dev]"
python -m pytest tests/ -v
python -m mypy src/code_review_agent/ --ignore-missing-imports
code-review-agent --help
```

## Limitations

- Python repos and unified diffs only (multi-language is post-MVP)
- Local CLI — no GitHub PR comment publishing
- Read-only — never modifies the target repo
- `hybrid-live` quality depends on the backing model; deterministic eval covers the harness, not model capability
- Built-in benchmark is for development regression, not an external authority

## Design References

| Decision | Paper | Key argument |
|---|---|---|
| Evidence before LLM | Zietsman 2026 (2603.25773) | Same-family LLM review → correlated failure |
| `no_finding_accuracy` metric | Pereira et al. 2026 (2603.11078) | Staying silent is the scarce capability |
| Deterministic oracle | Zhao et al. 2026 (2604.16790) | LLM judge measures prompt artifacts |
| Metadata redaction | Mitropoulos et al. 2026 (2603.18740) | PR title biases LLM judgment via framing |
| Risk tags as rubric | Li et al. 2026 (2604.14261) | Explicit rubric beats free-form generation |
| Design constraint checks | Yu et al. 2026 (2604.05955) | Test pass rate overestimates patch quality |
