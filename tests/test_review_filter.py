"""Tests for review/filter.py — Phase 11."""

from __future__ import annotations

import pytest

from code_review_agent.models import (
    ChangedEntity,
    DiffFileChange,
    DiffHunk,
    DiffLine,
    EvidencePackage,
    ReviewEvidence,
    ReviewIssue,
)
from code_review_agent.review.filter import FilterResult, filter_issues, _merge_duplicates
from code_review_agent.review.filter import filter_findings
from code_review_agent.review.schema import Finding


# ── helpers ────────────────────────────────────────────────────────────────────

def _make_evidence(eid: str) -> ReviewEvidence:
    return ReviewEvidence(
        id=eid,
        kind="diff",
        source="src/foo.py",
        message="context",
    )


def _make_package(
    evidence_ids: list[str],
    *,
    changed_files: list[DiffFileChange] | None = None,
    changed_entities: list[ChangedEntity] | None = None,
) -> EvidencePackage:
    index = {eid: _make_evidence(eid) for eid in evidence_ids}
    return EvidencePackage(
        repo_root="/repo",
        changed_files=changed_files or [],
        changed_entities=changed_entities or [],
        risk_signals=[],
        evidence_index=index,
        metadata={},
    )


def _make_issue(
    *,
    file: str = "src/foo.py",
    line: int | None = 10,
    category: str = "test_gap",
    confidence: float = 0.8,
    evidence_ids: list[str] | None = None,
    message: str = "Business logic changed without test update.",
    suggestion: str = "Update tests.",
) -> ReviewIssue:
    return ReviewIssue(
        file=file,
        line=line,
        severity="medium",
        category=category,
        message=message,
        suggestion=suggestion,
        confidence=confidence,
        evidence_ids=evidence_ids if evidence_ids is not None else ["diff:src/foo.py:10"],
    )


def _changed_file_with_hunk() -> DiffFileChange:
    return DiffFileChange(
        old_path="src/foo.py",
        new_path="src/foo.py",
        change_type="modified",
        hunks=[
            DiffHunk(
                old_start=8,
                old_count=4,
                new_start=8,
                new_count=4,
                section_header="def run",
                lines=[
                    DiffLine("context", 8, 8, "def run():"),
                    DiffLine("removed", 9, None, "    return False"),
                    DiffLine("added", None, 9, "    return True"),
                    DiffLine("context", 10, 10, ""),
                    DiffLine("context", 11, 11, "def other():"),
                ],
            )
        ],
    )


def _changed_entity() -> ChangedEntity:
    return ChangedEntity(
        path="src/foo.py",
        entity_type="function",
        name="run",
        qualified_name="run",
        line_start=8,
        line_end=11,
        hunk_ids=["src/foo.py:8"],
    )


CHANGED = {"src/foo.py", "src/bar.py"}


# ── Rule 1: empty evidence_ids → discard ──────────────────────────────────────

def test_discard_empty_evidence_ids():
    pkg = _make_package(["diff:src/foo.py:10"])
    issue = _make_issue(evidence_ids=[])
    result = filter_issues([issue], [], pkg, CHANGED)
    assert result.findings == []
    assert result.needs_human_review == []
    assert len(result.discarded) == 1


# ── Rule 2: all evidence IDs absent from index → discard ─────────────────────

def test_discard_all_evidence_ids_missing():
    pkg = _make_package([])  # empty index
    issue = _make_issue(evidence_ids=["diff:src/foo.py:10"])
    result = filter_issues([issue], [], pkg, CHANGED)
    assert len(result.discarded) == 1
    assert result.findings == []


def test_partial_missing_keeps_issue_with_valid_ids_only():
    """If some evidence IDs are valid, keep the issue with only valid IDs."""
    pkg = _make_package(["diff:src/foo.py:10"])
    issue = _make_issue(evidence_ids=["diff:src/foo.py:10", "ghost:missing:99"])
    result = filter_issues([issue], [], pkg, CHANGED)
    assert len(result.findings) == 1
    assert result.findings[0].evidence_ids == ["diff:src/foo.py:10"]


