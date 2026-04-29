"""Tests for hygiene.llm_classifier module."""

from __future__ import annotations

import pytest

from code_review_agent.hygiene.llm_classifier import (
    FakeLLMClassifier,
    classify_with_llm,
    validate_semantic_classification,
)
from code_review_agent.hygiene.taxonomy import (
    ADHOC_SCRIPT,
    DESCRIPTIONS,
    EXPERIMENT_SCRIPT,
    UNCERTAIN,
)
from code_review_agent.models import HygieneEvidence, SemanticClassification


def _ev(path: str, signals: list[str] | None = None) -> HygieneEvidence:
    return HygieneEvidence(path=path, content_sample="", signals=signals or [])


# ---------------------------------------------------------------------------
# FakeLLMClassifier
# ---------------------------------------------------------------------------


def test_fake_classifier_returns_configured_type() -> None:
    clf = FakeLLMClassifier(responses={"download_data.py": ADHOC_SCRIPT})
    result = clf.classify(_ev("download_data.py"), DESCRIPTIONS)
    assert result.artifact_type == ADHOC_SCRIPT
    assert result.path == "download_data.py"


def test_fake_classifier_falls_back_to_uncertain() -> None:
    clf = FakeLLMClassifier()
    result = clf.classify(_ev("mystery.py"), DESCRIPTIONS)
    assert result.artifact_type == UNCERTAIN
    assert result.confidence < 0.5


def test_fake_classifier_rejects_invalid_type() -> None:
    # Internally FakeLLMClassifier normalises invalid types to UNCERTAIN.
    clf = FakeLLMClassifier(responses={"f.py": "not_a_real_type"})
    result = clf.classify(_ev("f.py"), DESCRIPTIONS)
    assert result.artifact_type == UNCERTAIN


def test_fake_classifier_includes_evidence_signals() -> None:
    clf = FakeLLMClassifier(responses={"exp.py": EXPERIMENT_SCRIPT})
    result = clf.classify(_ev("exp.py", signals=["s1", "s2", "s3", "s4"]), DESCRIPTIONS)
    # At most 3 signals forwarded.
    assert len(result.evidence) <= 3


def test_fake_classifier_suggested_action_matches_taxonomy() -> None:
    clf = FakeLLMClassifier(responses={"exp.py": EXPERIMENT_SCRIPT})
    result = clf.classify(_ev("exp.py"), DESCRIPTIONS)
    assert result.suggested_action == "move"


# ---------------------------------------------------------------------------
# classify_with_llm
# ---------------------------------------------------------------------------


def test_classify_with_llm_processes_all_inputs() -> None:
    clf = FakeLLMClassifier(
        responses={"a.py": EXPERIMENT_SCRIPT, "b.py": ADHOC_SCRIPT}
    )
    evidence_list = [_ev("a.py"), _ev("b.py"), _ev("c.py")]
    results = classify_with_llm(evidence_list, clf)
    assert len(results) == 3
    assert results[0].artifact_type == EXPERIMENT_SCRIPT
    assert results[1].artifact_type == ADHOC_SCRIPT
    assert results[2].artifact_type == UNCERTAIN


def test_classify_with_llm_raises_on_invalid_schema() -> None:
    """A classifier that returns a bad artifact_type must raise ValueError."""

    class BadClassifier:
        def classify(self, evidence, taxonomy_descriptions):
            return SemanticClassification(
                path=evidence.path,
                artifact_type="totally_wrong",
                confidence=0.9,
                suggested_action="move",
                reason="bad",
            )

    with pytest.raises(ValueError, match="Invalid artifact_type"):
        classify_with_llm([_ev("x.py")], BadClassifier())


# ---------------------------------------------------------------------------
# validate_semantic_classification
# ---------------------------------------------------------------------------


def test_validation_passes_for_valid_object() -> None:
    sc = SemanticClassification(
        path="f.py",
        artifact_type=EXPERIMENT_SCRIPT,
        confidence=0.75,
        suggested_action="move",
        reason="looks like an experiment",
    )
    validate_semantic_classification(sc)  # must not raise


def test_validation_fails_for_invalid_artifact_type() -> None:
    sc = SemanticClassification(
        path="f.py",
        artifact_type="bad_type",
        confidence=0.5,
        suggested_action="move",
        reason="reason",
    )
    with pytest.raises(ValueError, match="Invalid artifact_type"):
        validate_semantic_classification(sc)


def test_validation_fails_for_out_of_range_confidence() -> None:
    sc = SemanticClassification(
        path="f.py",
        artifact_type=EXPERIMENT_SCRIPT,
        confidence=1.5,
        suggested_action="move",
        reason="reason",
    )
    with pytest.raises(ValueError, match="confidence"):
        validate_semantic_classification(sc)


def test_validation_fails_for_empty_reason() -> None:
    sc = SemanticClassification(
        path="f.py",
        artifact_type=EXPERIMENT_SCRIPT,
        confidence=0.7,
        suggested_action="move",
        reason="   ",
    )
    with pytest.raises(ValueError, match="reason"):
        validate_semantic_classification(sc)


def test_validation_fails_for_mismatched_action() -> None:
    sc = SemanticClassification(
        path="f.py",
        artifact_type=EXPERIMENT_SCRIPT,
        confidence=0.7,
        suggested_action="needs_human_review",  # wrong for EXPERIMENT_SCRIPT
        reason="reason",
    )
    with pytest.raises(ValueError, match="suggested_action"):
        validate_semantic_classification(sc)
