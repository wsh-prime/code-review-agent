"""Stable JSON report helpers for review output."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REVIEW_REPORT_SCHEMA_VERSION = "1.1"


def normalize_review_report(report: dict[str, Any]) -> dict[str, Any]:
    """Return a stable, JSON-friendly review report dict."""

    normalized = {
        "schema_version": report.get("schema_version", REVIEW_REPORT_SCHEMA_VERSION),
        "summary": dict(report.get("summary", {})),
        "findings": list(report.get("findings", [])),
        "needs_human_review": list(report.get("needs_human_review", [])),
        "discarded": list(report.get("discarded", [])),
        "changed_files": list(report.get("changed_files", [])),
        "changed_entities": list(report.get("changed_entities", [])),
        "risk_signals": list(report.get("risk_signals", [])),
        "evidence_index": dict(report.get("evidence_index", {})),
        "missing_evidence_ids": list(report.get("missing_evidence_ids", [])),
        "agent_runs": list(report.get("agent_runs", [])),
        "prompt_exports": dict(report.get("prompt_exports", {})),
    }
    normalized["summary"].setdefault("target_repo_modified", False)
    normalized["summary"].setdefault("discarded_count", len(normalized["discarded"]))
    normalized["summary"].setdefault("agent_run_count", len(normalized["agent_runs"]))
    normalized["summary"].setdefault("prompt_exported", bool(normalized["prompt_exports"]))
    return normalized


def review_report_to_json(report: dict[str, Any]) -> str:
    """Serialize review report data with stable field order and indentation."""

    return json.dumps(
        normalize_review_report(report),
        indent=2,
        ensure_ascii=False,
        sort_keys=False,
    )


def write_review_json(report: dict[str, Any], path: Path | str) -> None:
    """Write a stable review JSON report."""

    Path(path).write_text(review_report_to_json(report), encoding="utf-8")