# ── Rule 3: file not in changed paths → discard ───────────────────────────────

def test_discard_file_not_in_changed_paths():
    pkg = _make_package(["diff:src/other.py:5"])
    issue = _make_issue(file="src/other.py", evidence_ids=["diff:src/other.py:5"])
    result = filter_issues([issue], [], pkg, {"src/foo.py"})  # other.py NOT in changed
    assert len(result.discarded) == 1
    assert result.discarded[0].reason == "file_not_changed"


def test_file_not_changed_but_related_evidence_goes_to_human_review():
    pkg = _make_package(["diff:src/foo.py:10"])
    issue = _make_issue(file="tests/test_foo.py", evidence_ids=["diff:src/foo.py:10"])
    result = filter_issues([issue], [], pkg, {"src/foo.py"})
    assert result.findings == []
    assert len(result.needs_human_review) == 1
    assert result.discarded == []


def test_unrelated_line_goes_to_human_review():
    pkg = _make_package(
        ["diff:src/foo.py:9"],
        changed_files=[_changed_file_with_hunk()],
        changed_entities=[_changed_entity()],
    )
    issue = _make_issue(line=30, evidence_ids=["diff:src/foo.py:9"])
    result = filter_issues([issue], [], pkg, CHANGED)
    assert result.findings == []
    assert len(result.needs_human_review) == 1


def test_related_line_passes_changed_hunk_check():
    pkg = _make_package(
        ["diff:src/foo.py:9"],
        changed_files=[_changed_file_with_hunk()],
        changed_entities=[_changed_entity()],
    )
    issue = _make_issue(line=9, evidence_ids=["diff:src/foo.py:9"])
    result = filter_issues([issue], [], pkg, CHANGED)
    assert len(result.findings) == 1


# ── Rule 4: style preference → discard ───────────────────────────────────────

def test_discard_style_preference_message():
    pkg = _make_package(["diff:src/foo.py:10"])
    issue = _make_issue(message="Please fix the naming convention for this variable.")
    result = filter_issues([issue], [], pkg, CHANGED)
    assert len(result.discarded) == 1
    assert result.findings == []


def test_style_heuristic_case_insensitive():
    pkg = _make_package(["diff:src/foo.py:10"])
    issue = _make_issue(message="Violates PEP8 style preference.")
    result = filter_issues([issue], [], pkg, CHANGED)
    assert len(result.discarded) == 1


def test_discard_low_signal_maintainability_comment_request():
    pkg = _make_package(["diff:src/foo.py:10"])
    issue = _make_issue(
        category="maintainability",
        message="allowed_paths=None is not explicitly documented.",
        suggestion="Add a comment clarifying that None means all paths.",
    )

    result = filter_issues([issue], [], pkg, CHANGED)

    assert result.findings == []
    assert result.discarded[0].reason == "low_signal_suggestion"


def test_keep_low_value_category_with_concrete_failure():
    pkg = _make_package(["diff:src/foo.py:10"])
    issue = _make_issue(
        category="maintainability",
        message="This duplicates evidence ids and causes an incorrect refill.",
        suggestion="Deduplicate ids before returning them.",
    )

    result = filter_issues([issue], [], pkg, CHANGED)

    assert len(result.findings) == 1


def test_discard_speculative_correctness_without_failure_scenario():
    pkg = _make_package(["diff:src/foo.py:10"])
    issue = _make_issue(
        category="correctness",
        message="This may change behavior when max_context_requests is 0.",
        suggestion="Consider adding a guard.",
    )

    result = filter_issues([issue], [], pkg, CHANGED)

    assert result.findings == []
    assert result.discarded[0].reason == "low_signal_suggestion"


def test_keep_concrete_correctness_failure():
    pkg = _make_package(["diff:src/foo.py:10"])
    issue = _make_issue(
        category="correctness",
        message="This drops requested evidence ids and causes an incorrect refill.",
        suggestion="Preserve explicit evidence ids before filtering.",
    )

    result = filter_issues([issue], [], pkg, CHANGED)

    assert len(result.findings) == 1


