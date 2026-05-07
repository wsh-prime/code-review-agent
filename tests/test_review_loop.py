from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from code_review_agent.models import (
    CritiqueResult,
    DiffFileChange,
    DiffHunk,
    DiffLine,
    EvidencePackage,
    PriorFeedback,
    ReviewEvidence,
    ReviewIssue,
    RiskSignal,
    UncertainFeedbackItem,
)
from code_review_agent.review.agents import (
    FakeLLMCriticAgent,
    FakeLLMReviewAgent,
    run_fake_hybrid_agents,
)
from code_review_agent.review.filter import filter_issues
from code_review_agent.review.loop import (
    LOOP_CHECKPOINT_FILENAME,
    IterativeHarnessRunner,
)
from code_review_agent.review.risk import TEST_GAP


def test_loop_max_iter_one_matches_current_fake_hybrid_findings() -> None:
    package = _package()
    changed_paths = {"src/foo.py"}
    runner = IterativeHarnessRunner(
        reviewer=FakeLLMReviewAgent(),
        critic=FakeLLMCriticAgent(),
        max_iter=1,
    )

    loop_result = runner.run(package, changed_paths)
    legacy_result = run_fake_hybrid_agents(package)
    loop_filtered = filter_issues(
        loop_result.final_issues,
        loop_result.needs_human_review,
        package,
        changed_paths,
    )
    legacy_filtered = filter_issues(
        legacy_result.findings,
        legacy_result.needs_human_review,
        package,
        changed_paths,
    )

    assert [issue.category for issue in loop_filtered.findings] == [
        issue.category for issue in legacy_filtered.findings
    ]
    assert any(
        item.reason == "invalid_evidence_ids" for item in loop_result.discarded
    )


def test_loop_converges_when_no_uncertain() -> None:
    runner = IterativeHarnessRunner(
        reviewer=_StaticReviewer([_issue()]),
        critic=_KeepCritic(),
        max_iter=2,
    )

    result = runner.run(_package(), {"src/foo.py"})

    assert result.converged is True
    assert result.iterations_completed == 1
    assert result.final_issues[0].category == TEST_GAP


def test_loop_runs_second_iter_for_uncertain() -> None:
    reviewer = _StaticReviewer([_issue()])
    critic = _OneUncertainCritic()
    runner = IterativeHarnessRunner(reviewer=reviewer, critic=critic, max_iter=2)

    result = runner.run(_package(), {"src/foo.py"})

    assert result.converged is True
    assert result.iterations_completed == 2
    assert reviewer.seen_feedback[0] is None
    assert reviewer.seen_feedback[1] is not None
    assert result.iterations[0].uncertain_count == 1
    assert result.iterations[1].keep_count == 1


def test_loop_stops_on_stable_issue_set() -> None:
    runner = IterativeHarnessRunner(
        reviewer=_StaticReviewer([_issue()]),
        critic=_AlwaysUncertainCritic(),
        max_iter=3,
    )

    result = runner.run(_package(), {"src/foo.py"})

    assert result.converged is True
    assert result.iterations_completed == 2
    assert result.iterations[0].issue_set == result.iterations[1].issue_set


def test_loop_routes_ungrounded_to_discarded() -> None:
    runner = IterativeHarnessRunner(
        reviewer=_StaticReviewer(
            [_issue(evidence_ids=["fake:invalid:evidence"])]
        ),
        critic=_KeepCritic(),
        max_iter=2,
    )

    result = runner.run(_package(), {"src/foo.py"})

    assert result.final_issues == []
    assert result.discarded[0].reason == "invalid_evidence_ids"


def test_loop_records_agent_runs_per_iteration() -> None:
    runner = IterativeHarnessRunner(
        reviewer=_StaticReviewer([_issue()]),
        critic=_OneUncertainCritic(),
        max_iter=2,
    )

    result = runner.run(_package(), {"src/foo.py"})

    assert len(result.agent_runs) == 4
    assert [run.iteration for run in result.agent_runs] == [0, 0, 1, 1]
    assert result.agent_runs[0].feedback_hash == ""
    assert result.agent_runs[2].feedback_hash.startswith("sha256:")


def test_checkpoint_written_after_iteration(tmp_path: Path) -> None:
    runner = IterativeHarnessRunner(
        reviewer=_StaticReviewer([_issue()]),
        critic=_KeepCritic(),
        max_iter=2,
        out_dir=tmp_path,
        mode="hybrid-fake",
    )

    result = runner.run(_package(), {"src/foo.py"})
    checkpoint = tmp_path / LOOP_CHECKPOINT_FILENAME
    data = json.loads(checkpoint.read_text(encoding="utf-8"))

    assert checkpoint.exists()
    assert result.checkpoint_path == str(checkpoint)
    assert data["schema_version"] == "1.0"
    assert data["iteration"] == 1
    assert data["converged"] is True
    assert data["package_hash"].startswith("sha256:")
    assert data["diff_hash"].startswith("sha256:")


