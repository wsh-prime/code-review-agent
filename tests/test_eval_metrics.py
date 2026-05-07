from __future__ import annotations

import json
from pathlib import Path

from code_review_agent.eval.metrics import (
    evaluate_case,
    finding_matches_expected,
    line_range_overlap,
    summarize_case_results,
)
from code_review_agent.eval.cases import load_eval_cases
from code_review_agent.eval.runner import run_eval_benchmark


def test_line_range_overlap_uses_expected_range_width() -> None:
    assert line_range_overlap([10, 12], [11, 14]) == 0.5
    assert line_range_overlap([1, 2], [10, 12]) == 0.0


def test_finding_match_requires_file_category_and_line_overlap() -> None:
    finding = {
        "file": "src/shop/service.py",
        "category": "test_gap",
        "line": 35,
    }
    expected = {
        "file": "src/shop/service.py",
        "category": "test_gap",
        "line_range": [30, 40],
    }

    assert finding_matches_expected(finding, expected)
    assert not finding_matches_expected(
        {**finding, "category": "error_handling_change"},
        expected,
    )


def test_evaluate_case_counts_matches_and_false_positives() -> None:
    ground_truth = {
        "case_id": "case_001_test_gap",
        "expected_findings": [
            {
                "category": "test_gap",
                "file": "src/shop/service.py",
                "line_range": [30, 40],
                "key_bug": True,
            }
        ],
        "expected_no_finding": False,
    }
    findings = [
        {
            "category": "test_gap",
            "file": "src/shop/service.py",
            "line": 35,
        },
        {
            "category": "security_sensitive",
            "file": "src/shop/service.py",
            "line": 35,
        },
    ]

    result = evaluate_case(findings, ground_truth)

    assert result["true_positives"] == 1
    assert result["false_positives"] == 1
    assert result["false_negatives"] == 0
    assert result["key_bug_inclusion"] is True


def test_no_finding_case_and_summary_metrics() -> None:
    no_finding = evaluate_case(
        [],
        {
            "case_id": "case_003_no_finding_doc_only",
            "expected_findings": [],
            "expected_no_finding": True,
        },
    )
    missed = evaluate_case(
        [],
        {
            "case_id": "case_002_error_handling",
            "expected_findings": [
                {
                    "category": "error_handling_change",
                    "file": "src/shop/service.py",
                    "line_range": [10, 14],
                    "key_bug": True,
                }
            ],
            "expected_no_finding": False,
        },
    )

    summary = summarize_case_results([no_finding, missed])

    assert no_finding["no_finding_correct"] is True
    assert summary["case_count"] == 2
    assert summary["recall"] == 0.0
    assert summary["no_finding_accuracy"] == 1.0
    assert summary["false_negatives"] == 1


def test_micro_eval_fixtures_are_loadable() -> None:
    project_root = Path(__file__).resolve().parents[1]
    cases_root = project_root / "examples" / "eval_cases"
    expected_cases = {
        "case_001_test_gap",
        "case_002_api_change",
        "case_003_error_handling",
        "case_004_artifact_pollution",
        "case_005_no_finding_doc_only",
        "case_006_no_finding_test_only",
        "case_007_design_constraint",
    }

    loaded_cases = {case.case_id for case in load_eval_cases(cases_root)}

    assert loaded_cases == expected_cases


def test_eval_runner_writes_metrics_case_results_and_markdown(tmp_path: Path) -> None:
    project_root = Path(__file__).resolve().parents[1]
    cases_root = project_root / "examples" / "eval_cases"

    metrics = run_eval_benchmark(cases_root, tmp_path / "eval", mode="rules")

    assert metrics["case_count"] == 7
    assert "rules" in metrics["variants"]
    assert "balanced" in metrics["variants"]["rules"]
    assert metrics["variants"]["rules"]["balanced"]["discarded_count"] >= 0
    assert metrics["variants"]["rules"]["balanced"]["needs_human_review_count"] >= 0
    assert metrics["variants"]["rules"]["balanced"]["checkpoint_written_count"] == 0
    assert metrics["phase16_smoke"] == {}
    assert (tmp_path / "eval" / "metrics.json").exists()
    assert (tmp_path / "eval" / "case_results.json").exists()
    assert (tmp_path / "eval" / "eval_report.md").exists()

    data = json.loads((tmp_path / "eval" / "metrics.json").read_text(encoding="utf-8"))
    assert data["schema_version"] == "1.1"
    assert data["target_repo_modified"] is False
    assert data["variants"]["rules"]["balanced"]["no_finding_accuracy"] == 1.0


def test_eval_runner_all_mode_compares_loop_variants(tmp_path: Path) -> None:
    project_root = Path(__file__).resolve().parents[1]
    cases_root = project_root / "examples" / "eval_cases"

    metrics = run_eval_benchmark(cases_root, tmp_path / "eval", mode="all")

    assert list(metrics["variants"]) == [
        "rules",
        "hybrid-fake-iter1",
        "hybrid-fake-iter2",
    ]
    assert metrics["variant_descriptions"]["hybrid-fake-iter2"]
    assert (
        metrics["variants"]["hybrid-fake-iter1"]["balanced"][
            "loop_iterations_completed"
        ]
        == 7
    )
    assert (
        metrics["variants"]["hybrid-fake-iter2"]["balanced"][
            "loop_enabled_count"
        ]
        == 7
    )
    assert (
        metrics["variants"]["hybrid-fake-iter2"]["balanced"][
            "checkpoint_written_count"
        ]
        == 7
    )
    assert (
        metrics["variants"]["hybrid-fake-iter2"]["balanced"]["fallback_used_count"]
        == 0
    )
    assert (
        metrics["variants"]["hybrid-fake-iter2"]["balanced"]["tracing_run_count"]
        >= 14
    )
    assert (
        metrics["variants"]["hybrid-fake-iter2"]["balanced"][
            "tracing_status_counts"
        ]["ok"]
        >= 14
    )
    smoke = metrics["phase16_smoke"]
    assert smoke["checkpoint_resume"]["checkpoint_written"] is True
    assert smoke["checkpoint_resume"]["resume_used"] is True
    assert smoke["checkpoint_resume"]["resume_ignored_reason"] is None
    assert smoke["checkpoint_resume"]["target_repo_modified"] is False
    assert smoke["fallback_rules"]["mode"] == "hybrid-live/fallback-rules"
    assert smoke["fallback_rules"]["fallback_used"] is True
    assert smoke["fallback_rules"]["fallback_reason_present"] is True
    assert "fallback" in smoke["fallback_rules"]["agent_statuses"]
    assert smoke["fallback_rules"]["target_repo_modified"] is False

    report = (tmp_path / "eval" / "eval_report.md").read_text(encoding="utf-8")
    assert "`hybrid-fake-iter1`" in report
    assert "`hybrid-fake-iter2`" in report
    assert "Needs Human Review" in report
    assert "Phase 16 Reliability Smoke" in report
    assert "Checkpoints" in report
