from __future__ import annotations

import json

from code_review_agent.output.json_report import (
    REVIEW_REPORT_SCHEMA_VERSION,
    review_report_to_json,
)
from code_review_agent.output.review_markdown import render_review_markdown


def test_review_markdown_uses_stable_section_order_and_finding_details() -> None:
    markdown = render_review_markdown(_sample_report())

    expected_order = [
        "# Review Report",
        "## Summary",
        "## Findings",
        "## Needs Human Review",
        "## Changed Files",
        "## Changed Entities",
        "## Risk Signals",
        "## Evidence Index",
    ]
    positions = [markdown.index(section) for section in expected_order]
    assert positions == sorted(positions)
    assert "`test_gap` medium at `src/shop/service.py:4` (0.80)" in markdown
    assert "Evidence: `diff:src/shop/service.py:4`" in markdown


def test_review_markdown_explains_no_finding_cases() -> None:
    report = _sample_report()
    report["findings"] = []
    report["summary"]["finding_count"] = 0
    report["summary"]["mode"] = "hybrid-fake"

    markdown = render_review_markdown(report)

    assert "No findings." in markdown
    assert "Checked changed files, changed entities" in markdown
    assert "rules-only finding" not in markdown
    assert "review finding was produced" in markdown


def test_review_markdown_truncates_long_issue_evidence_lists() -> None:
    report = _sample_report()
    report["findings"][0]["evidence_ids"] = [
        f"diff:src/shop/service.py:{line}" for line in range(1, 16)
    ]

    markdown = render_review_markdown(report)

    assert "`diff:src/shop/service.py:10`" in markdown
    assert "`diff:src/shop/service.py:11`" not in markdown
    assert "... 5 more" in markdown


def test_review_json_has_stable_schema_version_and_fields() -> None:
    data = json.loads(review_report_to_json(_sample_report()))

    assert data["schema_version"] == REVIEW_REPORT_SCHEMA_VERSION
    assert list(data) == [
        "schema_version",
        "summary",
        "findings",
        "needs_human_review",
        "discarded",
        "changed_files",
        "changed_entities",
        "risk_signals",
        "evidence_index",
        "missing_evidence_ids",
        "agent_runs",
        "prompt_exports",
        "context_budget",
        "loop",
        "tracing",
    ]
    assert data["summary"]["target_repo_modified"] is False


def test_review_markdown_includes_loop_summary_when_enabled() -> None:
    report = _sample_report()
    report["summary"]["loop_enabled"] = True
    report["summary"]["loop_iterations_completed"] = 1
    report["summary"]["loop_converged"] = True
    report["loop"] = {
        "enabled": True,
        "max_iter": 2,
        "iterations_completed": 1,
        "converged": True,
        "iterations": [
            {
                "i": 0,
                "candidate_issue_count": 2,
                "verified_count": 1,
                "uncertain_count": 0,
                "keep_count": 1,
                "reject_count": 0,
            }
        ],
    }
    report["tracing"] = {
        "total_latency_ms": 0,
        "total_token_count_in": 0,
        "total_token_count_out": 0,
        "total_retry_count": 0,
        "run_count": 2,
    }

    markdown = render_review_markdown(report)

    assert "## Loop Summary" in markdown
    assert "Iteration 0" in markdown


def test_review_markdown_includes_context_budget_when_enabled() -> None:
    report = _sample_report()
    report["summary"]["context_budget_enabled"] = True
    report["summary"]["context_truncated"] = True
    report["summary"]["selected_evidence_count"] = 2
    report["summary"]["omitted_evidence_count"] = 5
    report["summary"]["review_shard_count"] = 1
    report["context_budget"] = {
        "enabled": True,
        "strategy": "risk_first_v1",
        "max_input_tokens": 1000,
        "estimated_input_tokens": 900,
        "selected_evidence_count": 2,
        "omitted_evidence_count": 5,
        "context_truncated": True,
        "shard_count": 1,
        "warnings": [],
    }

    markdown = render_review_markdown(report)

    assert "## Context Budget Summary" in markdown
    assert "| Selected evidence | 2 |" in markdown


def _sample_report() -> dict:
    return {
        "summary": {
            "mode": "rules",
            "changed_file_count": 1,
            "changed_entity_count": 1,
            "risk_signal_count": 1,
            "finding_count": 1,
            "needs_human_review_count": 0,
            "discarded_count": 0,
            "evidence_count": 3,
            "missing_evidence_id_count": 0,
            "agent_run_count": 0,
            "prompt_exported": False,
            "target_repo_modified": False,
        },
        "findings": [
            {
                "file": "src/shop/service.py",
                "line": 4,
                "severity": "medium",
                "category": "test_gap",
                "message": "Business logic changed while related tests exist.",
                "suggestion": "Update related tests.",
                "confidence": 0.8,
                "evidence_ids": [
                    "diff:src/shop/service.py:4",
                    "test_discovery:tests/test_service.py",
                ],
            }
        ],
        "needs_human_review": [],
        "discarded": [],
        "changed_files": [
            {
                "old_path": "src/shop/service.py",
                "new_path": "src/shop/service.py",
                "change_type": "modified",
                "hunks": [],
            }
        ],
        "changed_entities": [
            {
                "path": "src/shop/service.py",
                "entity_type": "function",
                "name": "create_order",
                "qualified_name": "create_order",
                "line_start": 1,
                "line_end": 4,
                "hunk_ids": ["src/shop/service.py:1"],
            }
        ],
        "risk_signals": [
            {
                "tag": "test_gap",
                "confidence": 0.8,
                "reason": "Related tests exist but no test file changed.",
                "evidence_ids": [
                    "diff:src/shop/service.py:4",
                    "test_discovery:tests/test_service.py",
                ],
            }
        ],
        "evidence_index": {
            "diff:src/shop/service.py:4": {
                "id": "diff:src/shop/service.py:4",
                "kind": "diff",
                "source": "src/shop/service.py:4",
                "message": "Added line.",
            },
            "test_discovery:tests/test_service.py": {
                "id": "test_discovery:tests/test_service.py",
                "kind": "test_discovery",
                "source": "tests/test_service.py",
                "message": "Related test.",
            },
        },
        "missing_evidence_ids": [],
        "agent_runs": [],
        "prompt_exports": {},
    }
