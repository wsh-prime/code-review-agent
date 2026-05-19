from __future__ import annotations

from code_review_agent.models import (
    DiffFileChange,
    DiffHunk,
    DiffLine,
    EvidencePackage,
    ReviewEvidence,
    ReviewIssue,
)
from code_review_agent.review.schema import (
    ChangeSet,
    EvidenceStore,
    Finding,
    IssueLifecycleResult,
)


def test_change_set_from_legacy_package_preserves_hunks() -> None:
    package = _package()

    change_set = ChangeSet.from_legacy_package(package)

    assert change_set.repo_root == "/repo"
    assert len(change_set.files) == 1
    changed_file = change_set.files[0]
    assert changed_file.path == "src/app.ts"
    assert changed_file.language == "typescript"
    assert changed_file.file_role == "source"
    assert [hunk.evidence_id for hunk in changed_file.hunks] == [
        "diff_hunk:src/app.ts:10",
        "diff_hunk:src/app.ts:40",
    ]


def test_evidence_store_from_legacy_package_is_queryable() -> None:
    package = _package()

    store = EvidenceStore.from_legacy_package(package)

    assert store.ids_for_path("src/app.ts") == [
        "diff:src/app.ts:10",
        "diff_hunk:src/app.ts:10",
        "diff_hunk:src/app.ts:40",
        "risk:behavior_change:src/app.ts",
    ]
    assert store.ids_for_path_and_type("src/app.ts", "diff_hunk") == [
        "diff_hunk:src/app.ts:10",
        "diff_hunk:src/app.ts:40",
    ]
    item = store.get("diff:src/app.ts:10")
    assert item is not None
    assert item.path == "src/app.ts"
    assert item.range is not None
    assert item.range.start_line == 10


def test_finding_from_legacy_issue_sets_explicit_status() -> None:
    issue = ReviewIssue(
        file="src/app.ts",
        line=10,
        severity="medium",
        category="correctness",
        message="Bug.",
        suggestion="Fix it.",
        confidence=0.8,
        evidence_ids=["diff:src/app.ts:10"],
    )

    finding = Finding.from_legacy_issue(issue, status="needs_human_review", reason="low_confidence")

    assert finding.status == "needs_human_review"
    assert finding.reason == "low_confidence"
    assert finding.evidence_ids == ["diff:src/app.ts:10"]
    assert finding.to_legacy_issue() == issue


def test_issue_lifecycle_result_from_legacy_buckets_counts_statuses() -> None:
    issue = ReviewIssue(
        file="src/app.ts",
        line=10,
        severity="medium",
        category="correctness",
        message="Bug.",
        suggestion="Fix it.",
        confidence=0.8,
        evidence_ids=["diff:src/app.ts:10"],
    )

    lifecycle = IssueLifecycleResult.from_legacy_buckets(
        findings=[issue],
        needs_human_review=[issue],
        discarded=[
            {
                **issue.to_dict(),
                "filter_reason": "low_confidence",
            }
        ],
    )

    assert lifecycle.counts_by_status() == {
        "finding": 1,
        "needs_human_review": 1,
        "discarded": 1,
    }
    assert lifecycle.by_status("discarded")[0].reason == "low_confidence"


def _package() -> EvidencePackage:
    return EvidencePackage(
        repo_root="/repo",
        changed_files=[
            DiffFileChange(
                old_path="src/app.ts",
                new_path="src/app.ts",
                change_type="modified",
                hunks=[
                    DiffHunk(
                        old_start=10,
                        old_count=2,
                        new_start=10,
                        new_count=2,
                        section_header="run",
                        lines=[DiffLine("added", None, 10, "run();")],
                    ),
                    DiffHunk(
                        old_start=40,
                        old_count=2,
                        new_start=40,
                        new_count=2,
                        section_header="stop",
                        lines=[DiffLine("removed", 40, None, "stop();")],
                    ),
                ],
            )
        ],
        evidence_index={
            "diff_hunk:src/app.ts:10": ReviewEvidence(
                id="diff_hunk:src/app.ts:10",
                kind="diff_hunk",
                source="src/app.ts:10",
                message="@@ -10 +10 @@",
            ),
            "diff_hunk:src/app.ts:40": ReviewEvidence(
                id="diff_hunk:src/app.ts:40",
                kind="diff_hunk",
                source="src/app.ts:40",
                message="@@ -40 +40 @@",
            ),
            "diff:src/app.ts:10": ReviewEvidence(
                id="diff:src/app.ts:10",
                kind="diff",
                source="src/app.ts:10",
                message="Added line: run();",
            ),
            "risk:behavior_change:src/app.ts": ReviewEvidence(
                id="risk:behavior_change:src/app.ts",
                kind="risk",
                source="behavior_change",
                message="Behavior changed.",
            ),
        },
    )
