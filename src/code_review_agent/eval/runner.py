"""Run deterministic review eval benchmarks."""

from __future__ import annotations

import json
import os
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from code_review_agent.eval.cases import EvalCase, load_eval_cases
from code_review_agent.eval.metrics import evaluate_case, summarize_case_results
from code_review_agent.review.pipeline import run_review_pipeline


EVAL_SCHEMA_VERSION = "1.1"
PROFILE_THRESHOLDS: dict[str, float] = {
    "strict": 0.75,
    "balanced": 0.5,
    "recall": 0.25,
}
SUPPORTED_EVAL_MODES = {"rules", "hybrid-fake", "all"}


EVAL_VARIANTS: dict[str, dict[str, Any]] = {
    "rules": {
        "pipeline_mode": "rules",
        "max_iter": 1,
        "description": "Deterministic rules baseline.",
    },
    "hybrid-fake-iter1": {
        "pipeline_mode": "hybrid-fake",
        "max_iter": 1,
        "description": "Fake hybrid agent with single-pass loop behavior.",
    },
    "hybrid-fake-iter2": {
        "pipeline_mode": "hybrid-fake",
        "max_iter": 2,
        "description": "Fake hybrid agent with critic-to-reviewer loop enabled.",
    },
}


def run_eval_benchmark(
    cases_root: Path | str,
    out_path: Path | str,
    *,
    mode: str = "rules",
) -> dict[str, Any]:
    """Run review benchmark cases and write eval reports."""

    if mode not in SUPPORTED_EVAL_MODES:
        raise ValueError("Supported eval modes are: rules, hybrid-fake, all.")

    root = Path(cases_root)
    out = Path(out_path)
    repo = root / "demo_repo"
    if not repo.exists():
        raise FileNotFoundError(f"Missing eval demo repo: {repo}")

    cases = load_eval_cases(root)
    variants = _variants_for_mode(mode)
    out.mkdir(parents=True, exist_ok=True)

    case_results: list[dict[str, Any]] = []
    metrics_by_variant: dict[str, dict[str, Any]] = {}
    profile_frontier: list[dict[str, Any]] = []

    for variant in variants:
        reports_by_case = _run_variant(repo, out, variant, cases)
        metrics_by_variant[variant] = {}
        for profile, threshold in PROFILE_THRESHOLDS.items():
            profile_results = [
                _evaluate_report(
                    case,
                    reports_by_case[case.case_id],
                    variant=variant,
                    profile=profile,
                    overlap_threshold=threshold,
                )
                for case in cases
            ]
            summary = summarize_case_results(profile_results)
            summary["evidence_coverage"] = _evidence_coverage(profile_results)
            summary["overlap_threshold"] = threshold
            summary.update(_review_burden_summary(profile_results))
            metrics_by_variant[variant][profile] = summary
            profile_frontier.append(
                {
                    "variant": variant,
                    "profile": profile,
                    **summary,
                }
            )
            case_results.extend(profile_results)

    metrics = {
        "schema_version": EVAL_SCHEMA_VERSION,
        "mode": mode,
        "case_count": len(cases),
        "variants": metrics_by_variant,
        "variant_descriptions": {
            variant: EVAL_VARIANTS[variant]["description"] for variant in variants
        },
        "profile_frontier": profile_frontier,
        "phase16_smoke": (
            _run_phase16_smoke(repo, out, cases) if mode == "all" else {}
        ),
        "target_repo_modified": False,
    }
    case_results_doc = {
        "schema_version": EVAL_SCHEMA_VERSION,
        "mode": mode,
        "case_results": case_results,
        "target_repo_modified": False,
    }

    (out / "metrics.json").write_text(
        json.dumps(metrics, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (out / "case_results.json").write_text(
        json.dumps(case_results_doc, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (out / "eval_report.md").write_text(
        render_eval_markdown(metrics, case_results),
        encoding="utf-8",
    )
    return metrics


def render_eval_markdown(
    metrics: dict[str, Any], case_results: list[dict[str, Any]]
) -> str:
    """Render a compact Markdown eval report."""

    lines = [
        "# Eval Report",
        "",
        "## Summary",
        "",
        f"- Mode: `{metrics['mode']}`",
        f"- Cases: {metrics['case_count']}",
        f"- Target repo modified: {metrics['target_repo_modified']}",
        "",
        "## Profile Frontier",
        "",
        "| Variant | Profile | Recall | Spurious/PR | Precision | No-finding Accuracy | Evidence Coverage | Needs Human Review | Discarded | Loop Converged | Checkpoints | Fallback | Retry | Trace Runs |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for item in metrics["profile_frontier"]:
        lines.append(
            "| "
            f"`{item['variant']}` | "
            f"`{item['profile']}` | "
            f"{item['recall']:.4f} | "
            f"{item['false_positives_per_pr']:.4f} | "
            f"{item['precision']:.4f} | "
            f"{item['no_finding_accuracy']:.4f} | "
            f"{item['evidence_coverage']:.4f} | "
            f"{item['needs_human_review_count']} | "
            f"{item['discarded_count']} | "
            f"{item['loop_converged_count']} | "
            f"{item['checkpoint_written_count']} | "
            f"{item['fallback_used_count']} | "
            f"{item['total_retry_count']} | "
            f"{item['tracing_run_count']} |"
        )

    smoke = metrics.get("phase16_smoke", {})
    if smoke:
        checkpoint_resume = smoke["checkpoint_resume"]
        fallback_rules = smoke["fallback_rules"]
        lines.extend(
            [
                "",
                "## Phase 16 Reliability Smoke",
                "",
                "| Check | Result |",
                "|---|---:|",
                f"| Checkpoint written | {_yes_no(checkpoint_resume['checkpoint_written'])} |",
                f"| Resume used | {_yes_no(checkpoint_resume['resume_used'])} |",
                f"| Resume ignored reason | `{checkpoint_resume['resume_ignored_reason'] or ''}` |",
                f"| Fallback mode | `{fallback_rules['mode']}` |",
                f"| Fallback used | {_yes_no(fallback_rules['fallback_used'])} |",
                f"| Fallback reason present | {_yes_no(fallback_rules['fallback_reason_present'])} |",
                f"| Fallback agent status | `{', '.join(fallback_rules['agent_statuses'])}` |",
            ]
        )

    balanced = [result for result in case_results if result["profile"] == "balanced"]
    lines.extend(
        [
            "",
            "## Balanced Case Results",
            "",
            "| Variant | Case | TP | FP | FN | No Finding Correct | Key Bug Included | Surfaced Issues |",
            "|---|---|---:|---:|---:|---|---|---:|",
        ]
    )
    for result in balanced:
        lines.append(
            "| "
            f"`{result['variant']}` | "
            f"`{result['case_id']}` | "
            f"{result['true_positives']} | "
            f"{result['false_positives']} | "
            f"{result['false_negatives']} | "
            f"{_yes_no(result['no_finding_correct'])} | "
            f"{_yes_no(result['key_bug_inclusion'])} | "
            f"{result['surface_issue_count']} |"
        )

    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- Oracle: file equality, category equality, and deterministic line-range overlap.",
            "- LLM judges are not used.",
            "- Surfaced issues include findings and needs-human-review items because both consume reviewer attention.",
            "",
        ]
    )
    return "\n".join(lines)


def _run_variant(
    repo: Path,
    out: Path,
    variant: str,
    cases: list[EvalCase],
) -> dict[str, dict[str, Any]]:
    reports: dict[str, dict[str, Any]] = {}
    variant_config = EVAL_VARIANTS[variant]
    for case in cases:
        report = run_review_pipeline(
            repo,
            case.patch_path,
            out / "runs" / variant / case.case_id,
            mode=variant_config["pipeline_mode"],
            max_iter=variant_config["max_iter"],
        )
        reports[case.case_id] = report
    return reports


def _evaluate_report(
    case: EvalCase,
    report: dict[str, Any],
    *,
    variant: str,
    profile: str,
    overlap_threshold: float,
) -> dict[str, Any]:
    surface_issues = _issues_for_oracle(report)
    result = evaluate_case(
        surface_issues,
        case.ground_truth,
        overlap_threshold=overlap_threshold,
    )
    result.update(
        {
            "variant": variant,
            "profile": profile,
            "overlap_threshold": overlap_threshold,
            "patch": case.patch,
            "finding_count": len(report.get("findings", [])),
            "needs_human_review_count": len(report.get("needs_human_review", [])),
            "discarded_count": len(report.get("discarded", [])),
            "surface_issue_count": len(surface_issues),
            "surface_issue_with_evidence_count": sum(
                1 for issue in surface_issues if issue.get("evidence_ids")
            ),
            "loop_enabled": bool(report.get("summary", {}).get("loop_enabled", False)),
            "loop_converged": bool(
                report.get("summary", {}).get("loop_converged", False)
            ),
            "loop_iterations_completed": int(
                report.get("summary", {}).get("loop_iterations_completed", 0)
            ),
            "checkpoint_written": _checkpoint_written(report),
            "fallback_used": bool(report.get("summary", {}).get("fallback_used", False)),
            "resume_used": bool(report.get("summary", {}).get("resume_used", False)),
            "resume_ignored": bool(
                report.get("summary", {}).get("resume_ignored_reason")
            ),
            "total_retry_count": int(
                report.get("tracing", {}).get("total_retry_count", 0)
            ),
            "tracing_run_count": int(report.get("tracing", {}).get("run_count", 0)),
            "tracing_status_counts": dict(
                report.get("tracing", {}).get("status_counts", {})
            ),
            "review_summary": dict(report.get("summary", {})),
        }
    )
    return result


def _evidence_coverage(case_results: list[dict[str, Any]]) -> float:
    issue_count = sum(result["surface_issue_count"] for result in case_results)
    with_evidence_count = sum(
        result["surface_issue_with_evidence_count"] for result in case_results
    )
    if issue_count == 0:
        return 0.0
    return round(with_evidence_count / issue_count, 4)


def _review_burden_summary(case_results: list[dict[str, Any]]) -> dict[str, Any]:
    case_count = len(case_results)
    needs_human_review_count = sum(
        result["needs_human_review_count"] for result in case_results
    )
    discarded_count = sum(result["discarded_count"] for result in case_results)
    finding_count = sum(result["finding_count"] for result in case_results)
    surface_issue_count = sum(result["surface_issue_count"] for result in case_results)
    loop_enabled_count = sum(1 for result in case_results if result["loop_enabled"])
    loop_converged_count = sum(1 for result in case_results if result["loop_converged"])
    loop_iterations_completed = sum(
        result["loop_iterations_completed"] for result in case_results
    )
    checkpoint_written_count = sum(
        1 for result in case_results if result["checkpoint_written"]
    )
    fallback_used_count = sum(1 for result in case_results if result["fallback_used"])
    resume_used_count = sum(1 for result in case_results if result["resume_used"])
    resume_ignored_count = sum(1 for result in case_results if result["resume_ignored"])
    total_retry_count = sum(result["total_retry_count"] for result in case_results)
    tracing_run_count = sum(result["tracing_run_count"] for result in case_results)
    return {
        "finding_count": finding_count,
        "needs_human_review_count": needs_human_review_count,
        "discarded_count": discarded_count,
        "surface_issue_count": surface_issue_count,
        "avg_needs_human_review_per_pr": _safe_ratio(
            needs_human_review_count, case_count
        ),
        "avg_discarded_per_pr": _safe_ratio(discarded_count, case_count),
        "loop_enabled_count": loop_enabled_count,
        "loop_converged_count": loop_converged_count,
        "loop_iterations_completed": loop_iterations_completed,
        "checkpoint_written_count": checkpoint_written_count,
        "fallback_used_count": fallback_used_count,
        "resume_used_count": resume_used_count,
        "resume_ignored_count": resume_ignored_count,
        "total_retry_count": total_retry_count,
        "tracing_run_count": tracing_run_count,
        "tracing_status_counts": _status_counts(case_results),
    }


def _safe_ratio(numerator: int | float, denominator: int | float) -> float:
    if denominator == 0:
        return 0.0
    return round(float(numerator) / float(denominator), 4)


def _variants_for_mode(mode: str) -> list[str]:
    if mode == "all":
        return ["rules", "hybrid-fake-iter1", "hybrid-fake-iter2"]
    if mode == "hybrid-fake":
        return ["hybrid-fake-iter1", "hybrid-fake-iter2"]
    return ["rules"]


def _issues_for_oracle(report: dict[str, Any]) -> list[dict[str, Any]]:
    evidence_index = report.get("evidence_index", {})
    issues: list[dict[str, Any]] = []
    for issue in [
        *report.get("findings", []),
        *report.get("needs_human_review", []),
    ]:
        enriched = dict(issue)
        if enriched.get("line") is None and "line_range" not in enriched:
            line_range = _line_range_from_evidence(enriched, evidence_index)
            if line_range is not None:
                enriched["line_range"] = line_range
        issues.append(enriched)
    return issues


def _checkpoint_written(report: dict[str, Any]) -> bool:
    checkpoint_path = report.get("loop", {}).get("checkpoint_path")
    return bool(checkpoint_path and Path(checkpoint_path).exists())


def _status_counts(case_results: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for result in case_results:
        for status, count in result["tracing_status_counts"].items():
            counts[str(status)] = counts.get(str(status), 0) + int(count)
    return counts


def _run_phase16_smoke(
    repo: Path,
    out: Path,
    cases: list[EvalCase],
) -> dict[str, Any]:
    resume_case = _case_with_category(cases, "api_change") or cases[0]
    fallback_case = cases[0]

    resume_out = out / "runs" / "phase16-smoke" / "checkpoint-resume"
    first_report = run_review_pipeline(
        repo,
        resume_case.patch_path,
        resume_out,
        mode="hybrid-fake",
        max_iter=1,
    )
    resumed_report = run_review_pipeline(
        repo,
        resume_case.patch_path,
        resume_out,
        mode="hybrid-fake",
        max_iter=2,
        resume=True,
    )

    with _without_live_credentials():
        fallback_report = run_review_pipeline(
            repo,
            fallback_case.patch_path,
            out / "runs" / "phase16-smoke" / "fallback-rules",
            mode="hybrid-live",
            max_iter=2,
        )

    return {
        "checkpoint_resume": {
            "case_id": resume_case.case_id,
            "checkpoint_written": _checkpoint_written(first_report),
            "resume_used": bool(
                resumed_report.get("summary", {}).get("resume_used", False)
            ),
            "resume_ignored_reason": resumed_report.get("summary", {}).get(
                "resume_ignored_reason"
            ),
            "iterations_completed": resumed_report.get("summary", {}).get(
                "loop_iterations_completed", 0
            ),
            "loop_converged": bool(
                resumed_report.get("summary", {}).get("loop_converged", False)
            ),
            "target_repo_modified": bool(
                resumed_report.get("summary", {}).get("target_repo_modified", True)
            ),
        },
        "fallback_rules": {
            "case_id": fallback_case.case_id,
            "mode": fallback_report.get("summary", {}).get("mode"),
            "fallback_used": bool(
                fallback_report.get("summary", {}).get("fallback_used", False)
            ),
            "fallback_reason_present": bool(
                fallback_report.get("summary", {}).get("fallback_reason")
            ),
            "finding_count": int(
                fallback_report.get("summary", {}).get("finding_count", 0)
            ),
            "agent_statuses": [
                str(run.get("status", ""))
                for run in fallback_report.get("agent_runs", [])
            ],
            "target_repo_modified": bool(
                fallback_report.get("summary", {}).get("target_repo_modified", True)
            ),
        },
    }


def _case_with_category(cases: list[EvalCase], category: str) -> EvalCase | None:
    for case in cases:
        if any(
            item.get("category") == category
            for item in case.ground_truth.get("expected_findings", [])
        ):
            return case
    return None


@contextmanager
def _without_live_credentials():
    keys = [
        "SILICONFLOW_API_KEY",
        "OPENAI_COMPATIBLE_API_KEY",
    ]
    old_values = {key: os.environ.get(key) for key in keys}
    try:
        for key in keys:
            os.environ.pop(key, None)
        yield
    finally:
        for key, value in old_values.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def _line_range_from_evidence(
    issue: dict[str, Any], evidence_index: dict[str, Any]
) -> list[int] | None:
    issue_file = issue.get("file")
    for evidence_id in issue.get("evidence_ids", []):
        if evidence_id.startswith(("diff:", "diff_hunk:")):
            path, line = _diff_location(evidence_id)
            if path == issue_file and line is not None:
                return [line, line]

        evidence = evidence_index.get(evidence_id, {})
        source = evidence.get("source") if isinstance(evidence, dict) else None
        if not isinstance(source, str):
            continue
        parsed = _source_line_range(source)
        if parsed is None:
            continue
        path, start, end = parsed
        if path == issue_file:
            return [start, end]
    return None


def _diff_location(evidence_id: str) -> tuple[str | None, int | None]:
    parts = evidence_id.split(":")
    if len(parts) < 3 or parts[0] not in {"diff", "diff_hunk"}:
        return None, None
    line = int(parts[-1]) if parts[-1].isdigit() else None
    return ":".join(parts[1:-1]), line


def _source_line_range(source: str) -> tuple[str, int, int] | None:
    path, _, raw_range = source.rpartition(":")
    if not path:
        return None
    if "-" in raw_range:
        raw_start, _, raw_end = raw_range.partition("-")
        if raw_start.isdigit() and raw_end.isdigit():
            return path, int(raw_start), int(raw_end)
    if raw_range.isdigit():
        line = int(raw_range)
        return path, line, line
    return None


def _yes_no(value: bool) -> str:
    return "yes" if value else "no"
