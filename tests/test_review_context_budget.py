from __future__ import annotations

from code_review_agent.models import (
    ContextRequest,
    DiffFileChange,
    DiffHunk,
    DiffLine,
    EvidencePackage,
    ReviewEvidence,
    RiskSignal,
)
from code_review_agent.review.context_budget import (
    aggregate_context_budget,
    build_context_refill,
    build_live_review_input,
    build_reviewer_contexts,
    estimate_tokens,
    score_evidence,
)


def test_estimate_tokens_uses_simple_character_budget() -> None:
    assert estimate_tokens("abcd") == 1
    assert estimate_tokens("a" * 40) == 10


def test_risk_first_selection_prefers_high_risk_evidence() -> None:
    package = _large_package()

    security_score = score_evidence(package, "diff:src/auth.py:1")
    ordinary_score = score_evidence(package, "diff:src/ordinary.py:1")

    assert security_score > ordinary_score


def test_build_live_review_input_selects_subset_and_audits_omitted() -> None:
    package = _large_package()

    live_input = build_live_review_input(
        package,
        max_input_tokens=900,
        max_evidence_per_file=2,
    )

    budget = live_input.context_budget
    selected_ids = set(budget["selected_evidence_ids"])
    assert budget["enabled"] is True
    assert budget["context_truncated"] is True
    assert budget["omitted_evidence_count"] > 0
    assert "diff:src/auth.py:1" in selected_ids
    assert selected_ids <= set(package.evidence_index)
    assert len(live_input.payload["evidence_index"]) == budget["selected_evidence_count"]
    assert len(live_input.payload["evidence_index"]) < len(package.evidence_index)


def test_build_live_review_input_limits_changed_file_summaries() -> None:
    package = _multi_file_package(file_count=6)

    live_input = build_live_review_input(
        package,
        max_input_tokens=700,
        max_files=2,
        max_evidence_per_file=2,
    )

    assert len(live_input.payload["changed_files"]) == 2
    assert live_input.payload["omitted_changed_file_count"] == 4
    assert live_input.context_budget["shard_count"] == 1
    assert live_input.context_budget["selected_evidence_count"] > 0


def test_build_live_review_input_does_not_embed_full_package() -> None:
    package = _large_package()

    live_input = build_live_review_input(
        package,
        max_input_tokens=900,
        max_evidence_per_file=2,
    )

    assert "metadata" not in live_input.payload
    assert set(live_input.payload["evidence_index"]) < set(package.evidence_index)
    assert "diff:src/ordinary.py:39" not in live_input.payload["evidence_index"]


def test_build_live_review_input_sends_compact_risk_cards() -> None:
    package = _large_package()
    package.risk_signals[0].evidence_ids = [
        "diff:src/auth.py:1",
        *[f"diff:src/ordinary.py:{index}" for index in range(40)],
    ]

    live_input = build_live_review_input(
        package,
        max_input_tokens=900,
        max_evidence_per_file=2,
    )

    risk_card = live_input.payload["risk_signals"][0]
    assert "evidence_ids" not in risk_card
    assert len(risk_card["primary_evidence_ids"]) <= 5
    assert risk_card["omitted_evidence_id_count"] > 0


def test_build_reviewer_contexts_splits_large_multi_file_package() -> None:
    package = _multi_file_package(file_count=5)

    contexts = build_reviewer_contexts(
        package,
        max_input_tokens=700,
        max_files=2,
        max_evidence_per_file=2,
    )
    budget = aggregate_context_budget(contexts)

    assert len(contexts) == 3
    assert {context.shard_id for context in contexts} == {
        "shard-001",
        "shard-002",
        "shard-003",
    }
    assert budget["shard_count"] == 3
    assert budget["selected_evidence_count"] == 5


def test_build_context_refill_uses_bounded_request_types() -> None:
    package = _large_package()
    live_input = build_live_review_input(
        package,
        max_input_tokens=900,
        max_evidence_per_file=1,
    )

    refill = build_context_refill(
        package,
        live_input.reviewer_context,
        [
            ContextRequest(
                request_type="risk_evidence",
                path="src/auth.py",
                risk_tag="security_sensitive",
                reason="Need risk summary.",
            )
        ],
        max_input_tokens=900,
    )

    assert refill is not None
    assert refill.is_refill is True
    assert refill.parent_shard_id == "shard-001"
    assert "risk:security_sensitive:src/auth.py" in refill.evidence_index


def _large_package() -> EvidencePackage:
    evidence_index = {
        "diff:src/auth.py:1": ReviewEvidence(
            id="diff:src/auth.py:1",
            kind="diff",
            source="src/auth.py:1",
            message="Added line: token validation changed.",
        ),
        "risk:security_sensitive:src/auth.py": ReviewEvidence(
            id="risk:security_sensitive:src/auth.py",
            kind="risk",
            source="security_sensitive",
            message="Security-sensitive keywords changed.",
        ),
    }
    for index in range(40):
        evidence_index[f"diff:src/ordinary.py:{index}"] = ReviewEvidence(
            id=f"diff:src/ordinary.py:{index}",
            kind="diff",
            source=f"src/ordinary.py:{index}",
            message="Added line: ordinary low-risk change " + ("x" * 120),
        )
    return EvidencePackage(
        repo_root="/repo",
        changed_files=[
            _change("src/auth.py"),
            _change("src/ordinary.py"),
        ],
        risk_signals=[
            RiskSignal(
                tag="security_sensitive",
                confidence=0.9,
                reason="Security-sensitive keywords changed.",
                evidence_ids=["diff:src/auth.py:1"],
            )
        ],
        evidence_index=evidence_index,
    )


def _multi_file_package(*, file_count: int) -> EvidencePackage:
    evidence_index = {}
    changes = []
    signals = []
    for index in range(file_count):
        path = f"src/file_{index}.py"
        evidence_id = f"diff:{path}:1"
        changes.append(_change(path))
        evidence_index[evidence_id] = ReviewEvidence(
            id=evidence_id,
            kind="diff",
            source=f"{path}:1",
            message="Added line: changed behavior.",
        )
        signals.append(
            RiskSignal(
                tag="behavior_change",
                confidence=0.7,
                reason=f"Executable logic changed in {path}.",
                evidence_ids=[evidence_id],
            )
        )
    return EvidencePackage(
        repo_root="/repo",
        changed_files=changes,
        risk_signals=signals,
        evidence_index=evidence_index,
    )


def _change(path: str) -> DiffFileChange:
    return DiffFileChange(
        old_path=path,
        new_path=path,
        change_type="modified",
        hunks=[
            DiffHunk(
                old_start=1,
                old_count=1,
                new_start=1,
                new_count=1,
                section_header="def run",
                lines=[
                    DiffLine("added", None, 1, "    return True"),
                ],
            )
        ],
    )