def test_resume_uses_checkpoint_feedback(tmp_path: Path) -> None:
    first_runner = IterativeHarnessRunner(
        reviewer=_StaticReviewer([_issue()]),
        critic=_AlwaysUncertainCritic(),
        max_iter=1,
        out_dir=tmp_path,
        mode="hybrid-fake",
    )
    first_runner.run(_package(), {"src/foo.py"})
    reviewer = _StaticReviewer([_issue()])
    second_runner = IterativeHarnessRunner(
        reviewer=reviewer,
        critic=_AlwaysUncertainCritic(),
        max_iter=2,
        out_dir=tmp_path,
        mode="hybrid-fake",
    )

    result = second_runner.run(_package(), {"src/foo.py"}, resume=True)

    assert result.resume_used is True
    assert result.resume_ignored_reason is None
    assert result.iterations_completed == 2
    assert reviewer.seen_feedback[0] is not None
    assert reviewer.seen_feedback[0].iteration == 0


def test_resume_ignored_when_package_hash_mismatch(tmp_path: Path) -> None:
    first_runner = IterativeHarnessRunner(
        reviewer=_StaticReviewer([_issue()]),
        critic=_AlwaysUncertainCritic(),
        max_iter=1,
        out_dir=tmp_path,
        mode="hybrid-fake",
    )
    first_runner.run(_package(), {"src/foo.py"})
    second_runner = IterativeHarnessRunner(
        reviewer=_StaticReviewer([_issue()]),
        critic=_KeepCritic(),
        max_iter=2,
        out_dir=tmp_path,
        mode="hybrid-fake",
        package_hash="sha256:different",
    )

    result = second_runner.run(_package(), {"src/foo.py"}, resume=True)

    assert result.resume_used is False
    assert result.resume_ignored_reason == "package_hash_mismatch"
    assert result.iterations_completed == 1


@dataclass(slots=True)
class _StaticReviewer:
    issues: list[ReviewIssue]
    seen_feedback: list[PriorFeedback | None] = field(default_factory=list)

    def review(
        self,
        package: EvidencePackage,
        *,
        prior_feedback: PriorFeedback | None = None,
    ) -> list[ReviewIssue]:
        del package
        self.seen_feedback.append(prior_feedback)
        return list(self.issues)


class _KeepCritic:
    def critique(
        self, issues: list[ReviewIssue], package: EvidencePackage
    ) -> CritiqueResult:
        del package
        return CritiqueResult(keep=list(issues))


@dataclass(slots=True)
class _OneUncertainCritic:
    calls: int = 0

    def critique(
        self, issues: list[ReviewIssue], package: EvidencePackage
    ) -> CritiqueResult:
        del package
        self.calls += 1
        if self.calls == 1:
            return CritiqueResult(uncertain=[_feedback_item(issues[0])])
        return CritiqueResult(keep=list(issues))


class _AlwaysUncertainCritic:
    def critique(
        self, issues: list[ReviewIssue], package: EvidencePackage
    ) -> CritiqueResult:
        del package
        return CritiqueResult(uncertain=[_feedback_item(issues[0])])


def _feedback_item(issue: ReviewIssue) -> UncertainFeedbackItem:
    return UncertainFeedbackItem(
        issue_id=f"{issue.category}:{issue.file}:{issue.line}",
        category=issue.category,
        critic_reason="low confidence",
        original_confidence=issue.confidence,
        evidence_ids=list(issue.evidence_ids),
    )


def _issue(
    *,
    evidence_ids: list[str] | None = None,
    confidence: float = 0.75,
) -> ReviewIssue:
    return ReviewIssue(
        file="src/foo.py",
        line=9,
        severity="medium",
        category=TEST_GAP,
        message="Business logic changed without related tests.",
        suggestion="Update tests.",
        confidence=confidence,
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
                old_count=2,
                new_start=8,
                new_count=2,
                section_header="def run",
                lines=[
                    DiffLine("context", 8, 8, "def run():"),
                    DiffLine("removed", 9, None, "    return False"),
                    DiffLine("added", None, 9, "    return True"),
                ],
            )
        ],
    )
    signal = RiskSignal(
        tag=TEST_GAP,
        confidence=0.8,
        reason="Related tests exist but no test changed.",
        evidence_ids=["diff:src/foo.py:9"],
    )
    return EvidencePackage(
        repo_root="/repo",
        changed_files=[change],
        changed_entities=[],
        risk_signals=[signal],
        evidence_index={
            "diff:src/foo.py:9": ReviewEvidence(
                id="diff:src/foo.py:9",
                kind="diff",
                source="src/foo.py:9",
                message="Added line.",
            ),
            "risk:test_gap:src/foo.py": ReviewEvidence(
                id="risk:test_gap:src/foo.py",
                kind="risk",
                source=TEST_GAP,
                message="Related tests exist but no test changed.",
            ),
        },
    )
