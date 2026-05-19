"""Stable JSON report helpers for review output."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REVIEW_REPORT_SCHEMA_VERSION = "1.3"


def normalize_review_report(report: dict[str, Any]) -> dict[str, Any]:
    """Return a stable, JSON-friendly review report dict."""

    normalized = {
        "schema_version": report.get("schema_version", REVIEW_REPORT_SCHEMA_VERSION),
        "summary": _dict_or_empty(report.get("summary")),
        "review_results": _dict_or_empty(report.get("review_results")),
        "change_set": _dict_or_empty(report.get("change_set")),
        "evidence_store_summary": _dict_or_empty(
            report.get("evidence_store_summary")
        ),
        "findings": list(report.get("findings", [])),
        "needs_human_review": list(report.get("needs_human_review", [])),
        "discarded": list(report.get("discarded", [])),
        "changed_files": list(report.get("changed_files", [])),
        "changed_entities": list(report.get("changed_entities", [])),
        "risk_signals": list(report.get("risk_signals", [])),
        "evidence_index": _dict_or_empty(report.get("evidence_index")),
        "missing_evidence_ids": list(report.get("missing_evidence_ids", [])),
        "agent_runs": list(report.get("agent_runs", [])),
        "prompt_exports": _dict_or_empty(report.get("prompt_exports")),
        "context_budget": _dict_or_empty(report.get("context_budget")),
        "loop": _dict_or_empty(report.get("loop")),
        "tracing": _dict_or_empty(report.get("tracing")),
    }
    normalized["summary"].setdefault("target_repo_modified", False)
    normalized["summary"].setdefault("discarded_count", len(normalized["discarded"]))
    normalized["summary"].setdefault("agent_run_count", len(normalized["agent_runs"]))
    normalized["summary"].setdefault(
        "review_result_count",
        len(normalized["review_results"].get("items", [])),
    )
    normalized["summary"].setdefault("prompt_exported", bool(normalized["prompt_exports"]))
    normalized["summary"].setdefault(
        "context_budget_enabled",
        bool(normalized["context_budget"].get("enabled", False)),
    )
    normalized["summary"].setdefault(
        "context_truncated",
        bool(normalized["context_budget"].get("context_truncated", False)),
    )
    normalized["summary"].setdefault(
        "selected_evidence_count",
        int(normalized["context_budget"].get("selected_evidence_count", 0)),
    )
    normalized["summary"].setdefault(
        "omitted_evidence_count",
        int(normalized["context_budget"].get("omitted_evidence_count", 0)),
    )
    normalized["summary"].setdefault(
        "review_shard_count",
        int(normalized["context_budget"].get("shard_count", 0)),
    )
    normalized["summary"].setdefault(
        "context_refill_count",
        int(normalized["context_budget"].get("refill_count", 0)),
    )
    normalized["summary"].setdefault(
        "context_request_count",
        int(normalized["context_budget"].get("context_request_count", 0)),
    )
    normalized["summary"].setdefault("loop_enabled", bool(normalized["loop"].get("enabled")))
    normalized["summary"].setdefault(
        "loop_iterations_completed",
        normalized["loop"].get("iterations_completed", 0),
    )
    normalized["summary"].setdefault(
        "loop_converged",
        normalized["loop"].get("converged", False),
    )
    normalized["summary"].setdefault("fallback_used", False)
    normalized["summary"].setdefault("fallback_reason", None)
    normalized["summary"].setdefault("resume_used", False)
    normalized["summary"].setdefault("resume_ignored_reason", None)
    normalized["summary"].setdefault(
        "total_latency_ms",
        normalized["tracing"].get("total_latency_ms", 0),
    )
    normalized["summary"].setdefault(
        "total_token_count_in",
        normalized["tracing"].get("total_token_count_in", 0),
    )
    normalized["summary"].setdefault(
        "total_token_count_out",
        normalized["tracing"].get("total_token_count_out", 0),
    )
    return normalized


def _dict_or_empty(value: object) -> dict[str, Any]:
    return dict(value) if isinstance(value, dict) else {}


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
