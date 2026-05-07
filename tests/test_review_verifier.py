from __future__ import annotations

from code_review_agent.models import (
    ChangedEntity,
    DiffFileChange,
    DiffHunk,
    DiffLine,
    EvidencePackage,
    ReviewEvidence,
    ReviewIssue,
)
from code_review_agent.review.verifier import ground_verify


def test_ground_verify_empty_evidence_ids() -> None:
    issue = _issue(evidence_ids=[])

    result = ground_verify([issue], _package(), {"src/foo.py"})

    assert result.verified == []
    assert result.discarded[0].reason == "missing_evidence"


def test_ground_verify_unknown_evidence_id() -> None:
    issue = _issue(evidence_ids=["diff:src/foo.py:9", "missing:evidence"])

    result = ground_verify([issue], _package(), {"src/foo.py"})

    assert result.verified == []
    assert result.discarded[0].reason == "invalid_evidence_ids"


def test_ground_verify_file_not_changed() -> None:
    issue = _issue(file="src/other.py", evidence_ids=["entity:src/other.py:run"])

    result = ground_verify([issue], _package(), {"src/foo.py"})

    assert result.verified == []
    assert result.discarded[0].reason == "file_not_changed"


def test_ground_verify_line_not_related() -> None:
    issue = _issue(line=40, evidence_ids=["diff:src/foo.py:9"])

    result = ground_verify([issue], _package(), {"src/foo.py"})

    assert result.verified == []
    assert result.needs_human_review == [issue]


def test_ground_verify_style_preference() -> None:
    issue = _issue(message="Code style: prefer a blank line here.")

    result = ground_verify([issue], _package(), {"src/foo.py"})

    assert result.verified == []
    assert result.discarded[0].reason == "style_preference"


def test_ground_verify_keeps_valid_issue() -> None:
    issue = _issue()

    result = ground_verify([issue], _package(), {"src/foo.py"})

    assert result.verified == [issue]
    assert result.needs_human_review == []
    assert result.discarded == []
    assert result.to_dict()["verified"][0]["category"] == "test_gap"


def _issue(
    *,
    file: str = "src/foo.py",
    line: int | None = 9,
    message: str = "Business logic changed without related tests.",
    evidence_ids: list[str] | None = None,
) -> ReviewIssue:
    return ReviewIssue(
        file=file,
        line=line,
        severity="medium",
        category="test_gap",
        message=message,
        suggestion="Update tests.",
        confidence=0.75,
        evidence_ids=(
            ["diff:src/foo.py:9"] if evidence_ids is None else evidence_ids
        ),
    )


def _package() -> EvidencePackage:
    change = DiffFileChange(
        old_path="src/foo.py",
        new_path="src/foo.py",
        change_type="modified",
        hunks=[
            DiffHunk(
                old_start=8,
                old_count=3,
                new_start=8,
                new_count=3,
                section_header="def run",
                lines=[
                    DiffLine("context", 8, 8, "def run():"),
                    DiffLine("removed", 9, None, "    return False"),
                    DiffLine("added", None, 9, "    return True"),
                    DiffLine("context", 10, 10, ""),
                ],
            )
        ],
    )
    entity = ChangedEntity(
        path="src/foo.py",
        entity_type="function",
        name="run",
        qualified_name="run",
        line_start=8,
        line_end=10,
        hunk_ids=["src/foo.py:8"],
    )
    return EvidencePackage(
        repo_root="/repo",
        changed_files=[change],
        changed_entities=[entity],
        evidence_index={
            "diff:src/foo.py:9": ReviewEvidence(
                id="diff:src/foo.py:9",
                kind="diff",
                source="src/foo.py:9",
                message="Added line.",
            ),
            "entity:src/other.py:run": ReviewEvidence(
                id="entity:src/other.py:run",
                kind="entity",
                source="src/other.py",
                message="Unchanged entity.",
            ),
        },
    )