# ── Rule 5: low confidence → needs_human_review ───────────────────────────────

def test_low_confidence_goes_to_needs_human_review():
    pkg = _make_package(["diff:src/foo.py:10"])
    issue = _make_issue(confidence=0.5)  # below default threshold 0.6
    result = filter_issues([issue], [], pkg, CHANGED)
    assert result.findings == []
    assert len(result.needs_human_review) == 1


def test_already_uncertain_always_goes_to_needs_human_review():
    """Issues from rules_result.needs_human_review stay in that bucket."""
    pkg = _make_package(["diff:src/foo.py:10"])
    issue = _make_issue(confidence=0.9)  # high confidence, but already_uncertain=True
    result = filter_issues([], [issue], pkg, CHANGED)
    assert result.findings == []
    assert len(result.needs_human_review) == 1


def test_custom_confidence_threshold():
    pkg = _make_package(["diff:src/foo.py:10"])
    issue = _make_issue(confidence=0.7)
    result = filter_issues([issue], [], pkg, CHANGED, confidence_threshold=0.8)
    assert len(result.needs_human_review) == 1
    assert result.findings == []


# ── Rule 6: duplicate merge ───────────────────────────────────────────────────

def test_duplicate_issues_merged():
    pkg = _make_package(["diff:src/foo.py:10", "diff:src/foo.py:20"])
    issue_a = _make_issue(confidence=0.8, evidence_ids=["diff:src/foo.py:10"])
    issue_b = _make_issue(confidence=0.75, evidence_ids=["diff:src/foo.py:20"])
    result = filter_issues([issue_a, issue_b], [], pkg, CHANGED)
    assert len(result.findings) == 1
    merged = result.findings[0]
    assert merged.confidence == 0.8
    assert "diff:src/foo.py:10" in merged.evidence_ids
    assert "diff:src/foo.py:20" in merged.evidence_ids


def test_no_duplicate_different_category():
    pkg = _make_package(["diff:src/foo.py:10"])
    issue_a = _make_issue(category="test_gap", evidence_ids=["diff:src/foo.py:10"])
    issue_b = _make_issue(category="error_handling_change", evidence_ids=["diff:src/foo.py:10"])
    result = filter_issues([issue_a, issue_b], [], pkg, CHANGED)
    assert len(result.findings) == 2


# ── happy path: valid high-confidence finding passes through ──────────────────

def test_valid_finding_passes_through():
    pkg = _make_package(["diff:src/foo.py:10"])
    issue = _make_issue()
    result = filter_issues([issue], [], pkg, CHANGED)
    assert len(result.findings) == 1
    assert result.discarded == []
    assert result.needs_human_review == []


# ── FilterResult.to_dict() ────────────────────────────────────────────────────

def test_filter_result_to_dict():
    pkg = _make_package(["diff:src/foo.py:10"])
    issue = _make_issue()
    result = filter_issues([issue], [], pkg, CHANGED)
    d = result.to_dict()
    assert "findings" in d
    assert "needs_human_review" in d
    assert "discarded" in d
    assert len(d["findings"]) == 1


def test_discarded_to_dict_includes_filter_reason():
    pkg = _make_package([])
    issue = _make_issue(evidence_ids=["ghost:missing"])
    result = filter_issues([issue], [], pkg, CHANGED)
    d = result.to_dict()
    assert d["discarded"][0]["filter_reason"] == "invalid_evidence_ids"


def test_filter_findings_returns_lifecycle_statuses():
    pkg = _make_package(["diff:src/foo.py:10"])
    finding = Finding.from_legacy_issue(_make_issue())
    low_confidence = Finding.from_legacy_issue(
        _make_issue(confidence=0.5),
        status="candidate",
    )

    lifecycle = filter_findings([finding, low_confidence], pkg, CHANGED)

    assert lifecycle.counts_by_status() == {
        "finding": 1,
        "needs_human_review": 1,
    }
    assert lifecycle.by_status("needs_human_review")[0].reason == "low_confidence"
