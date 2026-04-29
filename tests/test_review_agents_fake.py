from __future__ import annotations

import json
from pathlib import Path

from code_review_agent.models import (
    DiffFileChange,
    DiffHunk,
    DiffLine,
    EvidencePackage,
    ReviewEvidence,
    ReviewIssue,
    RiskSignal,
)
from code_review_agent.review.agents import (
    CROSS_STRATEGY,
    FakeLLMReviewAgent,
    export_agent_prompts,
    run_openai_compatible_review_agent,
    run_fake_hybrid_agents,
)
from code_review_agent.review.filter import filter_issues
from code_review_agent.review.risk import TEST_GAP


def test_fake_reviewer_returns_evidence_backed_candidate_and_invalid_probe() -> None:
    package = _package()
    issues = FakeLLMReviewAgent().review(package)

    assert any(issue.category == TEST_GAP for issue in issues)
    assert any(issue.category == "fake_unverified_candidate" for issue in issues)
    assert "diff:src/foo.py:9" in issues[0].evidence_ids


def test_fake_hybrid_candidates_go_through_evidence_filter() -> None:
    package = _package()
    fake_result = run_fake_hybrid_agents(package, pair_strategy=CROSS_STRATEGY)
    filtered = filter_issues(
        fake_result.findings,
        fake_result.needs_human_review,
        package,
        {"src/foo.py"},
    )

    assert len(fake_result.agent_runs) == 2
    assert all(run.prompt_hash for run in fake_result.agent_runs)
    assert any(issue.category == TEST_GAP for issue in filtered.findings)
    assert any(
        item.reason == "invalid_evidence_ids" for item in filtered.discarded
    )


def test_export_agent_prompts_writes_hash_and_redacted_input(tmp_path: Path) -> None:
    exports = export_agent_prompts(
        _package(),
        tmp_path / "prompts",
        mode="hybrid-fake",
    )

    review_prompt = Path(exports["files"][1]).read_text(encoding="utf-8")
    review_input = json.loads(Path(exports["files"][0]).read_text(encoding="utf-8"))

    assert "prompt_hash:" in review_prompt
    assert review_input["prompt_hash"] == exports["review_prompt_hash"]
    assert "author" in review_input["redacted_metadata_fields"]


def test_openai_compatible_runner_records_agent_metadata() -> None:
    package = _package()
    result = run_openai_compatible_review_agent(package, agent=_FakeLiveAgent())

    assert result.findings[0].category == TEST_GAP
    assert result.agent_runs[0].agent_name == "openai_compatible_reviewer"
    assert result.agent_runs[0].model == "test-live-model"
    assert result.agent_runs[0].input_evidence_ids == sorted(package.evidence_index)


class _FakeLiveAgent:
    model = "test-live-model"

    def review(self, package: EvidencePackage):
        return [
            ReviewIssue(
                file="src/foo.py",
                line=9,
                severity="medium",
                category=TEST_GAP,
                message="Live model candidate.",
                suggestion="Update tests.",
                confidence=0.7,
                evidence_ids=["diff:src/foo.py:9"],
            )
        ]


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
        metadata={
            "redacted": ["pr_title", "pr_description", "commit_message", "author"],
            "target_repo_modified": False,
        },
    )
