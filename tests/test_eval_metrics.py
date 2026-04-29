from __future__ import annotations

import json
from pathlib import Path

from code_review_agent.eval.metrics import (
    evaluate_case,
    finding_matches_expected,
    line_range_overlap,
    summarize_case_results,
)


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
        "case_002_error_handling",
        "case_003_no_finding_doc_only",
    }

    loaded_cases = set()
    for ground_truth_path in sorted((cases_root / "ground_truth").glob("*.json")):
        data = json.loads(ground_truth_path.read_text(encoding="utf-8"))
        loaded_cases.add(data["case_id"])
        assert (cases_root / data["patch"]).exists()

    assert expected_cases.issubset(loaded_cases)
