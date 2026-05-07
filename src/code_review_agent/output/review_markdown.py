"""Markdown rendering for review reports."""

from __future__ import annotations

from typing import Any


MAX_EVIDENCE_ITEMS = 30
MAX_ISSUE_EVIDENCE_ITEMS = 10


def render_review_markdown(report: dict[str, Any]) -> str:
    """Render a concise, README-friendly review report."""

    summary = report["summary"]
    lines = [
        "# Review Report",
        "",
        "## Summary",
        "",
        f"- Mode: `{summary['mode']}`",
        f"- Changed files: {summary['changed_file_count']}",
        f"- Changed entities: {summary['changed_entity_count']}",
        f"- Risk signals: {summary['risk_signal_count']}",
        f"- Findings: {summary['finding_count']}",
        f"- Needs human review: {summary['needs_human_review_count']}",
        f"- Discarded: {summary.get('discarded_count', 0)}",
        f"- Agent runs: {summary.get('agent_run_count', 0)}",
        f"- Loop enabled: {summary.get('loop_enabled', False)}",
        f"- Target repo modified: {summary['target_repo_modified']}",
        "",
    ]

    if summary.get("loop_enabled", False):
        lines.extend(_loop_summary_lines(report))

    if summary.get("context_budget_enabled", False):
        lines.extend(_context_budget_summary_lines(report))

    lines.extend([
        "## Findings",
        "",
    ])

    if report["findings"]:
        for issue in report["findings"]:
            lines.extend(_issue_lines(issue))
    else:
        lines.extend(
            [
                "No findings.",
                "",
                (
                    "Checked changed files, changed entities, deterministic risk "
                    "signals, and evidence references. No high-confidence "
                    "review finding was produced."
                ),
                "",
            ]
        )

    lines.extend(["## Needs Human Review", ""])
    if report["needs_human_review"]:
        for issue in report["needs_human_review"]:
            lines.extend(_issue_lines(issue))
    else:
        lines.append("None.")
        lines.append("")

    lines.extend(["## Changed Files", ""])
    for change in report["changed_files"]:
        path = change.get("new_path") or change.get("old_path") or "<unknown>"
        lines.append(f"- `{path}` ({change['change_type']})")
    if not report["changed_files"]:
        lines.append("None.")
    lines.append("")

    lines.extend(["## Changed Entities", ""])
    for entity in report["changed_entities"]:
        lines.append(
            f"- `{entity['path']}:{entity['line_start']}-{entity['line_end']}` "
            f"{entity['entity_type']} `{entity['qualified_name']}`"
        )
    if not report["changed_entities"]:
        lines.append("None.")
    lines.append("")

    lines.extend(["## Risk Signals", ""])
    for signal in report["risk_signals"]:
        lines.append(
            f"- `{signal['tag']}` ({signal['confidence']:.2f}): {signal['reason']}"
        )
    if not report["risk_signals"]:
        lines.append("None.")
    lines.append("")

    lines.extend(["## Evidence Index", ""])
    evidence_ids = sorted(report["evidence_index"])
    for evidence_id in evidence_ids[:MAX_EVIDENCE_ITEMS]:
        evidence = report["evidence_index"][evidence_id]
        lines.append(f"- `{evidence_id}` [{evidence['kind']}]: {evidence['source']}")
    if len(evidence_ids) > MAX_EVIDENCE_ITEMS:
        remaining = len(evidence_ids) - MAX_EVIDENCE_ITEMS
        lines.append(f"- ... {remaining} more evidence items omitted.")
    if not evidence_ids:
        lines.append("None.")
    lines.append("")

    return "\n".join(lines)


def _issue_lines(issue: dict[str, Any]) -> list[str]:
    line = issue["line"] if issue["line"] is not None else "?"
    evidence_ids = list(issue["evidence_ids"])
    visible_evidence = evidence_ids[:MAX_ISSUE_EVIDENCE_ITEMS]
    evidence_text = ", ".join(f"`{item}`" for item in visible_evidence)
    if len(evidence_ids) > MAX_ISSUE_EVIDENCE_ITEMS:
        remaining = len(evidence_ids) - MAX_ISSUE_EVIDENCE_ITEMS
        evidence_text = f"{evidence_text}, ... {remaining} more"
    return [
        f"- `{issue['category']}` {issue['severity']} "
        f"at `{issue['file']}:{line}` ({issue['confidence']:.2f})",
        f"  - {issue['message']}",
        f"  - Suggestion: {issue['suggestion']}",
        f"  - Evidence: {evidence_text}",
        "",
    ]


def _loop_summary_lines(report: dict[str, Any]) -> list[str]:
    summary = report["summary"]
    loop = report.get("loop", {})
    tracing = report.get("tracing", {})
    lines = [
        "## Loop Summary",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Iterations | {summary.get('loop_iterations_completed', 0)} / "
        f"{loop.get('max_iter', 0)} |",
        f"| Converged | {summary.get('loop_converged', False)} |",
        f"| Fallback | {summary.get('fallback_used', False)} |",
        f"| Retry count | {tracing.get('total_retry_count', 0)} |",
        f"| Total latency | {summary.get('total_latency_ms', 0)} ms |",
        f"| Token in | {summary.get('total_token_count_in', 0)} |",
        f"| Token out | {summary.get('total_token_count_out', 0)} |",
        "",
    ]
    for item in loop.get("iterations", []):
        lines.append(
            f"- Iteration {item['i']}: "
            f"{item['candidate_issue_count']} candidates, "
            f"{item['verified_count']} verified, "
            f"{item['uncertain_count']} uncertain, "
            f"{item['keep_count']} kept, "
            f"{item['reject_count']} rejected"
        )
    lines.append("")
    return lines


def _context_budget_summary_lines(report: dict[str, Any]) -> list[str]:
    summary = report["summary"]
    budget = report.get("context_budget", {})
    lines = [
        "## Context Budget Summary",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Strategy | `{budget.get('strategy', 'unknown')}` |",
        f"| Max input tokens | {budget.get('max_input_tokens', 0)} |",
        f"| Estimated input tokens | {budget.get('estimated_input_tokens', 0)} |",
        f"| Selected evidence | {summary.get('selected_evidence_count', 0)} |",
        f"| Omitted evidence | {summary.get('omitted_evidence_count', 0)} |",
        f"| Context truncated | {summary.get('context_truncated', False)} |",
        f"| Review shards | {summary.get('review_shard_count', 0)} |",
        f"| Context requests | {summary.get('context_request_count', 0)} |",
        f"| Refills | {summary.get('context_refill_count', 0)} |",
        "",
    ]
    warnings = budget.get("warnings", [])
    if warnings:
        lines.append("Warnings:")
        for warning in warnings[:10]:
            lines.append(f"- `{warning}`")
        lines.append("")
    return lines
