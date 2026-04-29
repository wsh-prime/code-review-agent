"""Markdown rendering for review reports."""

from __future__ import annotations

from typing import Any


MAX_EVIDENCE_ITEMS = 30


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
        f"- Target repo modified: {summary['target_repo_modified']}",
        "",
        "## Findings",
        "",
    ]

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
    return [
        f"- `{issue['category']}` {issue['severity']} "
        f"at `{issue['file']}:{line}` ({issue['confidence']:.2f})",
        f"  - {issue['message']}",
        f"  - Suggestion: {issue['suggestion']}",
        f"  - Evidence: {', '.join(f'`{item}`' for item in issue['evidence_ids'])}",
        "",
    ]
