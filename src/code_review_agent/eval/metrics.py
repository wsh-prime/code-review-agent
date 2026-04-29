"""Deterministic metrics for planted-bug review cases."""

from __future__ import annotations

from typing import Any


DEFAULT_OVERLAP_THRESHOLD = 0.5


def line_range_overlap(
    finding_range: tuple[int, int] | list[int],
    expected_range: tuple[int, int] | list[int],
) -> float:
    """Return overlap ratio against the expected line range."""

    finding_start, finding_end = _normalize_range(finding_range)
    expected_start, expected_end = _normalize_range(expected_range)
    expected_width = expected_end - expected_start + 1
    if expected_width <= 0:
        return 0.0

    overlap_start = max(finding_start, expected_start)
    overlap_end = min(finding_end, expected_end)
    if overlap_start > overlap_end:
        return 0.0
    return (overlap_end - overlap_start + 1) / expected_width


def finding_matches_expected(
    finding: dict[str, Any],
    expected: dict[str, Any],
    *,
    overlap_threshold: float = DEFAULT_OVERLAP_THRESHOLD,
) -> bool:
    """Match one finding to one ground-truth entry without LLM judging."""

    if finding.get("file") != expected.get("file"):
        return False
    if finding.get("category") != expected.get("category"):
        return False
    if "line_range" not in finding and finding.get("line") is not None:
        line = int(finding["line"])
        expected_start, expected_end = _normalize_range(
            expected.get("line_range", [0, 0])
        )
        return expected_start <= line <= expected_end
    return (
        line_range_overlap(
            _finding_line_range(finding),
            expected.get("line_range", [0, 0]),
        )
        >= overlap_threshold
    )


def evaluate_case(
    findings: list[dict[str, Any]],
    ground_truth: dict[str, Any],
    *,
    overlap_threshold: float = DEFAULT_OVERLAP_THRESHOLD,
) -> dict[str, Any]:
    """Evaluate one case with deterministic matching."""

    expected_findings = list(ground_truth.get("expected_findings", []))
    expected_no_finding = bool(ground_truth.get("expected_no_finding", False))

    matched_finding_indexes: set[int] = set()
    matched_expected_indexes: set[int] = set()
    for expected_index, expected in enumerate(expected_findings):
        for finding_index, finding in enumerate(findings):
            if finding_index in matched_finding_indexes:
                continue
            if finding_matches_expected(
                finding,
                expected,
                overlap_threshold=overlap_threshold,
            ):
                matched_expected_indexes.add(expected_index)
                matched_finding_indexes.add(finding_index)
                break

    true_positives = len(matched_expected_indexes)
    false_positives = len(findings) - len(matched_finding_indexes)
    false_negatives = len(expected_findings) - len(matched_expected_indexes)
    key_expected_indexes = {
        index
        for index, expected in enumerate(expected_findings)
        if expected.get("key_bug", False)
    }
    key_bug_inclusion = (
        True
        if not key_expected_indexes
        else key_expected_indexes.issubset(matched_expected_indexes)
    )
    no_finding_correct = expected_no_finding and not findings

    return {
        "case_id": ground_truth.get("case_id"),
        "true_positives": true_positives,
        "false_positives": false_positives,
        "false_negatives": false_negatives,
        "expected_no_finding": expected_no_finding,
        "no_finding_correct": no_finding_correct,
        "key_bug_inclusion": key_bug_inclusion,
        "matched_expected_indexes": sorted(matched_expected_indexes),
        "matched_finding_indexes": sorted(matched_finding_indexes),
    }


def summarize_case_results(case_results: list[dict[str, Any]]) -> dict[str, Any]:
    """Aggregate case results into review benchmark metrics."""

    true_positives = sum(result["true_positives"] for result in case_results)
    false_positives = sum(result["false_positives"] for result in case_results)
    false_negatives = sum(result["false_negatives"] for result in case_results)
    case_count = len(case_results)
    no_finding_cases = [
        result for result in case_results if result["expected_no_finding"]
    ]

    precision_denominator = true_positives + false_positives
    recall_denominator = true_positives + false_negatives
    return {
        "case_count": case_count,
        "precision": _safe_ratio(true_positives, precision_denominator),
        "recall": _safe_ratio(true_positives, recall_denominator),
        "false_positives_per_pr": _safe_ratio(false_positives, case_count),
        "key_bug_inclusion": all(
            result["key_bug_inclusion"] for result in case_results
        )
        if case_results
        else True,
        "no_finding_accuracy": _safe_ratio(
            sum(result["no_finding_correct"] for result in no_finding_cases),
            len(no_finding_cases),
        ),
        "true_positives": true_positives,
        "false_positives": false_positives,
        "false_negatives": false_negatives,
    }


def _finding_line_range(finding: dict[str, Any]) -> list[int]:
    if "line_range" in finding:
        return list(finding["line_range"])
    line = finding.get("line")
    if line is None:
        return [0, 0]
    return [int(line), int(line)]


def _normalize_range(line_range: tuple[int, int] | list[int]) -> tuple[int, int]:
    start = int(line_range[0])
    end = int(line_range[1])
    if end < start:
        start, end = end, start
    return start, end


def _safe_ratio(numerator: int | float, denominator: int | float) -> float:
    if denominator == 0:
        return 0.0
    return round(float(numerator) / float(denominator), 4)
