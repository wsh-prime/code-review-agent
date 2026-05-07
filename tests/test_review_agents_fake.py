from __future__ import annotations

import json
from io import BytesIO
from pathlib import Path
from urllib import error

import pytest

from code_review_agent.models import (
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
    CROSS_STRATEGY,
    FakeLLMCriticAgent,
    FakeLLMReviewAgent,
    OpenAICompatibleReviewAgent,
    _AgentFatalError,
    _retry_with_backoff,
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


def test_fake_reviewer_uses_prior_feedback_conservatively() -> None:
    package = _package()
    feedback = PriorFeedback(
        iteration=0,
        uncertain_items=[
            UncertainFeedbackItem(
                issue_id="test_gap:src/foo.py:9",
                category=TEST_GAP,
                critic_reason="low confidence",
                original_confidence=0.77,
                evidence_ids=["diff:src/foo.py:9"],
            )
        ],
    )

    first_pass = FakeLLMReviewAgent().review(package)
    second_pass = FakeLLMReviewAgent().review(package, prior_feedback=feedback)

    first_issue = next(issue for issue in first_pass if issue.category == TEST_GAP)
    second_issue = next(issue for issue in second_pass if issue.category == TEST_GAP)
    assert second_issue.confidence < first_issue.confidence


def test_fake_critic_returns_structured_critique() -> None:
    package = _package()
    issues = FakeLLMReviewAgent().review(package)
    critique = FakeLLMCriticAgent().critique(issues, package)

    assert any(issue.category == TEST_GAP for issue in critique.keep)
    assert any(
        item.issue_id == "fake_unverified_candidate:src/foo.py:9"
        for item in critique.uncertain
    )
    assert critique.to_dict()["keep"]


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


def test_export_agent_prompts_redacts_full_package_for_hybrid_live(
    tmp_path: Path,
) -> None:
    exports = export_agent_prompts(
        _package(),
        tmp_path / "prompts",
        mode="hybrid-live",
    )

    review_input = json.loads(Path(exports["files"][0]).read_text(encoding="utf-8"))

    assert review_input["full_package_exported"] is False
    assert "package" not in review_input
    assert "live_review_input" in review_input
    assert review_input["live_review_input"]["schema"] == "live_review_input_v1"
    assert "context_budget" not in review_input["live_review_input"]


def test_openai_compatible_runner_records_agent_metadata() -> None:
    package = _package()
    result = run_openai_compatible_review_agent(package, agent=_FakeLiveAgent())

    assert result.findings[0].category == TEST_GAP
    assert result.agent_runs[0].agent_name == "openai_compatible_reviewer"
    assert result.agent_runs[0].model == "test-live-model"
    assert result.agent_runs[0].input_evidence_ids == sorted(package.evidence_index)


def test_openai_compatible_agent_sends_budgeted_live_input(monkeypatch) -> None:
    captured: dict = {}

    def fake_post(url, *, api_key, body, timeout_seconds):
        del url, api_key, timeout_seconds
        captured["body"] = body
        return {
            "choices": [
                {
                    "message": {
                        "content": json.dumps(
                            [
                                {
                                    "file": "src/foo.py",
                                    "line": 9,
                                    "severity": "medium",
                                    "category": TEST_GAP,
                                    "message": "Live model candidate.",
                                    "suggestion": "Update tests.",
                                    "confidence": 0.7,
                                    "evidence_ids": ["diff:src/foo.py:9"],
                                }
                            ]
                        )
                    }
                }
            ],
            "usage": {"prompt_tokens": 42, "completion_tokens": 12},
        }

    monkeypatch.setattr(
        "code_review_agent.review.agents._post_openai_compatible_json",
        fake_post,
    )
    agent = OpenAICompatibleReviewAgent(api_key="test-key")

    issues = agent.review(_package())

    content = captured["body"]["messages"][1]["content"]
    assert issues[0].category == TEST_GAP
    assert "ReviewerContext:" in content
    assert "EvidencePackage:" not in content
    assert "live_review_input_v1" in content
    context = json.loads(content.split("ReviewerContext:\n", 1)[1])
    assert "context_budget" not in context
    assert agent.last_agent_run is not None
    assert agent.last_agent_run.input_evidence_ids == sorted(_package().evidence_index)


def test_openai_compatible_agent_accepts_context_request_and_refills(monkeypatch) -> None:
    captured: list[dict] = []

    def fake_post(url, *, api_key, body, timeout_seconds):
        del url, api_key, timeout_seconds
        captured.append(body)
        if len(captured) == 1:
            content = {
                "issues": [],
                "context_requests": [
                    {
                        "request_type": "risk_evidence",
                        "path": "src/foo.py",
                        "risk_tag": TEST_GAP,
                        "reason": "Need risk summary.",
                    }
                ],
            }
        else:
            content = {
                "issues": [
                    {
                        "file": "src/foo.py",
                        "line": 9,
                        "severity": "medium",
                        "category": TEST_GAP,
                        "message": "Refill candidate.",
                        "suggestion": "Update tests.",
                        "confidence": 0.72,
                        "evidence_ids": ["risk:test_gap:src/foo.py"],
                    }
                ],
                "context_requests": [],
            }
        return {
            "choices": [{"message": {"content": json.dumps(content)}}],
            "usage": {"prompt_tokens": 20, "completion_tokens": 8},
        }

    monkeypatch.setattr(
        "code_review_agent.review.agents._post_openai_compatible_json",
        fake_post,
    )
    agent = OpenAICompatibleReviewAgent(api_key="test-key")
    agent.context_budget_tokens = 620
    agent.max_evidence_per_file = 1

    issues = agent.review(_package())

    assert len(captured) == 2
    assert issues[0].category == TEST_GAP
    assert agent.last_context_budget is not None
    assert agent.last_context_budget["context_request_count"] == 1
    assert agent.last_context_budget["refill_count"] == 1
    assert agent.last_agent_runs[-1].context_refill_used is True


def test_openai_compatible_agent_resumes_completed_context_shard(
    tmp_path: Path,
    monkeypatch,
) -> None:
    calls = 0

    def fake_post(url, *, api_key, body, timeout_seconds):
        nonlocal calls
        del url, api_key, body, timeout_seconds
        calls += 1
        return {
            "choices": [
                {
                    "message": {
                        "content": json.dumps(
                            {
                                "issues": [
                                    {
                                        "file": "src/foo.py",
                                        "line": 9,
                                        "severity": "medium",
                                        "category": TEST_GAP,
                                        "message": "Checkpointed candidate.",
                                        "suggestion": "Update tests.",
                                        "confidence": 0.72,
                                        "evidence_ids": ["diff:src/foo.py:9"],
                                    }
                                ],
                                "context_requests": [],
                            }
                        )
                    }
                }
            ],
            "usage": {"prompt_tokens": 20, "completion_tokens": 8},
        }

    monkeypatch.setattr(
        "code_review_agent.review.agents._post_openai_compatible_json",
        fake_post,
    )
    checkpoint = tmp_path / "live_context_checkpoint.json"
    first = OpenAICompatibleReviewAgent(api_key="test-key")
    first.context_checkpoint_path = str(checkpoint)
    first.context_checkpoint_package_hash = "pkg"
    first.context_checkpoint_diff_hash = "diff"

    first_issues = first.review(_package())

    assert calls == 1
    assert first_issues[0].category == TEST_GAP
    assert checkpoint.exists()

    def fail_post(url, *, api_key, body, timeout_seconds):
        del url, api_key, body, timeout_seconds
        raise AssertionError("resume should not call the live API")

    monkeypatch.setattr(
        "code_review_agent.review.agents._post_openai_compatible_json",
        fail_post,
    )
    second = OpenAICompatibleReviewAgent(api_key="test-key")
    second.context_checkpoint_path = str(checkpoint)
    second.context_checkpoint_package_hash = "pkg"
    second.context_checkpoint_diff_hash = "diff"
    second.context_checkpoint_resume = True

    resumed_issues = second.review(_package())

    assert resumed_issues[0].category == TEST_GAP
    assert second.last_agent_runs[0].status == "resumed"


def test_retry_on_503_then_success(monkeypatch) -> None:
    calls = 0
    sleeps: list[float] = []

    def call() -> dict:
        nonlocal calls
        calls += 1
        if calls < 3:
            raise error.HTTPError(
                "https://example.test",
                503,
                "Service Unavailable",
                None,
                BytesIO(b"busy"),
            )
        return {"ok": True}

    monkeypatch.setattr(
        "code_review_agent.review.agents.time.sleep",
        lambda seconds: sleeps.append(seconds),
    )
    retry_log: list[str] = []

    result = _retry_with_backoff(call, retry_log=retry_log)

    assert result == {"ok": True}
    assert calls == 3
    assert len(retry_log) == 2
    assert sleeps == [1.0, 2.0]


def test_no_retry_on_401(monkeypatch) -> None:
    calls = 0
    sleeps: list[float] = []

    def call() -> dict:
        nonlocal calls
        calls += 1
        raise error.HTTPError(
            "https://example.test",
            401,
            "Unauthorized",
            None,
            BytesIO(b"bad key"),
        )

    monkeypatch.setattr(
        "code_review_agent.review.agents.time.sleep",
        lambda seconds: sleeps.append(seconds),
    )

    with pytest.raises(_AgentFatalError):
        _retry_with_backoff(call, retry_log=[])

    assert calls == 1
    assert sleeps == []


def test_retry_after_header_is_respected(monkeypatch) -> None:
    calls = 0
    sleeps: list[float] = []

    def call() -> dict:
        nonlocal calls
        calls += 1
        if calls == 1:
            raise error.HTTPError(
                "https://example.test",
                429,
                "Too Many Requests",
                {"Retry-After": "2.5"},
                BytesIO(b"slow down"),
            )
        return {"ok": True}

    monkeypatch.setattr(
        "code_review_agent.review.agents.time.sleep",
        lambda seconds: sleeps.append(seconds),
    )

    _retry_with_backoff(call, retry_log=[], max_attempts=2)

    assert sleeps == [2.5]


def test_timeout_retries_then_becomes_transient(monkeypatch) -> None:
    calls = 0
    sleeps: list[float] = []

    def call() -> dict:
        nonlocal calls
        calls += 1
        raise TimeoutError("read operation timed out")

    monkeypatch.setattr(
        "code_review_agent.review.agents.time.sleep",
        lambda seconds: sleeps.append(seconds),
    )
    retry_log: list[str] = []

    with pytest.raises(Exception) as exc_info:
        _retry_with_backoff(call, retry_log=retry_log, max_attempts=3)

    assert exc_info.value.__class__.__name__ == "_AgentTransientError"
    assert calls == 3
    assert retry_log == [
        "attempt=1 error=timeout delay=1.00s",
        "attempt=2 error=timeout delay=2.00s",
    ]
    assert sleeps == [1.0, 2.0]


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
